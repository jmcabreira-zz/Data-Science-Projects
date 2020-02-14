import pandas as pd 

import os 


'''
Helper functions 

'''

# Save csv file ( dataframes )
def save_csv(df, data_dir, filename):
        '''Saves all of the dataframes of the notebook
        :param df :  dataframe
        :param data_dir: The directory where files will be saved'''
        
    
        #make data_dir, if it does not exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

            
        df.to_csv(os.path.join(data_dir, filename), index= True, header = True)
        
        
        print('Path created: '+str(data_dir)+'/'+str(filename))