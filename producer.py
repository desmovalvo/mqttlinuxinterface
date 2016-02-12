#!/usr/bin/python

# requirements
import sys
import paho.mqtt.client as mqtt

# main
if __name__ == "__main__":

    # set global attributes
    topic = "command/"

    # read command line parameters
    try:
        host = sys.argv[1].split(":")[0]
        port = int(sys.argv[1].split(":")[1])
    except:
        print "This program must be invoked with:"
        print "$ python producer.py broker_host:broker_port"
        sys.exit(255)

    # connect to the broker
    try:
        mqttclient = mqtt.Client()
        mqttclient.connect(host, port, 60)
    except:
        print "Connection to the broker failed. Exiting."
        sys.exit(0)

    # cycle to read commands
    while true:

        try:
            # read desired commands
            cmd = raw_input('Command to issue: ')
            mqttclient.publish(topic, cmd)

        except KeyboardInterrupt:
            print "CTRL-C pressed. Bye."
            sys.exit(0)
