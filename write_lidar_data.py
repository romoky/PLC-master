import snap7
from snap7.types import Areas
import struct

IP = '192.168.1.9'
RACK = 0
SLOT = 1

DB_NUMber = 12
Start_adress = 0
Size = 259

plc = snap7.client.Client()

def connectToplc(IP,RACK,SLOT):

    plc.connect(IP,RACK,SLOT)

#连接至plc
#connectToplc(IP,RACK,SLOT)

#plc_info = plc.get_cpu_info()
#print(f'Module Type:{plc_info.ModuleTypeName}')


# state = plc.get_cpu_state()
# print(f'State:{state}')
# db = plc.db_read(1,0,259)

# trans_name = db[2:256].decode('UTF-8').strip('\x00')
# print(f'Trans Name:{trans_name}')

# trans_value = int.from_bytes(db[256:258],byteorder='big')
# print(trans_value)




# #write_db[256:258] = buffer
# #new_trans_value = int.from_bytes(write_db[256:258],byteorder='big')

# trans_status = bool(db[258])
# print(trans_status)

# 读 m 点数据
# a=plc.read_area(snap7.types.Areas.MK,0,3,1) #读取M3.0~M3.7数据
# print(a)
# b = struct.unpack('!?',a)[0]
# print(b)
# data = b|0b0001000
# write_value = plc.write_area(snap7.types.Areas.MK,0,3,struct.pack('! b',data))


#写db int数据
#my_int_value = 4321
def write_int(db_num,start_byte,int_value): #Integer yazma 
    data = bytearray(2)
    snap7.util.set_int(data,0,int_value)
    plc.write_area(snap7.types.Areas.DB,db_num,start_byte,data)  

#write_int(1,256,my_int_value)

def write_bool(db_num,start_byte,boolean_index,bool_value): #Bool yazma 
    data = bytearray(1)
    snap7.util.set_bool(data,0,boolean_index,bool_value)
    plc.write_area(snap7.types.Areas.DB,db_num,start_byte,data)

def write_byte(db_num,start_byte,byte_value): #Byte yazma 
    data = bytearray(1)
    snap7.util.set_byte(data,0,byte_value)
    plc.write_area(snap7.types.Areas.DB,db_num,start_byte,data)

def write_real(db_num,start_byte,real_value): #Real yazma 
    data = bytearray(4)
    snap7.util.set_real(data,0,real_value)
    plc.write_area(snap7.types.Areas.DB,db_num,start_byte,data)


#读 int数据

def read_int(db_num,start_byte,size):
    q = plc.read_area(snap7.types.Areas.DB,db_num,start_byte,size)
    outData = struct.unpack('!h',q)[0]
    return outData

# a =read_int(1,256,2)
# #解码
# outdata = struct.unpack('!h',a)[0]
# print(outdata)


# Format	C Type	Python	字节数
# x	pad byte	no value	1
# c	char	string of length 1	1
# b	signed char	integer	1
# B	unsigned char	integer	1
# ?	_Bool	bool	1
# h	short	integer	2
# H	unsigned short	integer	2
# i	int	integer	4
# I	unsigned int	integer or lon	4
# l	long	integer	4
# L	unsigned long	long	4
# q	long long	long	8
# Q	unsigned long long	long	8
# f	float	float	4
# d	double	float	8
# s	char[]	string	1
# p	char[]	string	1
# P	void *	long




# #写db int数据
# my_int_value = 5162
# byte_num = bytearray(2)
# snap7.util.set_int(byte_num,0,my_int_value)
# print(byte_num)
# #out_data = struct.pack('!h',in_value) 打包int value
# plc.write_area(snap7.types.Areas.DB,1,256,byte_num)


#写db bool
# db_bool = plc.read_area(snap7.types.Areas.DB,1,258,1)
# print(db_bool)
# db_bool_unpack = struct.unpack('!?',db_bool)[0]
# data_indb_bool = db_bool_unpack|0b00000011
# plc.write_area(snap7.types.Areas.DB,1,258,struct.pack('!b',data_indb_bool))