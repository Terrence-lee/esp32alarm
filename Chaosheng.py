from machine import Pin
import time
import network
from umqttsimple import MQTTClient

"""
echo脚会由0变为1此时MCU开始计时，当超声波模块接收到返回的声波时，echo由1变为0此时MCU停止计时
然后再通过声音的传输速度是340m/s就可以计算出距离，切记要除以2，毕竟声音是来回的距离
"""
# 引脚设定
trig = Pin(15, Pin.OUT)
echo = Pin(2, Pin.IN)
trig.value(0)
echo.value(0)

# output
led = Pin(5, Pin.OUT)


# 超声波用来驱动的函数
def measure():
    # 告诉芯片要开始测试了
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    # 检测回响信号，为低电平时，测距完成
    while echo.value() == 0:
        # 开始不断递增的微秒计数器 1
        t1 = time.ticks_us()
    print("---------------------")
    print(t1)
    # 检测回响信号，为高电平时，测距开始
    while echo.value() == 1:
        # 开始不断递增的微秒计数器 2
        t2 = time.ticks_us()

    # 计算两次调用 ticks_ms(), ticks_us(), 或 ticks_cpu()之间的时间，这里是ticks_us()
    # 这时间差就是测距总时间，在乘声音的传播速度340米/秒，除2就是距离
    # 例如 t2-t1=12848此时单位是us，转换为秒就是12848 / 1000000 此时单位是秒，此时如果乘以340计算出的单位是米，
    # 然后再乘以100就是厘米，因此，直接 用12848/10000即可
    try:
        t3 = time.ticks_diff(t2, t1) / 10000
    except:
        t3 = 0

    # 这里返回的是：开始测距的时间减测距完成的时间*声音的速度/2（来回）
    return t3 * 340 / 2


def mea():  # 超声波工作的主函数
    # try/except语句用来检测try语句块中的错误，从而让except语句捕获异常信息并处理
    try:
        while True:
            distance = measure()
            print("当前测量距离为:%0.2f cm" % distance)
            if distance < 100:
                c.publish('car', 'car_come')
            else:
                led.value(0)
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    # ············


# 下面是传输数据部分的代码 mqtt
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('HUAWEI-2202', '13689816789')
        i = 1
        while not wlan.isconnected():
            print("正在链接...{}".format(i))
            i += 1
            time.sleep(1)
    print('network config:', wlan.ifconfig())


# 1. 联网
# do_connect()

# 2. 创建mqt
c = MQTTClient("umqtt_client", "192.168.3.59")  # 建立一个MQTT客户端
c.connect()  # 建立连接


def main():
    mea()


main()


