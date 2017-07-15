import operator
import os

import numpy

from bi.narratives import utils as NarrativesUtils


class ChiSquareAnalysis:
    def __init__ (self, chisquare_result, target_dimension, analysed_dimension, significant_variables, num_analysed_variables, appid=None):
        self._chisquare_result = chisquare_result
        self._target_dimension = target_dimension
        self._analysed_dimension = analysed_dimension
        self._significant_variables =  significant_variables
        self._num_analysed_variables = num_analysed_variables
        self._table = chisquare_result.get_contingency_table()
        self.appid = appid
        self.card1 = {}
        # self.card1 = {}
        # self.card2 = {}
        self.card4 = {}
        # self.card4 = {}
        # self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/chisquare/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/chisquare/"
        if self.appid != None:
            if self.appid == "1":
                self._base_dir += "appid1/"
            elif self.appid == "2":
                self._base_dir += "appid2/"
        self._generate_narratives()

    def _generate_narratives(self):
        chisquare_result = self._chisquare_result
        target_dimension = self._target_dimension
        analysed_dimension = self._analysed_dimension
        significant_variables = self._significant_variables
        num_analysed_variables = self._num_analysed_variables
        table = self._table
        total = self._table.get_total()

        levels = self._table.get_column_two_levels()
        level_counts = self._table.get_column_total()
        levels_count_sum = sum(level_counts)
        levels_percentages = [i*100.0/levels_count_sum for i in level_counts]
        sorted_levels = sorted(zip(level_counts,levels),reverse=True)
        level_differences = [0.0]+[sorted_levels[i][0]-sorted_levels[i+1][0] for i in range(len(sorted_levels)-1)]
        top_dims = [j for i,j in sorted_levels[:level_differences.index(max(level_differences))]]
        top_dims_contribution = sum([i for i,j in sorted_levels[:level_differences.index(max(level_differences))]])
        bottom_dim = sorted_levels[-1][1]
        bottom_dim_contribution = sorted_levels[-1][0]

        target_levels = self._table.get_column_one_levels()
        target_counts = self._table.get_row_total()
        sorted_target_levels = sorted(zip(target_counts,target_levels),reverse=True)
        top_target_count, top_target = sorted_target_levels[0]
        second_target_count, second_target = sorted_target_levels[1]

        top_target_contributions = [table.get_value(top_target,i) for i in levels]
        sum_top_target = sum(top_target_contributions)

        sorted_levels = sorted(zip(top_target_contributions,levels), reverse=True)
        level_differences = [0.0] + [sorted_levels[i][0]-sorted_levels[i+1][0] for i in range(len(sorted_levels)-1)]
        top_target_top_dims = [j for i,j in sorted_levels[:level_differences.index(max(level_differences))]]
        top_target_top_dims_contribution = sum([i for i,j in sorted_levels[:level_differences.index(max(level_differences))]])
        top_target_bottom_dim = sorted_levels[-1][1]
        top_target_bottom_dim_contribution = sorted_levels[-1][0]

        top_target_percentages = [i*100.0/sum_top_target for i in top_target_contributions]
        best_top_target_index = top_target_contributions.index(max(top_target_contributions))
        worst_top_target_index = top_target_contributions.index(min(top_target_contributions))
        top_target_differences = [x-y for x,y in zip(levels_percentages,top_target_percentages)]
        if len(top_target_differences)>4:
            tops = 2
            bottoms = -2
        elif len(top_target_differences)==4:
            tops = 2
            bottoms = -1
        else:
            tops = 1
            bottoms = -1
        sorted_ = sorted(enumerate(top_target_differences), key = lambda x: x[1])
        best_top_difference_indices = [x for x,y in sorted_[:tops]]
        worst_top_difference_indices = [x for x,y in sorted_[bottoms:]]

        second_target_contributions = [table.get_value(second_target,i) for i in levels]
        sum_second_target = sum(second_target_contributions)

        sorted_levels = sorted(zip(second_target_contributions,levels), reverse=True)
        level_differences = [0.0] + [sorted_levels[i][0]-sorted_levels[i+1][0] for i in range(len(sorted_levels)-1)]
        second_target_top_dims = [j for i,j in sorted_levels[:level_differences.index(max(level_differences))]]
        second_target_top_dims_contribution = sum([i for i,j in sorted_levels[:level_differences.index(max(level_differences))]])
        second_target_bottom_dim = sorted_levels[-1][1]
        second_target_bottom_dim_contribution = sorted_levels[-1][0]

        second_target_percentages = [i*100.0/sum_second_target for i in second_target_contributions]
        best_second_target_index = second_target_contributions.index(max(second_target_contributions))
        worst_second_target_index = second_target_contributions.index(min(second_target_contributions))
        second_target_differences = [x-y for x,y in zip(levels_percentages,second_target_percentages)]
        if len(second_target_differences)>4:
            seconds = 2
            bottoms = -2
        elif len(second_target_differences)==4:
            seconds = 2
            bottoms = -1
        else:
            seconds = 1
            bottoms = -1
        sorted_ = sorted(enumerate(second_target_differences), key = lambda x: x[1])
        best_second_difference_indices = [x for x,y in sorted_[:seconds]]
        worst_second_difference_indices = [x for x,y in sorted_[bottoms:]]

        data_dict = {}
        data_dict['num_significant'] = len(significant_variables)
        data_dict['colname'] = analysed_dimension
        data_dict['target'] = target_dimension
        data_dict['top_levels'] = top_dims
        data_dict['top_levels_percent'] = top_dims_contribution
        data_dict['bottom_level'] = bottom_dim
        data_dict['bottom_level_percent'] = round(bottom_dim_contribution,2)
        data_dict['second_target']=second_target
        data_dict['second_target_top_dims'] = second_target_top_dims
        data_dict['second_target_top_dims_contribution'] = second_target_top_dims_contribution
        data_dict['second_target_bottom_dim']=second_target_bottom_dim
        data_dict['second_target_bottom_dim_contribution']=second_target_bottom_dim_contribution
        data_dict['best_second_target'] = levels[best_second_target_index]
        data_dict['best_second_target_count'] = second_target_contributions[best_second_target_index]
        data_dict['best_second_target_percent'] = round(second_target_contributions[best_second_target_index]*100.0/total,2)
        data_dict['worst_second_target'] = levels[worst_second_target_index]
        data_dict['worst_second_target_percent'] = round(second_target_contributions[worst_second_target_index]*100.0/total,2)

        output = NarrativesUtils.paragraph_splitter(NarrativesUtils.get_template_output(self._base_dir,'card1.temp',data_dict))
        self.card1['heading'] = 'Relationship between '+ self._target_dimension + '  and '+self._analysed_dimension
        self.card1['paragraphs'] = output
        self.card1['chart']=[]
        self.card1['heat_chart']=self._table
        self.generate_card1_chart()
        print '-'*1500
        print self.card1
        print '='*1500
        self.card4['heading']='Distribution of ' + self._target_dimension + ' (' + second_target + ') across ' + self._analysed_dimension
        chart,bubble=self.generate_card4_chart(second_target, second_target_contributions, levels, level_counts, total)
        self.card4['chart'] = chart
        self.card4['bubble_data'] = bubble
        output3 = NarrativesUtils.paragraph_splitter(NarrativesUtils.get_template_output(self._base_dir,'card4.temp',data_dict))
        print self.card4

    def generate_card4_chart(self, second_target, second_target_contributions, levels, levels_count, total):
        chart = {}
        label = {'total' : '# of '+second_target+'(left)',
                  'percentage': '# of '+second_target+'(right)'}
        data = {}
        data['total'] = dict(zip(levels,second_target_contributions))
        second_target_percentages = [x*100.0/y for x,y in zip(second_target_contributions,levels_count)]
        data['percentage'] = dict(zip(levels,second_target_percentages))
        chart_data = {'label':label,
                                'data':data}
        print self.card4
        bubble_data1 = {}
        bubble_data2 = {}
        bubble_data1['value'] = NarrativesUtils.round_number(max(second_target_contributions)*100.0/total,2)+'%'
        m_index = second_target_contributions.index(max(second_target_contributions))
        bubble_data1['text'] = 'Percentage '+second_target+' from '+ levels[m_index]

        bubble_data2['value'] = NarrativesUtils.round_number(max(second_target_percentages),2)+'%'
        m_index = second_target_percentages.index(max(second_target_percentages))
        bubble_data2['text'] = levels[m_index] + ' has the highest rate of '+second_target

        bubble_data = [bubble_data1,bubble_data2]
        return chart_data, bubble_data

    def generate_card1_chart(self):
        table = self._table.table
        table_percent = self._table.table_percent
        table_percent_by_row = self._table.table_percent_by_row
        table_percent_by_column = self._table.table_percent_by_column
        target_levels = self._table.get_column_one_levels()
        dim_levels = self._table.get_column_two_levels()

        header = [self._analysed_dimension] + dim_levels + ['Total']
        data = []

        for idx, lvl in enumerate(dim_levels):
            data1 = header+['Tag']

            col_2_vals = zip(*table)[idx]
            data2 = [lvl] + list(col_2_vals) + [sum(col_2_vals)] + ['bold']
            dict_ = dict(zip(data1, data2))
            data.append(dict_)

            col_2_vals = zip(*table_percent_by_column)[idx]
            data2 = ['As % within '+self._analysed_dimension] + list(col_2_vals) + [100.0] + ['']
            dict_ = dict(zip(data1, data2))
            data.append(dict_)

            col_2_vals = zip(*table_percent_by_row)[idx]
            col_2_vals1 = zip(*table_percent)[idx]
            data2 = ['As % within '+self._target_dimension] + list(col_2_vals) + [round(sum(col_2_vals1),2)] + ['']
            dict_ = dict(zip(data1, data2))
            data.append(dict_)

            # col_2_vals = zip(*table_percent)[idx]
            data2 = ['As % of Total'] + list(col_2_vals1) + [round(sum(col_2_vals1),2)] + ['']
            dict_ = dict(zip(data1, data2))
            data.append(dict_)

        self.card1['chart']={'header':header,
                            'data':data}
