POOL_ADDRESS = "REMOVED_DGB_ADDRESS"

class Config:
    def __init__(self):
        self.settings = {}
        self.config_file = "/root/.digibyte/digibyte.conf"

    def load(self):
       	with open(self.config_file, "r") as config_file:
            for line in config_file:
                line = line.strip() 

                if line == "":
                    continue

                if line.startswith("#"):
                    continue

                parts = line.split("=",1)
                self.settings[parts[0]] = parts[1]


    def get(self, key):
        return self.settings[key]

