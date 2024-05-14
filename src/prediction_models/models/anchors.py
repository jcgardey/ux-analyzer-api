
from .sklearn_model import SklearnModel
from imblearn.under_sampling import RandomUnderSampler

class AnchorModel(SklearnModel):

    def clean_dataset(self):
        tk = RandomUnderSampler(sampling_strategy={1: 100}, replacement=True)