import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt




#================================================ trim_axs ==========================================================
def trim_axs(axs, N):
    '''   This function takes the an axes list, the number of plots and sets  the axes list with correct length
    
    ARG: 
    axs(array like): array with axes 
    N(integer): number of graphs to be plotted 
    
    RETURS:
    axs(array like): array with correct number of axes to be plotted
    '''

    axs = axs.flatten()
    for ax in axs[N:]:
        ax.remove()
    return axs[:N]


#================================================ bar_plots ==========================================================
def individual_bar_plot(df, col,  ax = None):
    '''
    Bar plot for each column
    
    
    ARG:
    df(daraframe): dataframe to be parsed 
    col(string): name of the column
        
    
    '''
    

    obj = df[col].value_counts(ascending = False, normalize = True)  

    obj.plot( kind = 'bar',
            #color = color,
            edgecolor = 'black', 
            ax = ax,   
            legend = None,              
            ).set_title(f'Variable:{col} ')
    
    ax.set_xlabel('Values')
    
#================================================ plot_dist ==========================================================   
    
def bar_plot(df, plot_num, col_list , nrows, ncols):
    
    ''' Plots percentage of each value or category for each feature
    ARG:
    df(dataframe): dataframe for parsing
    plot_num(integer): number of plots
    col_list(list): list of columns to be plotted 
    nrows(integer): number of rows for subplot
    ncols(integer): number of columns for subplot

    '''
    
    fig, ax = plt.subplots(nrows, ncols, figsize=(12, 12), sharey=False)
    
    ax = trim_axs(ax, plot_num)
    
    # ax.flatten() collapses the ax into one dimension array
    for subplot, col in zip(ax.flatten(), col_list):
        individual_bar_plot(df, col, ax=subplot)
    
    plt.tight_layout()
    
#================================================ missing_data_columns_df ==================================================   
  
    
def missing_data_columns_df(df, columns_to_drop = False, drop_columns = False):
    
    ''' Creates a missing values data frame and drops columns when needed 
    
    ARG:
    df(datarame): dataframe to be parsed
    drop_columns(binary): Binary that identifies whether we want to drop or not columns
    columns_to_drop(list): list of columns to be dropped'''
    
    if drop_columns:
        
        df.drop(columns_to_drop, axis = 1, inplace = True)
    
    missing_data = df.isnull().sum()[(df.isnull().sum() != 0)]

    total_rows = df.shape[0]

    missing_dict = {'Missing_Count': missing_data.values,
               'Pct_missing': np.round(missing_data.values*100/(total_rows),2)}

    x_train_missing = pd.DataFrame(missing_dict, index = missing_data.index)
    
    return x_train_missing


#================================================ compare_df_plot ==================================================

def compare_df_plot(df_low_missing, df_high_missing, column_names):
    
    
    ''' Compare distribution of two dataframes'''
    
    for column_name in column_names:
    
        fig = plt.figure(figsize = (15,5))
        ax1 = fig.add_subplot(121)
        ax1.title.set_text('Low Missing Values')
        sns.countplot(df_low_missing.loc[:, column_name])

        ax2 = fig.add_subplot(122)
        ax2.title.set_text('High Missing Values')
        sns.countplot(df_high_missing.loc[:,column_name])      
        
        #fig.subtitle(column_name)
        plt.plot()



#================================================ feature_engineering_ordinal ==================================================    
def feature_engineering_ordinal(df):
    
    '''encode all binary and ordinal features
    
    ARG:
    df(dataframe): dataframe to be re-encoded
    
    RETURNS:
    dummies_df(dataframe): re-encoded dataframe'''
    
    gender_values = {'M': 1, 'F':0} # TP_SEXO
    Q025_values = {'A':0 , 'B':1} # Q025
    Q026_values = {'A': 0 , 'B': 1, 'C': 2} #Q026  
    Q047_values = {'A': 0 , 'B': 1, 'C': 2, 'D':3, 'E':4}  #Q047
    Q024_values = {'A': 0 , 'B': 1, 'C': 2, 'D':3, 'E':4}  #Q024
    Q001_values = {'A': 0 , 'B': 1, 'C': 2, 'D':3, 'E':4, 'F':5, 'G':6 , 'H':7}  #Q001
    Q002_values = {'A': 0 , 'B': 1, 'C': 2, 'D':3, 'E':4, 'F':5, 'G':6 , 'H':7}  #Q002
    
    ### NOTE:Needs to be iterate 

    #code_list = [gender_values, 
    #             Q025_values,
     #            Q026_values,
      #           Q047_values,
       #          Q024_values,
        #         Q001_values,
         #        Q002_values
          #      ]

    #columns = ['TP_SEXO',
     #          'Q025',
      #         'Q026',
       #        'Q047',
        #       'Q024',
         #      'Q001',
          #     'Q002'
           #   ]
    
    #dummies_df = df.copy
    
    df['TP_SEXO'] = df['TP_SEXO'].map(gender_values)
    df['Q025'] = df['Q025'].map(Q025_values)
    df['Q026'] = df['Q026'].map(Q026_values)  
    df['Q047'] = df['Q047'].map(Q047_values)
    df['Q024'] = df['Q024'].map(Q024_values)
    df['Q001'] = df['Q001'].map(Q001_values)
    df['Q002'] = df['Q002'].map(Q002_values)

        
    return df

#================================================ one_hot_encode_top_x ========================================================  

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


#================================================ feature_engineering_encode ========================================================  

def feature_engineering_encode(df):
    
    df_dummies = feature_engineering_ordinal(df)
    
    df_dummies = one_hot_encode_top_x(df_dummies, variable_name ='SG_UF_RESIDENCIA',top_x_labels = 10)
    df_dummies = one_hot_encode_top_x(df_dummies, variable_name ='Q006'       ,top_x_labels = 10)
    df_dummies = one_hot_encode_top_x(df_dummies, variable_name ='CO_PROVA_CN',top_x_labels = 10)
    df_dummies = one_hot_encode_top_x(df_dummies, variable_name ='CO_PROVA_CH',top_x_labels = 10)
    df_dummies = one_hot_encode_top_x(df_dummies, variable_name ='CO_PROVA_LC',top_x_labels = 9)
    df_dummies = one_hot_encode_top_x(df_dummies, variable_name ='CO_PROVA_MT',top_x_labels = 9)
    
    return df_dummies