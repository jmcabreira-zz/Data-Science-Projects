import streamlit as st
from utils import *
import altair as alt
import pandas as pd


#<= == == == == == == == == == == == == == == == == == == == == == ==  load_data == == == == == == == == == == == == == ==  == = >

def load_data():
    data_path = "data/dashboard_cars.json"
    car_data = pd.read_json(data_path, lines=True)
    add_extra_feat = extra_features(car_data)
    clean_data = clean_df(add_extra_feat)
    return clean_data



#<= == == == == == == == == == == == == == == == == == == == == == ==  clean_df  == == == == == == == == == == == == == ==  == = >

def clean_df(df):
    
    '''Rename columns and replace zeros(missing values) with suitable values
    
    ARG:
    df(dataframe): The dataframe with car information
    
    RETURNS:
    df(dataframe): The formated dataframe'''
    
    cols = ['brand', 'model', 'version', 'gearbox', 'cartype', 'regdate' ,
            'motorpower', 'fuel', 'car_steering', 'carcolor', 'doors', 'financial']
    
    # replace missing value with 'no_information' string
    df[cols] = df[cols].replace(0,'no_information')
    #replace car brand name
    df[cols] = df[cols].replace('vwvolkswagen','volkswagen')
    #Replace carpower interval
    df[cols] = df[cols].replace('2.02.9','2.0-2.9')
    df['mileage'] = df['mileage'].replace(0,int(df['mileage'].mean()))
    
    return df





# <=============================================       extra_features     ===================================================>

def extra_features(df):
    ''' Create individual features from extra column
    ARG:
    df(dataframe): the dataframe tha will be parsed

    RETURNS:
    df(dataframe): The dataframe containing features extracted from the extra column'''

    # check the greter extra variable length in order to identify all possible individual features

    string_length_list = [len(x) if type(x) == str else x for x in df.extra]

    greater_length = max(string_length_list)

    greater_length_index = max([(v, i) for i, v in enumerate(string_length_list)])[1]

    extra_features = df.iloc[greater_length_index].extra

    n_of_features = len(extra_features.rsplit(','))

    # Create column for each feature in extra column
    for feature in range(n_of_features):
        colname = extra_features.rsplit(',')[feature].strip()
        df[colname] = 0.0

    df = fill_in_the_features(df)

    return df

#<= == == == == == == == == == == == == == == == == == == == == == == fill_in_the_features == == == == == == == == == == == == == == == == == == == == == == == == = >

def fill_in_the_features(df):
    '''Fills in the feature cells stating whether the car contains the respective feature

    ARG:
    df(dataframe): The dataframe to be filled in

    RETURNS:
    df(dataframe): the dataframe with filled columns - 1 car has the feature and 0 car does not
    '''

    # find the index of the column extra
    columns = list(df.columns)
    index = columns.index('extra')

    for feature in df.columns[(index + 1):]:

        total_rows = df.shape[0]

        for row in range(total_rows):

            is_zero = (df.extra[row] == 0)

            if is_zero == True:

                df[feature].values[row] = 0.0

            else:

                contains_feature = feature in df.extra[row]

                if contains_feature == True:
                    df[feature].values[row] = 1
                else:
                    continue

    # delete extra column
    df.drop('extra', axis=1, inplace=True)

    return df

def data_info(df):

    cols =  ['vidro elétrico',
                 'air bag',
                 'trava elétrica',
                 'ar condicionado',
                 'direção hidráulica',
                 'alarme',
                 'som',
                 'sensor de ré']


    st.write(df[cols].sum())
    st.write(df['model'].value_counts())
    st.write(df['mileage'].describe().T)

#<= == == == == == == == == == == == == == == == == == == == == == == PLOTS == == == == == == == == == == == == == == == == == == == == == == == == = >



def scater_price_mileage(df):  
    selection = alt.selection_multi(fields =['brand'], bind='legend')

    domain = ['ford', 'volkswagen']
    range_ = ['steelblue', 'mediumvioletred']

    chart = alt.Chart(df).transform_calculate(
        ).mark_point().encode(
            #x='price:Q',
            #y='mileage',
            alt.X('price:Q', axis=alt.Axis(tickSize=0)),
            alt.Y('mileage', stack='center'),
            #alt.Color('brand:N', scale=alt.Scale(scheme='tableau20')),
            color=alt.Color('brand', scale=alt.Scale(domain=domain, range=range_)),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
            tooltip=['brand:N', 'model:N', 'price:N']
        ).add_selection(
            selection
    )
    return chart

def mean_price(df):
    selection = alt.selection_multi(fields=['model'], bind='legend')
    
    domain = ['fiesta', 'ka', 'focus', 'gol', 'voyage', 'fox', 'polo',
       'spacefox', 'up']
    range_ = ['#416ca6', '#7b9bc3', '#e9e9e9', '#7eb6d9','#4f4b43','#2c4786', '#425559', '#dce2f2','#011c40']

    chart = alt.Chart(df).mark_bar().encode(
        alt.X('mean(price)', axis=alt.Axis(tickSize=0)),
        alt.Y('model', stack='center'),
        #alt.Color('model:N', scale=alt.Scale(scheme='tableau20')),
        color=alt.Color('model', scale=alt.Scale(domain=domain, range=range_)),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.1))
    ).add_selection(
        selection
    )
    return chart


def model_regdate_count(df):

    selection = alt.selection_multi(fields=['regdate'], bind='legend')


    chart = alt.Chart(df).mark_bar().encode(
    alt.X('count()', axis=alt.Axis(tickSize=0)),
    alt.Y('model', sort = alt.Sort(encoding = 'x', order= 'descending')),
    tooltip = ['regdate','count()'],
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
    color = 'regdate:O'
    ).add_selection(
    selection
    )
    return chart

def financial_regdate(df):

    selection = alt.selection_multi(fields=['regdate'], bind='legend')


    chart = alt.Chart(df).mark_bar().encode(
    alt.X('count()', axis=alt.Axis(tickSize=0)),
    alt.Y('financial', sort = alt.Sort(encoding = 'x', order= 'descending')),
    tooltip = ['regdate','count()'],
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
    color = 'regdate:O'
    ).add_selection(
    selection
    )
    return chart
    
def model_power_count(df):
    
    selection = alt.selection_multi(fields=['motorpower'], bind='legend')
    
    chart = alt.Chart(df).mark_bar().encode(
    x = 'count()',
    y = alt.Y('model', sort = alt.Sort(encoding = 'x', order= 'descending')),
    tooltip = ['motorpower','count()'],
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
    color = 'motorpower:O'
    ).add_selection(
    selection
    )
    return chart

def model_power_price(df):
    
    selection = alt.selection_multi(fields=['motorpower'], bind='legend')
    
    chart = alt.Chart(df).mark_bar().encode(
    x = 'mean(price)',
    y = alt.Y('model', sort = alt.Sort(encoding = 'x', order= 'descending')),
    tooltip = ['motorpower','mean(price)'],
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
    color = 'motorpower:O'
    ).add_selection(
    selection
    )
    return chart