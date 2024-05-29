import pandas as pd
import math
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn import metrics
from blog.models import NeuralNetworkData, ModelMetrics

def initialize_model():
    from sklearn.ensemble import GradientBoostingRegressor
    return GradientBoostingRegressor(
        n_estimators=5000, learning_rate=0.05,
        max_depth=4, max_features='sqrt',
        min_samples_leaf=15, min_samples_split=10,
        loss='huber', random_state=5
    )

def train_and_predict():
    data = list(NeuralNetworkData.objects.all().values('price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot',
                                                       'floors', 'waterfront', 'view', 'condition', 'sqft_above',
                                                       'sqft_basement', 'yr_built', 'yr_renovated', 'city', 'statezip'))
    df = pd.DataFrame(data)


    df['city'] = df['city'].astype('category').cat.codes
    df = df.drop(columns=['statezip'])

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

    # Сохранение метрик в MongoDB
    ModelMetrics(mae=mae, mse=mse, rmse=rmse).save()

    return mae, mse, rmse
