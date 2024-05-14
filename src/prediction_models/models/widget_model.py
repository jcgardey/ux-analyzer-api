import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import  RepeatedStratifiedKFold


class WidgetModel:

    def load_dataset(self, filename, ignored_metrics):
        dataset = pd.read_csv(filename)
        dataset.drop(ignored_metrics, axis=1, inplace=True)
        self.dataset = dataset.dropna()
        self.x, self.y = self.get_dataset_values(self.dataset)
        self.clean_dataset()

    def clean_dataset(self):
        pass

    def save_dataset(self, filename):
        self.dataset.to_csv(os.path.join(
            os.getcwd(), filename), index=False)

    def get_minority_rating_count(self, y):
        count_per_rating = np.unique(y[:, -1], return_counts=True)
        return np.min(count_per_rating[1])

    def get_dataset_values(self, dataset):
        return dataset.values[:, 0:-1], dataset.values[:, -1:]

    def split_training_test(self):
        porc_test = 0.25
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.x, self.y, test_size=porc_test)

    def get_testing_dataset(self):
        return self.convert_values_to_dataset(self.x_test, self.y_test)

    def convert_values_to_dataset(self, x, y):
        return pd.DataFrame(np.concatenate((x, y), axis=1), columns=self.dataset.columns)

    def oversample_data(self, x, y):
        # Oversampling
        sm = SMOTE(sampling_strategy='minority', k_neighbors=(self.get_minority_rating_count(y) - 1))
        x_oversampled, y_oversampled = sm.fit_resample(x, y)
        return self.clean_oversampled_data(x_oversampled, y_oversampled)

    def clean_oversampled_data(self, x, y):
        #oversampled_dataset.interactions = oversampled_dataset.interactions // 1
        return x, y

    def normalize_data(self, fit_set, target_set):
        # Normalizar
        scaler = StandardScaler()
        scaler.fit(fit_set)
        return scaler.transform(target_set)

    def create_model(self):
        pass

    def fit(self, x, y, epochs=None, batch_size=None, class_weight=None):
        pass

    def evaluate(self, model, x, y):
        pass

    def get_metrics_names(self):
        pass

    def get_features_names(self):
        column_names = self.dataset.columns.values.tolist()
        return column_names[:-1]

    def print_results(self, results, message):
        print(message)
        for i, result in enumerate(results):
            print("%s: %s" % (self.get_metrics_names()[i], result))
    

    def rating_count(self):
        return np.unique(self.y, return_counts=True)

    def cross_validation(self, n_splits=5, n_repeats=10, epochs=30, batch_size=10, verbose=0, shuffle=True, class_weight=None):

        #kfold = StratifiedKFold(n_splits=n_splits, shuffle=shuffle)
        kfold = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats)
        fold_number = 1
        final_result, per_rating_result = None, None
        ratings = np.unique(self.y[:, -1])
        features_importance = np.zeros(self.x.shape[1])
        for train_index, val_index in kfold.split(self.x, self.y):
            print("Runing FOLD %s" % fold_number)
            x_train = self.x[train_index]
            y_train = self.y[train_index]
            x_test = self.x[val_index]
            y_test = self.y[val_index]

            #x_train, y_train = self.oversample_data(x_train, y_train)
            #x_test, y_test = self.oversample_data(x_test, y_test)
            #y_test = y_test.reshape(-1, 1)

            sd = StandardScaler()
            sd.fit(x_train)
            x_train = sd.transform(x_train)
            x_test = sd.transform(x_test)
            model = self.create_model()
            self.fit(model, x_train, y_train, epochs=epochs,
                     batch_size=batch_size, class_weight=class_weight)
            features_importance += model.feature_importances_         
            training_result = self.evaluate(model, x_train, y_train)
            self.print_results(training_result, "Training")
            fold_i_result = self.evaluate(model, x_test, y_test)
            self.print_results(fold_i_result, "Testing")
            if final_result is None:
                final_result = np.array(fold_i_result)
                final_result_per_rating = np.zeros((len(ratings), len(final_result)))
            else:
                final_result += fold_i_result
            #self.plot_differences(model,x_test, y_test, "Fold %s" % fold_number)
            """
            # evaluate each rating samples separately
            for rating in ratings:
                rating_i = y_test[:, -1] == rating
                x_test_rating_i = x_test[rating_i]
                y_test_rating_i = y_test[rating_i]
                rating_result = self.evaluate(
                    model, x_test_rating_i, y_test_rating_i)
                self.print_results(rating_result, "Rating %s (%s muestras)" % (
                    rating, x_test_rating_i.shape[0]))
                final_result_per_rating[int(rating - 1), :] += rating_result"""
            fold_number += 1  
        self.print_results(final_result / (n_splits * n_repeats), "FINAL RESULT")
        print(self.dataset.columns)
        print(features_importance / (n_splits * n_repeats))
        """
        for rating in ratings:
            self.print_results( final_result_per_rating[int(rating - 1),:] / (n_splits * n_repeats), "FINAL RESULT RATING %s" % rating)"""

    def plot_differences(self, model, x, y, tag):
        y_pred = model.predict(x)
        plt.figure(tag)
        xvalues = np.array(range(len(y)))
        plt.scatter(xvalues, y_pred, label="Prediction")
        plt.scatter(xvalues, y, label="Ground Truth")
        plt.xlabel("Sample")
        plt.ylabel("Prediction")
        plt.legend()
        plt.title(f"Subset: {tag}")
        plt.show()
    

    def plot_scatter_matrix(self):
        colormap = np.array(["red","blue","green"])
        colors=colormap[self.y.reshape(-1).astype(int)-1]
        pd.plotting.scatter_matrix(self.dataset,figsize=(20,20),c=colors)
        plt.show()
    
    def plot(self, x, y, rating, title='', xlabel='', ylabel=''):
        colormap = np.array(["red","blue","green"])
        colors=colormap[rating.reshape(-1).astype(int)-1]
        plt.scatter(x, y, c=colors, label=colors)

        score_1 = mpatches.Patch(color='red', label='1')
        score_2 = mpatches.Patch(color='blue', label='2')
        score_3 = mpatches.Patch(color='green', label='3')

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(handles=[score_1,score_2,score_3])

        #plt.legend()
        plt.show()
    
    def boxplot(self):
        fig, axs = plt.subplots(2,3)

        #scaler = StandardScaler()
        #df_normalized = pd.DataFrame(scaler.fit_transform(self.dataset), columns=self.dataset.columns)
        
        boxplots = self.dataset.boxplot(column=["mouseDwellTime"], by=['rating'], showfliers=False, grid=False, ax=ax, patch_artist=True)
        #ax.set_yscale('log')
        ax.set_title("Text Input")
        ax.set_ylabel("Mouse Dwell Time (ms)")
        ax.set_xlabel("Rating")
        fig.suptitle('')
        plt.show()



        
