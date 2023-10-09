import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel, Div
from bokeh.palettes import Category20_19
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider
from bokeh.layouts import Column, Row



class DistArrDelay():
    def __init__(self, df, min, max, bins):
        self.flights = df
        self.__re = max
        self.__rs = min
        self.__distance = self.__re - self.__rs
        self.__bins = bins
        self.__cds = ColumnDataSource()
        self.__checkbox = None
        self.__slider = None
        self.__range_slider = None


    def make_hist_tab(self):
        airline_carriers = self.flights['carrier'].unique().tolist()
        airline_carriers.sort()

        logo_div, checkbox_title = self.__create_logo_and_checkbox(airline_carriers)

        # Create a slider and range slider widget
        self.__hist_widgets()

        # set an inital value for the plot and widgets
        active_checkbox = [self.__checkbox.labels[i] for i in self.__checkbox.active]
        self.__cds = ColumnDataSource(data = self.__prepare_data(active_checkbox))

        fig = self.__make_hist_plot(self.__cds)

        widgets = Column(logo_div, checkbox_title, self.__checkbox, self.__slider, self.__range_slider)
        contents = Row(widgets, fig)
        tab = Panel(child=contents, title='The Distribution of Arrival Delay')

        return tab


    def __create_logo_and_checkbox(self, airline_carriers):
        logo_image_url = 'https://i.postimg.cc/t4hhFVqm/3.png'
        logo_html = f"<img src='{logo_image_url}' style='height: 100px; width: auto;'>"
        logo_div = Div(text=logo_html)

        checkbox_title = Div(text="<span style='font-family:TimesNewRoman; font-size:14px'>Select your desired\
                                  Airline Carriers below</span>")
        self.__checkbox = CheckboxGroup(labels=airline_carriers, active=[0, 1])
        self.__checkbox.on_change('active', self.__update)

        return logo_div, checkbox_title


    def __hist_widgets(self):
        self.__slider = Slider(title='The histogram binning', start=1,
                               end=int(self.__distance/(self.__bins * 2)),
                               step=1, value=self.__bins)
        self.__slider.on_change('value', self.__update)

        self.__range_slider = RangeSlider(title='The arrival delay range in minutes',
                                          start=-80, end=160, step=5,
                                          value=(self.__rs, self.__re))
        self.__range_slider.on_change('value', self.__update) 
    

    def __prepare_data(self, active_checkboxes):
        df = pd.DataFrame(columns=['Frequency', 'Proportion', 'Lower Limit',
                                         'Upper Limit', 'Interval','Name', 'Color'])
        
        for i, carrier in enumerate(active_checkboxes):
            carrier_instances = self.flights[self.flights['carrier'] == carrier]
            frequencies_arr, limits_arr = np.histogram(a=carrier_instances['arr_delay'],
                                                       bins=abs(int(self.__distance/self.__bins)),
                                                       range=(self.__rs, self.__re))
            new_df = pd.DataFrame({
                "Frequency" : frequencies_arr,
                "Proportion" : frequencies_arr / np.sum(frequencies_arr),
                "Lower Limit" : limits_arr[:-1],
                "Upper Limit" : limits_arr[1:]
            })
            new_df['Interval'] = ["%d to %d" %(ll, ul) for ll, ul in zip(new_df['Lower Limit'],
                                                                        new_df['Upper Limit'])]
            new_df['Name'], new_df['Color'] = carrier, Category20_19[i] 
            df = pd.concat([df, new_df], join='inner', ignore_index=True)

        df.sort_values(['Name'])

        return df


    def __update(self, attr, old, new): # a Callback function 
        active_checkboxes = [self.__checkbox.labels[i] for i in self.__checkbox.active]

        self.__rs = self.__range_slider.value[0]
        self.__re = self.__range_slider.value[1]
        self.__bins = self.__slider.value

        self.__cds.data = (self.__prepare_data(active_checkboxes)
                               .to_dict(orient='list')) # update the existing ColumnDataSource object


    def __make_hist_plot(self, cds):
        fig =figure(plot_width=700, plot_height=600)

        fig.quad(source=cds, bottom=0, top='Proportion', left='Lower Limit',
                right='Upper Limit', color='Color', legend_field='Name', alpha=.7)
        
        title = Div(text="<span style='font-family:TimesNewRoman; font-size:13pt'><strong>The Gaussian distribution of arrival delay\n\
                    for the different U.S. Airline carriers in 2013</strong></span>", align='center')
        
        fig.xaxis.axis_label = "The range of time intervals for arrival delays in minutes"
        fig.yaxis.axis_label = 'The proportion of occurrences of instances within specific time intervals '
        fig.legend.title = 'Airline Carriers'
        fig.legend.title_text_font = 'TimesNewRoman'
        fig.legend.title_text_font_style = "bold"
        fig.legend.title_text_font_size = "10pt"
        fig.legend.title_text_color = "#F0F0F0"

        return Column(title, fig)



        


