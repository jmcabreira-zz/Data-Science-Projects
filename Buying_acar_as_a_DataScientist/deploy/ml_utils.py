import pandas as pd
import re
import joblib as jb
from scipy.sparse import hstack, csr_matrix
import numpy as np
import json

# <=========================================================================================================================>  
# <=================================================      MODEL        =====================================================> 
# <==========================================================================================================================> 






# LOAD MODELS
model_rf = jb.load('random_forest_car.pk.z')
model_lgbm = jb.load('lgbm_car.pk;.z')


# <=================================================      make_prediction        =====================================================> 

def make_prediction(data):
    
    feature_array = clean_data(data)
    
    if feature_array is None:
        return 0
    
    pred_rf= model_rf.predict_proba(feature_array)[0][1]
    pred_lgbm = model_lgbm.predict_proba(feature_array)[0][1]
    
    
    pred =  0.3*pred_rf + 0.7*pred_lgbm
    
    return pred


# <=================================================          clean_data        =====================================================> 

def clean_data(data):
    
    cols = ['price', 'regdate', 'mileage','model_ka', 'model_ecosport', 'model_fiesta', 'model_fox',
       'model_focus', 'model_gol', 'model_voyage', 'model_up', 'model_saveiro',
       'model_crossfox', 'model_jetta', 'model_golf', 'model_polo',
       'model_fusion', 'model_0', 'model_ranger', 'gearbox_manual', 'gearbox_manual',
       'gearbox_automatico', 'gearbox_semiautomatico', 'gearbox_0', 'financial_ipva_pago', 'financial_0',
       'financial_financiado', 'financial_de_leilao', 'financial_com_multas' ]


    clean_df = pd.DataFrame(columns = cols, index = [0])
    
    
    clean_df = clean_price(data, clean_df)
    clean_df = clean_regdate(data, clean_df)
    clean_df = clean_mileage(data, clean_df)
    clean_df = clean_model(data, clean_df)
    clean_df = clean_gearbox(data, clean_df)
    clean_df = clean_financial(data, clean_df)
    
    
    if any(clean_df.isnull().iloc[0]):
        return None
    
    
    
    feature_array = clean_df.iloc[0].to_numpy()
    
    #set right shape in order to feed the model
    feature_array = feature_array.reshape(-1,29)
    
    return feature_array



# <=================================================        clean_price        =====================================================> 

def clean_price(data, clean_df):

    if data['price'] == '':    
        clean_df['price'] = None
        
    else:
        numeric_price = int(data['price'])
        clean_df['price'] = numeric_price

            
    return clean_df
    
    

# <=================================================       clean_regdate        =====================================================>   

    
def clean_regdate(data,clean_df):
    
    if  data['regdate'] == '0' or data['regdate'] =='':
        
        clean_df['regdate'] = None
    else:
    
        numeric_regdate = int(data['regdate'])
        clean_df['regdate'] = numeric_regdate
    
    return clean_df


# <=================================================       clean_mileage        =====================================================> 

def clean_mileage(data,clean_df):
    
    if  data['mileage'] == '0':
        clean_df['mileage'] = None
    else:
        numeric_mileage = int(data['mileage'])

        clean_df['mileage'] = numeric_mileage
    
    return clean_df

# <================================================       clean_model             =====================================================> 


def clean_model(data,clean_df):
    
    models= ['ka', 'ecosport', 'fiesta', 'fox',
       'focus', 'gol', 'voyage', 'up', 'saveiro',
       'crossfox', 'jetta', 'golf', 'polo',
       'fusion', '0', 'ranger']
    
    
    for model in models:
        
        clean_df['model_'+model] = np.where(data['model'] == model,1,0)
        
    return clean_df

        
    
# <=================================================      clean_gearbox        =====================================================>     
        
        
def clean_gearbox(data, clean_df):
    
    
    gearboxes = ['manual', 'manual', 'automatico', 'semiautomatico', '0']
    
    for gearbox in gearboxes:
        clean_df['gearbox_'+gearbox] = np.where(data['gearbox'] == gearbox,1,0)
        
    return clean_df


# <=================================================      clean_financial        =====================================================> 



def clean_financial(data,clean_df):
    
    financials = [ 'ipva_pago', '0', 'financiado', 'de_leilao', 'com_multas']
    
    for financial in financials:
        clean_df['financial_'+financial] = np.where(data['financial'] == financial,1,0)
        
    return clean_df
        