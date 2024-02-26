# 说明

## 一、功能

1、整体说明：当有车辆经过时候，可以在室内的电脑音响上播放有车来了

2、分为三部分：1）处理超声波传感器的信号。2）使用MQTT协议进行数据的传输，将超声波传感器信号传输到电脑上 3）播放声音

## 二、文件说明

1、main.py是电脑端运行的主程序

2、在esp32上，将umqttsimple.py放在和主目录下，同时将ChaoSheng.py放到Boot.py里面

3、entrance.wav和exit.wav分别是用到的音频文件，用来播放车辆经过的声音

4、需要更改的地方：1）距离根据实际需要调整（程序目前是1m） 2）改变wifi密码和主机电脑的ip地址（mqtt服务器的ip） 3）最后打包python程序为exe

## 三、参考资料

1、购买配件

esp32开发板（23元），可以供电的两节充电模块（20元），超声波传感器（6元）

2、MQTT配置

https://doc.itprojects.cn/0006.zhishi.esp32/02.doc/index.html#/c05.mqtt