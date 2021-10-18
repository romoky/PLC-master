
from enum import Flag
from genericpath import getsize
import tkinter
from tkinter import ttk
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askdirectory,askopenfilename
from watchdog import observers
import write_lidar_data
import fnmatch
import os
import time
import logging
from logging import exception
import time
from watchdog.observers import Observer
from queue import Queue
import glo
from watchdog.events import PatternMatchingEventHandler
import os
import csv
import sys
import stat

global newIpAdress
newIpAdress = '10.192.12.12' #default ip adress
count = 0
countRight = 0
glo.init()
glo.set_value('watchStatus',False)
glo.set_value('connectPlc',False)
glo.set_value('buttonExit',False)
glo.set_value('countLog',0)
#glo.set_value('dirName','D:\\Minth_Shenyang_SE37\\PDF\\CSV')
glo.set_value('dirName','.//data')
glo.set_value('lidarResult','1000')
glo.set_value('plcDB','83') #default DB
glo.set_value('offset','0')  #default start bit
class handlers(object):
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    #myfileEvent = FileSystemEvent()



    def on_created(event):
        global sourcePath
        #跳过文件夹
        if event.is_directory:
            return
        if getext(event.src_path) == '.csv':
            #print('this is txt file use created')
            sourcePath = event.src_path
            #print(sourcePath)
            showinfo(str(sourcePath)+' has ctreated')
            #file = open("/Users/frank/Desktop/012345678901521250.csv")
            #os.chmod(sourcePath,stat.S_IRWXU)

            try:
                if(os.path.exists(sourcePath)):
                    sz = os.path.getsize(sourcePath)
                    if not sz:
                        showinfo(str(sourcePath)+'is empty')
                        return
                    
                    with open(sourcePath,'r+') as file:
                        csvreader = csv.reader(file)                   
                        rows = []
                        for row in csvreader:
                            rows.append(row)
                        lidarResultNew = rows[5][8]
                    file.close()
                    
                    glo.set_value('lidarResult',lidarResultNew)
                    showinfo('get the value : '+lidarResultNew)
                    lidarv.set(setResultValue())
                    if(LidarTransAuto_button['state'] == tk.NORMAL and LidarTransManual_button['state'] == tk.DISABLED):

                        lidarResult = glo.get_value('lidarResult')
                        offset = glo.get_value('offset')
                        plcDB = glo.get_value('plcDB')
                        write_lidar_data.write_int(int(plcDB),int(offset),int(lidarResult))
                    #print(lidarResultNew)
                else:
                    showinfo('file not exit')
            except Exception as e:
                showinfo('file open error')
                showinfo(str(e))
                #print(e)
                pass
            
            #header = next(csvreader)
            # print(header)
        else: 
            #print("event not txt file.. exiting...")
            pass

        # print(event)
        # print(f"hey, {event.src_path} has been created!")
    def on_deleted(event):
        # print(f"what the f**k! Someone deleted {event.src_path}!")
        if event.is_directory:
            return
        #print(event)


    def on_modified(event):
        global sourcePath
        #sourcePath = event.src_path
        global lastFile
        global n
        n=0


        if event.is_directory:
            return
        if getext(event.src_path) == '.txt':
            print('this is txt file use modified')
            #sourcePath = event.src_path
            #print(sourcePath)
        else: 
            #print("event not directory.. exiting...")
            pass

        #print(event)
        # print(f"hey buddy, {event.src_path} has been modified")
    def on_moved(event):
        print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved
