from .whoisds import WhoisDS


class Dominions:

    __whoisds = None
    __domain = []

    def __init__(self, thread_count=10):
        self.thread_count = thread_count

    @property
    def domain(self):
        return self.__domain

    @domain.setter
    def domain(self, value):
        self.__domain = value if isinstance(value, list) else [value]

    def __load(self, service):
        if service == 'whoisds':
            if not self.__whoisds:
                self.__whoisds = WhoisDS(thread_count=self.thread_count)

    def contained_in(self, source='whoisds'):
        self.__load(source)
        return_dict = {}
        for domain in self.domain:
            if domain not in return_dict:
                return_dict[domain] = {}
            contained_in = list(self.__whoisds.contained_in(domain))
            if contained_in:
                for item in contained_in:
                    if item not in return_dict[domain]:
                        return_dict[domain][item] = {}
                    if 'methods' not in return_dict[domain][item]:
                        return_dict[domain][item]['methods'] = []
                    return_dict[domain][item]['methods'].append('contained_in')
        return return_dict

    def confusables(self, source='whoisds'):
        self.__load(source)
        return_dict = {}
        for domain in self.domain:
            if domain not in return_dict:
                return_dict[domain] = {}
            confusables = list(self.__whoisds.confusables(domain))
            if confusables:
                for item in confusables:
                    if item not in return_dict[domain]:
                        return_dict[domain][item] = {}
                    if 'methods' not in return_dict[domain][item]:
                        return_dict[domain][item]['methods'] = []
                    return_dict[domain][item]['methods'].append('confusables')
        return return_dict

    def levenshtein(self, source='whoisds'):
        self.__load(source)
        return_dict = {}
        for domain in self.domain:
            if domain not in return_dict:
                return_dict[domain] = {}
            levenshtein = list(self.__whoisds.levenshtein(domain))
            if levenshtein:
                for item in levenshtein:
                    if item not in return_dict[domain]:
                        return_dict[domain][item] = {}
                    if 'methods' not in return_dict[domain][item]:
                        return_dict[domain][item]['methods'] = []
                    return_dict[domain][item]['methods'].append('levenshtein')
        return return_dict

    def __merge_dicts(self, destination, source):
        if isinstance(source, dict):
            for key,val in source.items():
                if key not in destination:
                    destination[key] = {}
                if val:
                    for k,v in val.items():
                        if k not in destination[key]:
                            destination[key][k] = {}
                        if 'methods' not in destination[key][k]:
                            destination[key][k]['methods'] = []
                        if v and isinstance(v.get('methods'), list):
                            for item in v.get('methods'):
                                destination[key][k]['methods'].append(item)
        return destination

    def all(self, source='whoisds'):
        self.__load(source)
        return_dict = {}
        return_dict.update(self.contained_in(source=source))
        return_dict = self.__merge_dicts(return_dict, self.confusables(source=source))
        return_dict = self.__merge_dicts(return_dict, self.levenshtein(source=source))
        return return_dict
