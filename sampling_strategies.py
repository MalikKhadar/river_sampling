import get_time
import menu
import model

class Cull_Params:
  def __init__(self, used=False):
    self.used = used

class Base_Model(model.Model):
  def __init__(self, samples, iterations, parameter, cull_params):
    super().__init__(samples, iterations, parameter)
    self.cull_params = cull_params

  def cull(self):
    '''base model has no culling strategy'''
    pass

class Time_Model(model.Model):
  def __init__(self, samples, iterations, parameter, cull_params):
    super().__init__(samples, iterations, parameter)
    self.cull_params = cull_params

  def cull(self):
    '''remove samples based on day of week and time of day'''
    if self.cull_params.used == False:
      self.cull_params.weekdays = get_time.get_weekdays()
      self.cull_params.time_range = get_time.time_range()
      self.cull_params.used = True
    new_samples = []

    for sample in self.samples:
      if get_time.in_range(sample[0], self.cull_params.weekdays, self.cull_params.time_range):
        new_samples.append(sample)

    self.samples = new_samples
