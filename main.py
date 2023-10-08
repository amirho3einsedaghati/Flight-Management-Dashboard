import pandas as pd
from bokeh.models.widgets import Tabs
from bokeh.io import curdoc
from bokeh.themes import Theme
from flight_dashboard.the_distribution_of_arrival_delay import DistArrDelay
from flight_dashboard.the_variability_of_arrival_delay import VarArrDelay
from flight_dashboard.search_us_airline_carrier_info import SearchAirlineCarrierInfo
from flight_dashboard.departure_time_summary import DepTimeSummary
from flight_dashboard.arrival_time_summary import ArrTimeSummary
from flight_dashboard.inference import Inference
from sqlalchemy import create_engine
from datetime import datetime
import os
import pickle


def load_data():
    username = 'Enter your username'
    password = 'Enter your password'
    server = 'localhost,1433'
    database = 'Enter your database name'
    driver ='ODBC Driver 18 for SQL Server'

    connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}"

    connect_args = {
        "TrustServerCertificate": "yes"
        }

    engine = create_engine(
        connection_string,
        connect_args = connect_args,
        echo=False
    )

    flights = pd.read_sql('SELECT origin, dest, distance, carrier, arr_time, dep_time, month, day, hour, minute, dep_delay, arr_delay FROM flights', engine).dropna()

    return flights, engine


def load_model_dependencies():
    def loading_data(data_name):

        return pickle.load(open(os.path.join(
            os.getcwd(),
            'model_dependencies',
            data_name
        ), 'rb'))
    
    skyc_le = loading_data('skyc_le')
    dep_time_le = loading_data('dep_time_le')
    sched_dep_time_le = loading_data('sched_dep_time_le')
    sched_arr_time_le = loading_data('sched_arr_time_le')
    arr_time_le = loading_data('arr_time_le')
    stacked_model = loading_data('stacked_model')

    return skyc_le, dep_time_le, sched_dep_time_le, sched_arr_time_le, arr_time_le, stacked_model


new_theme = Theme(
    json={
        'attrs': {
            'Figure': {
                'background_fill_color': "#212946", 
                'outline_line_color': "#212946",
                "border_fill_color": "#212946",
            },

            'Title': {
                'text_font': 'TimesNewRoman',
            },

            'Axis': {
                'axis_label_text_font': 'TimesNewRoman',
                'major_label_text_font': 'TimesNewRoman', 
                'axis_label_text_font_style': 'bold',
                'axis_label_text_color': '#F0F0F0',
                'major_label_text_color': '#F0F0F0',
                'axis_label_text_font_size' : '11pt',
                'major_label_text_font_size' : '11pt',
                'major_tick_line_color' : '#F0F0F0',
                'minor_tick_line_color' : '#F0F0F0',
                'minor_tick_in' : -3,
                'minor_tick_out' : 6
            },

            'Grid': {
                'grid_line_color': '#2A3459'
            },

            'Legend': {
                'label_text_font' : 'TimesNewRoman',
                'label_text_font_style' : 'bold',
                'label_text_color' : '#F0F0F0',
                'background_fill_color' : '#212946',
                'border_line_color': '#212946'
            },

            "Select": {
                'height' : 40,
                'height_policy' : 'fixed',
            },
            
            "TextInput": {
                'height' : 40,
                'height_policy' : 'fixed',
            },

            "TextAreaInput": {
                'height' : 60,
                'height_policy' : 'fixed',
            },

            "Slider": {
                'height' : 40,
                'height_policy' : 'fixed',
            },

            "RangeSlider": {
                'height' : 40,
                'height_policy' : 'fixed',
            },

            "Button": {
                'button_type' : 'primary',
                'height' : 40,
                'height_policy' : 'fixed',
            },

            "DatePicker" : {
                'height' : 40,
                'height_policy' : 'fixed', 
            }
        }
    }
)

# Apply your new theme to the current document
curdoc().theme = new_theme

def create_components(flights, engine, skyc_le, dep_time_le, sched_dep_time_le, sched_arr_time_le, arr_time_le, stacked_model, current_date):
    dist = DistArrDelay(df=flights[['carrier', 'arr_delay']], min=-80, max=160, bins=5)
    dist_tab = dist.make_hist_tab()

    dep_time = DepTimeSummary()
    dep_time_tab = dep_time.make_dep_time_tab(flights[['carrier', 'dep_time']])

    arr_time = ArrTimeSummary()
    arr_time_tab = arr_time.make_arr_time_tab(flights[['carrier', 'arr_time']])

    var = VarArrDelay(flights[['carrier', 'arr_delay', 'origin', 'dest']])
    var_tab = var.make_circle_tab()

    us_carriers = SearchAirlineCarrierInfo(flights[['carrier', 'arr_delay', 'dep_delay', 'month', 'day', 'hour', 'minute', 'origin', 'dest']])
    us_carriers_tab = us_carriers.make_carrier_tab()

    inference = Inference(skyc_le, dep_time_le, sched_dep_time_le, sched_arr_time_le, arr_time_le, stacked_model, flights[['origin', 'dest', 'distance']], engine)
    inference_tab = inference.make_inference_tab(current_date)

    return [inference_tab, dist_tab, var_tab, us_carriers_tab, dep_time_tab, arr_time_tab]

current_date = datetime.now()
current_date = "{:04d}-{:02d}-{:02d}".format(current_date.year, current_date.month, current_date.day)

# Load data and model dependencies
flights, engine = load_data()
skyc_le, dep_time_le, sched_dep_time_le, sched_arr_time_le, arr_time_le, stacked_model = load_model_dependencies()

# Create the components
components = create_components(flights, engine, skyc_le, dep_time_le, sched_dep_time_le, sched_arr_time_le, arr_time_le, stacked_model, current_date)

# Create the tabs
tabs = Tabs(tabs=components)

# Add the tabs to the document
curdoc().add_root(tabs)
curdoc().title = 'Flight Management Dashboard'
