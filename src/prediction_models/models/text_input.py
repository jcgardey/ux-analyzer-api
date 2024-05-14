from .sklearn_model import SklearnModel
from imblearn.under_sampling import RandomUnderSampler


class TextModel(SklearnModel):

    def clean_dataset(self):
        self.dataset = self.dataset[self.dataset.focusTime != 0]
        tk = RandomUnderSampler(sampling_strategy={1: 120}, replacement=True)
        self.x, self.y = tk.fit_resample(self.x, self.y)
        self.y = self.y.reshape(-1,1)
        pass

    def clean_oversampled_data(self, oversampled_dataset):
        oversampled_dataset.inputSwitches = oversampled_dataset.inputSwitches // 1
        oversampled_dataset.correctionAmount = oversampled_dataset.correctionAmount // 1
        return super().clean_oversampled_data(oversampled_dataset)