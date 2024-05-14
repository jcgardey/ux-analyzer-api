from .sklearn_model import SklearnModel
from imblearn.under_sampling import RandomUnderSampler

class SelectModel(SklearnModel):

    def clean_dataset(self):
        tk = RandomUnderSampler(sampling_strategy={1: 100}, replacement=True)
        self.x, self.y = tk.fit_resample(self.x, self.y)
        self.y = self.y.reshape(-1,1)