class Label1(object):
    def __init__(self) -> None:
        super().__init__()
    def label_defaultIpAdress(self,root,v,x,y): # a stringvar label 
        global new_IP
        ip_info_label = tkinter.Label(root,textvariable=v,bg='white',bd=2)
        ip_info_label.place(x=x,y=y,width=80,height=25)
    def label_IP(self,x,y):  #text label
        IP_info = 'IP ADDRESS'
        IP_label = ttk.Label(text=IP_info,background='white')
        IP_label.place(x=x,y=y,height=30,width=80)
    def label_db(self,x,y):
        dbValue_info = 'WHICH DB'  #text label
        db_label = ttk.Label(text=dbValue_info,background='white')
        db_label.place(x=x,y=y,width=80,height=30)
    def label_wichdb(self,root,dbv,x,y):
        # a stringvar label
        whichdb_label = ttk.Label(root,textvariable=dbv,background='white')
        whichdb_label.place(x=x,y=y,width=70,height=25)
    def label_rack(self):
        rack = ('机  架:'+str(write_lidar_data.RACK))
        rack_label = ttk.Label(text=rack,background='white')
        rack_label.place(x=60,y=80,width=100,height=30)
    def label_slot(self):
        slot = ('插  槽:'+str(write_lidar_data.SLOT))
        slot_label = ttk.Label(text=slot,background='white')
        slot_label.place(x=60,y=110,height=30,width=80)
    def label_dbStart(self,x,y):
        dbstart_info = 'DB OFFSET'
        dbstart_lable = ttk.Label(text=dbstart_info,background='white')
        dbstart_lable.place(x=x,y=y,width=80,height=30)
    def label_offset(self,offsetv,x,y):
        offset_label = ttk.Label(textvariable=offsetv,background='white')
        offset_label.place(x=x,y=y,width=80,height=25)
    def label_lidarValue(self,x,y):
        lidarValue_info = 'STATUS'
        lidarVlaue_label = ttk.Label(text=lidarValue_info,background='white')
        lidarVlaue_label.place(x=x,y=y,width=80,height=30)
    def label_status(self,lidarv,x,y):
        global status_label
        status_label = ttk.Label(textvariable=lidarv,background='white')
        status_label.place(x=x,y=y,width=80,height=25)

    def label_log(self):
        log_info = 'LOG 记录'
        log_label = ttk.Label(text=log_info,background='white')
        log_label.place(x=400,y=30,height=30,width=70)
class Button1(object):
    def button_codeConfirm(self,root):
        codeConfirm_button = Button(root,text='OK',bg='blue',fg="lightyellow",bd=2,relief=FLAT)
        codeConfirm_button.place(x=170,y=8)
        codeConfirm_button['command'] = lambda:call_getCode()
    def button_set_IP(self,root,x,y):
        global setIp_button
        setIp_button = Button(root,text='SET',bg="orange",bd=2,relief=FLAT)
        setIp_button.place(x=x,y=y)
        setIp_button['command'] = lambda:set_ip_window() #get a window
    def button_ipConfirm(self,root,x,y):
        ipConfirm_button = Button(root,text='OK',bg= "green",bd=2,relief=FLAT)
        ipConfirm_button.place(x=x,y=y)
        ipConfirm_button['command'] = lambda:call_getEntryIP()  #set value in stringVar
    def button_set_DB(self,root,x,y):
        global plcDBwrite_buuton
        plcDBwrite_buuton = Button(root,text='SET',bg="orange",bd=2,relief=FLAT)
        plcDBwrite_buuton.place(x=x,y=y)
        plcDBwrite_buuton['command'] = lambda:set_db_window()  #get a window
    def button_DbConfirm(self,root,x,y):
        DbConfirm_button = Button(root,text='OK',bg='lightyellow',bd=2,relief=FLAT)
        DbConfirm_button.place(x=x,y=y)
        DbConfirm_button['command'] = lambda:call_getEntryDB()  #set value 
    def button_connectToPlc(self,root,x,y):
        connectToPlc_button = Button(root,text='CONNECT',bg='green',bd=2,relief=FLAT)
        connectToPlc_button.place(x=x,y=y)
        connectToPlc_button['command'] = lambda:set_connectToPlc()
    def button_set_Offset(self,root,x,y):
        global set_Offset_button
        set_Offset_button = Button(root,text='SET',bg='orange',relief=FLAT)
        set_Offset_button.place(x=x,y=y)
        set_Offset_button['command'] = lambda:set_offset_window()
    def button_OffsetConfirm(self,root,x,y):
        dbStartAdd_button = Button(root,text='写入',bg="green",bd=2,relief=FLAT)
        dbStartAdd_button.place(x=x,y=y)
        dbStartAdd_button['command'] = lambda:call_getEntryOffset()
    def button_lidarValueAdd(self,root,x,y):
        lidarValueAdd_button = Button(root,text='写入',bg="green",bd=2,relief=FLAT)
        lidarValueAdd_button.place(x=x,y=y)
        lidarValueAdd_button['command'] = lambda:set_lidarValue()
    def button_LidarValueWrite(self,root,x,y):
        global LidarValueWrite_button
        LidarValueWrite_button = Button(root,text='LINK',bg='orange',bd=2,relief=FLAT)
        LidarValueWrite_button.place(x=x,y=y)
        LidarValueWrite_button['command'] = lambda:transValue()
    def button_fileChoose(self,root,x,y):
        global fileChoose_button
        fileChoose_button = Button(root,text='PATH',bg='green',bd=2,relief=FLAT)
        fileChoose_button.place(x=x,y=y)
        fileChoose_button['command'] = lambda:set_filePath_window()
    def button_filepathConfirm(self,root,x,y):
        global setfilePath_button 
        setfilePath_button = Button(root,text= 'OK',bg='orange',relief=FLAT)
        setfilePath_button.place(x=x,y=y)
    def button_LidarTransManual(self,root):
        global LidarTransManual_button
        LidarTransManual_button = Button(root,text='MANUAL',bg='orange',bd=2,relief=FLAT)
        LidarTransManual_button.place(x=80,y=230)
        LidarTransManual_button['command'] = lambda:manualTransValue()
    def button_LidarTransAuto(self,root):
        global LidarTransAuto_button
        LidarTransAuto_button = Button(root,text='AUTO',bg='orange',bd=2,relief=FLAT)
        LidarTransAuto_button.place(x=230,y=230)
        LidarTransAuto_button['command'] = lambda:autoTransValue()
