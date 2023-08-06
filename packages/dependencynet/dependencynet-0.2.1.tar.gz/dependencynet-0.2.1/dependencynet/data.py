"""
This module provides data sources
"""
import logging

import pandas

def data(name):
    return data_journey

def source_data_journey(compact_columns_journey):
    filename = path.join('tests', 'scenario', 'journey', 'resources', 'journey.csv')
    data = pd.read_csv(filename, delimiter=';')
    columns = ['country', 'town', 'monument', 'flight_in', 'flight_out']
    df = pd.DataFrame(data, columns=compact_columns_journey)

    # FIXME factprize
    return df
