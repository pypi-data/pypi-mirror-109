# -*- coding: utf-8 -*-
'''
dwave testing client GET/POST to agent via RESTFUL API, loaded json testing config file
testing-client.py
@copyright: (c) 2021 by CAICT
@modified: 2021-06-09
'''
import requests
import json
import time
import random

class Testing_Client_Dwave_Leap:
    def __init__(self):
        '''
        qc testing config parameters as json format
        @ tester: name of tester
        @ ip: ip address of agent server
        @ port: port number of agent server
        @ provider: provider of remote qc cloud platform via Internet
        @ operation_time: time of testing operation. e.g. 2021-06-09 09:40:30
        @ token: token to login qc cloud platform
        @ if_mq: if or not writing the recording results to MQ. e.g. datahub of aliyun
        @ query_type: type of qpu or simulator with qc provider. e.g. qpu_2000q is 2000qubit Quantum Annealing QPU provided by Dwave
        @ operation_item: type of testing operation. e.g. query runtime means checking the runtime of excuting qc task
        @ category_item: selected category of benchmarking framework designed by CAICT
        @ testing_epoch: epoch for testing or attempts
        '''
        self.config_params = {
            'tester': 'xx-caict',
            'ip': '8.140.123.60',
            'provider': 'dwave-leap',
            'operation_time': time.strftime('%Y/%m/%d %H:%M:%S'),
            'token': '*********your token*****************',
            'if_mq': 'True',
            'query_type': 'qpu_2000q',
            'operation_item': 'query_runtime',
            'category_item': 'operation_maintenance',
            'testing_epoch': '10',
        }
        print('successfully create instance of dwave leap testing client!!!!')
    
    def testing_params_config(self, config_params):
        keys = config_params.keys()
        for key in keys:
            self.config_params[key] = config_params[key]
        print('successfully config testing params of testing client!!!!!!')
        print(self.config_params)
        return self.config_params

    def save_config_file(self, config_params, filename = 'caict-testing-config.json'):
        self.config_params = config_params
        prex = time.strftime('%Y-%m-%d-%H-%M-%S-')
        with open(prex + filename, "w") as f:
            json.dump(self.config_params, f)
            print("successfully save config file!!!!!!!")

    def load_config_file(self, filename):
        with open(filename) as f:
            self.config_params = json.load(f)
            print('successfully load config file!!!!!')
            print(self.config_params)
        return self.config_params

    def login_agent_server(self):
        body = self.config_params
        url = 'http://' + body['ip'] + ':' + body['port'] + '/login'
        time1 = time.time()
        # ret = requests.post("http://8.140.123.60:1981/login", json.dumps(body))
        ret = requests.post(url, json.dumps(body))
        print('login time:')
        time2 = time.time()
        print("ELAPSED: ", time2 - time1)
        print("RESULT:", ret.json())
        return ret.json()

    def query_runtime(self):
        body = self.config_params
        url = 'http://' + body['ip'] + ':' + body['port'] + '/query_runtime/' + str(body['tester'])
        epoch = int(body['testing_epoch'])
        body['operation_time'] = time.strftime('%Y/%m/%d %H:%M:%S')
        if body['operation_item'] == 'query_runtime':
            for num in range(epoch):
                time1 = time.time()
                ret = requests.post(url, json.dumps(body))
                print('serving time of query_runtime:')
                time2 = time.time()
                print("ELAPSED: ", time2 - time1)
                print("RESULT:", ret.json())
        else:
            return {'query_status': False, 'debug_info': 'wrong testing param for query runtime:' + body['operation_item']}
        return ret.json()

    def query_solver(self):
        body = self.config_params
        url='http://' + body['ip'] + ':' + body['port'] + '/query_solver/' + str(body['tester'])
        epoch = int(body['testing_epoch'])
        body['operation_time'] = time.strftime('%Y/%m/%d %H:%M:%S')
        if body['operation_item'] == 'query_solver':
            for num in range(epoch):
                time1 = time.time()
                ret = requests.post(url, json.dumps(body))
                print('serving time of query_solver:')
                time2 = time.time()
                print("ELAPSED: ", time2 - time1)
        else:
            return {'query_status': False, 'debug_info': 'wrong testing param for query solver:' + body['operation_item']}
        return ret.json()
        # print("RESULT:", ret.json())

if __name__ == '__main__':
    config_body = {'tester': 'lvbo-caict',
            'ip': '8.140.123.60',
            'port': '1981',
            'provider': 'dwave-leap',
            'operation_time': time.strftime('%Y/%m/%d %H:%M:%S'),
            'token': '*********your token*****************',
            'if_mq': 'True',
            'query_type': 'qpu_2000q',
            'operation_item': 'query_runtime',
            'category_item': 'operation_maintenance',
            'testing_epoch': '3',
            }
    ## create instance of testing client for dwave_leap qc cloud platform
    dwave_client = Testing_Client_Dwave_Leap()
    ## config params of testing client
    dwave_client.testing_params_config(config_body)
    ## save config file as json
    dwave_client.save_config_file(config_body,'lvbo.json')
    ## load config params from json file
    dwave_client.query_runtime()
