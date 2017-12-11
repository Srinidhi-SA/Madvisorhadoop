import os
import math
import json
import time
import requests
from math import *
from re import sub
import traceback
import uuid
import md5

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
from numpy import size, zeros, where, transpose
from numpy.random import normal
from scipy import linspace
import array
# from matplotlib.pyplot import hist

from pyspark.conf import SparkConf
from pyspark.sql import SparkSession

from decorators import accepts
from math import log10, floor



def round_sig(x, sig=3):
    try:
        if abs(x)>=1:
            x = round(x,sig)
        else:
            x = round(x, sig-int(floor(log10(abs(x))))-1)
    except:
        pass
    return x

def get_secret_key():
    secretKey = "GETMETADATAOBJECT"
    return secretKey

def generate_signature(json_obj,secretKey=None):
    """
    json_obj = json obj with {"key1":"DSDDD","key2":"DASDAA","signature":None}
    secretKey = "secret key"
    """
    existing_key = json_obj["key1"]+"|"+json_obj["key2"]+"|"+secretKey
    newhash = md5.new()
    newhash.update(existing_key)
    value = newhash.hexdigest()
    return value

def get_metadata(dataframe_context):
    baseUrl = dataframe_context.get_metadata_url()
    slugs = dataframe_context.get_metadata_slugs()
    jsonToken = {"key1":uuid.uuid4().hex,"key2":uuid.uuid4().hex,"signature":None,"generated_at":time.time()}
    secretKey = get_secret_key()
    sigString = generate_signature(jsonToken,secretKey)
    jsonToken["signature"] = sigString
    url = "http://{}{}/?key1={}&key2={}&signature={}&generated_at={}".format(baseUrl,slugs[0],jsonToken["key1"],jsonToken["key2"],jsonToken["signature"],jsonToken["generated_at"])
    metaObj = requests.get(url)
    return metaObj.json()

@accepts((int, long, float), (int, long, float), num_steps=int)
def frange(start, stop, num_steps=10):
    """
    Create num_step equal sized ranges form start to stop, useful in histogram generation
    :param start:
    :param stop:
    :param num_steps:
    :return:
    """
    step_size = start+1
    if start == stop:
        start=start - 0.8
        stop = stop + 0.8
    step_size = 1.0 * (stop-start) / num_steps
    rounding_digits = 0
    if step_size >= 1:
        step_size = int(math.ceil(step_size))
    else:
        rounding_digits = 1
        while num_steps >= (step_size * math.pow(10, rounding_digits)):
            rounding_digits += 1
        step_size = round(step_size, rounding_digits)

    rounded_start = math.floor(1.0 * start / step_size) * step_size
    rounded_stop = math.ceil(1.0 * (stop+step_size/num_steps) / step_size) * step_size
    i = rounded_start
    result = []
    while i < rounded_stop:
        result.append(round(i, rounding_digits))
        i += step_size
    if result[-1] < rounded_stop:
        result.append(round(rounded_stop, rounding_digits))
    result = list(set(result))
    result.sort()
    return result


@accepts(app_name=basestring)
def get_spark_session(app_name='Demo App'):
    return SparkSession.builder.appName(app_name).config(conf=SparkConf()).getOrCreate()
    #return SparkSession.builder.appName(app_name).getOrCreate()

def clean(x):
    from re import sub
    # \g<1> is whatever matches the the first (...)
    #x = sub( r'(\d+)[kK]', r'\g<1>000', x )
    x = sub('[^0-9.a-zA-z/-]','',x)
    return x

