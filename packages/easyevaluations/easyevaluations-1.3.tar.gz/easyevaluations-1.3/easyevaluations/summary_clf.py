import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score

def summary_clf (y_true, y_pred):
    """
    This function prints a thorough overview of the performance of the classification algorithm that is being evaluated.
    
    :param y_true: the true test data with which the prediction will be compared
    :param y_pred: the prediction of the algorithm
    
    :returns: a thorough overview of the metrics of the respective algorithm. Includes a confusion matrix, f1, precision, recall,
              accuracy, fpr, roc_auc_score
    """
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    f1 = f1_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    accuracy = accuracy_score(y_true, y_pred)
    fpr = fp / (fp+tn)
    roc_score = roc_auc_score(y_true, y_pred)
    print(f"""
                                  TRUE CONDITION
                            
                         POSITIVE                    NEGATIVE
                    
  PREDICTED  POS      True Positive: {tp}   |  False Positive: {fp} 
             --------------------------------------------------------
  CONDITION  NEG      False Negative: {fn}  |  True  Negative: {tn}
 
Accuracy:    {round(accuracy*100,2)}%
Precision:   {round(precision*100,2)}%
Recall/TPR:  {round(recall*100,2)}%
F1 Score:    {round(f1*100,2)}%
FPR:         {round(fpr*100,2)}%
ROC score:   {round(roc_score*100,2)}%
    """)  