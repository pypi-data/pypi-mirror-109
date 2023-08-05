# -*- coding: utf-8 -*-
'''
dwave testing client GET/POST to agent via RESTFUL API, adopting argparse mode
'''
import argparse
import testing_client_json as client_module
import time
import logging
import sys
import json
FORMAT = '[%(asctime)s, %(levelname)-7s]: %(message)s'
logging.basicConfig(format = FORMAT)
logger = logging.getLogger('spider')
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description = 'caict testing qc benchmark platform project')
parser.add_argument('-v', '--verbose', help = 'debug info', action = 'store_true')
#group = parser.add_mutually_exclusive_group() # config manually or load config file is exclusive
parser.add_argument('-t', '--tester', help = 'name of tester', default = 'caict')
parser.add_argument('-i', '--ip', help = 'ip address of agent server', default = '8.140.123.60')
parser.add_argument('-p', '--port', help = 'port number of agent server', default = '1981')
parser.add_argument('-pr', '--provider', help = 'qc provider', default = 'dwave-leap')
parser.add_argument('-ti', '--operation_time', help = 'time of testing operation', default = time.strftime('%Y/%m/%d %H:%M:%S'))
parser.add_argument('-tk', '--token', help = 'login token of qc cloud platform', default = 'xxxxxxxxx your token xxxxxxxxxx')
parser.add_argument('-mq', '--if_mq', help = 'if or not recording testing results to MQ. e.g. datahub of aliyun', default = 'True')
parser.add_argument('-q', '--query_type', help = 'type of qpu or simulator', default = 'qpu_2000q')
parser.add_argument('-o', '--operation_item', help = 'type of testing operation', default = 'query_runtime')
parser.add_argument('-c', '--category_item', help = 'category benchmark designed by CAICT', default = 'operation_maintenance')
parser.add_argument('-e', '--testing_epoch', help = 'epoch of testing attemps repeadlly', default = '3')
parser.add_argument('-lc', '--load_config', help = 'load config from json file', default = '')
parser.add_argument('-sc', '--save_config', help = 'save config from json file', default = 'ignore')

args = parser.parse_args()

config_body = {}

if len(args.load_config) >0:
    print('==== load config file! ====')
    filename = args.load_config
    print(filename)
    with open(filename) as f:
        config_body = json.load(f)
elif args.load_config == '':
    config_body['tester'] = args.tester
    config_body['ip'] = args.ip
    config_body['port'] = args.port
    config_body['provider'] = args.provider
    config_body['operation_time'] = args.operation_time
    config_body['token'] = args.token
    config_body['if_mq'] = args.if_mq
    config_body['query_type'] = args.query_type
    config_body['operation_item'] = args.operation_item
    config_body['category_item'] = args.category_item
    config_body['testing_epoch'] = args.testing_epoch
else:
    print('======  error argument!!! ===========')

if args.save_config is not 'ignore':
    prex = time.strftime('%Y-%m-%d-%H-%M-%S-')
    with open(prex + args.save_config, 'w') as f:
        json.dump(config_body, f)
        print('successfully save config file!!!!!!!!!!')

# create instance of testing client for dwave_leap qc cloud platform
dwave_client = client_module.Testing_Client_Dwave_Leap()
## config params of testing client
dwave_client.testing_params_config(config_body)
## save config file as json
#dwave_client.save_config_file(config_body,'lvbo.json')
## load config params from json file
dwave_client.query_runtime()
time.sleep(2)