class Entry1(object):

    def __init__(self) -> None:
        super().__init__()
    def Entry_code(self,root):
        global code_entry
        code_entry = ttk.Entry(root)
        code_entry.place(x=5,y=5,width=150,height=35)
        code_entry.bind('<Return>',new_windows)
    def Entry_ip(self,root,x,y):
        global ip_entry
        ip_entry = ttk.Entry(root)
        ip_entry.place(x=x,y=y,width=150,height=30)
    def Entry_DB(self,root,x,y):
        global db_Entry
        plcDB = glo.get_value('plcDB')
        db_Entry = ttk.Entry(root,background='white')
        db_Entry.insert(END,plcDB)
        db_Entry.place(x=x,y=y,width=90,height=30)     
    def Entry_Offset(self,root,x,y):
        global dbStart_entry
        offset = glo.get_value('offset')
        dbStart_entry = ttk.Entry(root,background='white')
        dbStart_entry.insert(END,offset)
        dbStart_entry.place(x=x,y=y,width=90,height=30)
    def Entry_lidarValue(self,root,lidarv):
        global lidarValue_entry
        lidarValue_entry = ttk.Entry(root,textvariable=lidarv,background='white')
        lidarValue_entry.place(x=150,y=520,width=90,height=30)
    def Entry_showPath(self,root,path_var,x,y):
        global showPath_entry
        #dirpath = glo.get_value('dirName')
        showPath_entry = ttk.Entry(root,textvariable=path_var,background='white')
        #showPath_entry.insert(END,str(dirpath))
        showPath_entry.place(x=x,y=y,width=200,height=30)
