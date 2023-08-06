import os
import json
import idna
import pendulum
import confusables
from .utils.logger import LoggingBase


class Core(metaclass=LoggingBase):

    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

    def __normalize_domain(self, string, prioritize_alpha=True):
        normal_forms = set([""])
        for char in string:
            normalized_chars = []
            confusable_chars = confusables.confusable_characters(char)
            if confusable_chars:
                if not confusables.is_ascii(char) or not char.isalpha():
                    for confusable in confusable_chars:
                        if prioritize_alpha:
                            if (confusables.is_ascii(confusable) and confusable.isalpha()) and confusable not in confusables.NON_NORMAL_ASCII_CHARS:
                                normal = confusable
                                if len(confusable) > 1:
                                    normal = self.__normalize_domain(confusable, prioritize_alpha=True)[0]
                                normalized_chars.append(normal)
                        else:
                            if confusables.is_ascii(confusable) and confusable not in confusables.NON_NORMAL_ASCII_CHARS:
                                normal = confusable
                                if len(confusable) > 1:
                                    normal = self.__normalize_domain(confusable)[0]
                                normalized_chars.append(normal)
                else:
                    normalized_chars = [char]
            if len(normalized_chars) == 0:
                normalized_chars = [char]
            normal_forms = set([x[0] + x[1].lower() for x in list(confusables.product(normal_forms, normalized_chars))])
        return sorted(list(normal_forms))

    def process_domain(self, domain):
        try:
            site_name = domain.split('.')[0]
            if "xn--" in domain:
                depunyfied_domain = f"{idna.decode(domain)}"
                normalized_domain_no_tld_list = self.__normalize_domain(depunyfied_domain, prioritize_alpha=True)
                site_name = normalized_domain_no_tld_list[0]
            if site_name:
                return {domain: site_name}
        except:
            self.__logger.warning(f"Error processing site_name")

    def chunk(self, items, n):
        n = max(1, n)
        return (items[i:i+n] for i in range(0, len(items), n))

    def save_data(self, data, name):
        date = pendulum.now().to_date_string()
        self.__logger.info(f'Saving WhoisDS Data for {date}')
        data = {
            'timestamp': date,
            'data': data
        }
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        with open(os.path.join(self.save_path, name), 'w+') as f:
            json.dump(data, f)

    def get_data(self, name):
        if os.path.exists(os.path.join(self.save_path, name)):
            with open(os.path.join(self.save_path, name)) as f:
                return json.load(f)
