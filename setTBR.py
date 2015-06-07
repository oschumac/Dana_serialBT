
import serial, io
import datetime
from time import sleep
import sys

zahl = sys.argv[1]

print ('Mal schnell TBR auf  '+ zahl + ' % anpassen')    # echo line of text on-screen
print 
addr  = 'COM12'  # Edison UART1 PORT NAME
baud  = 9600            # baud rate for serial port

def crc16_ccitt(crc, data):
    msb = crc >> 8
    lsb = crc & 255
    for c in data:
        x = ord(c) ^ msb
        x ^= (x >> 4)
        msb = (lsb ^ (x >> 3) ^ (x << 4)) & 255
        lsb = (x ^ (x << 5)) & 255
    return (msb << 8) + lsb
	
# Telegramm Kopf 
tel_header='\x7e\x7e'
tel_len='\x05'
tel_dir='\xf1'
# Telegrammtyp
tel_type='\x04\x01'   # TBR setzen

# Insulin Abgabe in Telegramm eintraggen
param = int(zahl)
tel_data=chr(param&255)+chr(1)
# tel_data='\x00\x32'
my_hex=crc16_ccitt(0,(tel_dir+tel_type+tel_data))
print("CRC berechnet -> %4x \n"% (my_hex))
tel_crc=chr(my_hex>>8)+chr(my_hex&255)
# Telegramm Ende Kennung
tel_end='\x00\x2e'


tel_TBRSTOP='\x7e\x7e\x03\xf1\x04\x03\x28\xc5\x00\x2e'
# Telegramm zusammen bauen
tel_send=tel_header+tel_len+tel_dir+tel_type+tel_data+tel_crc+tel_end

# Debug Ausgabe
print ('Senden Hexval Len(%i): '% (len(tel_TBRSTOP))),
tel_sendascii=''
for c in tel_TBRSTOP:
    print ("%2.2x"% ord(c) + ' '),

print

ser = serial.Serial(addr,baud,timeout = 1)
now = datetime.datetime.now()

ser.write(tel_TBRSTOP)
print ('TBR Stop gesendet')

 
read_byte = ser.read()
tel_emp=''
last_read=''
while read_byte is not None:
    
	read_byte = ser.read()
	
	if len(read_byte) > 0:
		print ("%2.2x"% ord(read_byte) + ' '),
		if (read_byte == chr(46)) & (last_read ==chr(46)) :
			print
		last_read=read_byte
	else:
		read_byte=None


print ('Senden Hexval Len(%i): '% (len(tel_send))),

for c in tel_send:
    print ("%2.2x"% ord(c) + ' '),
print

ser.write(tel_send)
print ('TBR gesendet!!!')    # echo line of text on-screen


read_byte = ser.read()
tel_emp=''
last_read=''
while read_byte is not None:
    
	read_byte = ser.read()
	
	if len(read_byte) > 0:
		print ("%2.2x"% ord(read_byte) + ' '),
		if (read_byte == chr(46)) & (last_read ==chr(46)) :
			print
		last_read=read_byte
	else:
		read_byte=None

