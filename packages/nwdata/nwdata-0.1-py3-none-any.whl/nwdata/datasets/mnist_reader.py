import numpy as np
from functools import partial
from overrides import overrides
from typing import Iterator, Tuple, List
from .dataset import Dataset
from ..reader.h5_batched_reader import H5BatchedReader
from ..utils import batchIndexFromBatchSizes, toCategorical

class MNISTReader(H5BatchedReader, Dataset):
	def __init__(self, datasetPath:str, normalization:str = "min_max_0_1"):
		assert normalization in ("none", "min_max_0_1")

		rgbTransform = {
			"min_max_0_1" : (lambda x : np.float32(x) / 255),
			"none" : (lambda x : x)
		}[normalization]

		super().__init__(datasetPath,
			dataBuckets = {"data" : ["images"], "labels" : ["labels"]},
			dimTransform = {
				"data" : {"images" : rgbTransform},
				"labels" : {"labels" : lambda x : toCategorical(x, numClasses=10)}
			}
		)
		self.isCacheable = True

	@overrides
	def processRawData():
		pass

	@overrides
	def getBatches(self):
		if self.batches is None:
			nData = len(self.getDataset()["images"])
			batches = np.arange(nData).reshape(-1, 1)
			self.setBatches(batches)
		return self.batches

	@overrides
	def __getitem__(self, index):
		item = super().__getitem__(index)
		return {"data" : item["data"], "labels" : item["labels"]["labels"]}
