from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import regex as re
import holidays



#######################################################

class ConvertToMile(BaseEstimator, TransformerMixin):
    def fit(self, distance_str:str, y=None):
        return self
    
    
    def transform(self, distance_str:str):
        distance_str = distance_str.replace(" ", "").lower()

        km_states = ['km', 'kilometre', 'kilometres']
        miles_states = ['mile', 'miles']
        total_state = km_states + miles_states
        without_unit_list = []

        for i in range(5):
            if total_state[i] in distance_str:
                if total_state[i] in km_states:

                    try:
                        distance = float(distance_str.split(total_state[i])[0])

                    except:
                        return f'Expected a number before the kilometre symbol, Not {distance_str.split(total_state[i])[0]}!' 
                    
                    else:
                        distance /= 1.609
                        return round(distance, 2)
            
                elif total_state[i] in miles_states:
                    try:
                        distance = float(distance_str.split(total_state[i])[0])

                    except:
                        return f'Expected a number before the mile symbol, Not {distance_str.split(total_state[i])[0]}!'
                    
                    else:
                        return round(distance, 2)
            else:
                without_unit_list.append(0)

        if len(without_unit_list) == 5:
            return f"Expected an unit in the input value, {distance_str}!"
        
                
    def fit_transform(self, distance_str:str, y=None):
        self.fit(distance_str)
        return self.transform(distance_str)


#######################################################

class ConvertToHourMinute(BaseEstimator, TransformerMixin): # returns a time in a 24-hour format
    def fit(self, time_str:str, y=None):
        return self
    
    
    def __convert_to_24_hour(self, time_str:str):
        # Split the time string into hours, minutes, and AM/PM indicator
        time_parts = time_str.split(':')
        hour = int(time_parts[0])
        minute = int(time_parts[1][:2])
        am_pm = time_parts[1][2:]

        try:
            am_pm = am_pm.split(' ')[1]

        except:
            pass

        # Convert to 24-hour format
        if am_pm.lower() == 'pm':
            if hour != 12:
                hour += 12

        if am_pm.lower() == 'am':
            if hour == 12:
                hour = 0

        # Return the time in 24-hour format
        return '{:02d}:{:02d}'.format(hour, minute)

    
    def transform(self, time_str:str):
        try:
            time = int(time_str)
            
        except:
            time_str = time_str.replace(" ", "").lower()

            try:
                if (type(time_str.split(':')[0]) == str and type(time_str.split(':')[1][:2]) == str):
                    time_parts = time_str.split(':')

                    try:
                        hour, minute, am_pm = int(time_parts[0]), int(time_parts[1][:2]), time_parts[1][2:]

                    except:
                        return f'Expected a time in a 24-hour format or a 12-hour format, Not {time_str}!'
                    
                    else:
                        if hour in range(1, 25) and minute in range(0, 60) and len(am_pm) == 0: # in a 24-hour format
                            time = int("{:02d}{:02d}".format(hour, minute))

                            return time
                        
                        elif (hour in range(1, 13) and minute in range(0, 60)) and (am_pm == 'am' or am_pm == 'pm'): # in a 12-hour format
                            time = self.__convert_to_24_hour(time_str)
                            time_parts = time.split(':')
                            hour, minute = int(time_parts[0]), int(time_parts[1])
                            time = int("{:02d}{:02d}".format(hour, minute))

                            return time
                        
                        else:
                            return f'Expected a time in a 24-hour format or a 12-hour format, Not {time_str}!'
                                
            except:
                return f'Expected a time in a 24-hour format or a 12-hour format, Not {time_str}!'
                
        else:
            return time
        
        
    def fit_transform(self, time_str:str, y=None):
        self.fit(time_str)
        return self.transform(time_str)
    

#######################################################

class ConvertToFahrenheit(BaseEstimator, TransformerMixin):
    def fit(self, degree:str, y=None):
        return self
    

    def transform(self, degree:str):
        fdegree_units = ['fahrenheit', 'f']
        cdegree_units = ['celsius', 'c', 'centigrade']
        degree = degree.replace(" ", "").lower()

        try:
            degreeVal, unit = re.split(r'(\d+)(\D+)', degree)[1], re.split(r'(\d+)(\D+)', degree)[-2]

        except:
            return f"Expected a number with a tempreture unit"
        
        else:
            if unit in fdegree_units:
                return float(degreeVal)

            elif unit in cdegree_units:
                fdegreeVal = float(degreeVal) * 1.8 + 32

                return float(fdegreeVal)

            else:
                return f"Expected an unit after the degree value!"
        

    def fit_transform(self, degree:str, y=None):
        self.fit(degree)
        return self.transform(degree)


