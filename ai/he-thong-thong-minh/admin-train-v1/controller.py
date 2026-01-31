from typing import List, Optional
from models import Sample, TrainedModel
from dao import SampleDao, TrainedModelDao
from algo import cnn
from algo import landmark
from algo import random

from sklearn.model_selection import train_test_split
class TrainModelController:
    def __init__(self, sample_dao: SampleDao, model_dao: TrainedModelDao):
        self.sample_dao = sample_dao
        self.model_dao = model_dao

    def train(self, model: TrainedModel) -> Optional[TrainedModel]:

        # Split train/test 80/20
        train_samples, test_samples = train_test_split(model.training_samples, test_size=0.2, random_state=42)

        model_name_lower = model.name.lower()
        if model_name_lower == 'cnn':
            trained_model = cnn.train(train_samples, test_samples)
        elif model_name_lower in ['random forest', 'random_forest']:
            trained_model = random.train(train_samples, test_samples)
        elif model_name_lower == 'landmark':
            trained_model = landmark.train(model.training_samples)
        else:
            print(f" Unknown model type: {model.name}")
            return None

        return trained_model
