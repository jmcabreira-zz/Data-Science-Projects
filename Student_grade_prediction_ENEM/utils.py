import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.linear_model import Lasso
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import ElasticNet
from sklearn.pipeline import Pipeline
from sklearn.svm import SVR 
from sklearn.preprocessing import StandardScaler,MinMaxScaler


from sklearn.metrics import make_scorer
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import median_absolute_error

from sklearn.model_selection import learning_curve


from sklearn.model_selection import  KFold, cross_val_score


# <=========================================================================================================================>  
# <============================================ DATA PREPROCESSING ==========================================================> 
# <==========================================================================================================================>

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


# <=========================================================================================================================>  
# <============================================  FEATURE ENGINEERING ========================================================> 
# <==========================================================================================================================>

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

# <=========================================================================================================================>  
# <============================================ SUPERVISED LEARNING MODEL ===================================================> 
# <==========================================================================================================================>

#================================================ create_base_models ========================================================  

def create_base_models():
    
    '''Create base line models
    ARG: 
    None
    
    RETURNS:
    models(list): list containing base line models'''
    
    seed = 42
    
    models = []
    models.append(('Lasso', Lasso()))
    models.append(('Ridge', Ridge()))
    models.append(('ElasticNet', ElasticNet()))
    models.append(('RandromForest', RandomForestRegressor(random_state = seed)))
    models.append(('GradientBoost', GradientBoostingRegressor(random_state = seed)))
    models.append(('BagginRegressor', BaggingRegressor(random_state = seed)))
    models.append(('SVM' , SVR()))
    
    return models

#================================================ evaluate_models ========================================================== 


def evaluate_models(features, grades, models, learning_curve_ = False):
    ''' Evaluates models using X-Fold cross-validation. 
    Learning curve can also be plotted (optional).

    Args:
        features (dataframe) - dataset to be used for training.
        response (dataframe) - target variable
        models (list) - list of models to evaluated.
        curve (bool) - whether or not to plot learning curve.

    Returns:
        names (list) - list of models tested.
        results (list) - list of results for each model.
    '''  
    
    results = []
    names = []
    
    for name, model in models:
        cv_results = cross_val_score(model, 
                                    features,grades,
                                    cv = 10,
                                    scoring = 'neg_mean_squared_error',
                                    n_jobs = -1 )
        
        rmse = np.sqrt(-cv_results)
        rmse_score = np.round(np.mean(rmse),2)
        rmse_std = np.round(np.std(rmse),2)
        
        results.append(rmse_score)
        names.append(name)
        
        print()
        print('RMSE score for {} is {} with std of {}'.format(name, rmse_score, rmse_std))
        
        if learning_curve_:
            plot_learning_curve(features, grades, model, name)
            
            
    return names, results
    
#================================================ plot_learning_curve ==========================================================
    
def plot_learning_curve(features, grades, model, name):
    '''Plot learning curve curve of each model
    
    ARG: 
    features(datafame): dataframe with the features of the model
    grades(Serie): Serie with the target values
    model(string): model to be performed 
    name(string): name of the model
    
    RETURNS:
        none '''

    #for name, model in models:
    train_sizes, train_scores, test_scores = learning_curve(model,
                                                            features,
                                                            grades, 
                                                            cv = 10,
                                                            scoring = 'neg_mean_squared_error',
                                                            n_jobs =-1,
                                                            train_sizes = np.linspace(0.1, 1.0, 10)) 
 
    plt.grid()

    # Create means and standard deviations of training set score
    train_scores_mean = np.mean(train_scores, axis = 1)
    rmse_train = np.sqrt(-train_scores_mean)
    rmse_train_std = np.std(rmse_train)
    #train_std = np.std(train_scores, axis = 1)


    # Create means and standard deviations of test set score
    test_scores_mean = np.mean(test_scores, axis = 1)
    rmse_test = np.sqrt(-test_scores_mean)
    rmse_test_std = np.std(rmse_test)


    #test_std = np.std(test_scores, axis = 1)

    #Draw curve
    plt.plot(np.linspace(.1, 1.0, 10)*100, rmse_train, 'o-', color = "#111111",  label = 'training score')
    plt.plot(np.linspace(.1, 1.0, 10)*100, rmse_test,'o-', color = "blue", label ='cros-validation score' )

    #Draw bands

    plt.fill_between(np.linspace(.1, 1.0, 10)*100, rmse_train - rmse_train_std, rmse_train + rmse_train_std, color="#DDDDDD")
    plt.fill_between(np.linspace(.1, 1.0, 10)*100, rmse_test - rmse_test_std, rmse_test + rmse_test_std, color="#DDDDDD")


    # Plot
    plt.title('Learning Curve for {} model'.format(name))
    plt.xlabel('% of training set')
    plt.ylabel('RMS')
    #plt.yticks(np.arange(0.45, 1.02, 0.05))
    plt.xticks(np.arange(0., 100.05, 10))
    plt.legend(loc = 'best')
    plt.tight_layout()
    plt.show()
    print()
    
    
