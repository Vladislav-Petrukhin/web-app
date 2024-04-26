import pandas as pd
import numpy as np
import math
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn import metrics

def initialize_model():
    from sklearn.ensemble import GradientBoostingRegressor
    GBoost = GradientBoostingRegressor(
        n_estimators=5000, learning_rate=0.05,
        max_depth=4, max_features='sqrt',
        min_samples_leaf=15, min_samples_split=10,
        loss='huber', random_state=5
    )
    return GBoost


def train_and_predict():
    from sqlalchemy import create_engine
    username = 'root'
    password = 'admin'
    database = 'hh'
    table_name = 'db_neural_network'
    engine = create_engine(f'mysql+pymysql://{username}:{password}@db/{database}')
    df = pd.read_sql_table(table_name, engine)

    df.drop(df.columns[[0, 14, 16, 17]], axis=1, inplace=True)
    df['city'] = df['city'].map({
        'Shoreline': 0, 'Seattle': 1, 'Kent': 2, 'Bellevue': 3, 'Redmond': 4, 'Maple Valley': 5, 'North Bend': 6,
        'Lake Forest Park': 7, 'Sammamish': 8, 'Auburn': 9, 'Des Moines': 10, 'Bothell': 11, 'Federal Way': 12,
        'Kirkland': 13, 'Issaquah': 14, 'Woodinville': 15, 'Normandy Park': 16, 'Fall City': 17, 'Renton': 18,
        'Carnation': 19, 'Snoqualmie': 20, 'Duvall': 21, 'Burien': 22, 'Covington': 23, 'Inglewood-Finn Hill': 24,
        'Kenmore': 25, 'Newcastle': 26, 'Mercer Island': 27, 'Black Diamond': 28, 'Ravensdale': 29, 'Clyde Hill': 30,
        'Algona': 31, 'Skykomish': 32, 'Tukwila': 33, 'Vashon': 34, 'Yarrow Point': 35, 'SeaTac': 36, 'Medina': 37,
        'Enumclaw': 38, 'Snoqualmie Pass': 39, 'Pacific': 40, 'Beaux Arts Village': 41, 'Preston': 42, 'Milton': 43
    })
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    df = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]

    x = df.drop('price', axis=1)
    y = df['price']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=40)
    model = initialize_model()
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    rmse = math.sqrt(mean_squared_error(y_test, predictions))

    mae = metrics.mean_absolute_error(y_test, predictions)
    mse = metrics.mean_squared_error(y_test, predictions)

    return mae, mse, rmse