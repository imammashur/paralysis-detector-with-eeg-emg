import json
import socket
import hashlib
import logging

LOGFILE = 'logfile.log' #buat file log untuk keluaran eeg
logging.basicConfig(filename=LOGFILE, format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG) #pengaturan basic untuk logfile nanti

STAT_FILE = 'demoeeg.csv' #nama file penyimpanan data eeg, yaitu demoeeg.csv
TGHOST = "127.0.0.1" #ip penyimpanan, ini adalah ip localhost, yaitu pc pribadi
TGPORT = 13854 #port
APPNAME = "myapp" 
APPKEY = "mykey"
CONFSTRING = '{"enableRawOutput": false, "format": "Json"}' #pengaturan standar eeg
EEG_POWER = [ #keluaran sinyal beta eeg dset hanya mengeluarkan lowbeta
    u'lowBeta',
    #u'highBeta',
]

E_SENSE = [
    #u'attention',
    #u'meditation',
]


class ThinkGearConnection(): #Class koneksi dngan thinkgear untuk eeg dan neurosky
    def __init__(self): #Data autentikasi
        self.data_object = {}
        self.auth_request = {}
        self.app_key = ''
        self.app_name = ''
        self.data_to_write = []

    def connect(self, host, port): #Koneksi ke neurosky
        logging.info("Connecting to TGC socket...")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, int(port)))
        return self.sock

    def disconnect(self): #Apabila disconnect dengan neurosky
        pass

    def authenticate(self, app_name, app_key):
        logging.info("Authenticating...")
        self.app_name = app_name
        self.app_key = hashlib.sha1(self.app_key).hexdigest()
        self.auth_request = json.dumps({"appName": self.app_name, "appKey": self.app_key}, sort_keys=False)
        logging.info("Authenticate string: " + self.auth_request)
        #self.auth_request = '{"appName": "Brainwave Shooters", "appKey": "9f54141b4b4c567c558d3a76cb8d715cbde03096"}'
        self.sock.send(str(self.auth_request))
        self.auth_response = self.sock.recv(1024)
        return self.auth_response

    def configure(self): #konfigurasi json untuk kirim data
        logging.info("Configuring TGC to use JSON...")
        self.sock.send(CONFSTRING)
        pass

    def record_data(self): #fungsi merekam data
        logging.info("Recording brain data...") 
        f = open(STAT_FILE,"w") #buka file yg menjadi tempat penyimpanan data
        f.write(','.join(EEG_POWER)+ ','.join(E_SENSE) + '\n') #rekam data
        while (1):
            try: #merekam data low beta
                self.data = self.sock.recv(1024).strip()
                print self.data
                self.json_data = json.loads(str(self.data))
                print self.json_data
                if 'eegPower' in self.json_data:
                    for i in EEG_POWER:
                        if i in self.json_data[u'eegPower']:
                            self.data_to_write.append(str(self.json_data[u'eegPower'][i]))
                        else:
                            self.data_to_write.append('')
                    for i in E_SENSE:
                        if i in self.json_data[u'eSense']:
                            self.data_to_write.append(str(self.json_data[u'eSense'][i]))
                    f.write(','.join(self.data_to_write)+'\n')
                    print ','.join(self.data_to_write)
                    self.data_to_write = []

            except KeyboardInterrupt: #apabila ada interrupt dari keyboard, maka hentikan perekaman
                print "Quitting.."
                #f.close()
                break



if __name__ == "__main__": #fungsi utama program
    conn = ThinkGearConnection() #jalankan koneksi
    try:
        conn.connect(TGHOST, TGPORT)
        logging.info("Connected.")
        if (conn.authenticate(APPNAME, APPKEY)):
            conn.configure()
            conn.record_data()
        else:
            logging.debug(conn.__dict__)
            logging.error("Authorization failed!")
    except Exception: #bila tidak berhasil, maka...
        logging.exception("Exception:")
        logging.error("No connection with TGC socket")

