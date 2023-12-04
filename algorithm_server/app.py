from flask import Flask, request
from config import *
from log import logger
from utils.models import model
import flask
import traceback
import requests

import cv2
import numpy as np
import base64
import threading

#flask app
app = Flask(__name__)

#提供两种调用模式，同步调用和异步调用
#同步调用，在调用时，等待算法返回结果，适用于算法执行时间短的情况

#同步调用
@app.route(algorithm_server_sync_api, methods=['POST'])
def sync_api():
    # 每个接口需要定义自己的输入输出格式
    """
        input:{
            "time": str,
            "device_id": str,
            "data_type": str,
            "data_size": int,
            "data": str,
            ...
        }

        output:{
            "code": int,  #定义调用状态的返回码用于判断算法调用成功与否
            "message": str, #接口调用状态返回信息
            "result": list, #根据算法实际使用情况定义返回结果
            ...
        }
    """

    #用于返回的data list
    res_data = {
        "code": 0,
        "message": "success",
        "result": {}
    }

    #判断接口使用模式是否正确
    if request.method == 'POST':

        try:
            #--------------------------------获取数据--------------------------------
            req_data = request.json

            #需要对req_data进行判断和解析，判断是否符合接口定义的输入格式，解析出算法需要的数据

            #-------------------------------格式检查---------------------------------
            #
            # #check format
            # image_format = req_data['image_format']
            # if image_format not in ['jpg','jpeg','png']:
            #     logger.warning(f"ImageFormatException:device-{req_data['device']}-time-{req_data['time']}format{image_format}")
            #     raise Exception(f'ImageFormatException')

            img = req_data['data']
            img = base64.b64decode(img.encode('ascii'))   # 图片在网络流中的形式 原始数据->解码为字节流->base64编码->网络传输->base64解码->编码回ascii->原始数据

            #-------------------------------数据完整性检查----------------------------
            # #check image completity
            # if len(img) != req_data['image_size']:
            #     logger.warning(f"IncomleteImageException:device-{req_data['device']}-time-{req_data['time']}")
            #     raise Exception(f"IncompleteImageException")
            # 
            #--------------------------------算法输入数据解析------------------------------
            #decode image
            image_data = np.frombuffer(img,np.uint8)
            image_data = cv2.imdecode(image_data, cv2.IMREAD_COLOR)


            # ------------------------------保存数据（可选）
            try:
                image_path = data_path+req_data['device_id']+'.'+req_data['data_type']
                logger.info(image_path)
                cv2.imwrite(image_path, image_data)
                logger.info(f"get new base image:device-{req_data['device_id']}-time-{req_data['time']}")
            except Exception as e:
                raise Exception (f"save image error:{e}")
            
            # ------------------------------调用算法---------------------------------
            try:
                result = model(image_data)
                res_data["result"]["label"] = result
            except Exception as e:
                raise Exception(f"model error:{e}")


        except Exception as e:
            logger.warning(f'{e}')
            logger.warning(traceback.print_exc())
            res_data["message"] = str(e)
    return flask.jsonify(res_data)


#异步调用
@app.route(algorithm_server_async_api,methods=['POST'])
def async_api():
    # 每个接口需要定义自己的输入输出格式
    """
        input:{
            "time": str,
            "device_id": str,
            "data_type": str,
            "data_size": int,
            "data": str,
            ...
        }

        output:{
            "code": int,  #定义调用状态的返回码用于判断算法调用成功与否
            "message": str, #接口调用状态返回信息
            ...
        }
    """
    #用于返回的data list,不再带有结果 检验合法即返回成功
    res_data = {
        "code": 0,
        "message": "success",
    }
    if request.method == 'POST':

        try:
            #--------------------------------获取数据--------------------------------
            req_data = request.json

            #需要对req_data进行判断和解析，判断是否符合接口定义的输入格式，解析出算法需要的数据

            #-------------------------------格式检查---------------------------------
            #
            # #check format
            # image_format = req_data['image_format']
            # if image_format not in ['jpg','jpeg','png']:
            #     logger.warning(f"ImageFormatException:device-{req_data['device']}-time-{req_data['time']}format{image_format}")
            #     raise Exception(f'ImageFormatException')

            img = req_data['data']
            img = base64.b64decode(img.encode('ascii'))   # 图片在网络流中的形式 原始数据->解码为字节流->base64编码->网络传输->base64解码->编码回ascii->原始数据

            #-------------------------------数据完整性检查----------------------------
            # #check image completity
            # if len(img) != req_data['image_size']:
            #     logger.warning(f"IncomleteImageException:device-{req_data['device']}-time-{req_data['time']}")
            #     raise Exception(f"IncompleteImageException")
            # 
            #--------------------------------算法输入数据解析------------------------------
            #decode image
            image_data = np.frombuffer(img,np.uint8)
            image_data = cv2.imdecode(image_data, cv2.IMREAD_COLOR)


            # ------------------------------保存数据（可选）----------------------------
            try:
                image_path = data_path+req_data['device_id']+'.'+req_data['data_type']
                logger.info(image_path)
                cv2.imwrite(image_path, image_data)
                logger.info(f"get new base image:device-{req_data['device_id']}-time-{req_data['time']}")
            except Exception as e:
                raise Exception (f"save image error:{e}")
            
            # ------------------------------异步调用算法---------------------------------
            try:
                #使用一个子线程去异步执行async_and_res函数，该函数用于调用算法，并将结果通过request返回给调用者
                threading.Thread(target=async_and_res,args=(image_data,req_data)).start()
                pass
            except Exception as e:
                raise Exception(f"model error:{e}")


        except Exception as e:
            logger.warning(f'{e}')
            logger.warning(traceback.print_exc())
            res_data["message"] = str(e)
    return flask.jsonify(res_data)

#提供子线程的函数，用于异步调用算法，并将结果通过request返回给调用者
def async_and_res(data,res_data):
    res_data["result"] = {}
    result = model(data)
    res_data["result"]["label"] = result
    tmp_api = 'http://'+dispatcher_server_result_api+':'+str(dispatcher_server_port)+dispatcher_server_result_api
    r = requests.post(tmp_api,json=res_data)
    logger.info(f"async_and_res:{r.text}")


if __name__ == '__main__':
    app.run(host=algorithm_server_host, port=algorithm_server_port)