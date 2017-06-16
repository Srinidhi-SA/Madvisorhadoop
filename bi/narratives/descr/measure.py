import os

from bi.narratives import utils as NarrativesUtils


class MeasureColumnNarrative:

    MAX_FRACTION_DIGITS = 2

    def __init__(self, column_name, measure_descr_stats, df_helper, df_context):
        self._column_name = column_name.lower()
        self._capitalized_column_name = "%s%s" % (column_name[0].upper(), column_name[1:])
        self._measure_descr_stats = measure_descr_stats
        self._five_point_summary_stats = measure_descr_stats.get_five_point_summary_stats()
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self.title = None
        self.heading = self._capitalized_column_name + ' Performance Analysis'
        self.sub_heading = "Distribution Analysis"
        self.summary = None
        self._analysis1 = None
        self._analysis2 = None
        self.analysis = None
        self.take_away = None
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/descriptive/"
        self.num_measures = len(self._dataframe_helper.get_numeric_columns())
        self.num_dimensions = len(self._dataframe_helper.get_string_columns())
        self.num_time_dimensions = len(self._dataframe_helper.get_timestamp_columns())
        self._generate_narratives()


    def _generate_narratives(self):
        self._generate_title()
        self._generate_summary()
        self._analysis1 = self._generate_analysis_para1()
        self._analysis2 = self._generate_analysis_para2()
        self.analysis = [self._analysis1, self._analysis2]
        self.take_away = self._generate_take_away()

    def _generate_title(self):
        self.title = '%s Performance Report' % (self._capitalized_column_name,)

    def _generate_summary(self):

        ignored_columns = self._dataframe_context.get_ignore_column_suggestions()
        if ignored_columns == None:
            ignored_columns = []

        data_dict = {"n_c" : self._dataframe_helper.get_num_columns(),
                    "n_m" : len(self._dataframe_helper.get_numeric_columns()),
                    "n_d" : len(self._dataframe_helper.get_string_columns()),
                    "n_td" : len(self._dataframe_helper.get_timestamp_columns()),
                    "c" : self._column_name,
                    "d" : self._dataframe_helper.get_string_columns(),
                    "m" : self._dataframe_helper.get_numeric_columns(),
                    "td" : self._dataframe_helper.get_timestamp_columns(),
                    "observations" : self._dataframe_helper.get_num_rows(),
                    "ignorecolumns" : ignored_columns,
                    "n_t" : self._dataframe_helper.get_num_columns()+len(ignored_columns)
        }
        self.summary = NarrativesUtils.get_template_output(self._base_dir,\
                                        'descr_stats_summary.temp',data_dict)

    def _generate_analysis_para1(self):
        output = ''
        data_dict = {"cols" : self._dataframe_helper.get_num_columns(),
                    "min" : NarrativesUtils.round_number(self._measure_descr_stats.get_min(), 0),
                    "max" : NarrativesUtils.round_number(self._measure_descr_stats.get_max(), 0),
                    "n" : self._five_point_summary_stats.get_num_outliers(),
                    "l" : self._five_point_summary_stats.get_left_outliers(),
                    "r" : self._five_point_summary_stats.get_right_outliers(),
                    "m" : self._dataframe_helper.get_numeric_columns(),
                    "total" : NarrativesUtils.round_number(self._measure_descr_stats.get_total(), 0),
                    "avg" : NarrativesUtils.round_number(self._measure_descr_stats.get_mean(), 2),
                    "o": self._five_point_summary_stats.get_num_outliers(),
                    "col_name": self._column_name,
                    'rows': self._dataframe_helper.get_num_rows()
        }
        output = NarrativesUtils.get_template_output(self._base_dir,\
                                        'distribution_narratives.temp',data_dict)
        return output

    def _generate_analysis_para2(self):
        output = ''
        histogram_buckets = self._measure_descr_stats.get_histogram()
        threshold = self._dataframe_helper.get_num_rows() * 0.75
        s = 0
        start = 0
        end = len(histogram_buckets)
        flag = 0
        for bin_size in range(1,len(histogram_buckets)):
            s_t = 0
            for i in range(len(histogram_buckets)-bin_size+1):
                s_t = 0
                for j in range(i,i+bin_size):
                    s_t = s_t + histogram_buckets[j]['num_records']
                if(s_t >= threshold) and (s_t > s):
                    s = s_t
                    start = i
                    end = i + bin_size - 1
                    flag = 1
            if (flag == 1):
                break
        bin_size_75 = (end - start + 1)*100/len(histogram_buckets)
        s = s*100/self._dataframe_helper.get_num_rows()
        start_value = histogram_buckets[start]['start_value']
        end_value = histogram_buckets[end]['end_value']
        lowest = min(histogram_buckets[0]['num_records'],histogram_buckets[1]['num_records'],histogram_buckets[2]['num_records'])
        highest = max(histogram_buckets[0]['num_records'],histogram_buckets[1]['num_records'],histogram_buckets[2]['num_records'])

        data_dict = {"histogram" : histogram_buckets,
                    "per_cont_hist1" : NarrativesUtils.round_number(histogram_buckets[0]['num_records']*100/self._measure_descr_stats.get_total(), MeasureColumnNarrative.MAX_FRACTION_DIGITS),
                    "per_cont_hist2" : NarrativesUtils.round_number(histogram_buckets[1]['num_records']*100/self._measure_descr_stats.get_total(), MeasureColumnNarrative.MAX_FRACTION_DIGITS),
                    "lowest_cont" : NarrativesUtils.round_number(lowest*100/self._measure_descr_stats.get_total(), MeasureColumnNarrative.MAX_FRACTION_DIGITS),
                    "highest_cont" : NarrativesUtils.round_number(highest*100/self._measure_descr_stats.get_total(), MeasureColumnNarrative.MAX_FRACTION_DIGITS),
                    "num_bins" : len(histogram_buckets),
                    "seventy_five" : bin_size_75,
                    "col_name" : self._column_name,
                    "skew" : self._measure_descr_stats.get_skew(),
                    "three_quarter_percent" : round(s,2),
                    "start_value" : start_value,
                    "end_value" : end_value,
                    "measure_colname":self._column_name
        }
        output = NarrativesUtils.get_template_output(self._base_dir,\
                                        'histogram_narrative.temp',data_dict)
        return output

    def _generate_take_away(self):
        output = ''
        histogram_buckets = self._measure_descr_stats.get_histogram()
        threshold = self._dataframe_helper.get_num_rows() * 0.75
        s = 0
        start = 0
        end = len(histogram_buckets)
        flag = 0
        for bin_size in range(1,len(histogram_buckets)):
            s_t = 0
            for i in range(len(histogram_buckets)-bin_size+1):
                s_t = 0
                for j in range(i,i+bin_size):
                    s_t = s_t + histogram_buckets[j]['num_records']
                if(s_t >= threshold) and (s_t > s):
                    s = s_t
                    start = i
                    end = i + bin_size - 1
                    flag = 1
            if (flag == 1):
                break
        bin_size_75 = (end - start + 1)*100/len(histogram_buckets)
        s = s*100/self._dataframe_helper.get_num_rows()
        start_value = histogram_buckets[start]['start_value']
        end_value = histogram_buckets[end]['end_value']
        data_dict = {"num_bins" : len(histogram_buckets),
                    "seventy_five" : bin_size_75,
                    "col_name" : self._column_name,
                    "c_col_name" : self._capitalized_column_name,
                    "skew" : self._measure_descr_stats.get_skew(),
                    "start": start_value,
                    "end": end_value
                    }
        if (len(histogram_buckets)>3):
            output = NarrativesUtils.get_template_output(self._base_dir,\
                                            'histogram_takeaway.temp',data_dict)
        return output