class App(object):
    def __init__(self):


        #watch file
        #watch file adress
        #path = "C:\\Users\\ijkte\\Desktop\\data"
        global root
        root = Tk()
        global top
        root.title('LIDAR COMMUNICATE')
        root.geometry("790x330")
        root.configure(background='white')
        root.iconbitmap(default='.\\fft-ico.ico')

        #设置画布
        global canvas
        canvas = Canvas(root,height=900,width = 900,bg='CadetBlue')
        canvas.place(x=0,y=0)
        def round_rectangle(x1, y1, x2, y2, radius=25,width1=2, **kwargs):
            global points
            points = [x1+radius, y1,
                    x1+radius, y1,
                    x2-radius, y1,
                    x2-radius, y1,
                    x2, y1,
                    x2, y1+radius,
                    x2, y1+radius,
                    x2, y2-radius,
                    x2, y2-radius,
                    x2, y2,
                    x2-radius, y2,
                    x2-radius, y2,
                    x1+radius, y2,
                    x1+radius, y2,
                    x1, y2,
                    x1, y2-radius,
                    x1, y2-radius,
                    x1, y1+radius,
                    x1, y1+radius,
                    x1, y1]

            return canvas.create_polygon(points, **kwargs, smooth=True,outline='ForestGreen',width=width1)
        #canvas.create_rectangle(30,30,400,310,width=2)
        round_rectangle(30,30,340,290,radius=25,width1=3,fill = 'white')
        #canvas.create_polygon(points,**kwargs, smooth=True,outline='ForestGreen',width=2)
        # canvas.create_rectangle(30,300,320,630,width=2)


        separtor1 = ttk.Separator(root,orient = VERTICAL) #垂直分割线
        separtor1.place(x=370,y=0, relwidth=0, relheight=1)
    
        global v
        v= StringVar()
        global lidarv
        lidarv = StringVar()
        global dbv
        dbv = StringVar()
        global offsetv
        offsetv = StringVar()
        v.set(show_newIP())
        lidarv.set(setResultValue())
        dbv.set(show_newDB())
        offsetv.set(show_newOffset())
        label = Label1()
        label.label_IP(70,50)
        label.label_defaultIpAdress(root,v,198,53)
        round_rectangle(190,50,290,85,radius=10,fill = 'white')
        # label.label_rack()
        # label.label_slot()
        label.label_db(70,95)
        label.label_wichdb(root,dbv,200,95)
        round_rectangle(190,94,290,125,radius=10,fill = 'white')
        label.label_dbStart(70,135)
        label.label_offset(offsetv,200,135)
        round_rectangle(190,134,290,165,radius=10,fill = 'white')
        label.label_lidarValue(70,175)
        label.label_status(lidarv,200,175)
        round_rectangle(190,174,290,205,radius=10,fill = 'white')        
        # label.label_log()
        button = Button1()

        # button.button_set_DB()
        # button.button_OffsetConfirm(root)
        # button.button_lidarValueAdd(root)
        # button.button_connectToPlc(root)
        # button.button_LidarValueWrite(root)
        # button.button_set_DB(root)
        button.button_LidarTransManual(root)
        button.button_LidarTransAuto(root)
        # fileChoose_button.place_forget(root)
        #offset = glo.get_value('offset')
        # entry = Entry1()
        # entry.Entry_showPath(root,path_var,5,5)
        # entry.Entry_Offset(root)  #set db content start address bit  ,like 23
        # entry.Entry_lidarValue(root,lidarv)
        # entry.Entry_DB(root)  #set plc which db ,like db1 ,db2

        #text
        global text
        text = tk.Text(root,bd=2,relief=RIDGE) #设置高度和宽度
        text.place(x=405,y=30,height=260,width=350) 

        # dirName = askdirectory()
        # if(len(dirName)==0):
        #     sys.exit()    
        # glo.set_value('dirName',dirName)
        # showinfo('已选择监控的文件夹：'+dirName)
        call_handler()




        # chooseFile_button['command'] = lambda:set_toChooseFile()

        #set_toChooseFile()
        # dirName = askdirectory()
        # dirName = glo.get_value('dirName')
        # showinfo(dirName)
        #log
        #log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" #log的格式设定
        #time_format = "%Y-%m-%d %H:%M:%S" #时间格式设定
        #logging.basicConfig(filename='test.log',level=logging.INFO,format=log_format,datefmt=time_format) #log名字，等级设定，log默认生成在该py文件所在目录
        #call_handler(self)
        root.bind("<Destroy>",self.shutdown)
        #root.bind("<<WatchdogEvent>>", self.handle_watchdog_event)
    def shutdown(self,event):
        if(glo.get_value('watchStatus')==True):
            my_observer.stop()
            #my_observer.join()
        logging.shutdown()
        #write_lidar_data.plc.disconnect()
        write_lidar_data.plc.destroy()
        #exit()
        #print('shutdown')
    # def handle_watchdog_event(self, event):
    #     """Called when watchdog posts an event"""
    #     watchdog_event = self.queue.get()
    #     print("event type:", type(watchdog_event))
    #     self.text.insert("end", str(watchdog_event) + "\n")
    # def notify(self, event):
    #     """Forward events from watchdog to GUI"""
    #     self.queue.put(event)
    #     root.event_generate("<<WatchdogEvent>>", when="tail")
    def mainloop(self):   
        root.mainloop()
    
def call_handler():

        #path= glo.get_value('path')
        go_recursively = True
        global my_observer
        my_observer = Observer()
        handler = handlers
        path = glo.get_value('dirName')
        my_observer.schedule(handler.my_event_handler,path, recursive=go_recursively)
        my_observer.start()
        watchStatus = glo.set_value('watchStatus',True)