#================================================ f_regression_featue_selection ==========================================================




def f_regression_featue_selection( features,grades, num_features, display_df = False):
    '''Select features by calculating the correlation between each regressor and the target variable,
    than converting to an F score then to a p-value
    
    ARG:
    df(dataframe) : dataframe in which the test will be performed
    num_features(integer): number of top features to be selected
    
    RETURNS:
    score_df(dataframe): dataframe with the top score features
    
    '''
    from sklearn.feature_selection import SelectKBest
    from sklearn.feature_selection import f_regression
    
    k_best = SelectKBest(score_func = f_regression, k = num_features)

    k_best.fit(features, grades )
    
    
    print('Top {} features:'.format(num_features))
    print()
    feature_scores = pd.Series(data = k_best.scores_ , index = features.columns)
    feature_scores.nlargest(num_features).plot(kind = 'barh', figsize = (8,6))
    plt.ylabel('features')
    plt.xlabel('Scores')
    plt.title('Feature Scores X Feature names')

    score_df = pd.DataFrame(data = k_best.scores_, index = features.columns, columns =['Score']).iloc[:num_features]
    
    if display_df:
        display(score_df)
        print()
        
    
    reduced_df = features.loc[:,list(score_df.index)]
    
    return reduced_df
    
#=============================================================== scaler ==================================================================  
def scaler(scaler_type):
    
    
    ''' Creates machine learning pipelines with a specific type of scaler(whether MinMaxScaler or StandardScaler)
    ARG:
    scaler_type(string): name of scaler
    RETURNS:
    pip(pipelone): pipe line object created
    
    '''
    
    if scaler_type == 'standard':
        scaler = StandardScaler()
    elif scaler_type == 'minmax':
        scaler = MinMaxScaler()
        
    seed = 42
        
    pip = []
    pip.append((scaler_type+'_Lasso', Pipeline([('Scaler',scaler),('Lasso', Lasso())])))
    pip.append((scaler_type+'_Ridge', Pipeline([('Scaler',scaler),('Ridge', Ridge())])))
    pip.append((scaler_type+'_ElasticNet', Pipeline([('Scaler',scaler),('ElasticNet', ElasticNet())])))
    pip.append((scaler_type+'_RandromForest', Pipeline([('Scaler',scaler),('RandromForest', RandomForestRegressor(random_state = seed))])))
    pip.append((scaler_type+'_GradientBoost', Pipeline([('Scaler',scaler),('GradientBoost', GradientBoostingRegressor(random_state = seed))])))
    pip.append((scaler_type+'_BagginRegressor', Pipeline([('Scaler',scaler),('BagginRegressor', BaggingRegressor(random_state = seed))])))
    pip.append((scaler_type+'_SVM', Pipeline([('Scaler',scaler),('SVM', SVR())])))

    
    
    return pip

#=============================================================== df_scores ==================================================================  

def df_scores(names, results):
    
    '''Creates dataframe that display the name of the models and their comrresponding score
    ARG:
    names(list): list with model names
    results(list): list with scores of the models
    
    RETURNS:
    df(dataframe): dataframe with model names and their scores'''
    
    df_dict = {'Model_name':names,
              'Score':results}
    df = pd.DataFrame(df_dict)
    
    return df


#=============================================================== scaler ==================================================================  