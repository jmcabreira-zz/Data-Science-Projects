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
    
    
    
def impute_values(df):
    
    ''' 
    Impute most frequent value of a given column (replace nan with most frequent value of the column)
    
    ARG:
    df(dataframe): dataframe that will be imputed
    
    RETURNS:
    df(dataframe): dataframe with most frequent value of a given column inputed 
    
    '''
    

    columns = df.columns[df.isnull().any()]

    for column in columns:

        most_frequent_value = df.groupby([column])[column].count().sort_values(ascending = False).index[0]

        df[column].fillna(most_frequent_value, inplace = True)

    return df




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



def clean_df(df, missing_code_df, column_names = None, is_customer_df = False):
    
    ''' 
    Clean the datafraame and perform data engineering on it     
    
    ARG: 
    df(dataframe): dataframe to be parsed
    missing_code_df(dataframe): dataframe with missing code of each feature
    columns(array): array with the column names of the dataframe (after cleaning)
    customer_data(bool): boolean variable representing whether or not the df is the customer df 
    
    RETURNS:
    df_dummies(dataframe): clean and parsed dataframe
    
    
    '''

    if is_customer_df:
        
        print('======================== WORKING ON CUSTOMER DATAFRAME =================================')
        print('====== Delete CUSTOMER_GROUP, ONLINE_PURCHASE, PRODUCT_GROUP features ===============')
        print()
        df.drop(['CUSTOMER_GROUP', 'ONLINE_PURCHASE', 'PRODUCT_GROUP'], axis = 1, inplace = True)
    else:
        print('======================== WORKING ON AZDIAS DATAFRAME ===================================')
        
    
    print('============================= Drop index LNR ============================================')
    print()
    
    df.drop(['LNR'], axis = 1, inplace = True)
    
    print('========================== Converte Missing Code ========================================')
    print()
    

    missing_dict = create_missing_code_dict(missing_code_df)
    
  
    valid_values_dict_ = valid_values_dict(df, missing_dict)
    
    # Dataframe with missing codes converted to nan
    #df_copy = df.copy()

   
    for col in df.columns[1:]: 

        df[col] = df[col].map(valid_values_dict_[col])
        
    print('=================== Drop Features with more than 40% of missing values ==================')
    print()
    
    columns_to_drop = ['ALTER_KIND4',
                         'TITEL_KZ',
                         'ALTER_KIND3',
                         'D19_TELKO_ONLINE_DATUM',
                         'D19_BANKEN_OFFLINE_DATUM',
                         'ALTER_KIND2',
                         'D19_TELKO_ANZ_12',
                         'D19_BANKEN_ONLINE_QUOTE_12',
                         'D19_BANKEN_ANZ_12',
                         'D19_TELKO_ANZ_24',
                         'D19_VERSI_ANZ_12',
                         'D19_TELKO_OFFLINE_DATUM',
                         'ALTER_KIND1',
                         'D19_BANKEN_ANZ_24',
                         'D19_VERSI_ANZ_24',
                         'D19_BANKEN_ONLINE_DATUM',
                         'GREEN_AVANTGARDE',
                         'D19_BANKEN_DATUM',
                         'AGER_TYP',
                         'D19_VERSAND_ONLINE_QUOTE_12',
                         'D19_TELKO_DATUM',
                         'EXTSEL992',
                         'D19_GESAMT_ONLINE_QUOTE_12',
                         'D19_VERSAND_ANZ_12',
                         'D19_VERSAND_OFFLINE_DATUM',
                         'D19_GESAMT_ANZ_12',
                         'KK_KUNDENTYP',
                         'D19_VERSAND_ANZ_24',
                         'D19_GESAMT_OFFLINE_DATUM',
                         'D19_KONSUMTYP',
                         'D19_GESAMT_ANZ_24',
                         'D19_VERSAND_ONLINE_DATUM',
                         'KBA05_BAUMAX',
                         'D19_GESAMT_ONLINE_DATUM',
                         'D19_VERSAND_DATUM']

    
    #df_parsed = df.copy()
    df.drop(columns_to_drop, axis = 1, inplace = True)
    
    
    print('============================= Delete Columns ============================================')
    print()
    
    # Split dataframe 
    
    #df_copy = df_parsed.copy()
    df = df.dropna(thresh= 250) # Keep only the rows with at least 250 non-NA values
   
    
    print('=================== Impute the missing values (impute most frequent value) ==============')
    print()
    
    
    df_most_freq_values_imputed = impute_values(df)
    
    
    print('====================== Re-encode binary fature (OST_WEST_KZ) ============================')
    print()
    
    bin_values = {'W': 1, 'O':0}
    df_most_freq_values_imputed['OST_WEST_KZ'] = df_most_freq_values_imputed['OST_WEST_KZ'].map(bin_values)
    
    print('=====================  Re-encode multi-categorical features =============================')
    print()
    
    # replace X with 0 and transform values into numeric
    df_most_freq_values_imputed['CAMEO_DEUG_2015'] = df_most_freq_values_imputed.CAMEO_DEUG_2015.replace({'X': 0.0 }) 
    df_most_freq_values_imputed['CAMEO_DEUG_2015'] = pd.to_numeric(df_most_freq_values_imputed['CAMEO_DEUG_2015'])
    
    # replace XX with 0 and transform values into numeric in order to sum up int and float categories
    # convert each category to string so that its possible to compare them 
    df_most_freq_values_imputed['CAMEO_INTL_2015'] = df_most_freq_values_imputed.CAMEO_INTL_2015.replace({'XX': 0.0 }) 
    df_most_freq_values_imputed['CAMEO_INTL_2015'] = pd.to_numeric(df_most_freq_values_imputed['CAMEO_INTL_2015'])
    df_most_freq_values_imputed['CAMEO_INTL_2015'] = df_most_freq_values_imputed.CAMEO_INTL_2015.apply(str)
    

    
    # Ohe top_x categories of the variables 
    df_dummies = one_hot_encode_top_x(df_most_freq_values_imputed, variable_name ='CAMEO_DEU_2015',top_x_labels = 25)
    
    df_dummies = one_hot_encode_top_x(df_most_freq_values_imputed, variable_name ='CAMEO_INTL_2015',top_x_labels = 25)
    
    df_dummies = one_hot_encode_top_x(df_most_freq_values_imputed, variable_name ='D19_LETZTER_KAUF_BRANCHE',top_x_labels = 16)
    
    
    #to_reencode = ['CAMEO_DEU_2015',
                   #'CAMEO_INTL_2015',
                   #'D19_LETZTER_KAUF_BRANCHE']    
    #df_dummies = pd.get_dummies(df_most_freq_values_imputed, columns = to_reencode, drop_first = True)
    
    
    
    print('=================== Re-encode EINGEFUEGT_AM to year and month ===========================')
    print()
    
    df_dummies['EINGEFUEGT_AM'] = pd.to_datetime( df_dummies['EINGEFUEGT_AM'],
                                                 format = '%Y/%m/%d' )
                                                 
    df_dummies['EINGEFUEGT_AM_year'] = df_dummies['EINGEFUEGT_AM'].dt.year
    df_dummies['EINGEFUEGT_AM_month'] = df_dummies['EINGEFUEGT_AM'].dt.month
    df_dummies.drop(['EINGEFUEGT_AM'], axis = 1 , inplace = True)
                                                 
    
    if column_names is not None:
        
        diff = np.setdiff1d(column_names, df_dummies.columns)
        print(' Missing columns:',diff)
        print()
        
        print('======================== Add 0 to Missing columns ===================================')
       
        
        for column in diff:
            
            df_dummies[column] = 0.0
            df_dummies[column] = df_dummies[column].astype('float')

        print('========================= Dataframa is cleaned ======================================')
        
    return df_dummies    


