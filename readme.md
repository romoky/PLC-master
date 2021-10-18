# 使用须知
### 1.需求介绍

gui.py 负责界面生成，write_lidar_data.py 负责实现snap7开源库方法。本程序主要是项目上有需求，需要从上位机(PC)监控指定文件夹，并获取指定文件里面的值，把这个值写进PLC的DB块里。

### 2.程序界面

#### 1.主界面

![](C:\Users\frank\Pictures\1.PNG)

IP ADDRESS : 需要设置指定PLC的IP地址

WHICH DB : 设置指定PLC 的DB 块

DB OFFSET ：设置DB块的偏移地址

STATUS: 获取监控文件夹所读文件的值

右边区域为LOG，当有按钮触发，或者写入会有相对应的提示信息。

#### 2.专家模式

![](C:\Users\frank\Pictures\2.PNG)

当点击MANUAL 按钮会提示输入密码，默认密码为：expert

![](C:\Users\frank\Pictures\3.PNG)

输入正确密码后分别可以设置IP,DB,以及偏移地址。PATH 按钮是设置需要选择的文件夹，默认为主程序所在文件夹里的data文件夹(./data)，LINK 可以手动连接(成功会有LOG 显示)。

### 3.PLC设置

![](C:\Users\frank\Pictures\4.PNG)

![](C:\Users\frank\Pictures\5.PNG)

![](C:\Users\frank\Pictures\6.PNG)