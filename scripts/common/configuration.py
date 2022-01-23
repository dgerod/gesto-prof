import os
from pathlib import Path
import yaml


class Configuration:

    _TOOL_NAME = 'gesto-prof'
    _CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    _ROOT_DIRECTORY = '.gesto-prof'
    _TEMP_DIRECTORY = os.path.join(_ROOT_DIRECTORY, '_tmp_')
    _SETTINGS_FILE = os.path.join(_ROOT_DIRECTORY, 'settings.yaml')
    _TEMPLATES_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(_CURRENT_DIRECTORY)),
                                        'templates')
    
    def __init__(self):

        self._work_directory = self._find_directory()
        self._configuration_file = os.path.join(self._work_directory, self._SETTINGS_FILE)
        self._tmp_directory = os.path.join(self._work_directory, self._TEMP_DIRECTORY)

        self._data_directory, self._inputs_directory, \
            self._output_directory = self._load_directories()

        self._templates_directory = self._TEMPLATES_DIRECTORY

    def get_temp_directory(self):
        return self._tmp_directory
    
    def get_db_directory(self):
        return os.path.join(self._data_directory, 'gp-db')

    def get_outputs_directory(self):
        return self._output_directory

    def get_inputs_directory(self):
        return self._inputs_directory

    def get_templates_directory(self):
        return self._templates_directory

    def _load_directories(self):
            
        if not os.path.exists(self._configuration_file):
            raise NotADirectoryError('No existe el fichero de configuration')
            
        with open(self._configuration_file, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
                data_directory = data['db_path']
                inputs_directory = data['inputs_dir']
                output_directory = data['output_dir']

            except yaml.YAMLError as ex:
                raise
    
        return data_directory, inputs_directory, output_directory

    def _find_directory(self):
        """
        Search directory where app stores all the information
        """
    
        directory = ""
        current_directory = os.getcwd()
        
        found = False
        checking = True
        while checking and not found:

            found = Path(os.path.join(current_directory, Configuration._ROOT_DIRECTORY)).is_dir()
            
            if found:                
                directory = current_directory                                
            else:
                previous_directory = current_directory
                current_directory = os.path.dirname(current_directory)
                checking = current_directory != previous_directory
                        
        if not found:
            raise NotADirectoryError('Directory not ready to work with %s' %
                                     self._TOOL_NAME)
    
        return directory

