import logging
import os
from config import *

#设置 log相关
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
#判断log文件是否存在，不存在创建文件
if not os.path.exists(dispatcher_server_logger_path):
    os.mknod(dispatcher_server_logger_path)
handler = logging.FileHandler(dispatcher_server_logger_path)
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)
