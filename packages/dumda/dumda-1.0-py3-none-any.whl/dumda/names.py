import csv
from random import choice


class Names:

    def __init__(self):
        __file = open('baby-names.csv', 'r', encoding='utf-8')
        self.__reader = csv.DictReader(__file)

    def get_all(self):
        """
        take in consideration that this is 10s of thousands of names
        :return: list
        """
        return [name['name'] for name in list(self.__reader)]

    def get_single(self):
        """
        returns a single random name of any sex
        :return: str
        """

        return choice(self.get_all())

    def boy_names(self, n=None):
        """
        returns a list a given amount of boy designated names
        :param n: int
        :return: list
        """
        boys = [name['name'] for name in list(self.__reader)
                if name['sex'] == 'boy']
        # Check if no number was passed
        if n is None:
            return boys
        else:
            return self.get_random(n, boys)

    def girl_names(self, n=None):
        """
        returns a list a given amount of girl designated names
        :param n: int
        :return: list
        """

        girls = [name['name'] for name in list(self.__reader)
                 if name['sex'] == 'girl']

        if n is None:
            return girls
        else:
            return self.get_random(n, girls)

    def get_random(self, n, name_dir=None):
        """
        returns a list of random names based on a given amount
        :param name_dir:
        :param n: int
        :return:
        """
        if name_dir is None:
            name_dir = self.get_all()
        name_list = list()

        # Iterate through the given number
        for _ in range(n):
            name = choice(name_dir)
            # Make sure there are no repeat names in the final list
            while name in name_list:
                name = choice(name_dir)

            name_list.append(name)

        return name_list