def pca_analysis_plot(n_conponents, index, var_values, cum_sum):
    
    '''
    Plot graphs for PCA analysis (cumulative variance x number of components and percentage of variance explained x 
    number of components)
     
    ARG:
    n_components (integer): number of components
    index (array) : array with the same number of components 
    var_values(array): variance explained by the components
    cum_sum(array): cumulative variance explained

    '''
    
    
    # Frist Plot
    plt.figure(figsize=(13,15))
    plt.subplot(2, 1, 1)
    plt.bar(index, cumulative_sum_var,color = 'lightsteelblue')
    plt.ylabel('Cumulative Explaiden Variance (%)')
    plt.xlabel('Number of Principal Components')
    plt.xticks(np.linspace(0,500, 10, endpoint=False))
    #plt.yticks(np.linspace(0,100, 5, endpoint= True))
    plt.title('PCA Analysis Graph')


    # 196 components
    plt.hlines(y=90, xmin=0, xmax=196, color='black', linestyles='-',zorder=5)
    plt.vlines(x=196, ymin=0, ymax=90, color='black', linestyles='-',zorder=6)


    #Second Plot
    plt.subplot(2, 1, 2)
    plt.bar(index, values,color = 'lightsteelblue')
    plt.xticks(np.linspace(0,500, 10, endpoint=False))
    plt.xlabel('Number of Principal Components')
    plt.ylabel(' Variance Explained (%)')
    plt.title('PCA Analysis Graph');
    

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