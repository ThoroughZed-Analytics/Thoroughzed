import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LassoCV
from meta_data_query_and_loop_script import get_horse_data


def predict_horse_price(horse):
    '''
    Takes a horse id (INTEGER) and returns a predicted price (USD) based on a linear regression model.
    :param horse:
    :return:
    '''

    if type(horse) != int:
        raise ValueError('Please input an integer')

    # import data
    clean_market_data = pd.read_csv('master_db_no_outliers.csv')

    # drop rows where price is NA
    clean_market_data = clean_market_data[~pd.isna(clean_market_data['converted_price'])]

    # clean the dataset to only include desired predictors and separate out the X and y
    # X will only have continuous variables for now

    X = clean_market_data.drop(columns=['Unnamed: 0.1', 'converted_price', 'time_sold', 'horse_id', 'birthday', 'horse_id', 'mother', 'father', 'z_score', 'day_sold', 'bloodline', 'breed_type', 'color', 'genotype', 'horse_type', 'super_coat', 'Unnamed: 0'])

    y = clean_market_data.converted_price

    # Define the model
    model = LinearRegression()
    model.set_params(**{'fit_intercept': True, 'positive': False})

    # set up model train and test splits
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=156, test_size=0.2, shuffle=True)

    # fit model using LassoCV for feature selection
    # Create an instance of LassoCV
    lasso = LassoCV(cv=5)

    # Fit the LassoCV model to the data
    lasso.fit(X_train, y_train)

    # make a call to horse data api
    horse_id = horse

    # handle if horse is in our db or in the marketplace
    if horse_id in clean_market_data['horse_id'].values:
        horse_to_predict = clean_market_data[clean_market_data['horse_id'] == horse_id]
        print("was in database")
    else:
        horse_to_predict = get_horse_data(horse_id)

    # set up categories to filter metadata to what we need
    categories = ['free_win_rate', 'paid_win_rate', 'place','total_paid', 'win_rate', 'overall.first', 'overall.races', 'overall.second', 'overall.third']

    horse_to_predict = horse_to_predict.filter(categories)
    horse_to_predict = horse_to_predict.values.reshape(1,-1)
    prediction_test = lasso.predict(horse_to_predict)
    return prediction_test
