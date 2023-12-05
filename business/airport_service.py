import dal
import time
from exceptions import DalException, BusinessLogicException
from logging_config import get_logger
from models import Airport
from io import StringIO
import csv


URL = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'
logger = get_logger(__name__)


def process_response(response, tk_instance):
    if response.status_code == 200:
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
        tk_instance.after(0, tk_instance.update_results)
    else:
        # TODO probably need to improve this error handling
        logger.error("Bad Response")
        raise BusinessLogicException


def retrieve_airport_data(tk_instance):
    try:
        adapter = dal.AirportAdapter(tk_instance, process_response)
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
    except Exception:
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