def showinfo(result):
    countLog = glo.get_value('countLog')
    countLog = countLog + 1
    glo.set_value('countLog',countLog)
    realtime = time.strftime("%Y-%m-%d %H:%M:%S")
    textvar = realtime + '  ' +result #系统时间和传入结果
    text.insert('end',textvar) #显示在text框里面
    text.insert('insert','\n') #换行
    if(countLog == 30):
        countLog = 0
        glo.set_value('countLog',0)
        text.delete('1.0','28.0')

def new_windows(self):
    if(glo.get_value('buttonExit')):
        set_Offset_button.place_forget()
        setIp_button.place_forget()
        plcDBwrite_buuton.place_forget()
        LidarValueWrite_button.place_forget()
        fileChoose_button.place_forget()
        glo.set_value('buttonExit',False)
    else:
        code = code_entry.get()
        glo.set_value('code',code)
        if(str(glo.get_value('code')) == 'expert'):
            glo.set_value('firstTap',2)
            root_code.destroy()
            button = Button1()
            button.button_set_IP(root,295,50)
            button.button_set_DB(root,295,95)
            button.button_set_Offset(root,295,140)
            button.button_LidarValueWrite(root,160,230)
            button.button_fileChoose(root,285,230)
            glo.set_value('buttonExit',True)
            # button.button_OffsetConfirm(root)
            # button.button_lidarValueAdd(root)
            # button.button_connectToPlc(root)
            # button.button_LidarValueWrite(root)
            # button.button_set_DB(root)
                    #canvas.create_rectangle(30,30,400,310,width=2)
            
        else:
            if(glo.get_value('firstTap')==1):
                glo.set_value('firstTap',2)                
            else:
                showinfo('WRONG CODE')
        
def set_ip_window():
    global root_setIP
    root_setIP = tkinter.Tk()
    root_setIP.title('SET IP')
    root_setIP.geometry("320x50")
    entry = Entry1()
    entry.Entry_ip(root_setIP,5,5)
    button = Button1()
    button.button_ipConfirm(root_setIP,180,5)
    button.button_connectToPlc(root_setIP,220,5)
def set_db_window():
    root_set_DB = tkinter.Tk()
    root_set_DB.title('SET DB')
    root_set_DB.geometry("300x50")
    entry = Entry1()
    entry.Entry_DB(root_set_DB,5,5)
    button =Button1()
    button.button_DbConfirm(root_set_DB,180,5)
def set_offset_window():
    root_set_Offset = tkinter.Tk()
    root_set_Offset.title('SET OFFSET')
    root_set_Offset.geometry("300x50")
    entry = Entry1()
    entry.Entry_Offset(root_set_Offset,5,5)
    button = Button1()
    button.button_OffsetConfirm(root_set_Offset,180,5)
def set_filePath_window():
    window = tk.Toplevel()
    window.title('SET PATH')        # 设置窗口的标题
    window.geometry('300x50')
    global path_var
    path_var = StringVar()
    path_var.set(show_path())         # 设置窗口的大小
    entry = Entry1()
    entry.Entry_showPath(window,path_var,5,5)
    button = Button1()
    button.button_filepathConfirm(window,250,5)
    def click():
        file_name= filedialog.askdirectory(title='选择一个文件夹',
                                    initialdir='./'           # 打开当前程序工作目录
                                                )
        glo.set_value('dirName',file_name)
        path_var.set(show_path())
    setfilePath_button['command'] = lambda:click()
    showinfo('SET WATCH FILE',glo.get_value('dirName'))
    window.mainloop()
def call_getCode():
    new_windows(self=0)      
def call_getEntryIP():
    global newIpAdress
    newIpAdress = ip_entry.get()
    v.set(show_newIP())
    if fnmatch.fnmatch(newIpAdress,'*.*.*'):
        showinfo("SET IP "+newIpAdress)
        #logging.info('set ip to'+newIpAdress)
    else:
        #print('err type ! plz input right IP!')
        showinfo("err type ! plz input right IP!")
def call_getEntryDB():    
    plcDB = db_Entry.get()
    plcDB = glo.set_value('plcDB',plcDB)
    showinfo('SET DB',plcDB)
    dbv.set(show_newDB())
def call_getEntryOffset():
    offset = int(dbStart_entry.get())
    glo.set_value('offset',offset)
    offsetv.set(show_newOffset())
    showinfo("DB OFFSET"+str(offset))

def show_newIP():
    new_IP = (str(newIpAdress))
    return new_IP
