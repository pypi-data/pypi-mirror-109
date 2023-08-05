# -*- coding:utf-8 -*-
from dwave.cloud import Client
import json
from dwave.system import DWaveSampler, EmbeddingComposite, LeapHybridSampler
import random
# from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from datahub.models import FieldType, RecordSchema, TupleRecord, BlobRecord, CursorType, RecordType
from datahub.exceptions import ResourceExistException, DatahubException
from datahub import DataHub
import sys
import time
import traceback
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Dwave_leap():
    def __init__(self, TOKEN):
        self.client = Client.from_config(token = TOKEN)
        print('*' * 50)
        print('Successfully acess to Dwave Leap cloud platform!')
        print('*' * 50)
#        self.qpu_advantage_sampler_embedding = EmbeddingComposite(DWaveSampler(solver={'qpu': True}))
        self.qpu_advantage = DWaveSampler(solver={'topology__type': 'pegasus'})
        self.qpu_advantage_sampler_embedding = EmbeddingComposite(self.qpu_advantage)        
        self.qpu_2000q = DWaveSampler(solver={'topology__type': 'chimera'})
        self.qpu_2000q_sampler_embedding = EmbeddingComposite(self.qpu_2000q)
        self.hybrid_bqm_sampler = LeapHybridSampler()        
        print('--------------successfully load!!------------------')
    def query_solver(self):
        return self.client.get_solvers()
    
    def query_ising_model_runtime(self,query_type = 'qpu_2000q'):
        if query_type == 'qpu_2000q':
            sampleset = self.qpu_2000q_sampler_embedding.sample_ising({'a': 1}, {('a', 'b'): 1})
        elif query_type == 'qpu_advantage':
            sampleset = self.qpu_advantage_sampler_embedding.sample_ising({'a': 1}, {('a', 'b'): 1})            
        else:
            sampleset = {}                   
        print('runtime of runing 2 items of Isring model is:\n')
        print(sampleset.info['timing'])
        return sampleset.info
    
    def query_solver_property(self, query_type = 'qpu_2000q'):
        if query_type == 'qpu_2000q':
            res_2000q = {}
            keys = self.qpu_2000q.properties.keys()
            for key in keys:
                res_2000q[key] = self.qpu_2000q.properties[key]
            return res_2000q
        elif query_type == 'qpu_advantage':
            res_qpu_advantage = {}
            keys = self.qpu_advantage.properties.keys()
            for key in keys:
                res_qpu_advantage[key] = self.qpu_advantage.properties[key]
            return res_qpu_advantage
        elif query_type == 'hybrid_bqm_sampler':
            res_hybrid_bqm_sampler = {}
            keys = self.hybrid_bqm_sampler.properties.keys()
            for key in keys:
                res_hybrid_bqm_sampler[key] = self.hybrid_bqm_sampler.properties[key]
            return res_hybrid_bqm_sampler
        else:
            return {}

class MQ_Dwave_Leap_Runtime:
    def __init__(self):
        access_id = ''
        access_key = ''
        endpoint = 'https://dh-cn-beijing.aliyuncs.com'
        self.dh = DataHub(access_id, access_key, endpoint)
        project_name = 'qc_benchmark_dwave_leap'
        comment = 'caict qc_benchmark testing platform'
        try:
            self.dh.create_project(project_name, comment)
            print("create project success!")
            print("=======================================\n\n")
            
        except ResourceExistException:
            print("project already exist!")
            print("=======================================\n\n")
        except Exception as e:
            print(traceback.format_exc())
            sys.exit(-1)

        # --------------------- topic ---------------------
        tuple_topic = "query_ising_model_runtime"
        shard_count = 3
        life_cycle = 7
        record_schema = RecordSchema.from_lists(
            ['tester', 'operation_time', 'query_type','category_item', 'operation_item', 'qpu_sampling_time',
             'qpu_anneal_time_per_sample', 'qpu_readout_time_per_sample',
             'qpu_access_time', 'qpu_access_overhead_time', 'qpu_programming_time',
             'qpu_delay_time_per_sample', 'total_post_processing_time', 'post_processing_overhead_time', 'problem_id'],
            [FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING,
             FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING,
             FieldType.STRING])

        try:
            self.dh.create_tuple_topic(project_name, tuple_topic,
                                       shard_count, life_cycle, record_schema, comment)
            print("create detection topic success!")
            print("=======================================\n\n")
        except ResourceExistException:
            print("topic already exist!")
            print("=======================================\n\n")
        except Exception as e:
            print(traceback.format_exc())
            sys.exit(-1)

        # ===================== get topic =====================
        topic_result = self.dh.get_topic(project_name, tuple_topic)
        print(topic_result)
        print(topic_result.record_schema)

        # ===================== list shard =====================
        shards_result = self.dh.list_shard(project_name, tuple_topic)
        print(shards_result)
        self.project_name = project_name
        self.tuple_topic = tuple_topic
        self.record_schema = record_schema

        self.output_body = {}
        self.output_body['tester'] = 'lvbo'
        self.output_body['operation_time'] = '1970-01-01 00:00:00'
        self.output_body['query_type'] = 'qpu_advatange'
        self.output_body['category_item'] = 'operation_maintenance'


    def mq_write(self, config_body, input_body):

        try:
            self.dh.wait_shards_ready(self.project_name, self.tuple_topic)
            # print("shards all ready!!!")
            # print("=======================================\n\n")

            topic_result = self.dh.get_topic(
                self.project_name, self.tuple_topic)
            #        print(topic_result)
            if topic_result.record_type != RecordType.TUPLE:
                print("topic type illegal!")
                sys.exit(-1)
            #        print("=======================================\n\n")

            #record_schema = topic_result.record_schema
            #
            records0 = []
            record1 = TupleRecord(schema = self.record_schema)
            keys = config_body.keys()
            for key in keys:
                record1.set_value(str(key), str(config_body[key]))
            key_words = input_body.keys()
            for key in key_words:
                record1.set_value(str(key), str(input_body[key]))           
            record1.hash_key = '7FFFFFFFFFFFFFFD7FFFFFFFFFFFFFFD'
            records0.append(record1)

            self.dh.put_records(self.project_name, self.tuple_topic, records0)
            print('*'*30)
            print('successfully write to datahub(MQ)!!')
        except DatahubException as e:
            print(e)
            sys.exit(-1)

