"""
timeseries.py


Version 0.1.0
May 9, 2023
Aoyu Zou

This modules provides a series of code that helps retrieve, process/summarize and plot timeseries data in the folder named clean_data

Some use case are shown below:

Example #1:
To load retreieve any timeseries data with defined starting time and end time
data = ts.retrieve('2018-06-01 00:00:00', '2018-07-01 00:00:00', 'site_weather.csv').head(60)

Example #2:
To get the hourly or daily summary of the timeseries data (average calculation)
ts.hourly('2018-05-01 00:00:00', '2018-06-01 00:00:00', data)
ts.daily('2018-05-01 00:00:00', '2018-06-01 00:00:00', data)

Example #3:
To visualize the retreived timeseries data for a quick analysis or compare
weather_data = ts.retrieve('2018-06-01 00:00:00', '2018-06-10 00:00:00', 'site_weather.csv')
ts.ts_plot(weather_data, ['air_temp_set_1', 'solar_radiation_set_1'], [8, 8], separate = True)

Example #4:
To get the energy usage hourly or daily summary of the mechanical equipment (rooftop units)
ts.rtu_energy_hourly('2019-08-01 00:00:00', '2019-08-02 00:00:00', 3)
ts.rtu_energy_daily('2019-08-01 00:00:00', '2019-09-01 00:00:00', 3)


Any further enquiries regarding the timeseries analysis code, please contact aoyuzou@berkeley.edu
"""


def retrieve(start, end, data):
    
    """
    This is a function used to retrieve timeseries data within specific time duration.
    
    Arg:
        start: the start time of the dataset (format: %Y-%m-%d %H:%M:%S)
        end: the end time of the dataset (format: %Y-%m-%d %H:%M:%S)
        data: the name of the dataset/file (needs to be either a dataframe or filename string)
        
    Return:
        data_df: a dataframe that shows the within the defined time range
    """
    import os
    import datetime as dt
    from datetime import datetime
    import pandas as pd
    from zoneinfo import ZoneInfo
    
    if isinstance(data, str):
        path = 'clean_data'
        path = os.path.join(path, data)
        data = pd.read_csv(path)
    elif isinstance(data, pd.DataFrame):
        data = data
    else:
        raise TypeError("input must be a string or a dataframe")
    
    timezone = ZoneInfo('America/Los_Angeles')
    data['date'] = pd.to_datetime(data['date'], utc=True).dt.tz_convert('America/Los_Angeles')
    start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone)
    end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone)
    after_start_date = data["date"] >= start
    before_end_date = data["date"] <= end
    between_two_dates = after_start_date & before_end_date
    
    # Using pandas.DataFrame.loc to Filter Rows by Dates
    data_df = data.loc[between_two_dates]
    return data_df




def hourly(start, end, data):
    
    """
    This is a function defined to derive hourly summary of the dataset.
    
    Arg:
        start: the start time of the dataset (format: %Y-%m-%d %H:%M:%S)
        end: the end time of the dataset (format: %Y-%m-%d %H:%M:%S)
        data: the name of the dataset
        
    Return:
        data_df: a dataframe that shows the hourly summary of the input dataset

    """
    
    import datetime as dt
    import pandas as pd
    from datetime import datetime
    import numpy as np
    from zoneinfo import ZoneInfo
    
    timezone = ZoneInfo('America/Los_Angeles')
    data['date'] = pd.to_datetime(data['date'])
    interval = dt.timedelta(hours=1)
    value_df = pd.DataFrame()
    time_df = pd.DataFrame()
    data_temp = pd.Series(dtype='object')
    while start < end:
        end_next = datetime.strptime(start, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone) + interval
        end_next = datetime.strftime(end_next, "%Y-%m-%d %H:%M:%S")
        value = retrieve(start, end_next, data).mean(numeric_only=True)
        date = pd.Series({'date': start}, dtype='datetime64[ns]')
        value_df = pd.concat([value_df, pd.DataFrame(value).transpose()], axis = 0)
        time_df = pd.concat([time_df, pd.DataFrame(date).transpose()], axis = 0)
        start = end_next

    hourly_df = pd.concat([time_df, value_df], axis = 1).reset_index(drop=True)
    
    return hourly_df




def daily(start, end, data):
    
    """
    This is a function defined to derive daily summary of the dataset.
    
    Arg:
        start: the start time of the dataset (format: %Y-%m-%d %H:%M:%S)
        end: the end time of the dataset (format: %Y-%m-%d %H:%M:%S)
        data: the name of the dataset
        
    Return:
        data_df: a dataframe that shows the daily summary of the input dataset

    """
    
    import datetime as dt
    import pandas as pd
    from datetime import datetime
    import numpy as np
    from zoneinfo import ZoneInfo
    
    timezone = ZoneInfo('America/Los_Angeles')
    data['date'] = pd.to_datetime(data['date'])
    interval = dt.timedelta(days=1)
    value_df = pd.DataFrame()
    time_df = pd.DataFrame()
    data_temp = pd.Series(dtype='object')
    while start < end:
        end_next = datetime.strptime(start, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone) + interval
        end_next = datetime.strftime(end_next, "%Y-%m-%d %H:%M:%S")
        value = retrieve(start, end_next, data).mean(numeric_only=True)
        date = pd.Series({'date': start}, dtype='datetime64[ns]')
        value_df = pd.concat([value_df, pd.DataFrame(value).transpose()], axis = 0)
        time_df = pd.concat([time_df, pd.DataFrame(date).transpose()], axis = 0)
        start = end_next

    daily_df = pd.concat([time_df, value_df], axis = 1).reset_index(drop=True)
    
    return daily_df




