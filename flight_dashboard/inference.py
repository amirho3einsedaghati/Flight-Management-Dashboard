from bokeh.models.widgets import TextInput, Button, Select, Div, TextAreaInput, DatePicker
from bokeh.models import Panel
from bokeh.layouts import column, row
import pandas as pd
from model_dependencies.production_transformers import (ConvertToHourMinute, ConvertToMile,
                                                        ConvertToFahrenheit, OHE,
                                                        RelativeHumidity, GetMonthDay,
                                                        GetDateInfo, ReviseTimeFormat, RemoveColon,
                                                        CalcTemporalDifference, ReviseLabelFormat)
import random



class Inference():
    def __init__(self, skyc_le, dep_time_le, sched_dep_time_le, sched_arr_time_le,  arr_time_le, stacked_model, df, engine):
        self.__skyc_le, self.__arr_time_le, self.__sched_arr_time_le, self.__stacked_model = skyc_le, arr_time_le, sched_arr_time_le, stacked_model
        self.__df, self.__engine, self.__dep_time_le, self.__sched_dep_time_le = df, engine, dep_time_le, sched_dep_time_le
        self.__pred_input, self.__dep_time_input, self.__sched_dep_time_input = None, None, None
        self.__sched_arr_time_input, self.__temp_input, self.__relh_input = None, None, None
        self.__origin_ddmenu, self.__dest_ddmenu, self.__skyc_ddmenu, self.__vsby_input  = None, None, None, None
        self.__date_picker, self.__bttn, self.__fill_bttn = None, None, None
        self.__val1, self.__val2, self.__val3, self.__val4, self.__val5 = None, None, None, None, None
        self.__val6, self.__val7, self.__val8, self.__val9, self.__val10 = None, None, None, None, None
        self.__val11, self.__val12, self.__val13 = None, None, None
        self.__sky_conditions = None
        self.__origin, self.__dest = None, None
        self.__encoded_val = None


    def make_inference_tab(self, current_date):
        self.__origin = sorted(self.__df.origin.unique().tolist())
        self.__dest = sorted(self.__df.dest.unique().tolist())
        self.__sky_conditions = {
            'BKN' : 'BKN : The Sky is Partially Covered by Clouds',
            'CLR' : 'CLR : The Sky is Mostly or Completely Clear of Clouds',
            'FEW' : 'FEW : Only a few Clouds are Present in the Sky',
            'OVC' : 'OVC : The Sky is Completely Covered by Clouds',
            'SCT' : 'SCT : The Sky is Covered by Scattered Clouds',
            'VV'  : 'VV : The Sky is Covered by Vertical Obstructions such as Fog, Haze, or Precipitation'
        }

        # Create Row 1 Widgets
        row1_widgets = self.__create_row1(current_date)

        # Create Row 2 Widgets
        row2_widgets = self.__create_row2()

        # Create Row 3 Widgets
        row3_widgets = self.__create_row3()

        # Create The section 1 of the Row 4 and 5 widgets
        section1_row45 = self.__create_section1_row45(current_date)

        # Create The section 2 of the Row 4 and 5 widgets
        row45_widgets = self.__create_section2_row45(section1_row45)
        
        # Create Row 6 Widgets
        self.__create_row6()

        # Create Row 7 Widgets
        pred_input_layouts = self.__create_row7()

        layouts = column(
            row1_widgets,
            row2_widgets,
            row3_widgets,
            row45_widgets,
            self.__bttn,
            pred_input_layouts,
            align='start'
            )
        tab = Panel(child=layouts, title='Predicting Arival Time')

        return tab
    

    def __create_row1(self, current_date):
        curr_date = Div(text=f"<span style='font-family:TimesNewRoman; font-size:14px;'>\
                             Today's Date : <strong>{current_date}</strong></span>")
        
        dep_time_title = Div(text="<span style='font-family:TimesNewRoman; font-size:14px;'>\
                             The Real Departure Time</span>")
        dep_time_title.default_size = 600
        self.__dep_time_input = TextInput(placeholder='It can be entered in a 12-hour format e.g. 5:17AM| 24-hour format e.g. 5:17| specific format e.g. 517', value='', default_size=600)
        dep_time_layouts = column(curr_date, dep_time_title, self.__dep_time_input)

        temp1_pad = Div(style={'height' : '19px'})
        temp_title = Div(text="<span style='font-family:TimesNewRoman; font-size:14px;'>\
                             The Temperature at The Time of Departure</span>")
        temp_title.default_size = 600
        self.__temp_input = TextInput(placeholder='It can be entered in these formats e.g. 39 Fahrenheit | 39 F | 3.88 C | 3.88 celsius | 3.88 centigrade', value='', default_size=600)

        temp_layouts = column(temp1_pad, temp_title, self.__temp_input)
        temp2_pad = Div(style={'height' : '50px'})
        row1_widgets = row(dep_time_layouts, temp2_pad, temp_layouts)

        return row1_widgets
    

    def __create_row2(self):
        sched_dep_time_title = Div(text="<span style='font-family:TimesNewRoman; font-size:14px;'>\
                             The Scheduled Departure Time</span>")
        sched_dep_time_title.default_size = 600
        self.__sched_dep_time_input = TextInput(placeholder='It can be entered in a 12-hour format e.g. 5:15AM| 24-hour format e.g. 5:15| specific format e.g. 515', value='', default_size=600)
        sched_dep_time_layouts = column(sched_dep_time_title, self.__sched_dep_time_input)

        relh_title = Div(text="<span style='font-family:TimesNewRoman; font-size:14px;'>\
                             The relative Humidity at The Time of Departure</span>")
        relh_title.default_size = 600
        self.__relh_input = TextInput(placeholder='It can be entered in these formats e.g. 54.77 | 54.77 %', value='', default_size=600)

        relh_layouts = column(relh_title, self.__relh_input)
        relh_pad = Div(style={'height' : '50px'})
        row2_widgets = row(sched_dep_time_layouts, relh_pad, relh_layouts)

        return row2_widgets
    

    def __create_row3(self):
        sched_arr_time_title = Div(text="<span style='font-family:TimesNewRoman; font-size:14px;'>\
                             The Scheduled Arrival Time</span>")
        sched_arr_time_title.default_size = 600
        self.__sched_arr_time_input = TextInput(placeholder='It can be entered in a 12-hour format e.g. 8:19AM| 24-hour format e.g. 8:19| specific format e.g. 819', value='', default_size=600)
        sched_arr_time_layouts = column(sched_arr_time_title, self.__sched_arr_time_input)

        skyc_title = Div(text="<span style='font-family:TimesNewRoman; font-size:14px;'>\
                             The Sky Condition at The Time of Departure</span>")
        skyc_title.default_size = 600
        self.__skyc_ddmenu = Select(value=list(self.__sky_conditions.values())[0], options=list(self.__sky_conditions.values()), default_size=600)
        self.__skyc_ddmenu.on_change('value', self.__preprocessing_drop_down_menus)

        skyc_layouts = column(skyc_title, self.__skyc_ddmenu)
        skyc_pad = Div(style={'height' : '50px'})
        row3_widgets = row(sched_arr_time_layouts, skyc_pad, skyc_layouts)

        return row3_widgets
    

    def __create_section1_row45(self, current_date):
        origin_airport_title = Div(text="<span style='font-family:TimesNewRoman; font-size:14px;'>\
                             The IATA Codes of The Origin Airports</span>")
        origin_airport_title.default_size = 285
        self.__origin_ddmenu = Select(value=self.__origin[0], options=self.__origin, default_size=285)
        origin_airport_layouts = column(origin_airport_title, self.__origin_ddmenu)

        dest_airport_title = Div(text="<span style='font-family:TimesNewRoman; font-size:14px;'>\
                             The IATA Codes of The Destination Airports</span>")
        dest_airport_title.default_size = 295
        self.__dest_ddmenu = Select(value=self.__dest[0], options=self.__dest, default_size=295)

        date_title = Div(text="<span style='font-family:TimesNewRoman; font-size:14px;'>\
                             Select The Date of Flight</span>")
        date_title.default_size = 295
        self.__date_picker = DatePicker(
            value='2013-01-01',
            min_date='2010-01-01',
            max_date=current_date,
            default_size=295,
        )
        self.__date_picker.on_change('value', self.__preprocessing_date) 

        date_layouts = column(date_title, self.__date_picker)
        dest_airport_layouts = column(dest_airport_title, self.__dest_ddmenu, date_layouts)
        dest_airport_pad = Div(style={'height' : '50px'})
        section1_row45 = row(origin_airport_layouts, dest_airport_pad, dest_airport_layouts)

        return section1_row45
    

    def __create_section2_row45(self, section1_row45):
        vsby_title = Div(text="<span style='font-family:TimesNewRoman; font-size:14px;'>\
                             The Visibility at The Time of Departure</span>")
        vsby_title.default_size = 600
        self.__vsby_input = TextInput(placeholder='It can be entered in these formats e.g. 10 Mile| 10 Miles| 16.09KM| 16.09Kilometre| 16.09Kilometres',value='', default_size=600)

        fill_bttn_pad = Div(style={'height' : '19px'})
        self.__fill_bttn = Button(label='Fill the Cells with new unseen data and Show the Result', disabled=False, default_size=295)
        self.__fill_bttn.on_click(self.__fill_the_blanks)

        fill_bttn_layouts = column(fill_bttn_pad, self.__fill_bttn)
        section2_row45 = column(vsby_title, self.__vsby_input, fill_bttn_layouts)
        pad45 = Div(style={'height' : '50px'})
        row45_widgets = row(section1_row45, pad45, section2_row45)

        return row45_widgets
    

    def __create_row6(self):
        self.__bttn = Button(label='Send', disabled=False, default_size=1225)
        self.__bttn.on_click(self.__preprocessing_predicting)


    def __create_row7(self):
        pred_input_title = Div(text="<span style='font-family:TimesNewRoman; font-size:14px;'>\
                             <strong>RESULT : The Predicted Real Arrival Time</strong></span>")
        pred_input_title.default_size = 1225
        self.__pred_input = TextAreaInput(value='', rows=5, default_size=1225)

        pred_input_layouts = column(pred_input_title, self.__pred_input)
        
        return pred_input_layouts
    

    def __preprocessing_predicting(self):
        self.__val1 = self.__dep_time_input.value
        self.__val2 = self.__sched_dep_time_input.value
        self.__val3 = self.__sched_arr_time_input.value
        self.__val1, self.__val2, self.__val3 = self.__to_hour_and_minute(self.__val1, self.__val2, self.__val3)

        try:
            self.__val4 = self.__df.loc[(
                self.__df['origin'] == self.__origin_ddmenu.value) & (self.__df['dest'] == self.__dest_ddmenu.value), 'distance'
                                        ].iloc[0]
            self.__val5 = self.__get_delay_status()

        except IndexError:
            self.__pred_input.value = f'I could not find any flights from {self.__origin_ddmenu.value} airport to {self.__dest_ddmenu.value} airport. Please choose an alternative route or use the fill button.'

        else:
            self.__val6 = self.__to_fahrenheit(self.__temp_input.value)

            self.__val7 = self.__get_humidity(self.__relh_input.value)

            self.__val8 = self.__to_mile(self.__vsby_input.value)

            month_day = GetMonthDay()
            self.__val9, self.__val10 = month_day.transform(self.__date_picker.value)

            date_info = GetDateInfo()
            dayofweek, is_weekend, is_usa_holiday = date_info.transform(self.__date_picker.value)
            self.__val11, self.__val12, self.__val13 = dayofweek, is_weekend, is_usa_holiday

            self.__preprocessing_cat_cols(self.__skyc_ddmenu.value)

            dep_time = None
            sched_dep_time = None
            sched_arr_time = None

            access_code = self.__are_these_string()
            if access_code == 1:
                time = ReviseTimeFormat()
                dep_time_label, desired_df, label_id, time_str = time.transform(
                    self.__engine, 'dep_time', self.__date_picker.value, self.__val1,
                    self.__val9, self.__val10, self.__val4, time_le=self.__dep_time_le, 
                    origin=self.__origin_ddmenu.value, dest=self.__dest_ddmenu.value,
                    )

                if type(dep_time_label) == str:
                    self.__pred_input.value = dep_time_label

                else:
                    self.__dep_time_input.value = time_str
                    self.__val1 = dep_time_label

                    remove_colon = RemoveColon()
                    dep_time = remove_colon.transform(time_str)

                    if (desired_df is not None) and (label_id is not None):
                        time_label, _, _, time_str = time.transform(
                            self.__engine, 'sched_dep_time', self.__date_picker.value, self.__val2,
                            self.__val9, self.__val10, self.__val4, time_le=self.__sched_dep_time_le,
                            with_df=True, desired_id=label_id, desired_df=desired_df
                            )
                        self.__sched_dep_time_input.value = time_str
                        self.__val2  = time_label

                        sched_dep_time = remove_colon.transform(time_str)

                        time_label, _, _, time_str = time.transform(
                            self.__engine, 'sched_arr_time', self.__date_picker.value, self.__val3,
                            self.__val9, self.__val10, self.__val4, time_le=self.__sched_arr_time_le,
                            with_df=True, desired_id=label_id, desired_df=desired_df
                            )
                        self.__sched_arr_time_input.value = time_str
                        self.__val3  = time_label

                        sched_arr_time = remove_colon.transform(time_str)

                    else:
                        time_label, _, _, time_str = time.transform(
                            self.__engine, 'sched_dep_time', self.__date_picker.value, self.__val2,
                            self.__val9, self.__val10, self.__val4, time_le=self.__sched_dep_time_le, 
                            )
                        self.__sched_dep_time_input.value = time_str
                        self.__val2  = time_label

                        sched_dep_time = remove_colon.transform(time_str)

                        time_label, _, _, time_str = time.transform(
                            self.__engine, 'sched_arr_time', self.__date_picker.value, self.__val3,
                            self.__val9, self.__val10, self.__val4, time_le=self.__sched_arr_time_le, 
                            )
                        self.__sched_arr_time_input.value = time_str
                        self.__val3  = time_label

                        sched_arr_time = remove_colon.transform(time_str)

                    df = self.__create_df()

                    y_pred = self.__stacked_model.predict(df)[0]

                    self.__pred_input.value = self.__postprocessing_data(self.__arr_time_le, y_pred, dep_time, sched_dep_time, sched_arr_time)


    def __fill_the_blanks(self):
        X_test_shape = 48397
        index = random.randint(0, X_test_shape)
        X_test = pd.read_sql(f'SELECT * FROM X_test WHERE id={index}', self.__engine)
        X_test = X_test.drop(['index', 'id'], axis=1)

        # Fill the cells
        self.__dep_time_input.value = self.__convert_to_time_str(self.__dep_time_le, X_test['dep_time'][0])
        self.__sched_dep_time_input.value = self.__convert_to_time_str(self.__sched_dep_time_le, X_test['sched_dep_time'][0])
        self.__sched_arr_time_input.value = self.__convert_to_time_str(self.__sched_arr_time_le, X_test['sched_arr_time'][0])

        self.__origin_ddmenu.value = self.__df[self.__df['distance'] == X_test['distance'][0]][['origin', 'dest']].iloc[0]['origin']
        self.__dest_ddmenu.value = self.__df[self.__df['distance'] == X_test['distance'][0]][['origin', 'dest']].iloc[0]['dest']

        self.__date_picker.value = f"{2013}-{X_test['month'][0]:02d}-{X_test['day'][0]:02d}"

        self.__temp_input.value = f"{X_test['tmpf'][0]} F"

        self.__relh_input.value = f"{X_test['relh'][0]} %"

        self.__skyc_ddmenu.value = self.__get_sky_condition(X_test[['BKN', 'CLR', 'FEW', 'OVC', 'SCT', 'VV']])

        self.__vsby_input.value = f"{X_test['vsby'][0]} Miles"

        y_pred = self.__stacked_model.predict(X_test)[0]

        remove_colon = RemoveColon()
        dep_time = remove_colon.transform(self.__dep_time_input.value)
        sched_dep_time = remove_colon.transform(self.__sched_dep_time_input.value)
        sched_arr_time = remove_colon.transform(self.__sched_arr_time_input.value)
        
        self.__pred_input.value = self.__postprocessing_data(self.__arr_time_le, y_pred, dep_time, sched_dep_time, sched_arr_time)
    

    def __preprocessing_date(self, attr, old, new):
        month_day = GetMonthDay()
        self.__val9, self.__val10 = month_day.transform(self.__date_picker.value)

        date_info = GetDateInfo()
        dayofweek, is_weekend, is_usa_holiday = date_info.transform(self.__date_picker.value)
        self.__val11, self.__val12, self.__val13 = dayofweek, is_weekend, is_usa_holiday


    def __preprocessing_drop_down_menus(self, attr, old, new):
        try:
            self.__val4 = self.__df.loc[(
                self.__df['origin'] == self.__origin_ddmenu.value) & (self.__df['dest'] == self.__dest_ddmenu.value), 'distance'
                        ].iloc[0]
            
        except IndexError:
            self.__pred_input.value = f'I could not find any flights from {self.__origin_ddmenu.value} airport to {self.__dest_ddmenu.value} airport. Please choose an alternative route or use the fill button.'


            

    def __preprocessing_cat_cols(self, skyc:str):
        if skyc.split(' : '):
            skyc_code_str = skyc.split(' : ')[0]
            skyc_code_int = self.__skyc_le.transform([skyc_code_str])[0]

            ohe = OHE()
            self.__encoded_val = ohe.transform(skyc_code_int)


    def __create_df(self):
        columns = [
            'dep_time', 'sched_dep_time', 'sched_arr_time', 'distance', 'with_dep_delay', 'tmpf', 'relh', 'vsby',
            'month', 'day', 'dayofweek', 'weekend', 'is_usa_holidays', 'SCT', 'OVC', 'BKN', 'FEW', 'CLR', 'VV'
        ]

        df = pd.DataFrame(columns=columns)

        # Append a row with the desired values
        df = df.append({
            'dep_time': self.__val1,
            'sched_dep_time': self.__val2,
            'sched_arr_time': self.__val3,
            'distance': self.__val4,
            'with_dep_delay': self.__val5,
            'tmpf': self.__val6,
            'relh': self.__val7,
            'vsby': self.__val8,
            'month': self.__val9,
            'day': self.__val10,
            'dayofweek': self.__val11,
            'weekend': self.__val12,
            'is_usa_holidays': self.__val13,
            'SCT': self.__encoded_val[4],
            'OVC': self.__encoded_val[3],
            'BKN': self.__encoded_val[0],
            'FEW': self.__encoded_val[2],
            'CLR': self.__encoded_val[1],
            'VV': self.__encoded_val[5]
        }, ignore_index=True)

        pd.set_option('display.max_columns', None)
        return df


    def __postprocessing_data(self, arr_time_le, y_pred:float, dep_time:int, sched_dep_time:int, sched_arr_time:int):
        time = ReviseLabelFormat()
        y_pred_str = time.transform(arr_time_le, y_pred)

        time_str = RemoveColon()
        arr_time = time_str.transform(y_pred_str)
        
        if type(arr_time) == str:
            return y_pred_str

        if arr_time <= dep_time and arr_time <= sched_dep_time:
            return "Something was wrong. Please choose an alternative route or use the fill button."
        
        else:
            temporal_diff = CalcTemporalDifference()
            _, arr_delay = temporal_diff.transform(arr_time, sched_arr_time)

            if str(arr_delay)[0] == '-':
                arr_delay = str(arr_delay).split('-')[1]

                if len(str(arr_time)) == 3:
                    return f"Probably, this flight will arrive at {self.__dest_ddmenu.value} airport {arr_delay} minutes earlier than expected, at {y_pred_str}."
                
                elif len(str(arr_time)) == 4:
                    return f"Probably, this flight will arrive at {self.__dest_ddmenu.value} airport {arr_delay} minutes earlier than expected, at {y_pred_str}."

            else:
                if arr_delay == 0:
                    if len(str(arr_time)) == 3:
                        return f"Probably, this flight will arrive at {self.__dest_ddmenu.value} airport exactly at the expected arrival time, at {y_pred_str}."
                    
                    elif len(str(arr_time)) == 4:
                        return f"Probably, this flight will arrive at {self.__dest_ddmenu.value} airport exactly at the expected arrival time, at {y_pred_str}."
                    
                else:
                    if len(str(arr_time)) == 3:
                        return f"Probably, this flight will arrive at {self.__dest_ddmenu.value} airport {arr_delay} minutes later than the expected time, at {y_pred_str}."
                    
                    elif len(str(arr_time)) == 4:
                        return f"Probably, this flight will arrive at {self.__dest_ddmenu.value} airport {arr_delay} minutes later than the expected time, at {y_pred_str}."
                

    def __are_these_string(self):
        if (type(self.__val1) == str and type(self.__val1) != "") or (type(self.__val2) == str and type(self.__val2) != "")\
        or (type(self.__val3) == str and type(self.__val3) != "") or (type(self.__val6) == str and type(self.__val6) != "")\
        or (type(self.__val7) == str and type(self.__val7) != "") or (type(self.__val8) == str and type(self.__val8) != ""):
            
            if type(self.__val1) == str and type(self.__val1) != "":
                self.__dep_time_input.value = self.__val1
                self.__pred_input.value = ""

            if type(self.__val2) == str and type(self.__val2) != "":
                self.__sched_dep_time_input.value = self.__val2
                self.__pred_input.value = ""

            if type(self.__val3) == str and type(self.__val3) != "":
                self.__sched_arr_time_input.value = self.__val3
                self.__pred_input.value = ""

            if type(self.__val6) == str and type(self.__val6) != "":
                self.__temp_input.value = self.__val6
                self.__pred_input.value = ""

            if type(self.__val7) == str and type(self.__val7) != "":
                self.__relh_input.value = self.__val7
                self.__pred_input.value = ""

            if type(self.__val8) == str and type(self.__val8) != "":
                self.__vsby_input.value = self.__val8
                self.__pred_input.value = ""

            return 0
        
        else:
            return 1
        

    def __get_sky_condition(self, ohe_df:pd.DataFrame):
        for active_val, sky_code in zip(ohe_df.values.reshape(-1), ohe_df.columns):
            if active_val == 1:
                return self.__sky_conditions[sky_code]


    def __convert_to_time_str(self, time_le, label:int):
        time = ReviseLabelFormat()
        return time.transform(time_le, label)
        

    def __get_humidity(self, val:str):
        relh = RelativeHumidity()
        return relh.transform(val)
    

    def __to_fahrenheit(self, val:str):
        temp = ConvertToFahrenheit()
        tempf = temp.transform(val)
        
        return tempf
    

    def __to_hour_and_minute(self, val1:str, val2:str, val3:str):
        to_hour_and_minute = ConvertToHourMinute()
        val1 = to_hour_and_minute.transform(val1)
        val2 = to_hour_and_minute.transform(val2)
        val3 = to_hour_and_minute.transform(val3)

        return val1, val2, val3
    

    def __to_mile(self, val:str):
        to_mile = ConvertToMile()
        val = to_mile.transform(val)

        return val


    def __get_delay_status(self):
        if type(self.__val1) == int and type(self.__val2) == int:
            temporal_diff = CalcTemporalDifference()
            delay_status, _ = temporal_diff.transform(self.__val1, self.__val2)

            return delay_status

        elif type(self.__val1) == str and self.__val1 != '' and type(self.__val2) == int:
            self.__dep_time_input.value = self.__val1

        elif type(self.__val1) == int and type(self.__val2) == str and self.__val2 != '':
            self.__sched_dep_time_input.value = self.__val2
        
        elif type(self.__val1) == str and self.__val1 != '' and type(self.__val2) == str and self.__val2 != '':
            self.__dep_time_input.value = self.__val1
            self.__sched_dep_time_input.value = self.__val2







