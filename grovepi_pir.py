import time
import grovepi
from ISStreamer.Streamer import Streamer

# --------- User Settings ---------
# Connect the PIR motion sensor to one of the digital pins (i.e. 2, 3, 4, 7, or 8)
PIR_SENSOR_PIN = 8
ROOM_NAME = "Office"
# Initial State settings
BUCKET_NAME = ROOM_NAME + " Log"
BUCKET_KEY = "pir022016"
ACCESS_KEY = "PLACE YOUR INITIAL STATE ACCESS KEY HERE"
# Set the time between sensor reads
SECONDS_BETWEEN_READS = .2
# ---------------------------------
  
grovepi.pinMode(PIR_SENSOR_PIN,"INPUT")
streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
lastValue = "-"
 
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
 
        time.sleep(SECONDS_BETWEEN_READS)
 
    except IOError:
        print "Error"
