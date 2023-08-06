from datetime import datetime
from datetime import timedelta
import base64
import requests
import pendulum
from io import BytesIO
from urllib.parse import urlparse
from zipfile import ZipFile
from concurrent.futures import ThreadPoolExecutor, as_completed, thread
from .core import Core


class WhoisDS(Core):

    domain_list = []
    identified_domains = set()
    __chunks = []

    def __init__(self, thread_count=10, save=True):
        self.thread_count = thread_count
        if not self.__chunks:
            self.__chunks = self.chunk(self.domain_list, int(len(self.domain_list) / self.thread_count))
        self.save = save
        if not self.domain_list:
            self.__logger.info('Getting latest WhoisDS data')
            self.__get_latest()

    def __get_latest(self):
        data = self.get_data('whois_data.json')
        if data and data.get('timestamp') == pendulum.now().to_date_string():
            self.__logger.info(f'Loaded WhoisDS Data from {pendulum.now().to_date_string()}')
            self.domain_list = data.get('data')
        else:
            past = datetime.strftime(pendulum.now() - timedelta(2), "%Y-%m-%d")
            filename = "{}.zip".format(past)
            encoded_filename = base64.b64encode(filename.encode('utf-8'))
            response = requests.get(f"https://www.whoisds.com//whois-database/newly-registered-domains/{encoded_filename.decode('ascii')}/nrd")
            with BytesIO(response.content) as zip_file:
                with ZipFile(zip_file) as zip_file:
                    for zip_info in zip_file.infolist():
                        with zip_file.open(zip_info) as ffile:
                            for line in ffile.readlines():
                                self.domain_list.append(
                                    self.process_domain(
                                        line.decode('utf-8', errors='ignore').strip()
                                    )
                                )
            if self.save:
                self.save_data(self.domain_list, 'whois_data.json')

    def threader(self, method):
        threads = []
        response = []
        self.__chunks = self.chunk(self.domain_list, int(len(self.domain_list) / self.thread_count))
        with ThreadPoolExecutor(max_workers=self.thread_count) as executor:
            for chunk in self.__chunks:
                threads.append(executor.submit(method, chunk))
            for task in as_completed(threads):
                result = task.result()
                if isinstance(result, list):
                    for item in result:
                        response.append(item)
        return response

    def contained_in(self, domain):
        self.__logger.info(f'Checking {domain} is contained in.')
        self.domain = domain.split('.')[0]
        return self.threader(self.__contained_in)

    def __contained_in(self, chunk):
        return_list = []
        for item in chunk:
            for key,val in item.items():
                if self.domain in key or self.domain in val:
                    return_list.append(key)
        return return_list

    def confusables(self, domain):
        self.__logger.info(f'Checking {domain} with Confusables')
        self.domain = domain.split('.')[0]
        return self.threader(self.__confusables)

    def __confusables(self, chunk):
        import confusables
        return_list = []
        for item in chunk:
            for key,val in item.items():
                if confusables.is_confusable(self.domain, key):
                    return_list.append(key)
                elif confusables.is_confusable(self.domain, val):
                    return_list.append(key)
        return return_list

    def levenshtein(self, domain):
        self.__logger.info(f'Checking {domain} with Levenhshtein Distance.')
        self.domain = domain.split('.')[0]
        return self.threader(self.__levenshtein)

    def __levenshtein(self, chunk):
        import Levenshtein
        return_list = []
        for item in chunk:
            for key,val in item.items():
                distance = Levenshtein.distance(self.domain, val)
                if  distance <= 2:
                    return_list.append(key)
        return return_list
