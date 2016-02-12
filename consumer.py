#!/usr/bin/python

# requirements
import sys
import subprocess
import paho.mqtt.client as mqtt

# command callback
def command_callback(client, userdata, msg):

    # get the payload (= command)
    command = msg.payload

    # run the command
    print "Issuing command %s" % command
    try:
        subprocess.call(command.split(" "))
    except:
        print "...command execution failed"
    
   
# main
if __name__ == "__main__":

    # set global attributes
    topic = "command/"
    allowed = ["alsamixer"]

    # read command line parameters
    try:
        host = sys.argv[1].split(":")[0]
        port = int(sys.argv[1].split(":")[1])
    except:
        print "This program must be invoked with:"
        print "$ python consumer.py broker_host:broker_port"
        sys.exit(255)

    # connect to the broker
    try:
        mqttclient = mqtt.Client()
        mqttclient.connect(host, port, 60)
    except:
        print "Connection to the broker failed. Exiting."
        sys.exit(0)

    # bind the callback
    mqttclient.on_message = command_callback

    # subscribe
    mqttclient.subscribe("command")

    # loop until ctrl-c is pressed  
    try:
        mqttclient.loop_forever()
    except KeyboardInterrupt:
        print "CTRL-C pressed, bye!"
        mqttclient.unsubscribe("command")
        mqttclient.disconnect()      
        sys.exit(0)
