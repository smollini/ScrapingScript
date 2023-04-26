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
    customer_id = '20336ba9-a051-4a62-b9d2-0a4f8279316b'  
    shared_key = "mtRkKxBRvDSNtBFKt1HP0vzCoxJm+ITnff+i4S92WYl9FJoLQobWwi9vjLjFweAtIgyPfskd83f5PlzD39Qgsw=="
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

#global body
#body = {"Date": "2023-04-20T09:19:00", "Value": 8094, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:20:00", "Value": 8097, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:21:00", "Value": 8087, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:22:00", "Value": 8089, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:23:00", "Value": 8093, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:24:00", "Value": 8081, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:25:00", "Value": 8084, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:26:00", "Value": 8083, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:27:00", "Value": 8084, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:28:00", "Value": 8090, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:29:00", "Value": 8096, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:30:00", "Value": 8096, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:31:00", "Value": 8087, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:32:00", "Value": 8086, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:33:00", "Value": 8085, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:34:00", "Value": 8081, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:35:00", "Value": 8078, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:36:00", "Value": 8079, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:37:00", "Value": 8081, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:38:00", "Value": 8084, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:39:00", "Value": 8088, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:40:00", "Value": 8093, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:41:00", "Value": 8082, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:42:00", "Value": 8081, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:43:00", "Value": 8085, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:44:00", "Value": 8073, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:45:00", "Value": 8079, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:46:00", "Value": 8077, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:47:00", "Value": 8079, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:48:00", "Value": 8086, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:49:00", "Value": 8091, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:50:00", "Value": 8094, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:51:00", "Value": 8084, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:52:00", "Value": 8079, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:53:00", "Value": 8083, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:54:00", "Value": 8076, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:55:00", "Value": 8077, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:56:00", "Value": 8079, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:57:00", "Value": 8080, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:58:00", "Value": 8087, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T09:59:00", "Value": 8089, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:00:00", "Value": 8093, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:01:00", "Value": 8082, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:02:00", "Value": 8078, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:03:00", "Value": 8086, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:04:00", "Value": 8074, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:05:00", "Value": 8080, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:06:00", "Value": 8075, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:07:00", "Value": 8075, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:08:00", "Value": 8084, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:09:00", "Value": 8089, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:10:00", "Value": 8093, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:11:00", "Value": 8082, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:12:00", "Value": 8079, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:13:00", "Value": 8086, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:14:00", "Value": 8074, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:15:00", "Value": 8076, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:16:00", "Value": 8078, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:17:00", "Value": 8078, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:18:00", "Value": 8086, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}, {"Date": "2023-04-20T10:19:00", "Value": 8088, "AOS": "BATCHAOS1-3afa9171-16b6-451d-bab9-9aafaecd788f", "MetricName": "\\\\Memory\\\\Available MBytes"}
username="devopsautomation@anegis.com" 
password ="8Fq@8T3J66_@=:dLJ'*MNM/)=!:YhVUv"
#Authorize(username,password)
def start():
    username = "devopsautomation@anegis.com" 
    password = "8Fq@8T3J66_@=:dLJ'*MNM/)=!:YhVUv"
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
