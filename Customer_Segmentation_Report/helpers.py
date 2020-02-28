import os 
import pandas as pd
import numpy as np






def create_missing_code_dict(feat_missing_code_df):
    '''
    This function creates a dictionary with each feature name as key and it's corresponding
    missing code as value.
    
    ARGS:
        feat_missing_code_df (dataframe) - dataframe with feature names and missing code.
    RETURNS:
        missing_dict (dict) - dictionary containing feature as name and missing as value.
    '''
    missing_dict = {}
    for row in feat_missing_code_df.itertuples():
        missing_dict[row.Attribute] = eval(row.Missing_Value)

    return missing_dict



# Create a dictionary with valid values for each column
def valid_values_dict(df,missing_dict):
    ''' 
    Iterate over all the df columns and check if value is valid or a missing code.
    
    ARG:
    
    df (dataframe) - dataframe with valid values and missing codes.
    
    missing_dict (dictionary) - a dictionary with Attribute as keys and missing codes as values.
    
    RETURNS:
    
    valid_values_dict (dictionary) - a dictionary with attribute as key and dict with valid values as values
     
    
    '''
   

    valid_values_dict = {}
    for col in azdias.columns[1:]: # skip first column (LNR)
        values_dict = {}
        for val in azdias[col].value_counts().index:
            if col not in missing_dict: # cases when column is missing in data_info dataframe 
                values_dict[val] = val
            elif val not in values_dict and val not in missing_dict[col]:
                values_dict[val] = val
        valid_values_dict[col] = values_dict

    return valid_values_dict




def save_csv(df, data_dir, filename):
    
        '''Saves all of the dataframes of the notebook
        ARGS:
            df :  dataframe
            data_dir: The directory where files will be saved
            filename: name of the file
        RETURN: 
            Msg with the created path
         '''
     
        
    
        #make data_dir, if it does not exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

            
        df.to_csv(os.path.join(data_dir, filename), index= True, header = True)
        
        
        print('Path created: '+str(data_dir)+'/'+str(filename))