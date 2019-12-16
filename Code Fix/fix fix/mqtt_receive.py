import paho.mqtt.client as mqttClient
import time
 
def on_connect(client, userdata, flags, rc): #Fungsi untuk connect ke broker
 
    if rc == 0: #Apabila berhasil terhubung, maka...
 
        print("Connected to broker") #Buat tulisn terubung dengan broker
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed") #ini kalau tidak berhasil terhubung
 
def on_message(client, userdata, message): #Fungsi pembuatan file csv dari emg broker
    print "Message received: "  + message.payload #Tampilkan pesan data diterima dari broker beserta nilai emg
    with open('demoemg.csv','a+') as f: #Buka file demoemg.csv dan write nilai emg
         f.write(message.payload + "\n") #Tulis pesan meg
 
Connected = False   #Diasumsikan secara awal bahwa mqtt tdak terhubung broker, tp klo terhubung maka variabel ini berubah jadi true
 
broker_address= "postman.cloudmqtt.com"  #Broker address
port = 15198                         #Broker port
user = "wqwqirvv"                    #Connection username
password = "PrZi1N3woApH"            #Connection password
 
client = mqttClient.Client("Python")               #buat objek baru yg terhubung dgn broker, atas nama Python
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #fungsi untuk koneksi broker
client.on_message= on_message                      #fungsi untuk pemanggilan bila dalam keadaan terima pesan
 
client.connect(broker_address, port=port)          #hubungkan ke broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Apabila tidak terjadi koneksi maka ...
    time.sleep(0.1) #Tunggu selama 0.1 detik lalu connnecting lagi
 
client.subscribe("esp/emg") #Subscribe topik esp/emg pada broker
 
try:
    while True:
        time.sleep(1)
 
except KeyboardInterrupt: #Bila ada interrupt dari keyboard, maka stop.
    print "exiting"
    client.disconnect()
    client.loop_stop()
