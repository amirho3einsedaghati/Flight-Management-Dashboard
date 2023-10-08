from bokeh.models.widgets import DataTable, TableColumn
from bokeh.models import ColumnDataSource, Panel, Column, Row, Div, HTMLTemplateFormatter



class DepTimeSummary():
    def __init__(self):
        self.__cds = None


    def make_dep_time_tab(self, df):
        flights_grouped = df.groupby('carrier')['dep_time'].describe()
        flights_grouped['mean'] = flights_grouped['mean'].round(2)
        flights_grouped['std'] = flights_grouped['std'].round(2)
        flights_grouped.drop(['25%', '50%', '75%'], axis=1, inplace=True)

        self.__cds = ColumnDataSource(flights_grouped)

        layout = self.__make_layout()
        dep_time_tab = Panel(child=layout, title='Departure Time Information')
        
        return  dep_time_tab
    

    def __make_layout(self):
        columns = [
                TableColumn(field='carrier', title='<span style="font-family:TimesNewRoman; font-size:13px;">\
                            <b>Airline Carrier</b></span>', formatter=HTMLTemplateFormatter(template="<span style='\
                            font-family:TimesNewRoman;font-size:12px;'><%= value %></span>")),

                TableColumn(field='count', title='<span style="font-family:TimesNewRoman; font-size:13px;"><b>Flight Count\
                            </b></span>', formatter=HTMLTemplateFormatter(template="<span style='font-family:Arial;\
                            font-size:12px;'><%= value %></span>")),

                TableColumn(field='mean', title='<span style="font-family:TimesNewRoman; font-size:13px;"><b>The Departure\
                            Time Average</b></span>', formatter=HTMLTemplateFormatter(template="<span style='font-family:\
                            Arial; font-size:12px;'><%= value %></span>")),

                TableColumn(field='std', title='<span style="font-family:TimesNewRoman; font-size:13px;"><b>The Departure Time\
                            Standard Deviation</b></span>', formatter=HTMLTemplateFormatter(template="<span style='\
                            font-family:Arial; font-size:12px;'><%= value %></span>")),

                TableColumn(field='min', title='<span style="font-family:TimesNewRoman; font-size:13px;"><b>The Shortest\
                            Departure Time</b></span>', formatter=HTMLTemplateFormatter(template= "<span style='\
                            font-family:Arial; font-size:12px;'><%= value %></span>")),

                TableColumn(field='max', title='<span style="font-family:TimesNewRoman; font-size:13px;"><b>The Longest\
                            Departure Time</b></span>', formatter=HTMLTemplateFormatter(template="<span style='font-family:\
                            Arial; font-size:12px;'><%= value %></span>"))]
        
        table = DataTable(
            source=self.__cds, columns= columns, autosize_mode='fit_columns', height=500,
            width=1265, sizing_mode= 'scale_both', background= "rgba(0,0,255,0.9)")
        
        title = Div(text="<h2 style='font-family:TimesNewRoman;'>The Statistical Information of Deparutre Time from Origin Airports\
                    in Minutes for U.S. Airline Carriers in 2013</h2>", align='center')
        title_pad = Div(style={'height' : '10px'})
        
        logo_image_url = 'https://i.postimg.cc/t4hhFVqm/3.png'
        logo_html = f"<img src='{logo_image_url}' style='height: 100px; width: auto;'>"
        logo_div = Div(text=logo_html)

        return Row(logo_div, Column(title_pad, title, table))