class MQ_Dwave_Leap_Sovler_property:
    def __init__(self):
        access_id = ''
        access_key = ''
        endpoint = 'https://dh-cn-beijing.aliyuncs.com'
        self.dh = DataHub(access_id, access_key, endpoint)
        project_name = 'qc_benchmark_dwave_leap'
        comment = 'caict qc_benchmark testing platform'
        try:
            self.dh.create_project(project_name, comment)
            print("create project success!")
            print("=======================================\n\n")
        except ResourceExistException:
            print("project already exist!")
            print("=======================================\n\n")
        except Exception as e:
            print(traceback.format_exc())
            sys.exit(-1)

        # --------------------- topic ---------------------
        tuple_topic = "query_solver_property"
        shard_count = 3
        life_cycle = 7
        record_schema = RecordSchema.from_lists(
            ['tester', 'operation_time', 'query_type','category_item', 'operation_item', 'num_qubits', 'qubits', 'couplers',
             'h_range', 'j_range', 'supported_problem_types', 'parameters', 'vfyc', 'anneal_offset_ranges', 'anneal_offset_step',
             'anneal_offset_step_phi0', 'annealing_time_range', 'chip_id', 'default_annealing_time', 'default_programming_thermalization',
             'default_readout_thermalization', 'extended_j_range', 'h_gain_schedule_range', 'max_anneal_schedule_points',
             'max_h_gain_schedule_points', 'num_reads_range', 'per_qubit_coupling_range', 'problem_run_duration_range',
             'programming_thermalization_range', 'readout_thermalization_range', 'tags', 'topology', 'category', 'quota_conversion_rate'],
            [FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING,
             FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING,
             FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING,
             FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING,
             FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING, FieldType.STRING])

        try:
            self.dh.create_tuple_topic(project_name, tuple_topic,
                                       shard_count, life_cycle, record_schema, comment)
            print("create detection topic success!")
            print("=======================================\n\n")
        except ResourceExistException:
            print("topic already exist!")
            print("=======================================\n\n")
        except Exception as e:
            print(traceback.format_exc())
            sys.exit(-1)

        # ===================== get topic =====================
        topic_result = self.dh.get_topic(project_name, tuple_topic)
        print(topic_result)
        print(topic_result.record_schema)

        # ===================== list shard =====================
        shards_result = self.dh.list_shard(project_name, tuple_topic)
        print(shards_result)
        self.project_name = project_name
        self.tuple_topic = tuple_topic
        self.record_schema = record_schema

        self.output_body = {}
        self.output_body['tester'] = 'lvbo'
        self.output_body['operation_time'] = '1970-01-01 00:00:00'
        self.output_body['query_type'] = 'qpu_2000q'
        self.output_body['category_item'] = 'operation_maintenance'


    def mq_write(self, config_body, input_body):

        try:
            self.dh.wait_shards_ready(self.project_name, self.tuple_topic)
            # print("shards all ready!!!")
            # print("=======================================\n\n")

            topic_result = self.dh.get_topic(
                self.project_name, self.tuple_topic)
            #        print(topic_result)
            if topic_result.record_type != RecordType.TUPLE:
                print("topic type illegal!")
                sys.exit(-1)
            #        print("=======================================\n\n")

            #record_schema = topic_result.record_schema
            #
            records0 = []
            record1 = TupleRecord(schema = self.record_schema)
            keys = config_body.keys()
            for key in keys:
                record1.set_value(str(key), str(config_body[key]))
            key_words = input_body.keys()
            for key in key_words:
                record1.set_value(str(key), str(input_body[key]))
            record1.hash_key = '6FFFFFFFFFFFFFFD7FFFFFFFFFFFFFFD'
            records0.append(record1)

            self.dh.put_records(self.project_name, self.tuple_topic, records0)
            print('*'*30)
            print('successfully write to datahub(MQ)!!')
        except DatahubException as e:
            print(e)
            sys.exit(-1)

if  __name__ == '__main__':
    config_body = {}
    config_body['tester'] = 'lvbo-caict'
    config_body['operation_time'] = 'cc'
    config_body['query_type'] = 'qpu_advantage'
    config_body['category_item'] = 'operation_maintenance'
    TOKEN = ''
    dwave_leap = Dwave_leap(TOKEN)
    mq_dwave_solver = MQ_Dwave_Leap_Sovler_property()
    mq_dwave_runtime = MQ_Dwave_Leap_Runtime()
    output_body = {}
    output_body = dwave_leap.query_ising_model_runtime(config_body['query_type'])
    input_body = {}
    input_body = output_body['timing']
    input_body['problem_id'] = output_body['problem_id']
    time.sleep(2)
    mq_dwave_runtime.mq_write(config_body, input_body)

