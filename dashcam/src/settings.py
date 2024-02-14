
class Settings:
    def __init__(self, file="settings.txt") -> None:
        self.settings_file = file

    def write_setting(self,setting, value):
        try:
            with open(self.settings_file, 'w') as file:
                for line in file:
                    if line.startswith(setting):
                        file.write(f"{setting}={value}\n")
                        return value # find the first instance of the setting and replace it with the new value
                    else:
                        file.write(line) #? may need to add a newline character
            return None # if the setting is not found, return None
        
        except OSError: # if the file is locked or something 
            print(f"Error writing to file {setting}")
            return None
            
    def read_setting(self,setting):
        try:
            with open(self.settings_file, 'r') as file:
                for line in file:
                    if line.startswith(setting):
                        return line.split("=")[1].strip() # find the first instance of the setting and return the value
            return None
        
        except OSError: # if the file is locked or something
            print(f"Error reading from file {setting}")
            return None
