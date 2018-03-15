CHISQUARELEVELLIMIT = 10
CHISQUARESIGNIFICANTDIMENSIONTOSHOW = 8

DECISIONTREERKMEANSTARGETNAME = ['Low','Medium','High']
HDFS_SECRET_KEY = "xfBmEcr_hFHGqVrTo2gMFpER3ks9x841UcvJbEQJesI="
ALGORITHMRANDOMSLUG = "f77631ce2ab24cf78c55bb6a5fce4db8"
ANOVAMAXLEVEL = 200
BLOCKSPLITTER = "|~NEWBLOCK~|"
BASEFOLDERNAME_MODELS = "mAdvisorModels"
BASEFOLDERNAME_SCORES = "mAdvisorScores"
PROBABILITY_RANGE_FOR_DONUT_CHART = {"50-60%":(50,60),"60-70%":(60,70),"70-80%":(70,80),"80-90%":(80,90),"90-100%":(90,100)}

PYSPARK_ML_LINEAR_REGRESSION_PARAMS = [
                {
                    "name":"maxIter",
                    "displayName":"Maximum Iteration",
                    "defaultValue":100,
                    "acceptedValue":None,
                    "valueRange":[1,200],
                    "paramType":"number",
                    "uiElemType":"slider"
                },
                {
                    "name":"regParam",
                    "displayName":"Regularization parameter",
                    "defaultValue":0.0,
                    "acceptedValue":None,
                    "valueRange":[0.0,1.0],
                    "paramType":"number",
                    "uiElemType":"slider"
                },
                {
                    "name":"elasticNetParam",
                    "displayName":"Elastic Net Param",
                    "defaultValue":0.0,
                    "acceptedValue":None,
                    "valueRange":[0.0,1.0],
                    "paramType":"number",
                    "uiElemType":"slider"
                },
                {
                    "name":"tol",
                    "displayName":"Convergence tolerance of iterations(e^-n)",
                    "defaultValue":6,
                    "acceptedValue":None,
                    "valueRange":[3,10],
                    "paramType":"number",
                    "uiElemType":"slider"
                },
                {
                     "name":"fitIntercept",
                     "displayName":"Fit Intercept",
                     "defaultValue":True,
                     "acceptedValue":None,
                     "paramType":"boolean",
                     "uiElemType":"checkbox"
                 },
                 {
                      "name":"standardization",
                      "displayName":"Standardization",
                      "defaultValue":True,
                      "acceptedValue":None,
                      "paramType":"boolean",
                      "uiElemType":"checkbox"
                  },
                  {
                       "name":"standardization",
                       "displayName":"Standardization",
                       "defaultValue":True,
                       "acceptedValue":None,
                       "paramType":"boolean",
                       "uiElemType":"checkbox"
                   },
                   {
                       "name":"solver",
                       "displayName":"Solver",
                       "defaultValue":[
                        {
                            "name":"l-bfgs",
                            "selected":False,
                            "displayName":"Limited-memory BFGS"
                        },
                        {
                            "name":"auto",
                            "selected":True,
                            "displayName":"Automatic Selection"
                        },
                        {
                            "name":"normal",
                            "selected":False,
                            "displayName":"Normal"
                        }
                       ],
                       "paramType":"list",
                       "uiElemType":"checkbox"
                   },
                {
                    "name":"aggregationDepth",
                    "displayName":"Aggregation Depth",
                    "defaultValue":2,
                    "acceptedValue":None,
                    "valueRange":[2,5],
                    "paramType":"number",
                    "uiElemType":"checkbox"
                },
                ]
