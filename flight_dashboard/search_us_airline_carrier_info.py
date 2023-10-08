from bokeh.models.widgets import DataTable, TableColumn, HTMLTemplateFormatter,\
                                 Div, Button, Panel, CheckboxGroup, TextInput
from bokeh.layouts import Column, Row
from bokeh.models import ColumnDataSource



class SearchAirlineCarrierInfo():
    cols = {'Airline Carrier': 'carrier',
        'Month of Flight': 'month',
        'Day of Flight': 'day',
        'Hour of Flight': 'hour',
        'Minute of Flight': 'minute',
        'Origin Airport': 'origin',
        'Destination Airport' : 'dest',
        'Departure Delay' : 'dep_delay',
        'Arrival Delay' : 'arr_delay'
        }
    

    def __init__(self, df):
        self.flights = df
        self.__column_instances = None
        self.__cds = None
        self.__n_rows_per_page = 15
        self.__page_number = Div()
        self.__prev_bttn = None
        self.__next_bttn = None 
        self.__carrier_checkboxes = None
        self.__txt_col_value = None
        self.__bttn_col_value = None
        self.__txt_col_header = None
        self.__bttn_col_header = None
        self.__column_name = None
        self.__column_value = None


    def make_carrier_tab(self):
        airline_carriers = list(set(self.flights['carrier'])) 
        airline_carriers.sort()
        
        # Create a logo and a checkbox widget
        checkbox_column = self.__create_logo_checkbox(airline_carriers)

        # Create a text input to get a table header
        txt_col_header_title, div_col_header = self.__create_header_input_and_bttn()

        # Create a text input to get a value for search
        txt_col_header_value, div_col_value = self.__create_val_input_and_bttn()
        
        # Get active airline carrier info from the dataframe self.flights
        carrier_airline_df = self.flights[self.flights['carrier'] == self.__carrier_checkboxes.
                                                                            labels[self.__carrier_checkboxes.active[0]]]
        self.__column_instances = carrier_airline_df.sort_values(['month', 'day'])

        self.__create_bttn_pagination()

        pagination_column = Row(self.__prev_bttn, self.__page_number, self.__next_bttn)
        search_col_header = Row(Column(txt_col_header_title, self.__txt_col_header),
                                Column(div_col_header, self.__bttn_col_header))
        search_col_value = Row(Column(txt_col_header_value, self.__txt_col_value),
                               Column(div_col_value, self.__bttn_col_value))
        widgets = Column(checkbox_column, search_col_header, search_col_value)

        self.__cds = ColumnDataSource(self.__column_instances)

        # set an initial value
        current_page = int(self.__page_number.text.split(' ')[1]) - 1
        self.__update_cds(None, None, current_page)
        init_layout = self.__make_layout()

        final_layout = Row(widgets, Column(init_layout, pagination_column))
        tab = Panel(child=final_layout, title='Search for The relevant details of Airline Carriers')

        return tab


    def __create_logo_checkbox(self, airline_carriers):
        logo_image_url = 'https://i.postimg.cc/t4hhFVqm/3.png'
        logo_html = f"<img src='{logo_image_url}' style='height: 100px; width: auto;'>"
        logo_div = Div(text=logo_html)

        checkbox_title = Div(text="<span style='font-family:TimesNewRoman; font-size:14px;'>\
                             Select a U.S. Airline Carrier each time below to see the information</span>")
        self.__carrier_checkboxes = CheckboxGroup(labels=airline_carriers, active=[0])
        self.__carrier_checkboxes.on_change('active', self.__reset_cds_using_checkbox)

        checkbox_column = Column(logo_div, checkbox_title, self.__carrier_checkboxes)

        return checkbox_column
    

    def __create_header_input_and_bttn(self):
        self.__txt_col_header = TextInput(value="", placeholder='e.g. Airline Carrier | month of flight')
        txt_col_header_title = Div(text='<span style="font-family:TimesNewRoman; font-size:14px;">According to the\
                                    headers shown in the table, Enter one of these headers</sapn>')
        
        self.__bttn_col_header = Button(label='Search', disabled=False, default_size=100)
        self.__bttn_col_header.on_click(self.__send_col_header)
        div_col_header = Div(style={'height' : '40px'}) 

        return txt_col_header_title, div_col_header
    

    def __create_val_input_and_bttn(self):
        self.__txt_col_value = TextInput(value="", placeholder='e.g. Alaska Airlines | 12')
        txt_col_header_value = Div(text='<span style="font-family:TimesNewRoman; font-size:14px;">Enter the value You\
                                    want to search</sapn>')
        
        self.__bttn_col_value = Button(label='Search', disabled=False, default_size=100)
        self.__bttn_col_value.on_click(self.__send_col_values)
        div_col_value = Div(style={'height' : '20px'})

        return txt_col_header_value, div_col_value
    

    def __create_bttn_pagination(self):
        self.__prev_bttn = Button(label='Previous Page', disabled=True, default_size=100)
        self.__next_bttn = Button(label='Next Page', disabled=False, default_size=100)
        self.__page_number.text = 'Page 1' # a symbolic number
        self.__prev_bttn.on_click(self.__previous_page) # event = click
        self.__next_bttn.on_click(self.__next_page)
    

    def __reset_cds_using_checkbox(self, attr, old, new):
        if len(new) > 1:
            self.__carrier_checkboxes.active = old

        if len(new) == 1:
            carrier_airline_df = self.flights[self.flights['carrier'] == self.__carrier_checkboxes.
                                                                        labels[self.__carrier_checkboxes.active[0]]]
            self.__column_instances= carrier_airline_df[['carrier', 'month', 'day', 'hour', 'minute',
                                                        'origin', 'dest', 'dep_delay', 'arr_delay']]
            self.__column_instances = self.__column_instances.sort_values(['month', 'day'])
            self.__update_cds(None, None, new=0) # reset table data


    # old <- a string header , new <- a string value
    def __reset_cds_using_search(self, attr, old, new):
        carrier_airline_df = self.flights[self.flights['carrier'] == self.__carrier_checkboxes.
                                                                        labels[self.__carrier_checkboxes.active[0]]]
        if (self.flights[old].dtypes == object) and (type(new) == str):
            carrier_airline_filtered = carrier_airline_df[carrier_airline_df[old] == new]

        if (self.flights[old].dtypes == int) and (type(new) == str):
            carrier_airline_filtered = carrier_airline_df[carrier_airline_df[old] == int(new)]

        if (self.flights[old].dtypes == float) and (type(new) == str):
            carrier_airline_filtered = carrier_airline_df[carrier_airline_df[old] == int(new)]

        self.__column_instances= carrier_airline_filtered[['carrier', 'month', 'day', 'hour', 'minute',
                                                        'origin', 'dest', 'dep_delay', 'arr_delay']]
        self.__column_instances = self.__column_instances.sort_values(['month', 'day'])
        self.__update_cds(None, None, new=0) # reset table data


    # create a handler function to understand whether a given column header exists
    def __send_col_header(self):
        text_input = self.__txt_col_header.value.split(' ')
        if len(text_input) == 3:
            (slice1, slice2, slice3) = (text_input[0].capitalize(),
                                        text_input[1].casefold(),
                                        text_input[2].capitalize())
            self.__txt_col_header.value = slice1 + " " + slice2 + " " + slice3

        elif len(text_input) == 2:
            slice1, slice2 = text_input[0].capitalize(), text_input[1].capitalize()
            self.__txt_col_header.value = slice1 + " " + slice2 

        else:
            self.__txt_col_header.value = "column {} not exists".format(self.__txt_col_header.value)
    
        if self.__txt_col_header.value in list(self.cols.keys()):
            self.__column_name = self.cols[self.__txt_col_header.value] # assign the same column as we saw in the original dataframe to the self.__column_name

        else:
            self.__txt_col_header.value = "Column {} not exists".format(self.__txt_col_header.value)     


    # create a handler function to understand whether a given value exists in the given header or not
    def __send_col_values(self):
        if (self.flights[self.cols[self.__txt_col_header.value]].dtypes == int) and (type(self.__txt_col_value.value) == str):
            carrier_airline_df = self.flights[self.flights[self.cols[self.__txt_col_header.value]] == int(self.__txt_col_value.value)]

        if (self.flights[self.cols[self.__txt_col_header.value]].dtypes == float) and (type(self.__txt_col_value.value) == str):
            carrier_airline_df = self.flights[self.flights[self.cols[self.__txt_col_header.value]] == float(self.__txt_col_value.value)]

        if (self.flights[self.cols[self.__txt_col_header.value]].dtypes == object) and (type(self.__txt_col_value.value) == str):
            carrier_airline_df = self.flights[self.flights[self.cols[self.__txt_col_header.value]] == self.__txt_col_value.value]
        
        if (carrier_airline_df.shape[0] != 0):
            self.__column_value = self.__txt_col_value.value # assign a string value
            self.__reset_cds_using_search(None, old=self.__column_name, new=self.__column_value)

        else:
            self.__txt_col_value.value = "Value {} not exists in Column {}".format(
                                        self.__txt_col_value.value, self.__txt_col_header.value)


    # create a handler function for the previous button
    def __previous_page(self):
        current_page =  int(self.__page_number.text.split(' ')[1]) - 1
        self.__update_cds(None, None, new=current_page - 1)


    # create a handler function for the next button
    def __next_page(self):
        current_page =  int(self.__page_number.text.split(' ')[1]) - 1
        self.__update_cds(None, None, new=current_page + 1)


    # define a callback function to update the data source and button states based on the selected page
    def __update_cds(self, attr, old, new):
        start = new * self.__n_rows_per_page
        end = start + self.__n_rows_per_page
        self.__cds.data = self.__column_instances.iloc[start:end, :].to_dict('list')

        if new == 0: # It shows the first page number
            self.__prev_bttn.disabled = True # deactivate
            
        else:
            self.__prev_bttn.disabled = False # activate

        if new == int(self.__column_instances.shape[0] / self.__n_rows_per_page) - 1: # It shows the last page number
            self.__next_bttn.disabled = True # deactivate

        else:
            self.__next_bttn.disabled = False # activate

        self.__page_number.text = f'Page {new + 1}'


    def __make_layout(self):
        columns = [
                TableColumn(field='carrier', title='<span style="font-family:TimesNewRoman; font-size:13px;">\
                            <b>Airline Carrier</b></span>', formatter=HTMLTemplateFormatter(template="<span style='font-family:\
                            TimesNewRoman;font-size:12px;'><%= value %></span>")),

                TableColumn(field='month', title='<span style="font-family:TimesNewRoman; font-size:13px;"><b>Month of Flight\
                            </b></span>', formatter=HTMLTemplateFormatter(template="<span style='font-family:Arial;\
                            font-size:12px;'><%= value %></span>")),

                TableColumn(field='day', title='<span style="font-family:TimesNewRoman; font-size:13px;"><b>Day of Flight\
                            </b></span>', formatter=HTMLTemplateFormatter(template="<span style='font-family:\
                            Arial; font-size:12px;'><%= value %></span>")),

                TableColumn(field='hour', title='<span style="font-family:TimesNewRoman; font-size:13px;"><b>Hour of Flight\
                            </b></span>', formatter=HTMLTemplateFormatter(template="<span style='font-family:Arial;\
                            font-size:12px;'><%= value %></span>")),

                TableColumn(field='minute', title='<span style="font-family:TimesNewRoman; font-size:13px;"><b>Minute of\
                            Flight</b></span>', formatter=HTMLTemplateFormatter(template= "<span style='font-family:Arial;\
                            font-size:12px;'><%= value %></span>")),

                TableColumn(field='origin', title='<span style="font-family:TimesNewRoman; font-size:13px;"><b>Origin\
                            Airport</b></span>', formatter=HTMLTemplateFormatter(template="<span style='font-family:\
                            TimesNewRoman; font-size:12px;'><%= value %></span>")),

                TableColumn(field='dest', title='<span style="font-family:TimesNewRoman; font-size:13px;"><b>Destination\
                            Airport</b></span>', formatter=HTMLTemplateFormatter(template="<span style='font-family:\
                            TimesNewRoman; font-size:12px;'><%= value %></span>")),

                TableColumn(field='dep_delay', title='<span style="font-family:TimesNewRoman; font-size:13px;"><b>Departure\
                            Delay</b></span>', formatter=HTMLTemplateFormatter(template="<span style='font-family:Arial;\
                            font-size:12px;'><%= value %></span>")),

                TableColumn(field='arr_delay', title='<span style="font-family:TimesNewRoman; font-size:13px;"><b>Arrival\
                            Delay</b></span>', formatter=HTMLTemplateFormatter(template="<span style='font-family:\
                            Arial; font-size:12px;'><%= value %></span>"))]
        
        table_title = Div(text="<h2 style='font-family:TimesNewRoman;'>The related information\
                        to the Flights of an Airline Carrier in 2013</h2>", align='center')
        
        table = DataTable(source=self.__cds, columns=columns,  autosize_mode='fit_columns', height=400,
            width=1265, sizing_mode= 'scale_both', background= "rgba(0,0,255,0.9)")
        
        table_pad = Div(style={'height' : '32px'})
        
        return Column(table_pad, table_title, table)