def get_updated_colnames(df):
    num_rows = len(df.index)
    final_column_names = []
    changed_cols = []
    for col in df.columns:
        if not df[col].dtype==object:
            final_column_names.append(col)
            continue
        temp = []
        try:
            temp = [x for x in df.dropna(subset=[col])[col]]
            initial_length = len(temp)
            if (initial_length<num_rows/2):
                raise ValueError('None Vals')
            temp1 = [float(clean(x)) for x in temp]
            final_length = len(temp1)
            if initial_length == final_length:
                changed_cols.append(col)
                try:
                    pre=int(temp[0][0])
                except:
                    col = col + '||pre:' + temp[0][0]
                try:
                    post=int(temp[0][-1])
                except:
                    col = col + '||post:' + temp[0][-1]

        except ValueError:
            # print "e1"
            pass
        else:
            pass
            # print "e2"
        final_column_names.append(col)
    return {'f':final_column_names, 'c':changed_cols}

def tryconvert(x):
    if x==None:
        return None
    try:
        x =float(sub('[^0-9.a-zA-z:/-]','',x))
        return x
    except:
        pass
    return None

def as_dict(obj):
    """
    Converts an object hierarchy into a dictionary object
    Ref: http://stackoverflow.com/questions/1036409/recursively-convert-python-object-graph-to-dictionary
    :param obj:
    :return:
    """
    if isinstance(obj, dict):
        return {k: as_dict(v) for (k, v) in obj.items()}
    elif hasattr(obj, "_ast"):
        return as_dict(obj._ast())
    elif hasattr(obj, '__iter__'):
        return [as_dict(v) for v in obj]
    elif hasattr(obj, '__dict__'):
        return dict([(key, as_dict(value))
                     for key, value in obj.__dict__.iteritems()
                     if not callable(value) and not key.startswith('_')])
    else:
        return obj

def recursiveRemoveNoneNodes(tree):
    if isinstance(tree, dict) and "children" not in tree.keys():
        return tree
    elif isinstance(tree, dict) and "children" in tree.keys():
        # if len(tree["children"]) != 0:
        if tree["children"] != [None]:
            for idx,stree in enumerate(tree["children"]):
                if stree != None:
                    tree["children"][idx] = (recursiveRemoveNoneNodes(stree))
            return tree
        else:
            tree.pop("children")
            return tree

