from numpy import sqrt
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import median_absolute_error
from sklearn.metrics import r2_score

def summary_reg (y_true, y_pred):
    """
    This function prints a thorough overview of the performance of the regression algorithm that is being evaluated 
    :param y_true: the true test data with which the prediction will be compared
    :param y_pred: the prediction of the algorithm
    :returns: a thorough overview of the metrics of the respective algorithm. Includes mean_absolute_error (MAE), mean_squared_error (MSE),
    root mean squared error (RMSE), mean_squared_log_error (MSLE), median_absolute_error (MedianAE)
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = sqrt(mean_squared_error(y_true, y_pred))
    msle = mean_squared_log_error(y_true, y_pred)
    medianae = median_absolute_error(y_true, y_pred)
    
    print(f"""
MAE:      {round(mae,4)}
MSE:      {round(mse,4)}
RMSE:     {round(rmse,4)}
MSLE:     {round(msle,4)}
MedianAE: {round(medianae,4)}
    """)  