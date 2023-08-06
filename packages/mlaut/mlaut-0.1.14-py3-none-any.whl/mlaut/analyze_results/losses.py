

import collections
import numpy as np
import pandas as pd
import logging

class Losses(object):
    """
    Calculates prediction losses on test datasets achieved by the trained estimators. When the class is instantiated it creates a dictionary that stores the losses.

    Args:
        metric(`mlaut.analyze_results.scores` object): score function that will be used for the estimation. Must be `mlaut.analyze_results.scores` object.
        estimators(`array of mlaut estimators`): Array of estimators on which the results will be compared.
        exact_match(Boolean): If `True` when predictions for all estimators in the estimators array is not available no evaluation is performed on the remaining estimators. 
    """

    def __init__(self, metric, estimators, exact_match):

        self._losses = collections.defaultdict(list)
        self._metric = metric
        self._errors_per_estimator = collections.defaultdict(list)
        self._errors_per_dataset_per_estimator = collections.defaultdict(list)
        self._estimators = estimators
        self._estimator_names = [estimator.properties['name'] for estimator in estimators]
        self._exact_match=exact_match


    def evaluate(self, predictions, true_labels, dataset_name):
        """
        Calculates the loss metrics on the test sets.

        Args:
            predictions(2d numpy array): Predictions of trained estimators in the form [estimator_name, [predictions]]
            true_labels(numpy array): true labels of test dataset.
            dataset_name(string): Name of the dataset.
            
        """
        #check exact match
        exact_match_errors = 0
        if self._exact_match:
            estimators_predeictions_names = [name[0] for name in predictions]
            for e in self._estimators:
                estimator_name = e.properties['name']
                
                if estimator_name not in estimators_predeictions_names:
                    logging.warning(f'Predictions for estimator {estimator_name} unavailable for dataset: {dataset_name}. Analyse Results will skip {dataset_name}.')
                    exact_match_errors +=1

        if exact_match_errors == 0:
            for prediction in predictions:
                #evaluates error per estimator
                estimator_name = prediction[0]
                estimator_predictions = prediction[1]

                if estimator_name in self._estimator_names:     
                    loss=0
                    loss = self._metric.calculate(true_labels, estimator_predictions)

                    
                    self._errors_per_estimator[estimator_name].append(loss)

                    #evaluate errors per dataset per estimator
                    errors = (estimator_predictions - true_labels)**2
                    errors = np.where(errors > 0, 1, 0)
                    n = len(errors)

                    std_score = np.std(errors)/np.sqrt(n) 
                    sum_score = np.sum(errors)
                    avg_score = sum_score/n
                    self._errors_per_dataset_per_estimator[dataset_name].append([estimator_name, avg_score, std_score])
        
    #TODO Check if this is being used somewhere.
    # def evaluate_per_dataset(self, 
    #                         predictions, 
    #                         true_labels, 
    #                         dataset_name):

    #     """
    #     Calculates the error of an estimator per dataset.
        
    #     Parameters
    #     ----------
    #     predictions (array): 2d array-like in the form [estimator name, [estimator_predictions]].
    #     true_labels (array): 1d array-like
        
    #     """
    #     estimator_name = predictions[0]
    #     estimator_predictions = np.array(predictions[1])
    #     errors = (estimator_predictions - true_labels)**2
    #     n = len(errors)

    #     std_score = np.std(errors)/np.sqrt(n) 
    #     sum_score = np.sum(errors)
    #     avg_score = sum_score/n
    #     self._losses[dataset_name].append([estimator_name, avg_score, std_score])

    def get_losses(self):
        """
        When the Losses class is instantiated a dictionary that holds all losses is created and appended every time the evaluate() method is run. This method returns this dictionary with the losses.

        Returns
        -------
            errors_per_estimator (dictionary), errors_per_dataset_per_estimator (dictionary), errors_per_dataset_per_estimator_df (pandas DataFrame): Returns dictionaries with the errors achieved by each estimator and errors achieved by each estimator on each of the datasets.  ``errors_per_dataset_per_estimator`` and ``errors_per_dataset_per_estimator_df`` return the same results but the first object is a dictionary and the second one a pandas DataFrame. ``errors_per_dataset_per_estimator`` and ``errors_per_dataset_per_estimator_df`` contain both the mean error and deviation.
        """ 
        return (self._errors_per_estimator, 
                self._errors_per_dataset_per_estimator,
                self._losses_to_dataframe(self._errors_per_dataset_per_estimator))

    def _losses_to_dataframe(self, losses):
        """
        Reformats the output of the dictionary returned by the :func:`mlaut.analyze_results.losses.Losses.get_losses` to a pandas DataFrame. This method can only be applied to reformat the output produced by :func:`mlaut.analyze_results.Losses.evaluate_per_dataset`.

        Parameters
        ----------

        losses: dictionary returned by the :func:`mlaut.analyze_results.losses.Losses.get_losses` generated by :func:`mlaut.analyze_results.losses.Losses.evaluate_per_dataset`
        """

        df = pd.DataFrame(losses)
        #unpivot the data
        df = df.melt(var_name='dts', value_name='values')
        df['classifier'] = df.apply(lambda raw: raw.values[1][0], axis=1)
        df['loss'] = df.apply(lambda raw: raw.values[1][1], axis=1)
        df['std_error'] = df.apply(lambda raw: raw.values[1][2], axis=1)
        df = df.drop('values', axis=1)
        #create multilevel index dataframe
        dts = df['dts'].unique()
        estimators_list = df['classifier'].unique()
        score = df['loss'].values
        std = df['std_error'].values
        
        df = df.drop('dts', axis=1)
        df=df.drop('classifier', axis=1)
        
        df.index = pd.MultiIndex.from_product([dts, estimators_list])

        return df.round(5)
