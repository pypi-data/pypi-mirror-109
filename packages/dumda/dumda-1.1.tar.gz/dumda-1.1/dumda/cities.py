from random import choice
import csv
import os

class Cities:

    def __init__(self):

        __csv_path = os.path.join("dumda", "world_cities.csv")
        __file = open(__csv_path, 'r', encoding='utf-8')
        self.__reader = csv.DictReader(__file)

    def get_all(self):
        """
        return list of all cities
        :return:
        """
        return [city['name'].rstrip() for city in list(self.__reader)]

    def get_single(self, country=None):
        """
        returns a string of a random city
        :param country: str, optional parameter choosing which country the city is from
        :return: str, city name
        """
        # Check if there a country preference was given
        if country is None:
            return choice(self.get_all())
        else:
            return choice(self.get_by_country(country))

    def get_random_cities(self, n):
        """
        returns a list of random cities in the given amount
        :param n: int, number of desired cities
        :return: list
        """
        cities = list()

        # Iterate through the given number
        for _ in range(n):
            city = choice(self.get_all())
            # Make sure there are no repeat cities in the final list
            while city in cities:
                city = choice(self.get_all())

            cities.append(city)

        return cities

    def get_by_country(self, name):
        """
        returns a list of cities based on a given country
        Note: There is only 'United Kingdom' not England
        :param name: str, country name
        :return: list
        """
        return [city['name'] for city in self.get_all()
                if city['country'].lower() == name.lower()]

    def get_by_letter(self, letter):
        """
        returns a list of cities based on a given letter
        :param letter: chr
        :return: list
        """
        cities = list()

        for city in self.get_all():
            if city[0].lower() == letter:
                cities.append(city)

        return cities