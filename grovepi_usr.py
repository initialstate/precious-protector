import time
import grovepi
from ISStreamer.Streamer import Streamer
  
# --------- User Settings ---------
# Connect the ultrasonic ranger sensor to one of the digital pins (i.e. 2, 3, 4, 7, or 8)
USR_SENSOR_PIN = 4
OBJECT_NAME = "Cookies"
OBJECT_EMOJI_TOKEN = ":cookie:"
# Initial State settings
BUCKET_NAME = OBJECT_NAME + " Log"
BUCKET_KEY = "pir022016"
ACCESS_KEY = "PLACE YOUR INITIAL STATE ACCESS KEY HERE"
# Set the time between sensor reads
SECONDS_BETWEEN_READS = .2
# ---------------------------------
  
streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
proximity = 1000
lastProximity = 0
compromised = False
 
while True:
    try:
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