PYSPARK_ML_GBT_REGRESSION_PARAMS = [
                {
                    "name":"maxIter",
                    "displayName":"Maximum Iteration",
                    "defaultValue":20,
                    "acceptedValue":None,
                    "valueRange":[1,100],
                    "paramType":"number",
                    "uiElemType":"slider"
                },
                {
                    "name":"maxDepth",
                    "displayName":"Depth Of Trees",
                    "defaultValue":5,
                    "acceptedValue":None,
                    "valueRange":[2,20],
                    "paramType":"number",
                    "uiElemType":"slider"
                },
                {
                    "name":"maxBins",
                    "displayName":"Maximum Number Of Bins",
                    "defaultValue":32,
                    "acceptedValue":None,
                    "valueRange":[16,128],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "powerOf2":True
                },
                {
                    "name":"checkpointInterval",
                    "displayName":"Check Point Interval",
                    "defaultValue":10,
                    "acceptedValue":None,
                    "valueRange":[10,20],
                    "paramType":"number",
                    "uiElemType":"slider"
                },
                {
                    "name":"minInstancesPerNode",
                    "displayName":"Minimum Instances Per Node",
                    "defaultValue":1,
                    "acceptedValue":None,
                    "valueRange":[1,10],
                    "paramType":"number",
                    "uiElemType":"slider"
                },
                {
                    "name":"subsamplingRate",
                    "displayName":"Sub Sampling Rate",
                    "defaultValue":1.0,
                    "acceptedValue":None,
                    "valueRange":[0.0,1.0],
                    "paramType":"number",
                    "uiElemType":"slider"
                },
                {
                    "name":"minInfoGain",
                    "displayName":"Minimum Info Gain",
                    "defaultValue":0.0,
                    "acceptedValue":None,
                    "valueRange":[0.0,1.0],
                    "paramType":"number",
                    "uiElemType":"slider"
                },
                {
                    "name":"maxMemoryInMB",
                    "displayName":"Maximum Memory Available",
                    "defaultValue":256,
                    "acceptedValue":None,
                    "valueRange":[128,10240],
                    "paramType":"number",
                    "uiElemType":"slider"
                },
                {
                     "name":"cacheNodeIds",
                     "displayName":"Cache Node Ids",
                     "defaultValue":False,
                     "acceptedValue":None,
                     "paramType":"boolean",
                     "uiElemType":"checkbox"
                 },
               {
                   "name":"lossType",
                   "displayName":"Loss Type",
                   "defaultValue":[
                    {
                        "name":"squared",
                        "selected":True,
                        "displayName":"Squared Loss"
                    },
                    {
                        "name":"absolute",
                        "selected":False,
                        "displayName":"Huber Loss"
                    }
                   ],
                   "paramType":"list",
                   "uiElemType":"checkbox"
               },
               {
                   "name":"impuriy",
                   "displayName":"Impurity Index",
                   "defaultValue":[
                    {
                        "name":"variance",
                        "selected":True,
                        "displayName":"Variance"
                    }
                   ],
                   "paramType":"list",
                   "uiElemType":"checkbox"
               },
                ]
DEFAULT_VALIDATION_OBJECT = {
         "name":"trainAndtest",
         "displayName":"Train and Test",
         "value":0.7
       }

APPS_ID_MAP = {
  '11': {
    'displayName': 'Asset Health Prediction',
    'type': 'CLASSIFICATION',
    'name': 'asset_health_prediction',
    'heading': 'Factors influencing Asset Health'
  },
  '10': {
    'displayName': 'Claims Prediction',
    'type': 'CLASSIFICATION',
    'name': 'claims_prediction',
    'heading': 'Factors influencing Claims'
  },
  '13': {
    'displayName': 'Automated Prediction',
    'type': 'REGRESSION',
    'name': 'regression_app',
    'heading': 'Feature Importance'
  },
  '12': {
    'displayName': 'Employee Attrition',
    'type': 'CLASSIFICATION',
    'name': 'employee_attrition',
    'heading': 'Factors influencing Attrition'
  },
  '1': {
    'displayName': 'Opportunity Scoring',
    'type': 'CLASSIFICATION',
    'name': 'opportunity_scoring',
    'heading': 'Factors influencing Opportunity Score'
  },
  '3': {
    'displayName': 'Robo Advisor',
    'type': 'ROBO',
    'name': 'robo_advisor_insights',
    'heading': None
  },
  '2': {
    'displayName': 'Automated Prediction',
    'type': 'CLASSIFICATION',
    'name': 'automated_prediction',
    'heading': 'Feature Importance'
  },
  '5': {
    'displayName': 'Stock Sense',
    'type': 'STOCK_SENSE',
    'name': 'stock_sense',
    'heading': None
  },
  '4': {
    'displayName': 'Speech Analytics',
    'type': 'SPEECH',
    'name': 'speech_analytics',
    'heading': None
  },
  '7': {
    'displayName': 'Re-admission Prediction',
    'type': 'CLASSIFICATION',
    'name': 're_admission_prediction',
    'heading': 'Factors influencing Re-admission'
  },
  '6': {
    'displayName': 'Churn Prediction',
    'type': 'CLASSIFICATION',
    'name': 'churn_prediction',
    'heading': 'Factors influencing Churn'
  },
  '9': {
    'displayName': 'Credit Card Fraud',
    'type': 'CLASSIFICATION',
    'name': 'credit_card_fraud',
    'heading': 'Factors influencing Fraud'
  },
  '8': {
    'displayName': 'Physician Attrition',
    'type': 'CLASSIFICATION',
    'name': 'physician_attrition',
    'heading': 'Factors influencing Attrition'
  }
}


