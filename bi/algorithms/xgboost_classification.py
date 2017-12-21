import xgboost as xgb
import operator

from bi.algorithms import utils as MLUtils
from bi.common import utils as CommonUtils



class XgboostClassifier:
    def __init__(self, data_frame, data_frame_helper, spark):
        # self._spark = spark
        # self.data_frame = data_frame.toPandas()
        # self._measure_columns = data_frame_helper.get_numeric_columns()
        # self._dimension_columns = data_frame_helper.get_string_columns()
        # self.classifier = initiate_forest_classifier(10,5)
        print "XGBOOST INITIALIZATION DONE"

    def initiate_xgboost_classifier(self):
        general_params = {"booster":"gbtree","silent":0,"nthread":2}
        booster_params = {"eta":0.3,}
        task_params = {}
        clf = xgb.XGBClassifier()
        return clf

    def train_and_predict(self,x_train, x_test, y_train, y_test,clf,drop_cols):
        """
        Output is a dictionary
        y_prob => Array probability values for prediction
        feature_importance => features ranked by their Importance
        feature_Weight => weight of features
        """
        if len(drop_cols) > 0:
            x_train = drop_columns(x_train,drop_cols)
            x_test = drop_columns(x_test,drop_cols)
        clf = clf.fit(x_train, y_train)
        y_score = clf.predict(x_test)
        y_prob = clf.predict_proba(x_test)
        y_prob = [0]*len(y_score)

        feature_importance = dict(sorted(zip(x_train.columns,clf.feature_importances_),key=lambda x: x[1],reverse=True))
        for k, v in feature_importance.iteritems():
            feature_importance[k] = CommonUtils.round_sig(v)
        return {"trained_model":clf,"actual":y_test,"predicted":y_score,"probability":y_prob,"feature_importance":feature_importance,"featureList":list(x_train.columns)}

    def predict(self,x_test,trained_model,drop_cols):
        """
        """
        if len(drop_cols) > 0:
            x_test = MLUtils.drop_columns(x_test,drop_cols)
        y_score = trained_model.predict(x_test)
        y_prob = trained_model.predict_proba(x_test)
        x_test['responded'] = y_score
        y_prob = MLUtils.calculate_predicted_probability(y_prob)
        return {"predicted_class":y_score,"predicted_probability":y_prob}