def dateTimeFormatsSupported():
    data = {}
    data["formats"] = ('%m/%d/%Y %H:%M','%d/%m/%Y %H:%M','%m/%d/%y %H:%M','%d/%m/%y %H:%M',
            '%m-%d-%Y %H:%M','%d-%m-%Y %H:%M','%m-%d-%y %H:%M','%d-%m-%y %H:%M',
            '%b/%d/%Y %H:%M','%d/%b/%Y %H:%M','%b/%d/%y %H:%M','%d/%b/%y %H:%M',
            '%b-%d-%Y %H:%M','%d-%b-%Y %H:%M','%b-%d-%y %H:%M','%d-%b-%y %H:%M',
            '%B/%d/%Y %H:%M','%d/%B/%Y %H:%M','%B/%d/%y %H:%M','%d/%B/%y %H:%M',
            '%B-%d-%Y %H:%M','%d-%B-%Y %H:%M','%B-%d-%y %H:%M','%d-%B-%y %H:%M',
            '%Y-%m-%d %H:%M','%Y/%m/%d %H:%M','%Y-%b-%d %H:%M','%Y-%B-%d %H:%M',
            '%m-%d-%Y %r','%d-%m-%Y %r','%m-%d-%Y %R',
            '%d-%m-%Y %R', '%m-%d-%y %r','%d-%m-%y %r','%m-%d-%y %R',
            '%d-%m-%y %R', '%b-%d-%Y %r','%d-%b-%Y %r', '%Y-%b-%d %r','%b-%d-%Y %R',
            '%d-%b-%Y %R', '%b-%d-%y %r','%d-%b-%y %r','%b-%d-%y %R','%d-%b-%y %R',
            '%B-%d-%Y %r','%d-%B-%Y %r','%B-%d-%Y %R','%d-%B-%y %R',
            '%d-%B-%Y %R', '%B-%d-%y %r','%d-%B-%y %r','%B-%d-%y %R',
            '%y-%m-%d %R','%y-%m-%d %r','%Y-%m-%d %r','%Y-%B-%d %r',
            '%d %B %Y', '%d %B %y', '%d %b %y', '%d %b %Y',
            '%m/%d/%Y','%d/%m/%Y','%m/%d/%y','%d/%m/%y',
            '%m-%d-%Y','%d-%m-%Y','%m-%d-%y','%d-%m-%y',
            '%b/%d/%Y','%d/%b/%Y','%b/%d/%y','%d/%b/%y',
            '%b-%d-%Y','%d-%b-%Y','%b-%d-%y','%d-%b-%y',
            '%B/%d/%Y','%d/%B/%Y','%B/%d/%y','%d/%B/%y',
            '%B-%d-%Y','%d-%B-%Y','%B-%d-%y','%d-%B-%y',
            '%Y-%m-%d','%Y/%m/%d','%Y-%b-%d','%Y-%B-%d',
            '%b %d, %Y','%B %d, %Y','%B %d %Y','%m/%d/%Y',
            '%d %B, %Y', '%d %B, %y','%d %b, %Y', '%d %b, %y',
            '%m/%d/%y', '%b %Y','%B %y','%m/%y','%m/%Y',
            '%B%Y','%b %d,%Y','%m.%d.%Y','%m.%d.%y','%b/%y',
            '%m - %d - %Y','%m - %d - %y','%B %d, %y','%b %d, %y',
            '%d-%B','%d-%b', '%b,%y','%B,%y','%b,%Y','%B,%Y',
            '%b %Y', '%b %y','%B %Y','%B %y','%b-%y','%b/%Y','%b-%Y')

    data["dual_checks"] = ('%m/%d/%Y %H:%M','%m/%d/%y %H:%M','%m-%d-%Y %H:%M','%m-%d-%y %H:%M','%m-%d-%Y %r','%m-%d-%Y %R', '%m-%d-%y %r','%m-%d-%y %R',
                            '%m/%d/%Y %r','%m/%d/%Y %R', '%m/%d/%y %r','%m/%d/%y %R','%m/%d/%Y','%m/%d/%y','%m-%d-%Y','%m-%d-%y','%m.%d.%Y','%m.%d.%y','%m - %d - %Y',
                            '%m - %d - %y')
    return data

def write_to_file(filepath,obj):
    if filepath.startswith("file"):
        filepath = filepath[7:]
    f = open(filepath, 'w')
    f.write(obj)
    f.close()

def get_level_count_dict(df,categorical_columns,separator,output_type="string",dataType="pandas"):
    count_dict = {}
    out = []
    for col in categorical_columns:
        if dataType == "spark":
            count_dict[col] = len(df.select(col).distinct().collect())
        else:
            count_dict[col] = len(df[col].unique())
        out.append(col)
        out.append(str(count_dict[col]))
    if output_type == "string":
        return separator.join(out)
    else:
        return count_dict

def send_message_API(monitor_api, task, message, complete, progress):
    url = monitor_api
    message_dict = {}
    message_dict['task'] = task
    message_dict['message'] = message
    message_dict['complete'] = complete
    message_dict['progress'] = progress
    #r = requests.post(url, data=json.dumps(message_dict))
    #print json.loads(r.content)['message'] + " for ", task +'\n'

def temp_convertor(x):
    try:
        return x.__dict__
    except Exception as e:
        return "{}".format(x)

def convert_python_object_to_json(object):
    return json.dumps(object, default=temp_convertor)


def byteify(input):
    if isinstance(input, dict):
        return dict([(byteify(key), byteify(value)) for key, value in input.iteritems()])
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def save_result_json(url,jsonData):
    url += "set_result"
    print "url",url
    res = requests.put(url=url,data=jsonData)
    return res

