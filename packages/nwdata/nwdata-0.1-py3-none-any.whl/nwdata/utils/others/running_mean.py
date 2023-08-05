import numpy as np
from typing import Union, Optional, Sequence, Dict
from numbers import Number
from collections import OrderedDict

class RunningMeanNumber:
	def __init__(self, initValue:Number):
		self.value = initValue
		self.count = 0

	def update(self, value:Number, count:Optional[int] = None):
		if not count:
			count = 1
		self.value += value
		self.count += count

	def updateBatch(self, value:Sequence):
		value = np.array(value)
		assert len(value.shape) == 1
		self.update(value.sum(axis=0), value.shape[0])

	def get(self):
		assert self.count > 0
		return self.value / self.count

class RunningMeanSequence:
	def __init__(self, initValue:Sequence):
		self.value = np.array(initValue)
		self.count = 0

	def update(self, value:Sequence, count:Optional[int] = None):
		value = np.array(value)
		if not count:
			count = 1
		self.value += value
		self.count += count

	def updateBatch(self, value:Sequence):
		value = np.array(value)
		assert len(value.shape) == len(self.value.shape) + 1
		self.update(value.sum(axis=0), value.shape[0])

	def get(self):
		assert self.count > 0
		return self.value / self.count

class RunningMeanDict:
	def __init__(self, initValue:Dict):
		self.value = initValue
		self.count = 0

	def update(self, value:Dict, count:Optional[int] = None):
		if not count:
			count = 1
		self.value = {k:self.value[k] + value[k] for k in self.value}
		self.count += count

	def updateBatch(self, value:Dict):
		assert False, "Only valid for Number and Sequence"

	def get(self):
		assert self.count > 0
		return {k:self.value[k] / self.count for k in self.value}

class RunningMean:
	def __init__(self, initValue:Union[Number, Sequence, Dict]):
		if isinstance(initValue, Number):
			self.obj = RunningMeanNumber(initValue) # type: ignore
		elif isinstance(initValue, (list, tuple, set, np.ndarray)):
			self.obj = RunningMeanSequence(initValue)
		elif isinstance(initValue, (dict, OrderedDict)): # type: ignore
			self.obj = RunningMeanDict(initValue) # type: ignore
		else:
			print("[RunningMean] Doing a running mean on unknown type %s" % type(initValue))
			self.obj = RunningMeanNumber(initValue)

	def update(self, value:Union[Number, Sequence, Dict], count:Optional[int] = 0):
		self.obj.update(value, count)

	def updateBatch(self, value:Dict):
		self.obj.updateBatch(value)

	def get(self):
		return self.obj.get()

	def __repr__(self):
		return str(self.get())

	def __str__(self):
		return str(self.get())