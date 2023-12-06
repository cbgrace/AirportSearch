import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk, messagebox
import business as b
import validation
from exceptions import BusinessLogicException


"""
In this module we have a class, AirportForm, that creates a gui for the user to interact with in order to search 
for airports based on various parameters.

Methods:
--------
    create_widgets(self):
        Creates the widgets in the GUI form AirportForm
    search_onclick(self):
        handles the click event for the search button
    clear_onclick(self):
        handles the click event for the clear button
    export_onclick(self):
        passes the contents of the results text to a method which will export them to results_export.txt
    show_all_onclick(self):
        handles click event for the 'show all' button
    get_search_params(self):
        builds a dict of search parameters that the user selects/inputs
    filter_airport_results(self):
        filters a list of airport objects by checking for matches to the user's search parameters
    update_results(self):
        updates the GUI with results from a search
    update_all(self):
        updates the GUI with results if user selects "update all"
    display_error(self, message):
        displays an error message
    update_text(self, message):
        Updates results_text with a given message
    validation_error_message(self, entry):
        displays error message if there is a validation issue with the search parameters
    on_close(self):
        shuts down the executor if the gui is closed
    set_airport_list(cls, list_to_set):
        used to update the airport list from outside of this class
        
Constants:
----------
    COUNTRY_LIST: list of countries to select from (pulled from website provided in assignment)
    DST_LIST: list of DST options pulled from website provided in assignment
"""