SLUG_MODEL_MAPPING = {
            ALGORITHMRANDOMSLUG+"rf":"randomforest",
            ALGORITHMRANDOMSLUG+"lr":"logisticregression",
            ALGORITHMRANDOMSLUG+"xgb":"xgboost",
            ALGORITHMRANDOMSLUG+"svm":"svm",
            ALGORITHMRANDOMSLUG+"linr":"linearregression",
            ALGORITHMRANDOMSLUG+"gbtr":"gbtregression"
            }
MODEL_SLUG_MAPPING = {
            "randomforest":ALGORITHMRANDOMSLUG+"rf",
            "logisticregression":ALGORITHMRANDOMSLUG+"lr",
            "xgboost":ALGORITHMRANDOMSLUG+"xgb",
            "svm":ALGORITHMRANDOMSLUG+"svm",
            "linearregression":ALGORITHMRANDOMSLUG+"linr",
            "gbtregression":ALGORITHMRANDOMSLUG+"gbtr"
            }

scriptsMapping = {
    "overview" : "Descriptive analysis",
    "performance" : "Measure vs. Dimension",
    "influencer" : "Measure vs. Measure",
    "prediction" : "Predictive modeling",
    "trend" : "Trend",
    "association" : "Dimension vs. Dimension"
}
measureAnalysisRelativeWeight = {
    "initialization":0.25,
    "Descriptive analysis":1,
    "Measure vs. Dimension":3,
    "Measure vs. Measure":3,
    "Trend":1.5,
    "Predictive modeling":1.5
}
dimensionAnalysisRelativeWeight = {
    "initialization":0.25,
    "Descriptive analysis":1,
    "Dimension vs. Dimension":4,
    "Trend":2.5,
    "Predictive modeling":2.5
}
mlModelTrainingWeight = {
    "initialization":{"total":10,"script":10,"narratives":10},
    "randomForest":{"total":30,"script":30,"narratives":30},
    "logisticRegression":{"total":30,"script":30,"narratives":30},
    "xgboost":{"total":30,"script":30,"narratives":30},
    "svm":{"total":30,"script":30,"narratives":30}
}
mlModelPredictionWeight = {
    "initialization":{"total":10,"script":10,"narratives":10},
    "randomForest":{"total":20,"script":20,"narratives":20},
    "logisticRegression":{"total":20,"script":20,"narratives":20},
    "xgboost":{"total":20,"script":20,"narratives":20},
    "svm":{"total":20,"script":20,"narratives":20},
    "Descriptive analysis":{"total":10,"script":10,"narratives":10},
    "Dimension vs. Dimension":{"total":10,"script":5,"narratives":5},
    "Predictive modeling":{"total":10,"script":5,"narratives":5}
}
metadataScriptWeight = {
    "initialization":{"total":3,"script":2,"narratives":1},
}
subsettingScriptWeight = {
    "initialization":{"total":3,"script":2,"narratives":1},
}
