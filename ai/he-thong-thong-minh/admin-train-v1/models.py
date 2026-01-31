from dataclasses import dataclass, field
from typing import List


@dataclass
class Sample:
    """
    Corresponds to the 'Sample' class and 'tbl_sample' table.
    Represents a single data sample, likely for object detection.
    """
    id: int
    image_file_path: str
    label: str
    x_min: int
    y_min: int
    x_max: int
    y_max: int

@dataclass
class TrainingSample:
    """
    Corresponds to the 'TrainingSample' association class.
    Links a TrainedModel to the Sample it used.
    """
    sample: Sample

@dataclass
class TrainedModel:
    """
    Corresponds to the 'TrainedModel' class and 'tbl_trained_model' table.
    Represents a model that has been trained.
    """
    id: int
    name: str
    artifact_path: str
    accuracy: float
    f1: float
    precision: float
    recall: float
    training_samples: List[TrainingSample] = field(default_factory=list)
