import socket
import datetime
from datetime import datetime, timedelta
import re
import os
import pandas as pd
import numpy as np
import time

class GazePoint:
    def __init__(self, host, port, base_dir):
        self.host = host
        self.port = port
        self.address = (self.host, self.port)
        self.input_buffer_size = 4096
        self.base_dir = base_dir

    def run_gazepoint(self):

        # Get the gaze tracking screen position and size or set the screen on which the gaze tracking is to be performed.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.address)

        s.send(str.encode('<GET ID="SCREEN_SIZE" />\r\n'))
        s.send(str.encode('<SET ID="ENABLE_SEND_DATA" STATE="1" />\r\n'))
        rxdat = s.recv(self.input_buffer_size)
        string = bytes.decode(rxdat)
        ID, X, Y, WIDTH, HEIGHT = re.findall(r'"(.*?)"', string)
        if ID == 'SCREEN_SIZE':
            print('captured screen dimensions')
        else:
            print('did not captured screen dimensions')
        s.close()
        time.sleep(0.25)

        # configure data server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.address)
        s.send(str.encode('<SET ID="ENABLE_SEND_COUNTER" STATE="1" />\r\n'))
        s.send(str.encode('<SET ID="ENABLE_SEND_CURSOR" STATE="1" />\r\n'))
        s.send(str.encode('<SET ID="ENABLE_SEND_POG_FIX" STATE="1" />\r\n'))
        s.send(str.encode('<SET ID="ENABLE_SEND_POG_LEFT" STATE="1" />\r\n'))
        s.send(str.encode('<SET ID="ENABLE_SEND_POG_RIGHT" STATE="1" />\r\n'))
        # s.send(str.encode('<SET ID="ENABLE_SEND_TIME" STATE="1" />\r\n'))

        # start data server sending data
        s.send(str.encode('<SET ID="ENABLE_SEND_DATA" STATE="1" />\r\n'))
        time.sleep(0.25)

        ii = -1
        tot_sec = 120  # 120, actually not necessary
        print('run tracking for', tot_sec, 'seconds')
        t_end = datetime.now() + timedelta(seconds = tot_sec)

        # csv_filename = self.base_dir + 'gaze_data.csv'
        csv_filename = os.path.join(self.base_dir, 'gaze_data.csv')
        if not os.path.exists(csv_filename):
            df = pd.DataFrame(
                columns=['Date', 'Time', 'FPOGID', 'FPOGD', 'FPOGX', 'FPOGY', 'LPOGX', 'LPOGY', 'RPOGX', 'RPOGY', 'CX',
                         'CY', 'timestamp'])
            df.to_csv(csv_filename, index=False)

        while datetime.now() < t_end:

            timestamp0 = time.time()
            rxdat = s.recv(self.input_buffer_size)
            string = bytes.decode(rxdat)

            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            timestamp = time.time()
            # print(timestamp - timestamp0)
            # print(string)
            # only parse if a data REC response was recieved (ignore CALib etc)
            if len(rxdat) > 0 and "<REC" in string:
                string = [i for i in string.split('<') if i[:3] == 'REC'][0]

                re.findall(r'"(.*?)"', string)
                CNT, FPOGX, FPOGY, FPOGS, FPOGD, FPOGID, FPOGV, LPOGX, LPOGY, LPOGV, RPOGX, RPOGY, RPOGV, CX, CY, CS = re.findall(
                    r'"(.*?)"', string)

                if FPOGV == "1":
                    FPOGV = 1.0
                else:
                    FPOGV = np.nan
                    continue

                if LPOGV == "1":
                    LPOGV = 1.0
                else:
                    LPOGV = np.nan

                if RPOGV == "1":
                    RPOGV = 1.0
                else:
                    RPOGV = np.nan

                dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # ii += 1
                # df.loc[ii]
                new_row = dt.split(' ')[0] + ',' + dt.split(' ')[1] + ',' + FPOGID+ ',' + str(np.float(FPOGD) * FPOGV) \
                             + ',' + str(np.float(FPOGX) * FPOGV) + ',' + str(np.float(FPOGY) * FPOGV) \
                             + ',' + str(np.float(LPOGX) * LPOGV) + ',' + str(np.float(LPOGY) * LPOGV) \
                             + ',' + str(np.float(RPOGX) * RPOGV) + ',' + str(np.float(RPOGY) * RPOGV) \
                             + ',' + CX + ',' + CY + ',' + str(timestamp) + '\n'

                with open(csv_filename, 'a') as fd:
                    fd.write(new_row)
                # df.to_csv(self.base_dir + 'gaze_data.csv', mode='a', index=False)
                # print("write new data to csv!")

        s.close()
        print('Done!')


# if __name__ == '__main__':
#     HOST = '127.0.0.1'
#     PORT = 4242
#     ADDRESS = (HOST, PORT)
#     InputBufferSize = 4096
#     base_dir = "C:\\Users\\zhangzhida\\Desktop\\EyeGazePipeline\\DataCollection\\"
#
#     eyegaze = GazePoint(HOST, PORT, base_dir)
#     eyegaze.run_gazepoint()