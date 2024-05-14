from sklearn.preprocessing import StandardScaler
from prediction_models.models.text_input import TextModel
from prediction_models.models.select import SelectModel
from prediction_models.models.sklearn_model import SklearnModel
from prediction_models.models.anchors import AnchorModel

import pickle
import os

class PredictionModels:

    def __init__(self):
        if os.path.exists(os.path.join(os.path.realpath(os.path.dirname(__file__)),'db/models.pickle')):
            self.load_models_from_file('models.pickle')

    def load_models_from_file(self, filename):
        self.models = pickle.load(open(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'db', filename), 'rb'))

    def train_widget_model(self, className, dataFileName, excluded_features):
        processor = className()
        processor.load_dataset(dataFileName, excluded_features)
        model = processor.create_model()
        model.scaler = StandardScaler()
        model.scaler.fit(processor.x)
        x_normalized = model.scaler.transform(processor.x)
        model.fit(x_normalized, processor.y)
        return model

    common_features_excluded = ["widgetType", "hoverAndBack", "exitAndBack", "label", "id"]

    features_excluded = {
        "TextInput": ["enteredText"],
        "SelectInput": ["optionsCount"],
        "RadioSet": ["optionsCount"],
        "DateSelect": ["optionsCount", "interactions", "optionsSelected"],
        "Anchor": ["misclicks"]   
    }

    def train_models(self):
        text_model = self.train_widget_model(TextModel, os.path.join(os.path.realpath(os.path.dirname(__file__)),"training/TextInput.csv"),self.common_features_excluded + ["enteredText"])
        select_model = self.train_widget_model(SelectModel,os.path.join(os.path.realpath(os.path.dirname(__file__)),"training/SelectInput.csv"),self.common_features_excluded + ["optionsCount"])
        radio_model = self.train_widget_model(SklearnModel,os.path.join(os.path.realpath(os.path.dirname(__file__)),"training/RadioSet.csv"),self.common_features_excluded + ["optionsCount"])
        date_select_model = self.train_widget_model(SklearnModel,os.path.join(os.path.realpath(os.path.dirname(__file__)),"training/DateSelect.csv"),self.common_features_excluded + ["optionsCount"])
        anchor_model = self.train_widget_model(AnchorModel,os.path.join(os.path.realpath(os.path.dirname(__file__)),"training/Anchor.csv"),self.common_features_excluded + ["misclicks"])

        self.models = {
            "TextInput": text_model,
            "SelectInput": select_model,
            "RadioSet": radio_model,
            "DateSelect": date_select_model,
            "Anchor": anchor_model   
        }
        pickle.dump(self.models, open( os.path.join(os.path.realpath(os.path.dirname(__file__)),'db/models.pickle'), 'wb')) 
    
    def get_widget_model(self, widget_name):
        return self.models[widget_name]

prediction_models = PredictionModels()