def show_newDB():
    new_DB = glo.get_value('plcDB')
    return new_DB
def show_newOffset():
    newOffset = glo.get_value('offset')
    return newOffset
def show_path():
    new_path = glo.get_value('dirName')
    return new_path
    #print(offset)
def set_lidarValue():
    lidarValue = lidarValue_entry.get()
    glo.set_value('lidarResult',lidarValue)
    #print(lidarValue)
    showinfo("SET VALUE"+lidarValue)
def set_connectToPlc():

    try:
        if(glo.get_value('connectPlc')==False):
            write_lidar_data.connectToplc(newIpAdress,write_lidar_data.RACK,write_lidar_data.SLOT)
            print('connect true')
            glo.set_value('connectPlc',True)
        if write_lidar_data.plc.get_connected():
            showinfo("CONNECT TO PLC SUCCESS")
            plc_info = write_lidar_data.plc.get_cpu_info()
            #print('connect to plc success')
            #print('the plc info :'+str(plc_info))
    except Exception as e:
        showinfo('FAIL TO CONNECT TO PLC')
def transValue():
    if(glo.get_value('connectPlc')==False):
        write_lidar_data.connectToplc(newIpAdress,write_lidar_data.RACK,write_lidar_data.SLOT)
        glo.set_value('connectPlc',True)
        print('connect')
    lidarResult = glo.get_value('lidarResult')
    offset = glo.get_value('offset')
    plcDB = glo.get_value('plcDB')
    write_lidar_data.write_int(int(plcDB),int(offset),int(lidarResult))
    #print('lidarValue:',lidarResult)
    datainDB = write_lidar_data.read_int(int(plcDB),int(offset),2)
    #print('read lidarValue',datainDB)
    if datainDB==int(lidarResult):
        #print('传输成功')
        showinfo("MANUAL LINK SUCCESS")
    else:
        #print('传输错误')
        showinfo("MANUAL LINK FAIL")

def manualTransValue():
    global root_code
    root_code = tkinter.Tk()
    root_code.title('EXPERT MODE')
    root_code.geometry("300x50")
    glo.set_value('code','')
    glo.set_value('firstTap',1)
    codeEntry = Entry1()
    codeEntry.Entry_code(root_code)
    codeButton = Button1()
    codeButton.button_codeConfirm(root_code)
    
def autoTransValue():
    if(LidarTransManual_button['state'] ==tk.NORMAL):     
        LidarTransManual_button['state'] = tk.DISABLED
        showinfo('CHANGE TO AUTO MODE')
        if(glo.get_value('buttonExit')==True):
            new_windows(self=0)
    else:
        LidarTransManual_button['state'] =tk.NORMAL
    if(LidarTransManual_button['state'] == tk.DISABLED):
        global count
        global countRight
        if(count==countRight):
            try:
                if(glo.get_value('connectPlc')==False):
                    write_lidar_data.connectToplc(newIpAdress,write_lidar_data.RACK,write_lidar_data.SLOT)
                    glo.set_value('connectPlc',True)
                if write_lidar_data.plc.get_connected():
                    showinfo("AUTO CONNECT TO PLC SUCCESS")
                plc_info = write_lidar_data.plc.get_cpu_info()
                #print('connect to plc success')
                #print('the plc info :'+str(plc_info))
            except Exception as e:
                showinfo('FAIL TO AUTO CONNECT TO PLC')
            lidarResult = glo.get_value('lidarResult')
            offset = glo.get_value('offset')
            plcDB = glo.get_value('plcDB')
            write_lidar_data.write_int(int(plcDB),int(offset),int(lidarResult))
            datainDB = write_lidar_data.read_int(int(plcDB),int(offset),2)
            if datainDB==int(lidarResult):
                showinfo('CONNECT SUCCESS'+','+'AND VALUE IS'+str(datainDB))
                countRight = countRight+1
            else:
                showinfo('FAIL TO AUTO CONNECT')
                count = count-1
                countRight = countRight-1
        else:
            
            if(LidarTransManual_button['state'] == tk.NORMAL):
                showinfo('CANCEL AUTO MODE')
            else:
                showinfo('AUTO CONNECT')

def getext(filename):
    return os.path.splitext(filename)[-1].lower()
def setResultValue():
    
    lidarResult = glo.get_value('lidarResult')
    
    return lidarResult   

app = App()
app.mainloop()