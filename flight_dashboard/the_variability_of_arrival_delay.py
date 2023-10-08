from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import Select, Div
from bokeh.layouts import Column, Row
from itertools import chain
from bokeh.models import FuncTickFormatter
from bokeh.models.tickers import FixedTicker



class VarArrDelay():
    def __init__(self, df):
        self.flights = df
        self.__cds = ColumnDataSource() # the original ColumnDataSource Object
        self.__carrier_dict = dict()
        self.__origin_ddmenu  = None
        self.__dest_ddmenu = None 
        self.__fig = None 


    def make_circle_tab(self):
        originAP = self.flights['origin'].unique().tolist()
        originAP.sort()
        destAP = self.flights['dest'].unique().tolist()
        destAP.sort()

        logo_div = self.__create_logo()

        # create a dropdown menu for orgin and destination airports 
        ddmenu_origin_style, ddmenu_origin_text, ddmenu_dest = self.__create_dropdown_menu_widgets(originAP, destAP)

        # set an initial value
        self.__cds, self.__carrier_dict = self.__prepare_data(self.__origin_ddmenu.value, self.__dest_ddmenu.value)
        
        fig = self.__make_circle_plot(self.__cds, self.__carrier_dict)

        widgets = Column(logo_div, ddmenu_origin_style, ddmenu_origin_text, self.__origin_ddmenu, ddmenu_dest, self.__dest_ddmenu)
        content = Row(widgets, fig)
        circle_tab = Panel(child=content, title='The Variability of Arrival Delay')

        return circle_tab


    def __create_logo(self):
        logo_image_url = 'https://i.postimg.cc/t4hhFVqm/3.png'
        logo_html = f"<img src='{logo_image_url}' style='height: 100px; width: auto;'>"
        logo_div = Div(text=logo_html)

        return logo_div
    

    def __create_dropdown_menu_widgets(self, originAP, destAP):
        ddmenu_origin_style = Div(style={'height' : '120px'})
        ddmenu_origin_text = Div(text="<span style='font-family:TimesNewRoman; font-size:14px;'>\
                             The IATA Codes of The Origin Airports</span>")
        self.__origin_ddmenu = Select(value=originAP[1], options=originAP)
        self.__origin_ddmenu.on_change('value', self.__update)

        ddmenu_dest = Div(text="<span style='font-family:TimesNewRoman; font-size:14px;'>\
                             The IATA Codes of The Destination Airports</span>")
        self.__dest_ddmenu = Select(value=destAP[5], options=destAP)
        self.__dest_ddmenu.on_change('value', self.__update)

        return ddmenu_origin_style, ddmenu_origin_text, ddmenu_dest
    
    
    def __prepare_data(self, origin, dest):
        origin_dest_df = self.flights[(self.flights['origin'] == origin) & (self.flights['dest'] == dest)]
        airline_carriers = origin_dest_df['carrier'].unique().tolist()

        delays, carrier_indexes, dic= [], [], {}
        for i, carrier in enumerate(airline_carriers):
            carrier_instances = origin_dest_df[origin_dest_df['carrier'] == carrier]
            delays.append(list(carrier_instances['arr_delay']))
            carrier_indexes.append([i for _ in range(len(carrier_instances['arr_delay']))])
            dic.update({i : carrier})

        delays = list(chain(*delays))
        carrier_indexes = list(chain(*carrier_indexes))

        cds = ColumnDataSource({'x' : delays, 'y': carrier_indexes})

        return cds, dic
     

    def __update(self, attr, old, new): # a Callback function 
        new_cds, new_dict = self.__prepare_data(self.__origin_ddmenu.value, self.__dest_ddmenu.value)
        self.__cds.data.update(new_cds.data)

        self.__carrier_dict.update(new_dict)

        self.__fig.yaxis[0].ticker.desired_num_ticks = len(new_dict)
        self.__fig.yaxis.ticker = FixedTicker(ticks = list(range(len(new_dict))))
        self.__fig.yaxis.formatter = FuncTickFormatter(
               code = """
                var labels = %s;
                return labels[tick];
                """ % new_dict)
                                                                            

    def __make_circle_plot(self, cds, dic):
        self.__fig = figure(plot_width=700, plot_height=600)
        self.__fig.circle(source=cds, x='x', y='y', color='white', 
                    size=10, alpha=.4)
        
        self.__fig.yaxis[0].ticker.desired_num_ticks = len(dic)
        self.__fig.yaxis.ticker = FixedTicker(ticks = list(range(len(dic))))
        self.__fig.yaxis.formatter = FuncTickFormatter(
            code = """
            var labels = %s;
            return labels[tick];
            """ % dic)

        title = Div(text="<span style='font-family:TimesNewRoman; font-size:13pt'><strong>The Arrival delay in Minutes from the selected Origin NYC Airports to the\n\
                    Destination Airports for the different U.S. Airline Carriers in 2013</strong></span>", align='center')
        
        self.__fig.xaxis.axis_label = "The arrival delay for the flights of each individual airline carrier"
        self.__fig.yaxis.axis_label = "Airline Carriers"

        return Column(title, self.__fig)
