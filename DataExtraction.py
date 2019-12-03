import sys
from flask import Flask
from flask_sockets import Sockets
import os
import time

app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/accelerometer')
def echo_socket(ws):
    #############################################################################################################
    #
    #
    # 1. open PhonePi app and enter your PC IP Address and append port number :5000
    #
    #
    #
    #
    ###############################################################################################################
    ###############################################################################################################
    ###############################################################################################################
    ###############################################################################################################
    ###############################################################################################################
    ###############################################################################################################
    ###############################################################################################################
    ###############################################################################################################
    ###############################################################################################################
    ###############################################################################################################
    ######################
    waiting = False
    cycle = False
    blocked = False
    num = 0
    released = True
    informed = False
    start = time.time()
    end = time.time()
    Gstart = time.time()
    blockingStartTime = time.time()
    gestureName = "up"
    index = 0
    #####
    i = 0
    c = False
    fileName = ""
    print("\n\n\n\n\n\n\n\n\n\n\n\nWaiting for New Gesture Start\n")
    #######################
    while True:
        message = ws.receive()
        # ws.send(message)
        data = str(message)
        Acc_data = data.split(",")
        a = float(Acc_data[2])
        #######################
        end = time.time()
        delay = end - start
        if ((not cycle) & blocked):
            delay = 0.0
            waiting = False
            if ((end - blockingStartTime) > 3.0):
                blocked = False
                if released:
                    print("\n\n\n\nWaiting for a New Gesture Start\n")
                else:
                    print("\n\n\n\nPLZ Shake Your Mobile then\nStart a New Gesture\n")
        Gtime = end - Gstart
        if ((delay > 5.0) & informed):
            informed = False
            waiting = False
            released = False
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nWaiting for New Gesture Start")
        if ((a > 9.0) & (a < 11)):
            if ((delay > 0.7) & waiting):
                if cycle:
                    cycle = False
                    released = False
                    waiting = False
                    if c:
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nGesture Recognized Successfully\n")
                else:
                    if not informed:
                        print("\n*\n**\n***\nGO AHEAD\n")
                        informed = True
                        os.system('spd-say "GO"')
            if ((not waiting) & released):
                start = time.time()
                waiting = True
        else:
            released = True
            if (informed):
                cycle = True
                informed = False
                waiting = False
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nRecording started\n*\n**\n***\n****\n\n")
                Gstart = end
            else:
                waiting = False
        #######################
        if cycle:
            if ((Gtime > 6.0) & c):
                f.close()
                os.remove(fileName)
                i = i - 1
                c = False
                cycle = False
                waiting = False
                informed = False
                released = False
                blocked = True
                blockingStartTime = time.time()
                print("Gesture Timeout >> TOO Long !!!\n\nTry Again\n\n")
                os.system('spd-say "long"')

            else:
                if not c:
                    fileName = "ACC_" + str(i + 67) + ".csv"
                    i = i + 1
                    if os.path.isfile(fileName) == False:
                        f = open(fileName, "w+")
                        print (message, file=f)
                        f.close()
                        c = True
                        numReadings = 1
                    else:
                        print("PLEASE REMOVE EXISTING FILES")


                else:
                    if os.path.isfile(fileName) == True:
                        f = open(fileName, "a")
                        print (message, file=f)
                        numReadings = numReadings + 1
                    else:
                        print("ERROR PLEASE REPEAT RECORDING")
        else:
            if c:
                if ((numReadings - 140) >= 200):
                    f.close()
                    c = False
                    print(
                        "Gesture Saved Successfully\nTotal Number of Useful Readings =%4d  (@Gtime=%.2fs)\n\nTOTAL No of Recorded Gestures = %4d  \n\n" % (
                        (numReadings - 140), Gtime, i))
                    say = str(i)
                    os.system('spd-say "Successfull"')
                    blocked = True
                    blockingStartTime = time.time()
                else:
                    f.close()
                    os.remove(fileName)
                    i = i - 1
                    c = False
                    blocked = True
                    blockingStartTime = time.time()
                    print("Gesture Deleted >> TOO Short !!!\n\nTry Again\n\n")
                    os.system('spd-say "short"')

        #######################
        ws.send(message)


#######################

@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == "__main__":
    a = 0
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('192.168.0.81', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
