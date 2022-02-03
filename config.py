import copy
import json
import queue
import multiprocessing as mp

from matplotlib.cbook import index_of

def load_config_file(configFile):
    with open(configFile, "r", newline='') as jsonFile:
        try:
            configData = json.load(jsonFile)
            return configData, None
        except Exception as exc:
            return None, exc

def validate_config(config):
    data, exc = config
    if not exc is None:
        print(exc)
        return None
    else:
        #requires keys (cores, variables and command)
        #cores must be integer value x, such that 1<=x<=max cores
        if not "cores" in data.keys():
            print("cores information missing")
            return None
        else:
            if isinstance(data["cores"], int) and data["cores"] >=1:
                data["cores"] = min(data["cores"], mp.cpu_count())
            else:
                print("cores must be a positive integer")
                return None
        #variables
        if not "variables" in data.keys():
            print("variables section missing")
            return None
        elif not isinstance(data["variables"], dict):
            print("variables information missing")
            return None
        else:
            var_erros = []
            for k,v in data["variables"].items():
                if not (isinstance(v, int) or (isinstance(v, list) and all(isinstance(e, (int, float)) for e in v))):
                    var_erros.append(k)
            if len(var_erros) > 0:
                print(f"the value of the variables must be a numeric or list of numeric: check the value of the variable(s) {', '.join(var_erros)}")
                return None
    return data

def get_custom_command_line(commandLine, varConfiguration):
    new_commandLine = commandLine
    for k,v in varConfiguration.items():
        if f"${k}" in new_commandLine:
            new_commandLine = new_commandLine.replace(f"${k}", str(v))
    return new_commandLine


def generate_variables_combination(configvars):
    particalConfig = queue.Queue()
    finalConfig = []
    particalConfig.put(configvars)
    while not particalConfig.empty():
        current = particalConfig.get()
        varList = get_ket_variable_listdata(current)
        if varList is None:
            finalConfig.append(current)
        else:
            for v in current[varList]:
                partialCopy = copy.copy(current)
                partialCopy[varList] = v
                particalConfig.put(partialCopy)
    return finalConfig
        
def get_ket_variable_listdata(parconfig):
    for k,v in parconfig.items():
        if isinstance(v, list):
            return k
    return None

def load_config_data(fileName):
    configData = load_config_file("coresconfig.json")
    data = validate_config(configData)
    if not data is None:
        varConfig = generate_variables_combination(data["variables"])
        config = {}
        config["cores"] = data["cores"]
        config["customCommand"] = [get_custom_command_line(data['command'], vc) for vc in varConfig]
        return config
    return None