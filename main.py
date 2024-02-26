# subscribe_basic.py
import time
import random
from paho.mqtt import client as mqtt_client
import json
import winsound
#from utils_logger import get_logger

broker = '192.168.3.59'  # mqtt代理服务器地址
port = 1883
keepalive = 60  # 与代理通信之间允许的最长时间段（以秒为单位）
topic = "car"
client_id = f'win2'  # 可自定义，但要注意客户端id不能重复


def connect_mqtt():
    '''连接mqtt代理服务器'''

    def on_connect(self,client, userdata, flags, rc):
        '''连接回调函数'''
        # 响应状态码为0表示连接成功
        if rc == 0:
            print("Connected to MQTT successfully!")
        else:
            print("Failed to connect, return code {0}".format(rc))

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2,client_id)
    client.on_connect = on_connect
    client.connect(broker, port, keepalive)
    return client


def publish(client):
    '''发布消息'''
    while True:
        '''每隔4秒发布一次信息'''
        time.sleep(4)
        # mqtt只能传输字符串数据
        info = {
            'msg1': 'Hello kristina',
            'msg2': 'msg {0}'.format(random.randint(0, 1000))
        }
        msg = json.dumps(info)
        # 默认retain=False，一个Topic只能有一个retained消息，后设置的会覆盖前面的消息
        result = client.publish(topic=topic, payload=msg, qos=0, retain=True)
        # 删除retained消息
        # result = client.publish(topic=topic, payload=None, qos=0, retain=True)
        if result[0] == 0:
            print("Send {0} to topic {1}".format(msg, topic))
        else:
            print("Failed to send message {0} to topic {1}".format(msg, topic))

def subscribe(client: mqtt_client):
    '''订阅主题并接收消息'''

    def on_message(client, userdata, msg):
        '''订阅消息回调函数'''
        # data = json.loads(msg.payload)  # data = 字典  #payload = json数据
        # print("Received message from topic {0} ".format(msg.topic))
        # print("The message have {0} information".format(len(data)))
        # print("The information is '{0}'".format(data))
        data=msg.payload.decode("utf-8")
        if data=="car_come":
            print(data)
            winsound.PlaySound('entrance.WAV', winsound.SND_FILENAME)
    # 订阅指定消息主题
    client.subscribe(topic=topic, qos=0)
    # 将回调函数指派给客户端实例
    client.on_message = on_message


def run():
    # 运行订阅者
    client = connect_mqtt()
    #publish(client)
    subscribe(client)
    #  运行一个线程来自动调用loop()处理网络事件, 阻塞模式
    client.loop_forever()  # 保持 loop()调用


if __name__ == '__main__':
    run()