

################################################################################
#################                    Model                     #################
################################################################################

from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, BaggingRegressor
from sklearn.cross_decomposition import PLSRegression
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import SCORERS
from sklearn.exceptions import UndefinedMetricWarning
from difflib import get_close_matches
import numpy as np
import inspect
import os
import pickle

from .evaluate import Evaluate

class Model():
    """
    Class for building, fitting and training a various range of predictive
    regression models and all their related methods and attributes.

    Attributes
    ----------
    algorithm : str
        sklearn regression algorithm to build and fit model with.
    parameters : dict (default = {})
        parameters to use for building regression model, by default the models'
        default parameters are used.
    test_split : float (default = 0.2)
        size of the test data.

    Methods
    -------
    get_model():

    train_test_split(X, Y, scale = True, test_size = 0.2,random_state=None, shuffle=True):

    fit():

    predict():

    save(save_folder):

    copy():

    hyperparameter_tuning(parameters, metric='r2', cv=5):

    model_fitted():

    """
    def __init__(self, algorithm,parameters={}):

        self.algorithm = algorithm
        self.parameters = parameters
        self.test_split = None

        #list of valid models available to use for this class
        self.valid_models = ['PlsRegression','RandomForestRegressor','AdaBoostRegressor',\
                            'BaggingRegressor','DecisionTreeRegressor','LinearRegression',\
                            'Lasso','SVR','KNeighborsRegressor', 'KNN']

        #get closest match of valid model from the input algorithm parameter value
        model_matches = get_close_matches(self.algorithm.lower(),[item.lower() \
            for item in self.valid_models], cutoff=0.4)

        #if algorithm is a valid model then set it to self.algorithm, else raise error
        if model_matches!=[]:
            self.algorithm = model_matches[0]
        else:
            raise ValueError('Input algorithm {} not found in available valid \
                models {}.'.format(self.algorithm, self.valid_models))

        #create instance of algorithm object
        self.model = self.get_model()
        self.model_fit = None

    def get_model(self):
        """
        Create instance of model type specifed by input 'algorithm' argument. If
        parameters input 'parameters' = {} then default parameters are used else set
        the parameters of the model to the values specified in the 'parameters' input
        parameter.

        Returns
        -------
        model : sklearn.model
            instantiated regression model with default or user-specified parameters.
        """
        if self.algorithm.lower() == 'plsregression':

            #get parameters of sklearn model and check that user inputted
            #  parameters are available in the model, only use those that are valid.
            model_params = set(dir(PLSRegression()))
            parameters = [i for i in model_params if i in self.parameters]

            #use default model parameters if user input parameters is empty, else
            #   use user-specified parameters.
            if parameters != {}:
                model = PLSRegression(**self.parameters)
            else:
                model = PLSRegression()

        elif self.algorithm.lower() == 'randomforestregressor':

            model_params = set(dir(RandomForestRegressor()))
            parameters = [i for i in model_params if i in self.parameters]

            if parameters != {}:
                model = RandomForestRegressor(**self.parameters)
            else:
                model = RandomForestRegressor()

        elif self.algorithm.lower() == 'adaboostregressor':

            model_params = set(dir(AdaBoostRegressor()))
            parameters = [i for i in model_params if i in self.parameters]

            if parameters != {}:
                model = AdaBoostRegressor(**self.parameters)
            else:
                model = AdaBoostRegressor()

        elif self.algorithm.lower() == 'baggingregressor':

            model_params = set(dir(BaggingRegressor()))
            parameters = [i for i in model_params if i in self.parameters]

            if parameters != {}:
                model = BaggingRegressor(**self.parameters)
            else:
                model = BaggingRegressor()

        elif self.algorithm.lower() == 'decisiontreeregressor':

            model_params = set(dir(DecisionTreeRegressor()))
            parameters = [i for i in model_params if i in self.parameters]

            if parameters != {}:
                model = DecisionTreeRegressor(**self.parameters)
            else:
                model = DecisionTreeRegressor()

        elif self.algorithm.lower() == 'linearregression':

            model_params = set(dir(LinearRegression()))
            parameters = [i for i in model_params if i in self.parameters]

            if parameters != {}:
                model = LinearRegression(**self.parameters)
            else:
                model = LinearRegression()

        elif self.algorithm.lower() == 'lasso':

            model_params = set(dir(Lasso()))
            parameters = [i for i in model_params if i in self.parameters]

            if parameters != {}:
                model = Lasso(**self.parameters)
            else:
                model = Lasso()

        elif self.algorithm.lower() == 'svr':

            model_params = set(dir(SVR()))
            parameters = [i for i in model_params if i in self.parameters]

            if parameters != {}:
                model = SVR(**self.parameters)
            else:
                model = SVR()

        elif self.algorithm.lower() == 'knn' or \
           self.algorithm.lower() == 'kneighborsregressor':

            model_params = set(dir(KNeighborsRegressor()))
            parameters = [i for i in model_params if i in self.parameters]

            if parameters != {}:
                model = KNeighborsRegressor(**self.parameters)
            else:
                model = KNeighborsRegressor()
        else:
            raise ValueError('Input Algorithm ({}) not found in available valid \
                models'.format(self.algorithm, self.valid_models))

        return model

    def train_test_split(self, X, Y, scale = True, test_size = 0.2,
        random_state=None, shuffle=True):
        """
        Split the X and Y input features and labels into random train and test
        subsets. By default a 80:20 split will be used, whereby 80% of the data
        will be used for training and 20% for testing. By default the input will
        be scaled first such that the mean is removed and features scaled to unit
        variance. By default data is shuffled before the split and random is None.

        Parameters
        ----------
        X : np.ndarray
            array of feaure data.
        Y : np.ndarray
            array of observed label values.
        scale : bool (default = True)
            if true then scale the features such that they are standardised.
        test_size : float (default = 0.2)
            proportion of the total dataset to use for testing.
        random_state : float (default = None)
            Controls the shuffling applied to the data before applying the split.
            Popular integer random seeds are 0 and 42.
        shuffle : bool (default = True)
            Whether or not to shuffle the data before splitting.

        Returns
        -------
        self.X_train, self.X_test, self.Y_train, self.Y_test : np.ndarray
            splitted training and test data features and labels.
        """
        #validate that X and Y arrays are of the same size
        if (len(X)!=len(Y)):
            raise ValueError('X and Y input parameters must be of the same length.')

        #reshape input arrays to 2D arrays
        if (X.ndim!=2):
            X = np.reshape(X, (-1,1))
        if (Y.ndim!=2):
            Y = np.reshape(Y, (-1,1))

        #if invalid test size input then set to default 0.2
        if (test_size <= 0 or test_size >=1):
            test_size = 0.2

        self.test_split = test_size     #setting test_size attribute

        #scale X
        if scale:
            X = StandardScaler().fit_transform(X)

        #split X and Y into training and test data
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y,
            test_size=test_size, random_state=random_state, shuffle=shuffle)

        #set X and Y attributes
        self.X_train = X_train
        self.X_test = X_test
        self.Y_train = np.reshape(Y_train, (len(Y_train),))
        self.Y_test = np.reshape(Y_test, (len(Y_test),))

        return self.X_train, self.X_test, self.Y_train, self.Y_test

    def fit(self):
        """
        Fit model to training data and target values X and Y.

        Returns
        -------
        self.model_fit : np.ndarray
            fitted sklearn model of type specified by algorithm attribute.
        """
        self.model_fit = self.model.fit(self.X_train, self.Y_train)
        return self.model_fit

    def predict(self):
        """
        Predict the target values of unseen test data using the model.

        Returns
        -------
        self.model_fit.predict(self.X_test) : np.ndarray
            array of predicted target values for unseen test data.
        """
        return self.model_fit.predict(self.X_test)

    def save(self, save_folder):
        """
        Save fitted model to specified save_folder.

        Parameters
        ----------
        save_folder : str
            folder to save model to.
        """
        save_path = os.path.join(save_folder, 'model.pkl')

        try:
            with open(save_path, 'wb') as file:
                pickle.dump(self.model, file)
        except (IOError, OSError, pickle.PickleError, pickle.UnpicklingError):
            print("Error pickling model with path: {} ".format(save_path))

    def hyperparameter_tuning(self, parameters, metric='r2', cv=5):
        """
        Hyperparamter tuning of model to find its optimal arrangment of parameters
        using a Grid Search.

        Parameters
        ----------
        parameters : dict
            dictionary of parameter names and their values.
        metric : str (default = r2)
            scoring metric used to evaluate the performance of the cross-validated
            model on the test set.
        cv : int (default = 5)
            Determines the cross-validation splitting strategy.

        Returns
        -------
        metrics_df: pd.DataFrame
            dataframe of best results and the associated parameters from the
            hyperparameter tuning process.
        """
        #input parameters parameter must be a dict, if not raise error
        if not isinstance(parameters, dict):
            raise TypeError('Parameters argument must be of type dict.')

        #input metric must be in available scoring metrics, if not raise error
        if metric not in sorted(SCORERS.keys()):
            raise UndefinedMetricWarning('Invalid scoring metric, \
                {} not in available Sklearn Scoring Metrics: {}\n'.format(
                    metric, SCORERS.keys()))

        #cv must be of type int and be between 5 and 10, if not then default of 5 is used
        if not (isinstance(cv, int)) or (cv<5 or cv>10):
            cv = 5

        #iterate through all parameter names to check if they are correct for model
        #   if parameter not found in model params then delete from dictionary
        for p in list(parameters.keys()):
            if p not in (list(self.model.get_params().keys())):
                del parameters[p]

        #grid search of hyperparameter space for model
        model_copy = self.copy()
        grid_search = GridSearchCV(estimator=model_copy, param_grid=parameters,\
            n_jobs=-1, cv=cv, scoring=metric,error_score=0)

        #fit X and Y to best model found in grid search
        grid_result = grid_search.fit(self.X_train, self.Y_train)

        #get best grid search metics values
        mean_test = grid_result.cv_results_['mean_test_score']
        std_test = grid_result.cv_results_['std_test_score']
        params = grid_result.cv_results_['params']

        #predict values of unseen test data
        best_model_pred = grid_result.predict(self.X_test)

        #create instance of Evaluate class and calculate metrics from best model
        eval = Evaluate(self.Y_test,best_model_pred)

        #print out results of grid search
        print('\n#############################################################')
        print('#################### Hyperparamter Results ####################')
        print('#############################################################\n')

        print('######################### Parameters ########################\n')
        print('# Best Params -> {}'.format(grid_result.best_params_))
        print('# Model Type -> {}'.format(repr(self)))
        print('# Scoring Metric -> {}'.format(metric))
        print('# CV -> {}'.format(cv))
        print('# Test Split -> {}'.format(self.test_size))

        print('########################## Metrics ###########################\n')
        print('# Best Score -> {}'.format(grid_result.best_score_))
        print('# RMSE: {} '.format(eval.rmse))
        print('# MSE: {} '.format(eval.mse))
        print('# MAE: {}'.format(eval.mae))
        print('# RPD {}'.format(eval.rpd))
        print('# Variance {}\n'.format(eval.explained_var))
        print('###############################################################')

    def copy(self):
        """
        Make a copy of the sklearn model stored in self.model instance variable.

        Returns
        -------
        model_copy : sklearn.model
            deep copy of model.
        """
        model_copy = self.model
        return model_copy

    def model_fitted(self):
        """
        Return if model has been fitted, true or false.

        Returns
        -------
        True/False : bool
            true if model (self.model) has been fitted, false if not.
        """
        return (self.model_fit != None)

######################          Getters & Setters          ######################

    @property
    def test_split(self):
        return self._test_split

    @test_split.setter
    def test_split(self, val):
        self._test_split = val

    @property
    def valid_models(self):
        return self._valid_models

    @valid_models.setter
    def valid_models(self,val):
        self._valid_models = val

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self,val):
        self._parameters = val

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self,val):
        self._algorithm = val

    @property
    def model_fit(self):
        return self._model_fit

    @model_fit.setter
    def model_fit(self,val):
        self._model_fit = val

    @property
    def valid_models(self):
        return self._valid_models

    @valid_models.setter
    def valid_models(self,val):
        self._valid_models = val

################################################################################

    def __str__(self):
        return "Model of type {} using {} parameters, model fit = {}".format(
            type(self.model).__name__, self.parameters, self.modelFitted())

    def __repr__(self):
        return type(self.model).__name__

    def __sizeof__(self):
        """ Get size of sklearn model """
        return self.model.__sizeof__()
