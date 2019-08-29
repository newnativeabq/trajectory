from joblib import load
import pandas as pd
import numpy as np

class models():
    def __init__(self):
        self.bmi_model = self.load_model(model_path='assets/bmi_model.joblib')
        self.general_health_model = self.load_model(model_path='assets/gen_health_model.joblib')
        self.model_status = 'Loading'

    def load_model(self, model_path):
        try:
            model = load(model_path)
            self.model_status = 'Models Ready'
            print('Model Loaded Successfully')
            return model
        except FileNotFoundError:
            print('Model not found.  Please contact administrator.')
        except NameError:
            print('joblib Load Module not defined')

class data():
    def __init__(self):
        self.default_data= None
        self.model_data = None
        self.user_data = None
        self.data_status = None
        self.set_default_data() #'default' or 'user' for each variable

    def get_data(self, data_name):
        return np.array([list(self.model_data[data_name].values())])

    def update_user_data(self, data_to_update):
        pass
    
    def get_model_names_if_key(self, data_to_check):
        assert type(data_to_check) == dict

        valid_keys = []
        if list(data_to_check.keys())[0] in self.model_data['bmi_data']:
            valid_keys.append('bmi_data')
        if list(data_to_check.keys())[0] in self.model_data['general_health_data']:
            valid_keys.append('general_health_data')
        
        return valid_keys


    def update_model_data(self, data_to_update):
        assert type(data_to_update) == dict

        model_keys = self.get_model_names_if_key(data_to_update)

        for model_key in model_keys:
            for model_var, new_val in data_to_update.items():
                self.model_data[model_key][model_var] = new_val

    def set_default_data(self, models='all'):
        self.default_data = {}
        
        default_bmi_data_path = 'assets/default_bmi_data.csv'
        default_general_health_data_path = 'assets/default_gen_health_data.csv'

        self.default_data['bmi_data'] = self.load_data(path=default_bmi_data_path)
        self.default_data['general_health_data'] = self.load_data(path=default_general_health_data_path)

        self.model_data = self.default_data
        self.strip_target(self.model_data['bmi_data'], 'bmi')
        self.strip_target(self.model_data['general_health_data'], 'general_health')


    def strip_target(self, data, target):
        try:
            del data[target]
        except:
            print('Could not strip target from [{}]'.format(target))

    def load_data(self, path):
        df = pd.read_csv(path, header=None, names=['variable', 'median_value'])
        default_dict = {}
        for i in range(len(df)):
            default_dict[df.iloc[i][0]] = df.iloc[i][1] 
        return default_dict