from pyspark.sql import DataFrame
from pyspark.sql import functions as FN
from pyspark.sql.functions import UserDefinedFunction
from pyspark.sql import SQLContext

from bi.common.decorators import accepts
from bi.common import BIException
from bi.common import DataFrameHelper
from bi.common.datafilterer import DataFrameFilterer
from bi.common import utils

import time
import math
import random
import itertools
from datetime import datetime
from datetime import timedelta
from collections import Counter

import numpy as np
import pandas as pd
from statistics import mean,median,mode,pstdev

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer as DV
from sklearn import linear_model, cross_validation, grid_search
from sklearn.metrics import roc_curve, auc
from sklearn.feature_selection import RFECV
from bi.algorithms import utils as MLUtils



class RandomForest:
    def __init__(self, data_frame, data_frame_helper, spark):
        # self._spark = spark
        # self.data_frame = data_frame.toPandas()
        # self._measure_columns = data_frame_helper.get_numeric_columns()
        # self._dimension_columns = data_frame_helper.get_string_columns()
        # self.classifier = initiate_forest_classifier(10,5)
        print "RANDOM FOREST INITIALIZATION DONE"

    def initiate_forest_classifier(self,n_estimators,max_features):
        clf = RandomForestClassifier(n_estimators=n_estimators,
                                         max_features = max_features,
        #                                  max_depth=None,
                                         min_samples_split = 10,
        #                                  min_samples_leaf=1,
        #                                  min_weight_fraction_leaf=0,
                                         max_leaf_nodes=None,
                                         warm_start=True,
                                         random_state=0,
                                         n_jobs=-1,
        #                                  oob_score = True,
    #                                      verbose= True
                                    )

        return clf

    def predict(self,x_test,trained_model,drop_cols):
        """
        """
        if len(drop_cols) > 0:
            x_test = MLUtils.drop_columns(x_test,drop_cols)
        y_score = trained_model.predict(x_test)
        y_prob = trained_model.predict_proba(x_test)
        y_prob = MLUtils.calculate_predicted_probability(y_prob)
        x_test['responded'] = y_score
        return {"predicted_class":y_score,"predicted_probability":y_prob}

    def train_and_predict(self,x_train, x_test, y_train, y_test,clf,plot_flag,print_flag,drop_cols):
        """
        Output is a dictionary
        y_prob => Array probability values for prediction
        results => Array of predicted class
        feature_importance => features ranked by their Importance
        feature_Weight => weight of features
        """
        if len(drop_cols) > 0:
            x_train = drop_columns(x_train,drop_cols)
            x_test = drop_columns(x_test,drop_cols)

        clf.fit(x_train, y_train)
        y_score = clf.predict(x_test)
        y_prob = clf.predict_proba(x_test)
        results = pd.DataFrame({"actual":y_test,"predicted":y_score,"prob":list(y_prob)})
        importances = clf.feature_importances_
        importances = map(float,importances)
        feature_importance = clf.feature_importances_.argsort()[::-1]
        imp_cols = [x_train.columns[x] for x in feature_importance]
        feature_importance = dict(zip(imp_cols,importances))
        # if print_flag:
        #     print("Classification Table")
        #     print(pd.crosstab(results.actual, results.predicted, rownames=['actual'], colnames=['preds']))
        #
        # fpr = dict()
        # tpr = dict()
        # roc_auc = dict()
        #
        # fpr["response"], tpr["response"], _ = roc_curve(y_test, y_score)
        # roc_auc["response"] = auc(fpr["response"], tpr["response"])
        # if plot_flag == True:
        #     plt.figure()
        #     lw = 2
        #     plt.plot(fpr['response'], tpr['response'], color='darkorange',
        #              lw=lw, label='ROC curve (area = %0.2f)' % roc_auc['response'])
        #     plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        #     plt.xlim([0.0, 1.0])
        #     plt.ylim([0.0, 1.05])
        #     plt.xlabel('False Positive Rate')
        #     plt.ylabel('True Positive Rate')
        #     plt.title('ROC Curve')
        #     plt.legend(loc="lower right")
        #     plt.show()

        # return {"y_prob":y_prob,"results":results,"feature_importance":feature_importance,
                # "feature_weight":importances,"auc":roc_auc["response"],"trained_model":clf}
        return {"trained_model":clf,"actual":y_test,"predicted":y_score,"probability":y_prob,"feature_importance":feature_importance}