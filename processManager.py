import config
import argparse                                                               
import subprocess as sp
import multiprocessing as mp

def create_parser():
    parser = argparse.ArgumentParser(prog = "processManager")
    parser.add_argument("-c", "--configFile", type = str, default = "coresconfig.json")
    return parser

def execute(customCommand):
    print(f"custom command {customCommand}")                                                            
    sp.call(customCommand)                                       

def main():
    parser = create_parser()
    args = parser.parse_args()
    configData = config.load_config_data(args.configFile)
    if not configData is None: 
        mp.freeze_support()
        process_pool = mp.Pool(processes = configData['cores'])
        process_pool.map(execute, configData['customCommand'])



if __name__ == '__main__':
    main()