COUNTRY_LIST = ['ALL', 'Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Angola', 'Anguilla', 'Antarctica',
                'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Ashmore and Cartier Islands', 'Australia',
                'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Baker Island', 'Bangladesh', 'Barbados', 'Belarus',
                'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bonaire, Saint Eustatius and Saba',
                'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory',
                'British Virgin Islands', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde',
                'Cambodia', 'Cameroon', 'Canada', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile',
                'China', 'Christmas Island', 'Clipperton Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros',
                'Congo Republic', 'Cook Islands', 'Coral Sea Islands', 'Costa Rica', "Cote d'Ivoire", 'Croatia',
                'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic',
                'DR Congo', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini',
                'Ethiopia', 'Europa Island', 'Faeroe Islands', 'Falkland Islands', 'Fiji', 'Finland', 'France',
                'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia',
                'Germany', 'Ghana', 'Gibraltar', 'Glorioso Islands', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe',
                'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti',
                'Heard and McDonald Islands', 'Honduras', 'Hong Kong', 'Howland Island', 'Hungary', 'Iceland', 'India',
                'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica',
                'Jan Mayen', 'Japan', 'Jarvis Island', 'Jersey', 'Johnston Atoll', 'Jordan', 'Juan de Nova Island',
                'Kazakhstan', 'Kenya', 'Kingman Reef', 'Kiribati', 'Kuwait', 'Kyrgyz Republic', 'Laos', 'Latvia',
                'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia',
                'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique',
                'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Fed. Sts.', 'Midway Islands', 'Moldova',
                'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia',
                'Nauru', 'Navassa Island', 'Nepal', 'Netherlands', 'Netherlands Antilles', 'New Caledonia',
                'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'North Korea',
                'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Palestine',
                'Palmyra Atoll', 'Panama', 'Papua New Guinea', 'Paracel Islands', 'Paraguay', 'Peru', 'Philippines',
                'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda',
                'Samoa', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone',
                'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa',
                'South Georgia and South Sandwich Is.', 'South Korea', 'South Sudan', 'Spain', 'Spratly Islands',
                'Sri Lanka', 'St. Helena', 'St. Kitts and Nevis', 'St. Lucia', 'St. Pierre and Miquelon',
                'St. Vincent and the Grenadines', 'Sudan', 'Suriname', 'Svalbard and Jan Mayen Islands', 'Sweden',
                'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo',
                'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tromelin Island', 'Tunisia', 'Turkey', 'Turkmenistan',
                'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom',
                'United States', 'United States Virgin Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela',
                'Vietnam', 'Wake Island', 'Wallis and Futuna Islands', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe']

DST_LIST = ['Unknown', 'European', 'US/Canada', 'S. America', 'Australia', 'New Zealand', 'None']


class AirportForm(tk.Tk):
    airport_list = []

    def __init__(self):
        super().__init__()
        self.title("Airport Search")
        self.create_widgets()
        self.executor = ThreadPoolExecutor()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        """
        Creates the widgets in the GUI form AirportForm
        :return: n/a
        """
        # first row labels
        self.airport_name_label = ttk.Label(self, text='Airport name: ')
        self.airport_name_label.grid(row=0, column=0, padx=5, sticky='w')
        self.iata_label = ttk.Label(self, text='IATA/FAA: ')
        self.iata_label.grid(row=0, column=1, padx=5)
        self.icao_label = ttk.Label(self, text='ICAO: ')
        self.icao_label.grid(row=0, column=2, padx=5)

        # second row entries
        self.airport_name_entry = ttk.Entry(self)
        self.airport_name_entry.grid(row=1, column=0, padx=5, pady=5)
        self.iata_entry = ttk.Entry(self, width=5)
        self.iata_entry.grid(row=1, column=1, padx=5, pady=5)
        self.icao_entry = ttk.Entry(self, width=5)
        self.icao_entry.grid(row=1, column=2, padx=5, pady=5)

        # third row labels
        self.city_name_label = ttk.Label(self, text='City name: ')
        self.city_name_label.grid(row=2, column=0, padx=5, stick="w")
        self.country_name_label = ttk.Label(self, text="Country name: ")
        self.country_name_label.grid(row=2, column=1, padx=5)

        # fourth row entries
        self.city_name_entry = ttk.Entry(self)
        self.city_name_entry.grid(row=3, column=0, padx=5, pady=5)
        self.country_name_combo = ttk.Combobox(self, values=COUNTRY_LIST, state='readonly')
        self.country_name_combo.grid(row=3, column=1, padx=5, pady=5)

        # fifth row labels
        self.latitude_label = ttk.Label(self, text='Latitude: ')
        self.latitude_label.grid(row=4, column=0, padx=5, sticky='w')
        self.longitude_label = ttk.Label(self, text='Longitude: ')
        self.longitude_label.grid(row=4, column=1, padx=5)
        self.elevation_label = ttk.Label(self, text='Elevation: ')
        self.elevation_label.grid(row=4, column=2, padx=5)
        self.utc_label = ttk.Label(self, text='UTC')
        self.utc_label.grid(row=4, column=3, padx=5)
        self.dst_label = ttk.Label(self, text='DST')
        self.dst_label.grid(row=4, column=4, padx=5)

        # sixth row entries
        self.latitude_entry = ttk.Entry(self)
        self.latitude_entry.grid(row=5, column=0, padx=5, pady=5)
        self.longitude_entry = ttk.Entry(self)
        self.longitude_entry.grid(row=5, column=1, padx=5, pady=5)
        self.elevation_entry = ttk.Entry(self, width=12)
        self.elevation_entry.grid(row=5, column=2, padx=5, pady=5)
        self.utc_entry = ttk.Entry(self, width=5)
        self.utc_entry = ttk.Entry(self, width=5)
        self.utc_entry.grid(row=5, column=3, padx=5, pady=5)
        self.dst_combo = ttk.Combobox(self, values=DST_LIST, state='readonly')
        self.dst_combo.grid(row=5, column=4, padx=5, pady=5)

        # frame for buttons
        self.button_frame = ttk.Frame(self, width=25, borderwidth=5, relief='sunken')
        self.button_frame.grid(row=0, rowspan=4, column=3, columnspan=2, padx=5, pady=5, ipady=5)

        # buttons
        self.search_button = ttk.Button(self.button_frame, text="Search", command=self.search_onclick)
        self.search_button.grid(row=1, column=3, padx=5, pady=5)
        self.clear_button = ttk.Button(self.button_frame, text="Clear", command=self.clear_onclick)
        self.clear_button.grid(row=1, column=4, padx=5, pady=5)
        self.export_button = ttk.Button(self.button_frame, text="Export", command=self.export_onclick, state='disabled')
        self.export_button.grid(row=2, column=3, padx=5, pady=5)
        self.show_all_button = ttk.Button(self.button_frame, text="Show All", command=self.show_all_onclick)
        self.show_all_button.grid(row=2, column=4, padx=5, pady=5)

        # results
        self.number_of_results_label = ttk.Label(self, text="Number of Results: ")
        self.number_of_results_label.grid(row=6, column=0, padx=5, pady=5)
        self.results_text = tk.Text(self, width=80, height=15, state='disabled')
        self.results_text.grid(row=7, column=0, columnspan=5, padx=5, pady=5)

    def search_onclick(self):
        """
        handles the click event for the search button
        :return: n/a
        """
        try:
            b.retrieve_airport_data(self)
            self.export_button.config(state='normal')
        except BusinessLogicException as e:
            self.display_error(f"Some error occurred: {e}")

    def clear_onclick(self):
        """
        handles the click event for the clear button
        :return: n/a
        """
        self.airport_name_entry.delete(0, tk.END)
        self.iata_entry.delete(0, tk.END)
        self.icao_entry.delete(0, tk.END)
        self.city_name_entry.delete(0, tk.END)
        self.country_name_combo.set("")
        self.latitude_entry.delete(0, tk.END)
        self.longitude_entry.delete(0, tk.END)
        self.elevation_entry.delete(0, tk.END)
        self.utc_entry.delete(0, tk.END)
        self.dst_combo.set("")
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END)
        self.results_text.config(state='disabled')
        self.export_button.config(state='disabled')
        self.number_of_results_label.config(text="Number of Results: 0")

    def export_onclick(self):
        """
        passes the contents of the results text to a method which will export them to results_export.txt
        :return: n/a
        """
        results = self.results_text.get(0.0, tk.END)
        if len(results) < 20:  # I chose 20 arbitrarily, for some reason if results == "" did not work here, even
            # if the results text was cleared immediately before.
            # I suspect a newline character or something, but I don't know...
            messagebox.showinfo('Error', 'Will not export with no results')
            return
        try:
            b.write_results_to_txt(results)
            messagebox.showinfo('Success', 'Data Exported to results_export.dat')
        except BusinessLogicException:
            messagebox.showinfo('Error', 'Unable export data.')

    def show_all_onclick(self):
        """
        handles click event for the 'show all' button
        :return: n/a
        """
        try:
            b.retrieve_airport_data(self, True)
            self.export_button.config(state='normal')
        except BusinessLogicException as e:
            self.display_error(f"Some error occurred: {e}")

    def get_search_params(self):
        """
        builds a dict of search parameters that the user selects/inputs
        :return: a dict of search parameters from the gui (or if there is some validation error, returns nothing)
        """
        # build the search params with a builder...
        builder = b.AirportSearchBuilder()
        # go through each entry one by one and if there is anything in it, add it to the builder
        airport_name = self.airport_name_entry.get()
        if airport_name != "":
            builder.with_param('airport_name', airport_name)
        iata_code = self.iata_entry.get()
        if iata_code != "":
            if validation.validate_iata(iata_code):
                builder.with_param('iata_code', iata_code)
            else:
                self.validation_error_message('IATA')
                return
        icao_code = self.icao_entry.get()
        if icao_code != "":
            if validation.validate_icao(icao_code):
                builder.with_param('icao_code', icao_code)
            else:
                self.validation_error_message('IACO')
                return
        city_name = self.city_name_entry.get()
        if city_name != "":
            builder.with_param('city_name', city_name)
        country_name = self.country_name_combo.get()
        if country_name != "":
            builder.with_param('country_name', country_name)
        latitude = self.latitude_entry.get()
        longitude = self.longitude_entry.get()
        if latitude != "":
            if longitude != "":
                if validation.is_float(latitude):
                    builder.with_param('latitude', latitude)
                else:
                    self.validation_error_message('Latitude')
                    return
            else:
                self.display_error('Must include a latitude AND longitude, or neither!')
                return
        if longitude != "":
            if latitude != "":
                if validation.is_float(longitude):
                    builder.with_param('longitude', longitude)
                else:
                    self.validation_error_message('Longitude')
                    return
            else:
                self.display_error('Must include a latitude AND longitude, or neither!')
                return
        elevation = self.elevation_entry.get()
        if elevation != "":
            if validation.is_positive_int(elevation):
                builder.with_param('elevation', elevation)
            else:
                self.validation_error_message('Elevation')
                return
        utc_offset = self.utc_entry.get()
        if utc_offset != "":
            if validation.validate_utc(utc_offset):
                builder.with_param('utc_offset', utc_offset)
            else:
                self.validation_error_message("UTC")
                return
        dst_area = self.dst_combo.get()
        if dst_area != "":
            builder.with_param('dst_area', dst_area)
        if len(builder.build()) == 0:
            self.display_error("You must use at least 1 parameter")
        return builder.build()

    def filter_airport_results(self):
        """
        filters a list of airport objects by checking for matches to the user's search parameters
        :return: a list of airport objects that match
        """
        results = []  # blank list to store results
        params = self.get_search_params()  # build search parameters into a dict
        for item in self.airport_list:
            if item.check_for_match(params):
                results.append(item)
        return results

    def update_results(self):
        """
        updates the GUI with results from a search
        :return: n/a
        """
        results = self.filter_airport_results()
        self.update_text(''.join(f"{airport}\n" for airport in results))
        self.number_of_results_label.config(text=f"Number of Results: {len(results)}")

    def update_all(self):
        """
        updates the GUI with results if user selects "update all"
        :return:
        """
        results = self.airport_list
        self.update_text(''.join(f"{airport}\n" for airport in results))
        self.number_of_results_label.config(text=f"Number of Results: {len(results)}")

    def display_error(self, message):
        """
        displays an error message
        :param message: what you want show the user
        :return: messagebox with error message
        """
        return messagebox.showinfo('Error', f"{message}")

    def update_text(self, message):
        """
        Updates results_text with a given message
        :param message: message to display to results_text
        :return: n/a
        """
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert(tk.END, f"{message}")
        self.results_text.config(state='disabled')

    def validation_error_message(self, entry):
        """
        displays error message if there is a validation issue with the search parameters
        :param entry: the field where the validation error has occurred
        :return: messagebox with error message
        """
        return messagebox.showinfo('Error', f'Invalid entry in the {entry} field.')

    def on_close(self):
        """
        shuts down the executor if the gui is closed
        :return: n/a
        """
        self.executor.shutdown(wait=False)
        self.destroy()

    @classmethod
    def set_airport_list(cls, list_to_set):
        """
        used to update the airport list from outside of this class
        :param list_to_set: list of airport objects
        :return: n/a
        """
        cls.airport_list = list_to_set

