import dal
from exceptions import DalException, BusinessLogicException
from logging_config import get_logger
from models import Airport
from io import StringIO
import csv


"""
This module contains logic to parse airport data from a website into Airport objects. It also contains a class to build
a dict of search parameters so that the user may search through the Airport objects.

Methods:
--------
    process_response(response, tk_instance, show_all=False):
        callback function for the AirportAdapter, processes response from the url into airport objects
    retrieve_airport_data(tk_instance, show_all=False):
        constructs an adapter and executor class from the DAL, and calls on them to retrieve data.
    write_results_to_txt(results):
        passes along a request from the gui to the dal to export the current results to results_export.dat
    parse_line(line):
        uses csv-reader to handle commas that are within double quotes within the lines of the results 
        
Classes:
--------
    AirportSearchBuilder:
        builds a dict of search parameters so that the user may search through the airport objects. 
        
Constants:
----------
    URL: the url that contains the airport data. 
    GOOD_STATUS_CODE: the status code I want from the URL request (200)
"""

URL = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'
GOOD_STATUS_CODE = 200
logger = get_logger(__name__)


def process_response(response, tk_instance, show_all=False):
    """
    callback function for the AirportAdapter, processes response from the url into airport objects
    :param response: response from the url
    :param tk_instance: tk instance that is calling this and other functions
    :param show_all: true if the gui is calling to show all airports, false if not
    :return: returns a list of airport objects to the gui layer
    """
    if response.status_code == GOOD_STATUS_CODE:
        airport_list = []
        for line in response.iter_lines():
            try:
                tokens = parse_line(line)
                airport = Airport(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4], tokens[5], tokens[6],
                                  tokens[7], tokens[8], tokens[9], tokens[10])
                airport_list.append(airport)
            except BusinessLogicException:
                raise
        logger.info('returning list of airport objects')
        tk_instance.after(0, tk_instance.set_airport_list, airport_list)
        if show_all:
            tk_instance.after(0, tk_instance.update_all)
        else:
            tk_instance.after(0, tk_instance.update_results)
    else:
        logger.error("Bad Response")
        raise BusinessLogicException


def retrieve_airport_data(tk_instance, show_all=False):
    """
    constructs an adapter and executor class from the DAL, and calls on them to retrieve data.
    :param tk_instance: the tkinter instance that is calling this function
    :param show_all: true if the gui is calling to show all airports, false if not
    :return: nothing directly, calls process_response as a callback.
    """
    try:
        adapter = dal.AirportAdapter(tk_instance, process_response, show_all)
        executor = dal.APIExecutor(adapter)
        executor.execute(URL)
    except DalException:
        logger.error("Failed to execute")
        raise BusinessLogicException


def write_results_to_txt(results):
    """
    calls the dal.write_results_to_txt method to write results from the gui to results_export.dat
    :param results: the results from the gui results_text field.
    :return: really nothing, calls a method from the dal to write data to a text file...
    """
    try:
        logger.info('Writing results to results_export.dat')
        return dal.write_results_to_txt(results)
    except DalException:
        raise BusinessLogicException


def parse_line(line):
    """
    parses a csv-like line into tokens
    :param line: line to be parsed
    :return: tokens from a csv line
    """
    try:
        line = line.decode('utf-8')
        fake_csv = StringIO(line)
        reader = csv.reader(fake_csv)
        tokens = next(reader)
        return tokens
    except Exception:  # TODO look into replacing this with something more specific.
        logger.error('Error parsing line with csv reader')
        raise BusinessLogicException


class AirportSearchBuilder:
    def __init__(self):
        self._params = {}

    def __str__(self):
        return ''.join(f"{key}, {value}\n" for key, value in self._params.items())

    def with_param(self, param_name, param_value):
        """
        adds a search parameter to the dict contained in self._params
        :param param_name: key
        :param param_value: value
        :return: self
        """
        self._params[param_name] = param_value
        return self

    def build(self):
        """
        returns self._params
        :return: dictionary of search parameters
        """
        return self._params

