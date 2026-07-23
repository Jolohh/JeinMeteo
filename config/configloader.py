import configparser
import os


BASE_DIR = os.path.abspath(".")

default_config = BASE_DIR+"/config/defaultconfig.ini"
user_config = BASE_DIR+"/config/config.ini"



class ConfigLoader:
    def __init__(self,section):
        self.section = section
        self.config = configparser.ConfigParser()
        self.config.read([default_config,user_config])
        
    
    def load(self):
        for key in self.config[f"{self.section}"]:
            if self.config[f"{self.section}"][key] == None:
                self.add_value(key)
        return self.config[f"{self.section}"]
    
    
    def load_dict(self):
        return dict(self.load())
    
    
    def add_value(self,key):
        value = input(f"Bitte den Wert für {key} initialisieren: ")
        self.config.set(f"{self.section}",key,value)


