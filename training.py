import pandas as pd
import numpy as np


from sklearn.base import BaseEstimator, TransformerMixin



class Preprocessor(BaseEstimator, TransformerMixin):
    """Custom Preprocessing Estimator for the custom case
    
    """
    
    def __init___(self):
        pass
    
    def transform(self, df):
        
        pred_vars = ['AvgBackgroundQ', 'AvgThreadPoolSize', 'AvgWorkflowQ',
       'CatalogSearchTime', 'CloudHealthIndex', 'Date', 'IsProductReleased',
        'LogSizeVolumePercent', 'NetworkConnectivitySNV-US1', 'UiNodeThreadsCount']
        
        df = df[pred_vars]
        
        # Make all negative values to NaN so that it can be replaced with single value
        df['AvgBackgroundQ'][df['AvgBackgroundQ'] < 1] = np.NAN
        df['AvgThreadPoolSize'][df['AvgThreadPoolSize'] < 1] = np.NAN
        df['AvgWorkflowQ'][df['AvgWorkflowQ'] < 1] = np.NAN
        df['CatalogSearchTime'][df['CatalogSearchTime'] < 1] = np.NAN
        df['UiNodeThreadsCount'][df['UiNodeThreadsCount'] < 1] = np.NAN
        
        df = df.fillna(-999)
        
        df1 = df.apply(lambda rec : pd.Series({'Day' : rec['Date'].day, 
                      'Month' : rec['Date'].month, 
                      'Year' :  rec['Date'].year,
                      'Hour' : rec['Date'].hour, 
                      'Minute' : rec['Date'].minute, 
                      'Second' :  rec['Date'].second,
                      'DayOfYear' : rec['Date'].dayofyear, 
                      'DayOfWeek' : rec['Date'].dayofweek, 
                      'WeekOfYear' :  rec['Date'].weekofyear,
                      'WeekOfYear' : rec['Date'].weekofyear, 
                      'Quarter' : rec['Date'].quarter,
                      'IsWeekend' : int(rec['Date'].dayofweek > 4), 
                      'IsMonthStart' : int(rec['Date'].is_month_start),
                      'IsMonthEnd' :  int(rec['Date'].is_month_end)
                     }), axis = 1)
        
        df = pd.concat([df, df1], axis=1)
        
        cloudHealthValues = {'FAIR' : 0, 'GOOD' : 1, 'CRITICAL' : 2}

        df.replace({'CloudHealthIndex': cloudHealthValues}, inplace=True)
        
        df = df[df.columns.drop(['Date'])]
        return df  #.as_matrix()
    
    def fit(self, df, y=None, **fit_params):
        
        return self;
  