#######################################################

class RelativeHumidity(BaseEstimator, TransformerMixin):
    def fit(self, relh:str, y=None):
        return self
    

    def transform(self, relh:str, y=None):
        relh = relh.replace(' ', '').lower()

        try:
            relh = float(relh)

        except:
            if '%' in re.split(r'(\d+)(\D+)', relh):
                beforeDot, afterDot = re.split(r'\D+', relh)[0], re.split(r'\D+', relh)[1]
                number = beforeDot + '.' + afterDot

                return float(number)
            
            else:
                return "Expected a number as a percentage"
            
        else:
            return relh
        

    def fit_transform(self, relh:str, y=None):
        self.fit(relh)
        return self.transform(relh)
            
    
#######################################################

class OHE(BaseEstimator, TransformerMixin):
    def fit(self, skyc:int, y=None):
        return self
    

    def transform(self, skyc:int):
        if skyc in range(6):
            ohe = [0] * 6
            ohe[skyc] = 1

            return ohe
    

    def fit_transform(self, skyc:int, y=None):
        self.fit(skyc)
        return self.transform(skyc)
    

#######################################################

class GetMonthDay(BaseEstimator, TransformerMixin):
    def fit(self, date:str, y=None):
        return self
    

    def transform(self, date:str):
        datetime_obj = pd.to_datetime(date)
        month, day = datetime_obj.month, datetime_obj.day

        return month, day
    

    def fit_transform(self, date:str, y=None):
        self.fit(date)
        return self.transform(date)
    
    
#######################################################

class GetDateInfo(BaseEstimator, TransformerMixin):
    def fit(self, date:str, y=None):
        return self
    

    def transform(self, date:str):
        datetime_obj = pd.to_datetime(date)
        dayofweek = datetime_obj.dayofweek

        if dayofweek == 5 or dayofweek == 6:
            is_weekend = 1

        else:
            is_weekend = 0

        usa_calender = holidays.USA()
        is_usa_holiday = int(date in usa_calender)

        return dayofweek, is_weekend, is_usa_holiday
    

    def fit_transform(self, date:str, y=None):
        self.fit(date)
        return self.transform(date)


#######################################################

