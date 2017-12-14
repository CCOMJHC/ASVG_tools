#!/usr/bin/env python
''' A python module for logging bandwidth utilization

'''

import subprocess
import time
import datetime
import json

class bandwidthLogger():
    ''' The bandwidth logger class.

    server_address:   IP address or hostename where the iperf3 server is running.
    interval          Interval between measurements (must be > 10 s)

    '''    
    def __init__(self,server_address="localhost", log_interval=60, verbose = True):
        self.server_address = server_address
        if log_interval < 10:
            print("ERROR: Interval must be > 10")
            return 1
            
            
            
        self.log_interval = log_interval
        self.client = None
        self.result = None
        self.verbose = verbose
        
    def measure_bandwidth(self):

        p = subprocess.Popen("/usr/bin/iperf3 -J -c mystiquec", 
                        stdout=subprocess.PIPE,
                        shell=True)
        (result, error) = p.communicate()
        p.wait()
        if not error:
            self.result = json.loads(result)
                #print(json.dumps(self.json_result,indent=4))
        else:
            print(error)        
        

    def basic_result(self):
        ''' Returns time in unix epoch seconds, Mbps received and retransmits of sender'''

        host = self.result["start"]["connecting_to"]["host"]        
        timesecs = self.result["start"]["timestamp"]["timesecs"]
        Mbps = self.result["end"]["streams"][0]["receiver"]["bits_per_second"]
        Mbps = float(Mbps) / 1024 / 1024
        retransmits = self.result["end"]["streams"][0]["sender"]["retransmits"]
        
        return ("%s\t%d\t%0.3f\t%d\n" % 
         (host,timesecs,Mbps,retransmits))        

    

    def run(self):

        while True:
           
            try:
    
                self.measure_bandwidth()

                print(self.basic_result())            
                time.sleep(self.log_interval - 10.0)
            except KeyboardInterrupt:
                return


if __name__ == '__main__':
    
    logger = bandwidthLogger(server_address = "mystiquec")
    logger.run()
    
    
