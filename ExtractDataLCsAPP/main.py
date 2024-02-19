import sys
import argparse
import AuthF
import json
import MetricData
import PostLcsCustomLogs
import inflect


#parser = argparse.ArgumentParser(description='Application to fetch Metric Data from LCS,needs LCS user without MFA')
#parser.add_argument('-username', '--usernameLogin', type=str, required=True, help='Username to login LCS')
#parser.add_argument('-password', '--passwordLogin', type=str, required=True,help='Password to LCS User')
#args = parser.parse_args()

#username = args.usernameLogin
#password = args.passwordLogin
import schedule
import time






def extract_aos_names(names):
    p = inflect.engine()
    result_list = [s.split('-')[0] for s in names]
    result = []
    p = inflect.engine()
    result = []
    for name in result_list:
        if name[-1].isdigit():
            num_word = p.number_to_words(int(name[-1]))
            result.append(name[:-1] + num_word)
        else:
            result.append(name)
    return result
def get_Config(filename):
    with open(filename, 'r') as json_file:
        return json.load(json_file)

def Authorize(username,password):
    try:
        AuthF.start(username, password)
    except Exception as e:
        print(f"Error occurred: {e}")

     #py main.py -username devopsautomation@anegis.com -password 8Fq@8T3J66_@=:dLJ'*MNM/)=!:YhVUv
def processData():
    config_file = get_Config("Config.json")
    print(len(config_file))
    customer_id = '---'  
    shared_key = "---"
    for item in config_file:
        Memdata = MetricData.get_MemAvalible_data(item['EnvID'],item['projectID'],item['CustomerName'])
        CpuData = MetricData.get_Cpu_data(item['EnvID'],item['projectID'],item['CustomerName'])
        print(Memdata)
        MemJson = json.dumps(Memdata)
        CpuJson = json.dumps(CpuData)
      
        postMemData(customer_id,shared_key,MemJson)
        postCpuData(customer_id,shared_key,CpuJson)

        #PostLcsCustomLogs.post_data(customer_id,shared_key,body,logType)
def postMemData(customer_id,shared_key,body):
    LogType = 'MemoryAvailible'
    PostLcsCustomLogs.post_data(customer_id,shared_key,body,LogType)
def postCpuData(customer_id,shared_key,body):
    LogType = 'CpuUtilization'
    PostLcsCustomLogs.post_data(customer_id,shared_key,body,LogType)

username="---" 
password ="---"
#Authorize(username,password)
def start():
    username = "---" 
    password = "---"
    Authorize(username, password)
    processData()
    print("Funkcja wywoływana co godzinę")

# Uruchomienie funkcji start() od razu po uruchomieniu skryptu:
start()

# Harmonogram wykonania funkcji start() co godzinę:
schedule.every().hour.do(start)

while True:
    schedule.run_pending()
    time.sleep(1)
