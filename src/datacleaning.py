# Returns a dataframe from a csv 
import pandas as pd
def get_data(path):
    return pd.read_csv(path)

# Splits the dataframe into test and training data to prevent data leakage.
# Returns a tuple of length 4, corresponding [0:4] to X_train, X_test, y_train, y_test
# The default test size is 20%, and the default seed is 69 for test consistency
from sklearn.model_selection import train_test_split
def test_split(df, test=0.2, seed=69):
    y = df.price
    X = df.drop(columns = ['price'])
    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size = test,
                                                        random_state = seed)
    return (X_train, X_test, y_train, y_test)

# Imputes missing values, drops unused columns, changes date's object to datetime
# Creates yard/ratio_15/years_old columns and dummy columns for condition
def clean_it(df):
    df.date = pd.to_datetime(df.date)
    df.waterfront = df.waterfront.fillna(value = 0)
    
    df.yr_renovated.fillna(0,
                           inplace = True) # Imputes 0 for NaN
    df['has_been_renovated'] = [1
                                if x != 0
                                else 0
                                for x in df.yr_renovated] # Feature engineered
                                                          # Has been renovated
    df.drop(columns = ['view',
                       'lat',
                       'long',
                       'zipcode',
                       'sqft_basement',
                       'yr_renovated'],
            inplace = True)
    
    df['ratio_15'] = df.sqft_living/df.sqft_living15
    df['years_old'] = 2020 - df.yr_built
    s = pd.get_dummies(df.condition,
                       drop_first = True,
                       prefix = 'condition')
    df = pd.concat([df, s],
                   axis = 1)
    df = df.drop(columns = ['condition'])
    return df