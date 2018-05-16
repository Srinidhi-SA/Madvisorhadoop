import json
import math

from bi.common import ChartJson
from bi.common import NormalCard, NarrativesTree, HtmlData, C3ChartData
from bi.common import utils as CommonUtils
from bi.narratives import utils as NarrativesUtils
from bi.settings import setting as GLOBALSETTINGS
from chisquare import ChiSquareAnalysis
from bi.transformations import Binner

from pyspark.sql import SQLContext
from pyspark.sql.types import *

class ChiSquareNarratives:
    #@accepts(object, int, DFChiSquareResult ,ContextSetter)
    def __init__(self, df_helper, df_chisquare_result, spark, df_context, data_frame, story_narrative,result_setter,scriptWeight=None, analysisName=None):
        self._story_narrative = story_narrative
        self._result_setter = result_setter
        self._data_frame = data_frame
        self._dataframe_context = df_context
        self._dataframe_helper = df_helper
        self._storyOnScoredData = self._dataframe_context.get_story_on_scored_data()
        self._measure_columns = df_helper.get_numeric_columns()
        self._df_chisquare = df_chisquare_result
        self._df_chisquare_result = df_chisquare_result.get_result()
        self.narratives = {}
        self._appid = df_context.get_app_id()
        self._chiSquareNode = NarrativesTree()
        self._chiSquareNode.set_name("Association")
        self._blockSplitter = GLOBALSETTINGS.BLOCKSPLITTER
        self._noOfSigDimsToShow = GLOBALSETTINGS.CHISQUARESIGNIFICANTDIMENSIONTOSHOW
        self._base_dir = "/chisquare/"
        self._spark = spark
        
        print 'self._measure_columns'*100
        print self._measure_columns
        print self._data_frame
        ############################DataFrame Measure to Dimesion Column#####################
        
        pandas_df = self._data_frame.toPandas()
        
        target_dimension = self._df_chisquare_result.keys()
        print target_dimension

        bin_data = {}
        for col in self._measure_columns:
            chisquare_result = self._df_chisquare.get_chisquare_result(target_dimension[0],col)
            bin_data[col] = chisquare_result.get_contingency_table().get_column_two_levels()

        print bin_data
        for bin_col in bin_data.keys():
            for split in bin_data[bin_col]:
                val = split.split('to')
                pandas_df[bin_col][(pandas_df[bin_col]>=float(val[0].replace(',',''))) & (pandas_df[bin_col]<float(val[1].replace(',','')))] =  split

        fields = [StructField(field_name, StringType(), True) for field_name in pandas_df.columns]
        schema = StructType(fields)

        SQLctx = SQLContext(sparkContext=self._spark.sparkContext, sparkSession=self._spark)
        self._data_frame = SQLctx.createDataFrame(pandas_df,schema)
        print self._data_frame.show()
        ############################DataFrame Measure to Dimesion Column#####################

        if self._appid != None:
            if self._appid == "1":
                self._base_dir += "appid1/"
            elif self._appid == "2":
                self._base_dir += "appid2/"

        self._completionStatus = self._dataframe_context.get_completion_status()
        if analysisName == None:
            self._analysisName = self._dataframe_context.get_analysis_name()
        else:
            self._analysisName = analysisName

        self._messageURL = self._dataframe_context.get_message_url()
        if scriptWeight == None:
            self._scriptWeightDict = self._dataframe_context.get_dimension_analysis_weight()
        else:
            self._scriptWeightDict = scriptWeight
        self._analysisDict = self._dataframe_context.get_analysis_dict()
        if self._analysisDict != {}:
            self._nColsToUse = self._analysisDict[self._analysisName]["noOfColumnsToUse"]
        else:
            self._nColsToUse = None

        self._scriptStages = {
            "initialization":{
                "summary":"Initialized the Frequency Narratives",
                "weight":0
                },
            "summarygeneration":{
                "summary":"summary generation finished",
                "weight":10
                },
            "completion":{
                "summary":"Frequency Stats Narratives done",
                "weight":0
                },
            }
        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._analysisName,"initialization","info",display=False,weightKey="narratives")

        self._generate_narratives()

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._analysisName,"summarygeneration","info",display=False,weightKey="narratives")

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._analysisName,"completion","info",display=False,weightKey="narratives")

    def _generate_narratives(self):
        """
        generate main card narrative and remaining cards are generated by calling ChiSquareAnalysis class for each of analyzed dimensions
        """
        for target_dimension in self._df_chisquare_result.keys():
            target_chisquare_result = self._df_chisquare_result[target_dimension]
            analysed_variables = target_chisquare_result.keys()  ## List of all analyzed var.
            # List of significant var out of analyzed var.
            significant_variables = [dim for dim in target_chisquare_result.keys() if target_chisquare_result[dim].get_pvalue()<=0.05]   
            effect_sizes = [target_chisquare_result[dim].get_effect_size() for dim in significant_variables]

            effect_size_dict = dict(zip(significant_variables,effect_sizes))
            significant_variables = [y for (x,y) in sorted(zip(effect_sizes,significant_variables),reverse=True)]
            #insignificant_variables = [i for i in self._df_chisquare_result[target_dimension] if i['pv']>0.05]
 
            num_analysed_variables = len(analysed_variables)
            num_significant_variables = len(significant_variables)
            self.narratives['main_card']= {}
            self.narratives['main_card']['heading'] = 'Relationship between '+target_dimension+' and other factors'
            self.narratives['main_card']['paragraphs'] = {}
            data_dict = {
                          'num_variables' : num_analysed_variables,
                          'num_significant_variables' : num_significant_variables,
                          'significant_variables' : significant_variables,
                          'target' : target_dimension,
                          'analysed_dimensions': analysed_variables,
                          'blockSplitter':self._blockSplitter
            } # for both para 1 and para 2
            paragraph={}
            paragraph['header'] = ''

            paragraph['content'] = NarrativesUtils.get_template_output(self._base_dir,'main_card.html',data_dict)
            self.narratives['main_card']['paragraphs']=[paragraph]
            self.narratives['cards'] = []
            chart = {'header':'Strength of association between '+target_dimension+' and other dimensions'}
            chart['data'] = effect_size_dict
            chart['label_text']={'x':'Dimensions',
                                'y':'Effect Size (Cramers-V)'}

            chart_data = []
            chartDataValues = []
            for k,v in effect_size_dict.items():
                chart_data.append({"key":k,"value":float(v)})
                chartDataValues.append(float(v))
            chart_data = sorted(chart_data,key=lambda x:x["value"],reverse=True)
            chart_json = ChartJson()
            chart_json.set_data(chart_data)
            chart_json.set_chart_type("bar")
            # chart_json.set_label_text({'x':'Dimensions','y':'Effect Size (Cramers-V)'})
            chart_json.set_label_text({'x':'  ','y':'Effect Size (Cramers-V)'})
            chart_json.set_axis_rotation(True)
            chart_json.set_axes({"x":"key","y":"value"})
            # chart_json.set_yaxis_number_format(".4f")
            chart_json.set_yaxis_number_format(NarrativesUtils.select_y_axis_format(chartDataValues))
            self.narratives['main_card']['chart']=chart


            main_card = NormalCard()
            header = "<h3>Strength of association between "+target_dimension+" and other dimensions</h3>"
            main_card_data = [HtmlData(data=header)]
            main_card_narrative = NarrativesUtils.get_template_output(self._base_dir,'main_card.html',data_dict)
            main_card_narrative = NarrativesUtils.block_splitter(main_card_narrative,self._blockSplitter)
            main_card_data += main_card_narrative
            # st_info = ["Test : Chi Square", "Threshold for p-value : 0.05", "Effect Size : Cramer's V"]
            # print "chartdata",chart_data
            if len(chart_data) > 0:
                statistical_info_array=[
                    ("Test Type","Chi-Square"),
                    ("Effect Size","Cramer's V"),
                    ("Max Effect Size",chart_data[0]["key"]),
                    ("Min Effect Size",chart_data[-1]["key"]),
                    ]
                statistical_inferenc = ""
                if len(chart_data) == 1:
                    statistical_inference = "{} is the only variable that have significant association with the {} (Target) having an \
                     Effect size of {}".format(chart_data[0]["key"],self._dataframe_context.get_result_column(),round(chart_data[0]["value"],4))
                elif len(chart_data) == 2:
                    statistical_inference = "There are two variables ({} and {}) that have significant association with the {} (Target) and the \
                     Effect size ranges are {} and {} respectively".format(chart_data[0]["key"],chart_data[1]["key"],self._dataframe_context.get_result_column(),round(chart_data[0]["value"],4),round(chart_data[1]["value"],4))
                else:
                    statistical_inference = "There are {} variables that have significant association with the {} (Target) and the \
                     Effect size ranges from {} to {}".format(len(chart_data),self._dataframe_context.get_result_column(),round(chart_data[0]["value"],4),round(chart_data[-1]["value"],4))
                if statistical_inference != "":
                    statistical_info_array.append(("Inference",statistical_inference))
                statistical_info_array = NarrativesUtils.statistical_info_array_formatter(statistical_info_array)
            else:
                statistical_info_array = []
            main_card_data.append(C3ChartData(data=chart_json,info=statistical_info_array))
            main_card.set_card_data(main_card_data)
            main_card.set_card_name("Key Influencers")

            if self._storyOnScoredData != True:
                self._chiSquareNode.add_a_card(main_card)
                self._result_setter.add_a_score_chi_card(main_card)

            print "target_dimension",target_dimension
            if self._appid=='2' and num_significant_variables>5:
                significant_variables = significant_variables[:5]
            else:
                if self._nColsToUse != None:
                    significant_variables = significant_variables[:self._nColsToUse]

            CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._analysisName,"custom","info",display=True,customMsg="Analyzing key drivers",weightKey="narratives")
            for analysed_dimension in significant_variables[:self._noOfSigDimsToShow]:
                chisquare_result = self._df_chisquare.get_chisquare_result(target_dimension,analysed_dimension)
                if self._appid=='2':
                    print "APPID 2 is used"
                    card = ChiSquareAnalysis(self._dataframe_context,self._dataframe_helper,chisquare_result, target_dimension, analysed_dimension, significant_variables, num_analysed_variables, self._data_frame, self._measure_columns, self._base_dir,None,target_chisquare_result)
                    # self.narratives['cards'].append(card)
                    self._result_setter.add_a_score_chi_card(json.loads(CommonUtils.convert_python_object_to_json(card.get_dimension_card1())))

                elif self._appid=='1':
                    print "APPID 1 is used"
                    card = ChiSquareAnalysis(self._dataframe_context,self._dataframe_helper,chisquare_result, target_dimension, analysed_dimension, significant_variables, num_analysed_variables, self._data_frame, self._measure_columns,self._base_dir, None,target_chisquare_result)
                    # self.narratives['cards'].append(card)
                    self._result_setter.add_a_score_chi_card(json.loads(CommonUtils.convert_python_object_to_json(card.get_dimension_card1())))
                else:
                    target_dimension_card = ChiSquareAnalysis(self._dataframe_context,self._dataframe_helper,chisquare_result, target_dimension, analysed_dimension, significant_variables, num_analysed_variables, self._data_frame, self._measure_columns,self._base_dir, None,target_chisquare_result)
                    self.narratives['cards'].append(target_dimension_card)
                    self._chiSquareNode.add_a_node(target_dimension_card.get_dimension_node())
        self._story_narrative.add_a_node(self._chiSquareNode)
        self._result_setter.set_chisquare_node(self._chiSquareNode)
