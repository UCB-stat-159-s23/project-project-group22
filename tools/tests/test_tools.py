import os
import glob
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import numpy as np
from tools import timeseries as ts
import pytest

data1 = ts.retrieve('2020-12-01 00:00:00', '2020-12-31 00:00:00', 'zone_co2.csv')
col_name = [8, 5]
unit = 3




def test_retrieve():
    data = 'zone_co2.csv'
    if isinstance(data, str):
        path = 'clean_data'
        path = os.path.join(path, data)
        data = pd.read_csv(path)
    elif isinstance(data, pd.DataFrame):
        data = data
    else:
        raise TypeError("input must be a string or a dataframe")
    
def test_hourly():
    hourly1 = ts.hourly('2020-12-01 00:00:00', '2020-12-02 00:00:00', data1)
    assert type(hourly1) == pd.DataFrame
    
    
def test_daily():
    daily_df = ts.daily('2020-12-01 00:00:00', '2020-12-02 00:00:00', data1)
    assert type(daily_df) == pd.DataFrame
    
def test_tsplot():
     if not col_name:
        raise ValueError("Input list cannot be empty.")
        
        
def test_rtu_energy_hourly():
    if unit not in range(1, 5):
        raise ValueError("Input rooftop unit not included, only unit 1~4 are available")

