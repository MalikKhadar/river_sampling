import csv
import datetime
import get_time
import menu
import numpy as np
import sampling_strategies
import settings

def flatten(l):
  '''Turn a 2d list into a 1d list'''
  flat_list = [item for sublist in l for item in sublist]
  return flat_list

class Data:
  '''Associates a list of nums with their SD, mean, and percentiles'''
  def __init__(self, values, calc_sd = False, calc_perc = True, calc_mean = True):
    self.mean = 0
    self.percentiles = []
    self.sd = 0

    #Each calculation is optional to save on computation time
    if calc_sd == True:
      self.sd = np.std(values)
    if calc_mean == True:
      self.mean = sum(values)/len(values)
    if calc_perc == True:
      self.percentiles = np.percentile(values, settings.p_vals)

def data_in_time_range(file_location, time_range=0, just_headers=False):
  '''returns data from file that is restrained to a time_range'''
  with open(file_location, 'r') as csvfile: 
    csvreader = csv.reader(csvfile) 
    data = []
    data.append(next(csvreader))

    if just_headers:
      return data[0]

    #the datetime info is in the first column
    for row in csvreader: 
      dt = datetime.datetime.fromisoformat(row[0])
      if dt < time_range[1] and dt > time_range[0]:    #only use data within the timerange
        data.append(row)  
    return data 

def transpose(m):
  '''returns transpose of 2d list'''
  return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

class Analysis_Params:
  '''set of parameters for running sample_analysis'''
  def __init__(self):
    #select a site
    self.sites = menu.select_site(single=False)
      
    #select num of iterations and time range
    self.iterations = menu.select_integer("Number of iterations")
    self.time_range = get_time.select_timerange()

    param_options = []
    #aggregate site params from all sites
    for site in self.sites:
      headers = data_in_time_range("site_data/" + site, just_headers=True)
      #skip the datetime column
      param_options.extend(headers[1:])
      #TODO: USE ABBREV TO CONDENSE OPTIONS
    param_options = list(set(param_options))  #remove duplicates
    self.site_params = menu.multiselect(param_options, "parameter", return_names=True)
    
    self.cp = sampling_strategies.Cull_Params()
    self.cp.name = self.choose_model()

  def choose_model(self):
    '''user may select a model'''
    options_dict = {
      "None": sampling_strategies.Base_Model, 
      "Time": sampling_strategies.Time_Model
    }
    options = list(options_dict.keys())
    choice = menu.select_element("Sampling strategy type", options)
    self.strategy = options_dict[choice]
    return choice