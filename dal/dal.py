import requests
from exceptions import DalException
from logging_config import get_logger

"""
This module contains classes to retrieve and return data from a website, as well as a method to export results from
the gui to results_export.dat

Methods:
--------
    write_results_to_txt(results):
        writes results from the gui to a text file called results_export.dat
        
Classes:
--------
    APIExecutor:
        used to submit AirportAdapter.run() into a threadpool executor. 
    AirportAdapter:
        retrieves a response from a provided URL, checks for several errors.        

"""

logger = get_logger(__name__)


class APIExecutor:
    def __init__(self, adapter):
        self.adapter = adapter

    def execute(self, *args, **kwargs):
        """
        calls the threadpool executor from tk_instance to run AirportAdapter.
        :param args: arguments
        :param kwargs: keyword arguments
        :return: n/a
        """
        try:
            self.adapter.tk_instance.executor.submit(self.adapter.run, *args, **kwargs)
        except DalException:
            raise


class AirportAdapter:
    def __init__(self, tk_instance, callback, show_all=False):
        self.tk_instance = tk_instance
        self.callback = callback
        self.show_all = show_all

    def run(self, url):
        """
        attempts to retrieve data from the provided url
        :param url: url to find the data
        :return: the results of the url request
        """
        try:
            logger.info("Getting airport data")
            response = requests.get(url, stream=True)
            self.callback(response, self.tk_instance, self.show_all)
        except requests.Timeout as time_out:
            logger.error(f"Request timed out: {time_out}")
            raise DalException
        except requests.ConnectionError as connection_error:
            logger.error(f"Connection failed: {connection_error}")
            raise DalException
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise DalException


def write_results_to_txt(results):
    """
    writes results from the gui to a text file called results_export.dat
    :param results: results from the results field in the gui
    :return: nothing, writes to file
    """
    try:
        with open('results_export.dat', 'w', newline='', encoding='UTF 8') as file:
            for line in results:
                file.write(line)
        logger.info('exported results to results_export.dat')
    except Exception:
        logger.error('unable to export results to results_export.dat')
        raise DalException