def create_progress_message_object(sectionDict,name,timeTaken,completionStatus):
    progressMessage = {
        "name" : name,
        "displayName" : sectionDict[name]["displayName"],
        "timeTaken" : timeTaken,
        "completionStatus" : completionStatus
    }
    return progressMessage

def create_progress_message_object(analysisName,stageName,messageType,shortExplanation,stageCompletionPercentage,globalCompletionPercentage):
    progressMessage = {
        "analysisName" : analysisName,
        "stageName" : stageName,
        "messageType" : messageType,
        "shortExplanation" : shortExplanation,
        "stageCompletionTimestamp" : time.time(),
        "globalCompletionPercentage" : globalCompletionPercentage,
        "stageCompletionPercentage" : stageCompletionPercentage
    }
    return progressMessage

def save_progress_message(url,jsonData,ignore=False):
    if ignore == False:
        res = requests.put(url=url,data=json.dumps(jsonData))
        return res


def keyWithMaxVal(dictObj):
     """ a) create a list of the dict's keys and values;
         b) return the key with the max value"""
     v=list(dictObj.values())
     k=list(dictObj.keys())
     return k[v.index(max(v))]

def print_errors_and_store_traceback(loggerDict,scriptName,error):
    print error
    exception = {"exception":error,"traceback":traceback.format_exc()}
    loggerDict[scriptName] = exception
    print "#####ERROR#####"*5
    print error
    print "#####ERROR#####"*5
    print "{} Script Failed".format("scriptName")

def get_duration_string(datarange):
    yr = str(datarange//365)
    mon = str((datarange%365)//30)
    if mon == "12":
        yr = str(int(yr)+1)
        mon = None
    if mon != None:
        durationString = yr+" years and "+mon+" months"
    else:
        durationString = yr+" years"
    return durationString

def get_splits(minVal,maxVal,n_split):
    # splits  = frange(minVal,maxVal,num_steps=n_split)
    diff = (maxVal - minVal)*1.0
    splits = [minVal,minVal+diff*0.2,minVal+diff*0.4,minVal+diff*0.6,minVal+diff*0.8,maxVal]
    splits = sorted(splits)
    splits_range = [(splits[idx],splits[idx+1]) for idx in range(len(splits)-1)]
    splits_data = {"splits":splits,"splits_range":splits_range}
    str_splits_range = [" to ".join([str(x[0]),str(x[1])]) for x in splits_range]
    splits_data["bin_mapping"] = dict(zip(range(len(splits_range)),str_splits_range))
    return splits_data

def ret_opt_bins(x):
	sd = np.std(x)
	mean = np.mean(x)

	final_list = [i for i in x if (i > mean - 3 * sd)]
	final_list = [i for i in final_list if (i < mean + 3 * sd)]

	x= pd.Series(final_list)

	#--------------Optimizing bins ---------------#

	x_max = max(x)
	x_min = min(x)

	N_MIN = 2   					# Minimum number of bins (integer)
	N_MAX = 30						# Maximum number of bins (integer)
	N = range(N_MIN,N_MAX) 			#of Bins
	N = np.array(N)
	D = (x_max-x_min)/N    			#Bin size vector
	C = zeros(shape=(size(D),1))

	# Computation of the cost function

	for i in xrange(size(N)):
		edges = linspace(x_min,x_max,N[i]+1)  # Bin edges
		ki = plt.hist(x,edges) 				  # Count # of events in bins
		ki = list(ki[0])
		k = np.mean(ki) 					  # Mean of event count
		v = sum((ki-k)**2)/N[i] 			  # Variance of event count
		C[i] = (2*k-v)/((D[i])**2.)        	  # The cost Function

	# Optimal Bin Size Selection

	cmin = min(C)
	idx  = where(C==cmin)
	idx = int(idx[0])
	optD = D[idx]

	# plt.clf()
	# plt.close()

	edges = linspace(x_min,x_max,N[idx]+1)

	return edges


if __name__ == '__main__':
    x = frange(0.01,0.02,5)
