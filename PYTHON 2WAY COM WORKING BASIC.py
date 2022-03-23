############################################################################
##TESTFILE FOR 2 WAY COMMUNICATION BETWEEN PYTHON AND ARDUINO             ##
##PYTHON PART                                                             ##
##                                                                        ##
##created by Jan Meyne                                                    ##
##22.03.2022 @DLR Köln                                                    ##
############################################################################
#
# Python sends:
# start,indexcom+1,int_data+1,float_data+1,string_data,end\n
# Arduino sends:
# start,indexcom+2,int_data+2,float_data+2,zyx+ard,end\n
# 
#
#Teststring for the Serial Monitor of Arduino IDE:
#   
# 
# 
# 
# 
# 
#  start,0,123,123.456,abcde,end\n



import serial
import time
############################################################################
#		
#			SETTINGS HERE:
#
############################################################################
#(check for your COM port in the device manager or easier the Arduino IDE )
COM_port_arduino	=	"COM5"
BAUD_rate_arduino	=	9600

#for how many iterations shall be tested here
Test_iterations		=	200
#How fast to iterate
Loop_speed			=	0.8		#[s]

#FYI: good values are about 0.3 s loopspeed as package loss increases if loop rate gets faster

#FYI: Different Mikrocontroller Boards may need a slower pace to work correctly 
# 											tested
# 											Arduino Uno: 	0.4	s Loopspeed 
# 											Arduino Mega:	1	s Loopspeed
############################################################################






#starts of data variables:
indexcom			=	0
int_data			=	123
float_data			=	123.456
string_data			=	"abcde"
package_reciv_index	= 	0
package_send_index	=	0
start_time			=   time.time()
#iterable
i					=	0

try:	
		Serialreader = serial.Serial(port=COM_port_arduino, baudrate=BAUD_rate_arduino,timeout=1, rtscts=True)
		#Serialreader.flushInput()
		time.sleep(0.05)
except:
		print("############################################################################")
		print("COM FAILED")	
		print("############################################################################")


#LOOP:
while i<Test_iterations:

	# Check if new data arrived:
	if Serialreader.inWaiting() > 0:
			#decode from utf8 into string
			serial_read_from_controller= Serialreader.readline().decode()
			#strip end
			serial_read_from_controller =serial_read_from_controller.strip("\n")
			#split at commata
			serialread_string_splitted=serial_read_from_controller.split(",")

			#check if line is complete if not skip reading
			if len(serialread_string_splitted)<6:
				pass

			else:
				print("DATA received:    " + serial_read_from_controller)
				indexcom_received			=	int(serialread_string_splitted[1])
				int_data_received			=	int(serialread_string_splitted[2])
				float_data_received			=	float(serialread_string_splitted[3])
				string_data_received		=	serialread_string_splitted[4]

				indexcom=indexcom_received+1
				package_reciv_index+=1

			
			#Data is always send 3 packets a time so rest needs to be cleared out
			Serialreader.flushInput()
	
	
	int_data=int_data+2
	float_data=float_data+2

	


	DATA_to_SEND = "start" +","+ str(indexcom) +","+ str(int_data) +","+ str(float_data) +","+ string_data +","+ "end" +"\n"

	print("DATA send:        "+ DATA_to_SEND)
	

	time.sleep(Loop_speed)

	#send data 3 pakets:
	Serialreader.write(bytes(DATA_to_SEND, 'utf-8'))
	Serialreader.write(bytes(DATA_to_SEND, 'utf-8'))
	Serialreader.write(bytes(DATA_to_SEND, 'utf-8'))

	lost_total= package_send_index-package_reciv_index
	if package_send_index>1:
		average_paket_loss=100-(package_reciv_index/package_send_index)*100
	else:
		average_paket_loss=0

	package_send_index+=1


	# calculate packet loss rate and total pakage loss
	i =i+1
	#calculate time of connection without major error(package read wrong as for e.g.  a comma gets lost and the data is invalid)
	connection_time = time.time() -start_time


	#print data to the Terminal of python environment
	print( "Package Nr:" + str(i) + "  PAKET_LOSS:  " + str(int(average_paket_loss)) + " %" + "  lost total: " + str(int(lost_total))+"    time of connection: " + str(int(connection_time)) +"seconds"  )  



	#EOLOOP