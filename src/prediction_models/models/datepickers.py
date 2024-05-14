
from .sklearn_model import SklearnModel

class DatepickerRegressor(SklearnModel):

    def clean_oversampled_data(self, oversampled_dataset):
        oversampled_dataset.clicks = oversampled_dataset.clicks // 1
        oversampled_dataset.selections = oversampled_dataset.selections // 1
        return super().clean_oversampled_data(oversampled_dataset)