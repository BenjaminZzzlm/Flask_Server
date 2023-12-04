#config of file storage path

data_path = '/disk2/zhanglingming/Flask_Server/Flask_Server/algorithm_server/data/'

#config of dispatcher server

dispatcher_server_host = '127.0.0.1'
dispatcher_server_port = 5000

#config of algorithm server

algorithm_server_host = '127.0.0.1'
algorithm_server_port = 5001


#config of algorithm server logger

algorithm_server_logger_path = '/disk2/zhanglingming/Flask_Server/Flask_Server/algorithm_server/log/algorithm_server.log'

#config of api
#------------------------------------------------------------------------------------------------
algorithm_server_sync_api = '/algorithm_server/sync'

algorithm_server_sync_api_req = {
                                    "time": str,
                                    "device_id": str,
                                    "data_type": str,
                                    "data_size": int,
                                    "data": str,
                                }

algorithm_server_sync_api_res = {
                                    "code": int,  #定义调用状态的返回码用于判断算法调用成功与否
                                    "message": str, #接口调用状态返回信息
                                    "result": list, #根据算法实际使用情况定义返回结果
                                }

#-----------------------------------------------------------------------------------------------
algorithm_server_async_api = '/algorithm_server/async'

algorithm_server_async_api_req = {
                                    "time": str,
                                    "device_id": str,
                                    "data_type": str,
                                    "data_size": int,
                                    "data": str,
                                }

algorithm_server_async_api_res = {
                                    "code": int,  #定义调用状态的返回码用于判断算法调用成功与否
                                    "message": str, #接口调用状态返回信息
                                }
#---------------------------------------------------------------------------------------------------
dispatcher_server_result_api = '/dispatcher_server/result'

dispatcher_server_result_api_req = {
                                    "time": str,
                                    "device_id": str,
                                    "data_type": str,
                                    "data_size": int,
                                    "data": str,
                                    "result":list,
                                }

dispatcher_server_result_api_res = {
                                    "code": int,  #定义调用状态的返回码用于判断结果返回成功与否
                                    "message": str, #接口调用状态返回信息
                                }
#----------------------------------------------------------------------------------------------------