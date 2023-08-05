# -*- coding: utf-8 -*-
'''
dwave agent linking to Leap and provide testing service as an agent
'''
import requests
import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Set, Union, Text, Tuple, Optional
from dwave_leap import Dwave_leap, MQ_Dwave_Leap_Runtime, MQ_Dwave_Leap_Sovler_property

class Item(BaseModel):
    tester: str = None
    operation_time: str = '1970-01-01 00:00:00'
    query_type: str = 'qpu_advantage'
    category_item: str = 'operation_maintenance'
    operation_item: str = 'query_runtime'
    if_mq: str = 'False'
    token: str


mq_dwave_solver = MQ_Dwave_Leap_Sovler_property()
mq_dwave_runtime = MQ_Dwave_Leap_Runtime()
app = FastAPI()

@app.get("/")
async  def root():
    return 'Hello dwave-leap QC cloud platform!'

@app.post("/login")
async  def login(item: Item):
    item_dict = item.dict()
    TOKEN = item_dict['token']
    # print(TOKEN)
    global dwave_leap
    dwave_leap = Dwave_leap(TOKEN)
    print('Hello dwave-leap QC cloud platform!!!!!!!!!!!!!!!!')
    return {"code": 200, "msg": "success", "login_state": True}

@app.post("/query_solver/{tester}")
async def query_solver(tester: str, item: Item):
    item_dict = item.dict()
    config_body = {}
    config_body['tester'] = str(tester)
    config_body['operation_time'] = item_dict['operation_time']
    config_body['query_type'] = item_dict['query_type']
    config_body['category_item'] = item_dict['category_item']
    config_body['operation_item'] = item_dict['operation_item']
    output_body = {}
    output_body = dwave_leap.query_solver_property(config_body['query_type'])
    res = output_body
    
    if item_dict['if_mq'] == 'True':
        mq_dwave_solver.mq_write(config_body, output_body)
        res['mq_write_state'] = True
    else:
        res['mq_write_state'] = False
    res['code'] = 200
    res['msg'] = 'success'
    return res

@app.post("/query_runtime/{tester}")
async def query_runtime(tester: str, item: Item):
    item_dict = item.dict()
    config_body = {}
    config_body['tester'] = str(tester)
    config_body['operation_time'] = item_dict['operation_time']
    config_body['query_type'] = item_dict['query_type']
    config_body['category_item'] = item_dict['category_item']
    config_body['operation_item'] = item_dict['operation_item']
    output_body = {}
    output_body = dwave_leap.query_ising_model_runtime(config_body['query_type'])
    input_body = {}
    input_body = output_body['timing']
    input_body['problem_id'] = output_body['problem_id']
    res = input_body

    if item_dict['if_mq'] == 'True':
        mq_dwave_runtime.mq_write(config_body, input_body)
        res['mq_write_state'] = True
    else:
        res['mq_write_state'] = False
    res['code'] = 200
    res['msg'] = 'success'
    return res


if __name__ == '__main__':
    uvicorn.run(app='agent_api:app', host = '0.0.0.0', port = 1981, reload= True, debug = True)