def ts_plot(data, col_name, fig_size, separate=False):
    """
    This is a function defined to make time series plot
    
    Arg:
        data: The dataset needed for the plot
        col_name: a list of vairable names that go into the plot
        separate: a boolean asking if variables should be separately plotted, default is set as FALSE
        fig_size: matplotlib plotting argument for adjusting figure size
        
    Return:
        A plot or subplots
    """
    
    import matplotlib.pyplot as plt
    
    if not col_name:
        raise ValueError("Input list cannot be empty.")
        
    plot_number = len(col_name)

    if separate & (plot_number > 1):
        fig, axs = plt.subplots(nrows = plot_number, ncols = 1, figsize = fig_size)
        for i, ax in enumerate(axs.flatten()):
            ax.plot(data['date'], data[col_name[i]])
            ax.set_title(col_name[i], fontsize = 13)
            ax.set_xlabel('Date', fontsize = 11)
            plt.sca(ax)
            plt.xticks(rotation=45, fontsize = 7)
        fig.subplots_adjust(hspace=0.75)
    else:
        plt.figure(figsize = fig_size)
        for i in col_name:
            plt.plot(data['date'], data[i])
            plt.title(i, fontsize = 15)
            plt.xlabel('Date', fontsize = 12)
            plt.legend(col_name, loc='best')
            plt.xticks(rotation=45, fontsize = 8)
            

            

def rtu_energy_hourly(start, end, unit):
    """
    This is a function defined to calculate thermal energy input by using outdoor air temperature, supply air temperature and air flow rate, from the rooftop unit for air conditioning
    
    Arg:
        start: the start time of the dataset (format: %Y-%m-%d %H:%M:%S)
        end: the end time of the dataset (format: %Y-%m-%d %H:%M:%S)
        unit: indicating which rooftop unit
    
    Return:
        Energy timeseries from calculation
    
    """
    
    import pandas as pd
    
    if unit not in range(1, 5):
        raise ValueError("Input rooftop unit not included, only unit 1~4 are available")
    else:
        ma_name = ['rtu_001_ma_temp', 'rtu_002_ma_temp', 'rtu_003_ma_temp', 'rtu_004_ma_temp'][unit - 1]
        sat_name = ['rtu_001_sa_temp', 'rtu_002_sa_temp', 'rtu_003_sa_temp', 'rtu_004_sa_temp'][unit - 1]
        afr_name = ['rtu_001_fltrd_sa_flow_tn', 'rtu_002_fltrd_sa_flow_tn', 'rtu_003_fltrd_sa_flow_tn', 'rtu_004_fltrd_sa_flow_tn'][unit - 1]
        
    ma_data = retrieve(start, end, 'rtu_ma_t.csv')[['date', ma_name]]
    ma_hourly = hourly(start, end, ma_data)

    sat_data = retrieve(start, end, 'rtu_sa_t.csv')
    sat_hourly = hourly(start, end, sat_data)[['date', sat_name]]

    afr_data = retrieve(start, end, 'rtu_sa_fr.csv')
    afr_hourly = hourly(start, end, afr_data)[['date', afr_name]]

    temp_hourly = pd.merge(left=ma_hourly, right=sat_hourly, left_on='date', right_on='date')
    temp_hourly['delta_T'] = (temp_hourly[ma_name] - temp_hourly[sat_name])
    energy_hourly = pd.merge(left=temp_hourly, right=afr_hourly, left_on='date', right_on='date')
    energy_hourly['energy_kw'] = energy_hourly['delta_T'] * energy_hourly[afr_name] * 1.08 / 3412
        
    return energy_hourly




def rtu_energy_daily(start, end, unit):
    """
    This is a function defined to calculate thermal energy input by using outdoor air temperature, supply air temperature and air flow rate, from the rooftop unit for air conditioning
    
    Arg:
        start: the start time of the dataset (format: %Y-%m-%d %H:%M:%S)
        end: the end time of the dataset (format: %Y-%m-%d %H:%M:%S)
        unit: indicating which rooftop unit
    
    Return:
        Energy timeseries from calculation
    
    """
    import pandas as pd
    import datetime as dt
    from datetime import datetime
    from zoneinfo import ZoneInfo
    
    if unit not in range(1, 5):
        raise ValueError("Input rooftop unit not included, only unit 1~4 are available")
        
    else:
        data = rtu_energy_hourly(start, end, unit)
        timezone = ZoneInfo('America/Los_Angeles')
        interval = dt.timedelta(days=1)
        value_df = pd.DataFrame()
        time_df = pd.DataFrame()
        data_temp = pd.Series(dtype='object')
        while start < end:
            end_next = datetime.strptime(start, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone) + interval
            end_next = datetime.strftime(end_next, "%Y-%m-%d %H:%M:%S")
            value = rtu_energy_hourly(start, end_next, unit).sum(numeric_only=True)
            date = pd.Series({'date': start}, dtype='datetime64[ns]')
            value_df = pd.concat([value_df, pd.DataFrame(value).transpose()], axis = 0)
            time_df = pd.concat([time_df, pd.DataFrame(date).transpose()], axis = 0)
            start = end_next
        
        energy_daily = pd.concat([time_df, value_df], axis = 1).reset_index(drop=True)
        
    return energy_daily



def avg_data(data, columnName):
    """
    helper function to take the average of all the data except 'date'
    Arg:
        data: input the data to take the average of
    Return:
        data_df: a dataframe that shows the average of the input dataset
    """
    data[columnName] = data.loc[:, data.columns != 'date'].mean(axis=1)
    return data[['date', columnName]]