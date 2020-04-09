import pandas as pd
import numpy as np

# ================================================================ to_numeric ===================================================================
def to_numeric(x):
    
    ''' Realiza parsing de cada elemento da serie e os converte em numerico 
    ARG:
    x(string): string que sera transformada em numerica
    
    RETURNS:
    X_num(float/int): valor convertido em numerico e ponto como casa decimal'''
    
    
    x = x.replace(',','.')
    sep = x.split('.')
    
    if len(sep) == 2:
        x = sep[0]+'.'+sep[1]
        
        
    elif len(sep) ==3 :
        x = sep[0]+sep[1]+'.'+sep[2]
    
    else:
        x = 0
    
    x_num = pd.to_numeric(x)

    return  x_num

# ================================================================ preprocess_df ===================================================================

def preprocess_df(df):
    
    '''Realiza pre-processamento dos dados de forma a gerar um dataframe no formato adequado (dateformat e numerico)
    ARG:
    df(dataframe): dataframe a ser pre-processado
    RETURNS:
    df(dataframe)': dataframe pre-processado'''
    
    # Determina novos nome de colunas
    df.columns = ["Date", "Speed(m/s)", "Direction(°)",'Energy(kWh)']
    
    df.Date = pd.to_datetime(df.Date, dayfirst= True)
    df.dtypes
    
    # Transforma colunas em numericos 
    df['Speed(m/s)'] = pd.to_numeric(df['Speed(m/s)'].apply(to_numeric))
    df['Direction(°)'] = pd.to_numeric(df['Direction(°)'].replace('-','0'))
    df['Energy(kWh)'] = df['Energy(kWh)'].apply(to_numeric)
    
    # Trransforma kWh em MWh
    df['Energy(MWh)'] = np.round(df['Energy(kWh)'] /1000 , 2)
    df.drop('Energy(kWh)', axis = 1, inplace = True)
    
    # Associa coluna Date ao index
    df.index = pd.to_datetime(df.Date, format="%m-%d-%Y")
    # dropa coluna Date extra 
    df.drop("Date", axis=1, inplace=True)
    
    return df


# ================================================================ preprocess_df ===================================================================

def fill_na_with_mean(df):
    
    '''Preenche valores nan com a media da coluna
    
    ARG: 
    df(dataframe): dataframe que sera processado
    
    RETURNS:
    df(dataframe): dataframe com nan values preenchidos com a media da coluna'''
    
    num_cols = len(list(df.columns.values))
    
    for col in range(num_cols):
        
        df.iloc[:,col] = df.iloc[:,col].fillna(df.iloc[:,col].mean())
        
    return df
    