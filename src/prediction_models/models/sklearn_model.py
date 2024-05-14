from .widget_model import WidgetModel
from sklearn.tree import DecisionTreeRegressor, export_graphviz
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics


class SklearnModel(WidgetModel):

    def clean_dataset(self):
        pass
        
    def create_model(self):
        self.model = self.create_decision_tree()
        return self.model
    
    def fit(self, model, x, y, epochs=None, batch_size=None, class_weight=None):
        model.fit(x, y)
    
    def predict(self, x):
        x_normalized = self.scaler.transform(x)
        return self.model.predict(x_normalized)
    
    def evaluate(self, model, x, y):
        print(model.feature_importances_)
        y_pred = model.predict(x)
        return [metrics.mean_absolute_error(y_pred,y), metrics.mean_squared_error(y_pred,y), metrics.r2_score(y,y_pred)]
    
    def get_metrics_names(self):
        return ["MAE", "MSE", "R^2"]

    def create_decision_tree(self):
        return DecisionTreeRegressor(min_samples_leaf=10,max_depth=4)
    
    def create_random_forest(self):
        return RandomForestRegressor(n_estimators=100, max_depth=5, max_features='sqrt')



    


