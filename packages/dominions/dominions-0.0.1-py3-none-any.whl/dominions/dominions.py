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
        return_list = []
        for domain in self.domain:
            return_list.extend(list(self.__whoisds.contained_in(domain)))
        return return_list

    def confusables(self, source='whoisds'):
        self.__load(source)
        return_list = []
        for domain in self.domain:
            return_list.extend(list(self.__whoisds.confusables(domain)))
        return return_list

    def levenshtein(self, source='whoisds'):
        self.__load(source)
        return_list = []
        for domain in self.domain:
            return_list.extend(list(self.__whoisds.levenshtein(domain)))
        return return_list

    def all(self, source='whoisds'):
        self.__load(source)
        return_list = []
        for domain in self.domain:
            return_list.extend(list(self.__whoisds.levenshtein(domain)))
            return_list.extend(list(self.__whoisds.confusables(domain)))
            return_list.extend(list(self.__whoisds.levenshtein(domain)))
        return return_list
