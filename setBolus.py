
import serial, io
import datetime
from time import sleep
import sys

zahl = sys.argv[1]

print ('\nAufruf mit '+ zahl + ' I.E.')
print ('Mal schnell nen kleinen Boli '+ zahl + ' I.E. abgeben')    # echo line of text on-screen
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
tel_type='\x01\x02'   # Bolus

# Insulin Abgabe in Telegramm eintraggen
param = int(float(zahl)*100)
tel_data=chr(param>>8)+chr(param&255)
# tel_data='\x00\x32'

# CRC Summe Berechnen und in Telgramm eintragen

# my_hex=crc16.crc16xmodem(tel_dir+tel_type+tel_data)
my_hex=crc16_ccitt(0,(tel_dir+tel_type+tel_data))
print("CRC berechnet -> %4x \n"% (my_hex))
tel_crc=chr(my_hex>>8)+chr(my_hex&255)

# Telegramm Ende Kennung
tel_end='\x00\x2e'

# Telegramm zusammen bauen
tel_send=tel_header+tel_len+tel_dir+tel_type+tel_data+tel_crc+tel_end

tel_sendlogin="\x7e\x7e\x03\xf1\x32\x07\xc7\x72\x00\x2e"

# Debug Ausgabe
print ('Senden: '+tel_send)
print ('Senden Hexval Len(%i): '% (len(tel_send))),
tel_sendascii=''
for c in tel_send:
    print ("%2.2x"% ord(c) + ' '),
	#tel_sendascii += hex(ord(c)) + ' '

print
# print ('Senden Hexval Len(%i): '% (len(tel_send))+tel_sendascii)
# print tel_send.encode('hex')

ser = serial.Serial(addr,baud,timeout = 1)
now = datetime.datetime.now()

# ser.write(tel_sendlogin)

ser.write(tel_send)
print ('gesendet!!!')    # echo line of text on-screen
 
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
