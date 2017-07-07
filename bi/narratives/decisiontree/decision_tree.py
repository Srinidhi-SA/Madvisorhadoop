import os

from bi.common.dataframe import DataFrameHelper
from bi.common.results import DecisionTreeResult
from bi.common.utils import accepts
from bi.narratives import utils as NarrativesUtils


class DecisionTreeNarrative:
    MAX_FRACTION_DIGITS = 2

    def _get_new_table(self):
        for keys in self.table.keys():
            self.new_table[keys]={}
            self.new_table[keys]['rules'] = self.table[keys]
            self.new_table[keys]['probability'] = [round(i,2) for i in self.success_percent[keys]]

    @accepts(object, (str, basestring), DecisionTreeResult,DataFrameHelper)
    def __init__(self, column_name, decision_tree_rules,df_helper):
        self._column_name = column_name.lower()
        self._colname = column_name
        self._capitalized_column_name = "%s%s" % (column_name[0].upper(), column_name[1:])
        self._decision_rules_dict = decision_tree_rules.get_decision_rules()
        self.table = decision_tree_rules.get_table()
        self.new_table={}
        self.succesful_predictions=decision_tree_rules.get_success()
        self.total_predictions=decision_tree_rules.get_total()
        self.success_percent= decision_tree_rules.get_success_percent()
        self._get_new_table()
        self._df_helper = df_helper
        self.subheader = None
        self.dropdownComment = None
        self.dropdownValues = None
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/decisiontree/"
        self._generate_narratives()


    def _generate_narratives(self):
        self._generate_summary()

    def _generate_summary(self):
        rules = self._decision_rules_dict
        colname = self._colname
        data_dict = {"dimension_name":self._colname}
        data_dict["plural_colname"] = NarrativesUtils.pluralize(data_dict["dimension_name"])
        data_dict["significant_vars"] = []
        rules_dict = self.table
        self.condensedTable={}
        for target in rules_dict.keys():
            self.condensedTable[target]=[]
            for rule in rules_dict[target]:
                rules1 = self._generate_rules(target,rule)
                self.condensedTable[target].append(rules1)
        self.dropdownValues = rules_dict.keys()
        self.dropdownComment = NarrativesUtils.get_template_output(self._base_dir,\
                                                    'decision_rule_summary.temp',data_dict)
        self.subheader = NarrativesUtils.get_template_output(self._base_dir,\
                                        'decision_tree_summary.temp',data_dict)

    def _generate_rules(self,target,rules):
        colname = self._colname
        key_dimensions,key_measures=NarrativesUtils.get_rules_dictionary(rules)
        temp_narrative = 'If '
        for var in key_measures.keys():
            if key_measures[var].has_key('upper_limit') and key_measures[var].has_key('lower_limit'):
                temp_narrative = temp_narrative + 'the value of ' + var + ' falls between ' + key_measures[var]['lower_limit'] + ' and ' + key_measures[var]['upper_limit']+', '
            elif key_measures[var].has_key('upper_limit'):
                temp_narrative = temp_narrative + 'the value of ' + var + ' is less than or equal to ' + key_measures[var]['upper_limit']+', '
            elif key_measures[var].has_key('lower_limit'):
                temp_narrative = temp_narrative + 'the value of ' + var + ' is greater than ' + key_measures[var]['lower_limit']+', '
        for var in key_dimensions.keys():
            if key_dimensions[var].has_key('in'):
                temp_narrative = temp_narrative + 'the ' + var + ' falls among ' + key_dimensions[var]['in'] + ', '
            elif key_dimensions[var].has_key('not_in'):
                temp_narrative = temp_narrative + 'the ' + var + ' does not fall in ' + key_dimensions[var]['not_in'] + ', '

        if temp_narrative == 'If ':
            temp_narrative = ""
        else:
            temp_narrative = str(temp_narrative) + 'then the ' + str(colname) + ' is most likely to fall under ' + str(target)
            return temp_narrative
