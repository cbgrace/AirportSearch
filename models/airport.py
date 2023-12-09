"""
This module contains a single class to model airport data

Methods:
--------
    check_for_match(self, param_dict):
        checks this current airport object for matches to the provided param_dict.
    convert_dst_value(self, value):
        converts the dst value from the gui (full words) to the single-letter values from the data
"""


class Airport:
    def __init__(self, airport_id, airport_name, city_name, country_name, iata_code, icao_code, latitude, longitude,
                 elevation, utc_offset, dst_area):
        self._airport_id = airport_id  # probably will use this to remove duplicates from search results?
        self._airport_name = airport_name
        self._city_name = city_name
        self._country_name = country_name
        self._iata_code = iata_code
        self._icao_code = icao_code
        self._latitude = latitude
        self._longitude = longitude
        self._elevation = elevation
        self._utc_offset = utc_offset
        self._dst_area = dst_area

    def __str__(self):
        # this is all the information that the form provides...
        if self._iata_code == '\\N':
            return f"{self._airport_name} ({self._icao_code}), {self._country_name}"
        return f"{self._airport_name} ({self._iata_code}), {self._country_name}"

    def __repr__(self):
        if self._iata_code == '\\N':
            return f"{self._airport_name} ({self._icao_code}), {self._country_name}"
        return f"{self._airport_name} ({self._iata_code}), {self._country_name}"

    def check_for_match(self, param_dict):
        """
        checks this current airport object for matches to the provided param_dict.
        :param param_dict: a dictionary of search parameters from the GUI
        :return: returns True if all submitted fields are a match, false if not
        """
        number_of_matches_needed = len(param_dict.keys())
        number_of_matches = 0
        if 'airport_name' in param_dict.keys():
            if param_dict['airport_name'].upper() in self._airport_name.upper():
                number_of_matches += 1
        if 'city_name' in param_dict.keys():
            if param_dict['city_name'].upper() in self._city_name.upper():
                number_of_matches += 1
        if 'iata_code' in param_dict.keys():
            if param_dict['iata_code'].upper() == self._iata_code.upper():
                number_of_matches += 1
        if 'icao_code' in param_dict.keys():
            if param_dict['icao_code'].upper() == self._icao_code.upper():
                number_of_matches += 1
        if 'country_name' in param_dict.keys():
            if param_dict['country_name'].upper() == self._country_name.upper().strip('"'):
                number_of_matches += 1
            elif param_dict['country_name'].upper() == 'ALL':
                number_of_matches += 1
        if 'utc_offset' in param_dict.keys():
            if self._utc_offset != "\\N":
                if float(param_dict['utc_offset']) == float(self._utc_offset):
                    number_of_matches += 1
        if 'latitude' in param_dict.keys() and 'longitude' in param_dict.keys():
            airport_lat = round(float(self._latitude), 2)
            airport_lon = round(float(self._longitude), 2)
            search_lat = round(float(param_dict['latitude']), 2)
            search_lon = round(float(param_dict['longitude']), 2)
            if airport_lat == search_lat and airport_lon == search_lon:
                number_of_matches += 2
        if 'elevation' in param_dict.keys():
            # I had no idea what to do with elevation???
            if int(param_dict['elevation']) <= int(self._elevation):
                number_of_matches += 1
        if "dst_area" in param_dict.keys():
            value = self.convert_dst_value(param_dict['dst_area'])
            if value == self._dst_area:
                number_of_matches += 1
        if number_of_matches == number_of_matches_needed:
            return True
        else:
            return False

    def convert_dst_value(self, value):
        """
        converts the dst value from the gui (full words) to the single-letter values from the data
        :param value: dst value from the dropdown in the gui
        :return: the single-letter equivalent for the provided dst value.
        """
        if value == 'European':
            return 'E'
        elif value == 'US/Canada':
            return 'A'
        elif value == 'S. America':
            return 'S'
        elif value == 'Australia':
            return 'O'
        elif value == 'New Zealand':
            return 'Z'
        elif value == 'None':
            return 'N'
        elif value == 'Unknown':
            return 'U'
