import pandas as pd
import numpy as np


from sklearn.base import BaseEstimator, TransformerMixin



class IncidentPreprocessor(BaseEstimator, TransformerMixin):
    """Custom Preprocessing Estimator for the custom case
    
    """
    
    def __init___(self):
        pass
    
    def transform(self, df):

        exceptionTypes  =  {'spanning tree event': 0, 'NA': 1, 'JDBC-connection-permit-failure': 2, '[AWGenericException: java.lang.IllegalStateException, Export-webservice-ConnectionTimeout]': 3, '[ScheduledTsak-ArchesBatchPublishInThisRealm-Failure, Arches Schema version mismatch]': 4, '[OutOfMemoryException, GT Nodes restarting]': 5} 

        cloudHealthValues  =  {'FAIR': 0, 'GOOD': 1, 'POOR': 2, 'NA': 3, 'CRITICAL': 4} 

        features_vars  =  ['Date', 'AvgBackgroundQ', 'AvgThreadPoolSize', 'AvgWorkflowQ', 'CatalogSearchTime', 'IncreasingBGQueueTrend', 
                           'IncreasingThreadTrend', 'IncreasingWFQueueTrend', 'Exception', 'LogSizeVolumePercent', 'NetworkConnectivitySNV-US1', 
                           'IsProductReleased', 'UiNodeThreadsCount', 'CloudHealthIndex'] 
        
        df = df[features_vars]
        
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

        df.replace({'CloudHealthIndex': cloudHealthValues}, inplace=True)
        df.replace({'Exception': exceptionTypes}, inplace=True)
        
        df = df[df.columns.drop(['Date'])]
        return df  #.as_matrix()
    
    def fit(self, df, y=None, **fit_params):
        
        return self;
 