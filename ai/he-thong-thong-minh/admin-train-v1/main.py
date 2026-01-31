from dao import SampleDao
from dao import TrainedModelDao
sampleDao = SampleDao()

samples = sampleDao.get_list_sample()
print(samples)


trainedModelDao = TrainedModelDao()