class ReviseTimeFormat(BaseEstimator, TransformerMixin):
    def fit(self, engine, col:str, date:str, time:int, month:int, day:int, distance:int, desired_id:int=None, desired_df:pd.DataFrame=None, time_le=None, with_df=False, origin:str=None, dest:str=None, y=None):
        return self
    

    def __find_the_closest_time(self, time_le, datetime:str, id_arr, labels):
        time_str = [f"{pd.DatetimeIndex([time_le.classes_[label]])[0].hour:02d}:{pd.DatetimeIndex([time_le.classes_[label]])[0].minute:02d}" for label in labels]
        
        time_ls = datetime.split(' ')[1].split(':00')[0].split(':')
        t_h, t_m = int(time_ls[0]), int(time_ls[1])

        if t_h == 0 and t_m == 0:
            t_h, t_m = 24, 0

        diff_time = []
        for i, time_colon in enumerate(time_str):
            time_h, time_m = int(time_colon.split(':')[0]), int(time_colon.split(':')[1])

            if time_h == 0 and time_m == 0:
                time_h, time_m = 24, 0

            hour_difference = abs(t_h - time_h)
            minute_difference = abs(t_m - time_m)
            diff =  hour_difference * 60 + minute_difference
            diff_time.append(tuple([diff, id_arr[i]]))

        return min(diff_time)
    

    def __check_conditions(self, revised_time:str, engine, col:str, month:int, day:int, distance:int, desired_id:int=None, desired_df:pd.DataFrame=None, time_le=None, with_df=False, origin:str=None, dest:str=None):
        if with_df == False:
            try:
                label = time_le.transform([revised_time])[0]

            except:
                if col == 'dep_time':
                    df = pd.read_sql(f'SELECT id, dep_time, sched_dep_time, sched_arr_time FROM X WHERE distance={distance} AND month={month} AND day={day}', engine)

                    if df.shape[0] == 0:
                        date = f"{pd.to_datetime(revised_time).year:04d}-{pd.to_datetime(revised_time).month:02d}-{pd.to_datetime(revised_time).day:02d}"
                        time = f"{pd.to_datetime(revised_time).hour:02d}:{pd.to_datetime(revised_time).minute:02d}"

                        return (f"""No flights occurred from {origin} airport to {dest} airport on {date} at approximately {time}.\
 To populate valid values for the departure time, scheduled departure time, and scheduled\
 arrival time cells. please use the fill button.""", None, None, None)

                    else:
                        if df.shape[0] == 1:
                            dep_time_label = df[col][0]
                            label_id = df['id'][0]
                            new_dep_time = "{:02d}:{:02d}".format(
                                pd.DatetimeIndex([time_le.classes_[dep_time_label]])[0].hour,
                                pd.DatetimeIndex([time_le.classes_[dep_time_label]])[0].minute
                                )
                            
                            return dep_time_label, df, label_id, new_dep_time
                        
                        elif df.shape[0] > 1:
                            _, label_id = self.__find_the_closest_time(time_le, revised_time, df['id'].values, df[col].values)
                            dep_time_label = df.loc[df['id'] == label_id, col].iloc[0]
                            new_dep_time = "{:02d}:{:02d}".format(
                                pd.DatetimeIndex([time_le.classes_[dep_time_label]])[0].hour,
                                pd.DatetimeIndex([time_le.classes_[dep_time_label]])[0].minute
                                )
                            
                            return dep_time_label, df, label_id, new_dep_time
                else:
                    return "", None, None, None
                
            else:
                time_str = "{:02d}:{:02d}".format(
                            pd.DatetimeIndex([time_le.classes_[label]])[0].hour,
                            pd.DatetimeIndex([time_le.classes_[label]])[0].minute
                            )
                
                return label, None, None, time_str
        
        else:
            if desired_df.shape[0] == 1:
                time_label = desired_df[col][0]
                time_str = "{:02d}:{:02d}".format(
                            pd.DatetimeIndex([time_le.classes_[time_label]])[0].hour,
                            pd.DatetimeIndex([time_le.classes_[time_label]])[0].minute
                            )
                
                return time_label, None, None, time_str
            
            elif desired_df.shape[0] > 1:
                time_label = desired_df.loc[desired_df['id'] == desired_id, col].iloc[0]
                time_str = "{:02d}:{:02d}".format(
                            pd.DatetimeIndex([time_le.classes_[time_label]])[0].hour,
                            pd.DatetimeIndex([time_le.classes_[time_label]])[0].minute
                            )
                
                return time_label, None, None, time_str
    

    def transform(self, engine, col:str, date:str, time:int, month:int, day:int, distance:int, desired_id:int=None, desired_df:pd.DataFrame=None, time_le=None, with_df=False, origin:str=None, dest:str=None):
        if len(str(time)) == 1:
            revised_time = f"{date} {str(time)[:1]}:{0:02d}"

            return self.__check_conditions(revised_time, engine, col, month, day, distance, desired_id, desired_df, time_le, with_df, origin, dest)

        elif len(str(time)) == 3:
            revised_time = f"{date} {str(time)[:1]}:{str(time)[1:]}"

            return self.__check_conditions(revised_time, engine, col, month, day, distance, desired_id, desired_df, time_le, with_df, origin, dest)
        
        elif len(str(time)) == 4:
            revised_time = f"{date} {str(time)[:2]}:{str(time)[2:]}"

            return self.__check_conditions(revised_time, engine, col, month, day, distance, desired_id, desired_df, time_le, with_df, origin, dest)


    def fit_transform(self, engine, col:str, date:str, time:int, month:int, day:int, distance:int, desired_id:int=None, desired_df:pd.DataFrame=None, time_le=None, with_df=False, origin:str=None, dest:str=None, y=None):

        self.fit(engine, col, date, time, month, day, distance, time_le, with_df, desired_id, desired_df, origin, dest)
        return self.transform(engine, col, date, time, month, day, distance, time_le, with_df, desired_id, desired_df, origin, dest)
    

