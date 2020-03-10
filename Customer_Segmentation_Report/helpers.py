import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# <=========================================================================================================================>  
# <============================================ DATA PREPROCESSING ==========================================================> 
# <==========================================================================================================================>

# <============================================= missing_code_df ===========================================================>

def missing_code_df(df):
    ''' 
    Parse the data_info dataframe in order to have a dataframe with two columns (Attribute and Missing_Value)
    
    ARG:
    df(dataframe) - the dataframe with attributes information
    
    RETURNS:
    df(dataframe) - A parsed dataframe with two columns ( Attribute and Missing_Value)
    

    '''
    
    print('Drop Description, Value and Meaning columns')
    df.drop(['Description','Value','Meaning'], axis = 1, inplace = True)
    print()
    print('Drop duplicates')
    df.drop_duplicates(keep='first',inplace=True) 
    print()
    print('Fillna with -1 in columns with no missing code')
    df.fillna('[-1]', inplace = True)
    df.reset_index(drop = True, inplace = True)
    print()
    print('            == DataFrame ==')
    display(df.head())

    return df


# <============================================ create_missing_code_dict ====================================================>

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


# <============================================ valid_values_dict =========================================================>
    
def valid_values_dict(df,missing_dict):
    ''' 
    Iterate over all the df columns and check if value is valid or a missing code.
    
    Create a dictionary with valid values for each column.
    
    ARG:
    
    df (dataframe) - dataframe with valid values and missing codes.
    
    missing_dict (dictionary) - a dictionary with Attribute as keys and missing codes as values.
    
    RETURNS:
    
    valid_values_dict (dictionary) - a dictionary with attribute as key and dict with valid values as values
     
    
    '''
   

    valid_values_dict = {}
    for col in df.columns[1:]: # skip first column (LNR)
        values_dict = {}
        for val in df[col].value_counts().index:
            if col not in missing_dict: # cases when column is missing in data_info dataframe 
                values_dict[val] = val
            elif val not in values_dict and val not in missing_dict[col]:
                values_dict[val] = val
        valid_values_dict[col] = values_dict

    return valid_values_dict

# <============================================ missing_values_barplt ===================================================> 

def missing_values_barplt(df, column_name, threshold=50):
    
    """
    Plot the number of missing value per features
    
    ARG:
    df(dataframe) : dataframe containing columns of missing values
    column_name (string) : string with the name of the column to be plotted 
    threshould (integer) : number of attributes to be plotted 
    
    
    """

    df_missing = df.sort_values(column_name, ascending=False)[:threshold]
    fig = plt.figure(figsize=(18,5))

    ax = sns.barplot(df_missing.index, df_missing[column_name], palette="Blues_d")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    
    ax.set_title("Missing values {} " .format(column_name),fontsize= 15)
    ax.set_ylabel('Number of Missing values', fontsize = 13)

    
    
    # <============================================hist_missing_values================================================>
    
def hist_missing_values(df,  threshold = None , greater_or_less = None  ):


    """
    Creates a histogram of missing values

    ARG: 

    df(dataframe) : dataframe containing columns of missing values
    threshold (integer) : set the threshold in which the dataframe will be parsed
    greater_or_less (string) : set the relationship between threshold and dataframe (greater or less than)


    NOTE: This function needs improvement in terms of testing


    """


    if threshold == None:
        df = df
    else:
        if greater_or_less == 'less':
             df = df[df['Percent_nan'] < threshold]
        elif greater_or_less == 'greater':
            df = df[df['Percent_nan'] > threshold]

    fig = plt.figure(figsize=(20,7))
    plt.hist(df['Percent_nan'],bins=np.linspace(0,100,21))
    plt.title('Distribution of Number of Missing Valer per Feature');
    plt.xticks(np.linspace(0,100,21))
    plt.xlabel('% Missing Values')
    plt.ylabel('Number of Features');
    
    
# <=========================================================================================================================>  
# <================================================= FEATURE ENGINEERING ====================================================> 
# <==========================================================================================================================>       
def unique_values_dict(df):
    
    
    
    """ Creates two dictionaries ( one for binary features and other for multiple features) containing
    both the name of the feature (column) and the total number of unique values
    
    ARG:
    
    df(dataframe) - dataframe containing the features 
    
    RETURNS: 
    binary_variable (dictionary) - binary features
    multiple_values_feature (dictionary) - multiple values features
    
    NOTE : it inclues ordinal feautes
    
    """

    binary_variable = {}
    multiple_values_feature = {}

    for column in df.columns:

        unique_values = df[column].nunique()

        if unique_values <= 2:

            binary_variable[column] = unique_values

        else:
            multiple_values_feature[column] = unique_values

    return binary_variable, multiple_values_feature

    
    
    
# <========================================================= save_csv ========================================================> 
    


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