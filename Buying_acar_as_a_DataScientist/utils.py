import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer






def clean_df(df):
    
    
    
    
    # Drop empty price rows
    cleaned_price = empty_price(df)
    
    # Create features from extra column and apply one hot encode
    df = extra_features(cleaned_price)
    
    # Apply Ohe on categorical features - considering only top frequency components
    
    to_dummies = ['financial', 'brand', 'cartype', 'model','gearbox', 'motorpower', 'fuel',          'car_steering','carcolor','exchange']
    
    top_x_feat = [4,2,8,32,3,10, 10,2,4,10,2]
        
    for feature, top_x in zip(to_dummies,top_x_feat):
        df_dummies = one_hot_encode_top_x(df, variable_name = feature ,top_x_labels = top_x)
        
        
    return df_dummies
        
    
    
    
    
    
    
    
    
def one_hot_encode_top_x(df, variable_name, top_x_labels):
    
    """Create dummy variables for the most X frequent categories of a given features
    note: other categories are considered as noise 
    
    ARG:
    
    top_x_labels (integer): Number of most frequent categories 
    variable_name (string): Name of the variable
    df (dataframe): dataframe to be re-encoded 
    
    RETURNS:
    
    df(dataframe): dataframe with top categories re-encoded (one hot encode)
    """
   
    top_x = [x for x in df[variable_name].value_counts().sort_values(ascending = False).head(top_x_labels).index]
    
    
    for label in top_x:
        df[variable_name+'_'+label] = np.where(df[variable_name] == label,1,0)
    
    df.drop([variable_name], axis = 1, inplace = True)
    
    
    return df  



def extra_features(df):
    
    
    ''' Create individual features from extra column
    ARG:
    df(dataframe): the dataframe tha will be parsed
    
    RETURNS:
    df(dataframe): The dataframe containing features extracted from the extra column'''
    
    
    
    # check the greter extra variable length in order to identify all possible individual features  
    
    string_length_list = [len(x) if type(x) == str else x for x in df.extra]
    
    greater_length = max(string_length_list)
    
    greater_length_index = max([(v,i) for i,v in enumerate(string_length_list)])[1]

    extra_features = df.iloc[greater_length_index].extra

    
    n_of_features = len(extra_features.rsplit(','))
    
    # Create column for each feature in extra column    
    for feature in range(n_of_features):
        colname = extra_features.rsplit(',')[feature].strip()
        df[colname] = 0.0
        
    
    df = fill_in_the_features(df)
    
    
    
    return df



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
    

    for feature in df.columns[(index+1):]:

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
    df.drop('extra', axis = 1, inplace = True)
    
    return df
    






def empty_price(df):
    
    ''' Deletes row with empty price
    ARG:
    df(dataframe): The dataframe to be cleaned
    
    RETURNS:
    no_empty_df(dataframe): The dataframe without empty prices'''
    
    
    
    #check for empty price and delete rows
    empty_price = np.where(df.applymap(lambda x: x == ''))[0]
    # drop rows with empty price
    no_empty_df = df.drop(index = empty_price)
    # reset index
    no_empty_df = no_empty_df.reset_index(drop=True)
    
    return no_empty_df



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    