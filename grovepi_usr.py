import time
import grovepi
from ISStreamer.Streamer import Streamer

# --------- User Settings ---------
PIR_SENSOR_PIN = 8
ROOM_NAME = "Office"
USR_SENSOR_PIN = 4
OBJECT_NAME = "Cookies"
OBJECT_EMOJI_TOKEN = ":cookie:"
# Initial State settings
BUCKET_NAME = ROOM_NAME + " Log"
BUCKET_KEY = "usrpir20"
ACCESS_KEY = "PLACE YOUR INITIAL STATE ACCESS KEY HERE"
# Set the time between sensor reads
SECONDS_BETWEEN_READS = .2
# ---------------------------------
  
grovepi.pinMode(PIR_SENSOR_PIN,"INPUT")
streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
lastValue = "-"
proximity = 1000
lastProximity = 0
compromised = False
 
while True:
    try:
        # Detect motion and log when there are changes
        if grovepi.digitalRead(PIR_SENSOR_PIN):
            if lastValue != "active":
                lastValue = "active"
                streamer.log (ROOM_NAME + " Motion", lastValue)
                streamer.flush()
                print 'Motion Detected'
        else:
            if lastValue != "inactive":
                lastValue = "inactive"
                streamer.log (ROOM_NAME + " Motion", lastValue)
                streamer.flush()
                print '-'
 
        # If distance value from Ultrasonic is less than 60 cm, log it
        proximity = grovepi.ultrasonicRead(USR_SENSOR_PIN)
        if proximity < 60:
            if proximity != lastProximity:
                if not compromised:
                    streamer.log(OBJECT_NAME + " Compromised", OBJECT_EMOJI_TOKEN)
                    compromised = True
                streamer.log ("Proximity to " + OBJECT_NAME + "(cm)", proximity)
                streamer.flush()
                print proximity
                lastProximity = proximity
        # Safe distance away
        else:
            proximity = 1000
            compromised = False
            if lastProximity != 1000:
                streamer.log ("Proximity to " + OBJECT_NAME + "(cm)", proximity)
                streamer.flush()
                print proximity
                lastProximity = proximity

        time.sleep(SECONDS_BETWEEN_READS)
 
    except TypeError:
        print "Error"
    except IOError:
        print "Error"
