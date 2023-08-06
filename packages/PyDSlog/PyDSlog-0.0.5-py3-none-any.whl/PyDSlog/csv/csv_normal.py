import os
import time
import numpy as np
import serial
from datetime import datetime, timedelta
import PyDSlog.stream.IO5640_stream as ssv_io  # import IO/5640-DS Stream module

class CSV_saver:
    
    def __init__(self, channels_to_use, cycles, frequency, file_name, filepath, header=True, add_tmp=None, 
                 date_format="%H:%M:%S,%d/%m/%Y", w_mode="a"):

        self.channels_to_use = channels_to_use
        self.cycles = cycles
        self.frequency = frequency
        self.file_name = file_name
        self.filepath = filepath
        self.header = header
        self.add_tmp = add_tmp
        self.w_mode = w_mode
        self.date_format = date_format
        

    def generate_csv(self, port, baudrate, block_size, n_frames=100):
        
        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)    

        period_block = float(block_size)/float(self.frequency) 
        period = float(1)/float(self.frequency)      # period
        period_ms = period * 1000
        #cycles = int(self.time/period_block)
        
        try:
            
            ser = serial.Serial(port, baudrate=baudrate)  # open serial port with baudrate 115200
            ssv_io.start_IO5640_stream(self.channels_to_use, self.frequency, ser)  # start stream    

            f = open(self.filepath + self.file_name , self.w_mode)
            
            if(self.header == True and self.add_tmp == "ms"):                
                header = "timestamp," + ','.join(self.channels_to_use) + "\n"
                f.write(header)
                
            elif(self.header == True and self.add_tmp == "date"):                
                header = "time,date," + ','.join(self.channels_to_use) + "\n"
                f.write(header)
                
            elif(self.header == True and self.add_tmp is None):                
                header = ','.join(self.channels_to_use) + "\n"
                f.write(header)

            for i in range(0, self.cycles):                    # read cycles times                   
                if(self.add_tmp == "ms"):
                    
                    millis = int(round(time.time() * 1000))       # actual timestamp in milliseconds
                    
                elif(self.add_tmp == "date"):                    
                    now_datetime = datetime.now()                
                
                r = ssv_io.read_IO5640_stream_block(block_size, len(self.channels_to_use), ser, block_size) 
                r = np.transpose(r)
                
                string = ""
                for d in range(0, r.shape[0]):                    
                    s = np.array2string(r[d], precision=0, separator=',',suppress_small=True)[1:-1]    
                    
                    if(self.add_tmp == "ms"):                        
                        s = str(millis + int(period_ms*d)) + "," + s + "\n"
                        
                    elif(self.add_tmp == "date"):                        
                        now = now_datetime + timedelta(0,period*d)
                        date_time = now.strftime(self.date_format)
                        s = date_time + "," + s + "\n"
                        
                    else:
                        s = s + "\n"
                        
                    string = string + s
                    
                string = string.replace(" ","")    
                f.write(string)
            
        finally:
            
            f.close()
            ssv_io.stop_IO5640_stream(ser)          # stop stream
            ser.close()  