#######################################################

class CalcTemporalDifference(BaseEstimator, TransformerMixin):
    def fit(self, time1:int, time2:int, y=None):
        return self
    
    def __calc(self, time1_h:int, time2_h:int, time1_m:int, time2_m:int):
        hour_difference = time1_h - time2_h
        minute_difference = time1_m - time2_m
        difference_between_dep_time_and_sched_dep_time =  hour_difference * 60 + minute_difference

        if difference_between_dep_time_and_sched_dep_time == 0:
            return 0, difference_between_dep_time_and_sched_dep_time
        
        elif difference_between_dep_time_and_sched_dep_time < 0:
            return -1, difference_between_dep_time_and_sched_dep_time
        
        else:
            return 1, difference_between_dep_time_and_sched_dep_time
        
    def transform(self, time1:int, time2:int):
        if time1 == 0:
            time1 = 2400
        if time2 == 0:
            time2 = 2400
            
        time1_str, time2_str = str(time1), str(time2)
        if len(time1_str) == 4 and len(time2_str) == 4:
            time1_h, time1_m = int(time1_str[:2]), int(time1_str[2:])
            time2_h, time2_m = int(time2_str[:2]), int(time2_str[2:])
            delay_status, diff_val = self.__calc(time1_h, time2_h, time1_m, time2_m)

            return delay_status, diff_val

        elif len(time1_str) == 3 and len(time2_str) == 3:
            time1_h, time1_m = int(time1_str[:1]), int(time1_str[1:])
            time2_h, time2_m = int(time2_str[:1]), int(time2_str[1:])
            delay_status, diff_val = self.__calc(time1_h, time2_h, time1_m, time2_m)

            return delay_status, diff_val

        elif len(time1_str) == 3 and len(time2_str) == 4:
            time1_h, time1_m = int(time1_str[:1]), int(time1_str[1:])
            time2_h, time2_m = int(time2_str[:2]), int(time2_str[2:])
            delay_status, diff_val = self.__calc(time1_h, time2_h, time1_m, time2_m)

            return delay_status, diff_val

        elif len(time1_str) == 4 and len(time2_str) == 3:
            time1_h, time1_m = int(time1_str[:2]), int(time1_str[2:])
            time2_h, time2_m = int(time2_str[:1]), int(time2_str[1:])
            delay_status, diff_val = self.__calc(time1_h, time2_h, time1_m, time2_m)

            return delay_status, diff_val
    
    def fit_transform(self, time1:int, time2:int, y=None):
        self.fit(time1, time2)
        return self.transform(time1, time2)


#######################################################

class ReviseLabelFormat(BaseEstimator, TransformerMixin):
    def fit(self, time_le, label, y=None):
        return self
    
    def transform(self, time_le, label):
        try:
            datetime = time_le.classes_[int(label)]

        except IndexError:
            tries_li = []
            for num in range(1, 102):
                try:
                    datetime = time_le.classes_[int(label - num)]
                    hour, minute = pd.DatetimeIndex([datetime])[0].hour, pd.DatetimeIndex([datetime])[0].minute
                    time = f"{hour:02d}:{minute:02d}"

                    return time
                
                except:
                    tries_li.append(1)

            if len(tries_li) == 100:
                return "I could not retrieve the arrival time of this flight. Maybe, there is an error in the input values or other technical issues."
            
        else:
            hour, minute = pd.DatetimeIndex([datetime])[0].hour, pd.DatetimeIndex([datetime])[0].minute
            time = f"{hour:02d}:{minute:02d}"
            
            return time 
    
    def fit_transform(self, time_le, label, y=None):
        self.fit(label)
        return self.transform(label)
    
    
#######################################################

class RemoveColon(BaseEstimator, TransformerMixin):
    def fit(self, time:str, y=None):
        return self
    
    def transform(self, time=str):
        try:
            hour, minute = time.split(':')[0], time.split(':')[1]

        except IndexError:
            return "IndexError occurred!"
        
        else:
            time_int = int(hour + minute)
            return time_int
        
    def fit_transform(self, time:str, y=None):
        self.fit(time)
        return self.transform(time)
    

