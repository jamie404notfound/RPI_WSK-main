import time
from time import sleep
from sense_hat import SenseHat
# from sense_emu import SenseHat
import csv
import thingspeak
import http.client as httplib
# import sqlite3


# Initialise Sense-Hat
sense = SenseHat()
sense.clear()
sense.low_light = True

# ThingSpeak Channel ID & Write Key
channel_id = xxxx
write_key = 'xxxx'
channel = thingspeak.Channel(id=channel_id, api_key=write_key)

# Arrays for Average Calculations
tempMean = []
humidMean = []
atmosMean = []

# Check Internet Status Boolean
_netCheck = False

# **** DISABLED TO SAVE POWER****
# Create Connection to SQLite3 Database
# conn = sqlite3.connect('concept.db')
# c = conn.cursor()

# Save Readings to DB
# def write_to_SQL():
#     c.execute("INSERT INTO sensehat(temperature,humidity,pressure,Date,Time) VALUES(?,?,?,?,?)",
#               (temperature, humidity, pressure, date, t))
#     conn.commit()
#     sense.show_message("Reading")

# Send Sensor Readings to ThingSpeak
def measure(channel):
    response = channel.update({'field1': temperature, 'field2': humidity, 'field3': pressure})

# Save Readings to CSV file
def write_to_CSV():
    # a for Append, w Overwrites the File
    with open('./sensor_readings.csv', mode='a') as sensor_readings:
        sensor_write = csv.writer(sensor_readings, delimiter=',',
                                  quotechar='”', quoting=csv.QUOTE_MINIMAL)
        write_to_log = sensor_write.writerow(
            [temperature, humidity, pressure, date, t])
        return (write_to_log)

# Show Temperature on LED Panel - Text & BG Colour
def show_Temp(meanTemp):
    sense.clear()
    sense.low_light = True
    temperatureWord = str(meanTemp)
    if meanTemp < 3.0:
        sense.low_light = True
        sense.show_message(temperatureWord+"C", text_colour=[0, 200, 200])
    elif meanTemp > 40.0:
        sense.low_light = True
        sense.show_message(temperatureWord+"C", text_colour=[200, 0, 0])
    else:
        sense.low_light = True
        sense.show_message(temperatureWord+"C",
                           text_colour=[255, 255, 255], back_colour=[0, 200, 0])
        
    sense.clear()
    
# Show Humidity on LED Panel - Text & BG Colour
def show_Humid(meanHumid):
    sense.clear()
    sense.low_light = True
    humidWord = str(meanHumid)
    sense.show_message(humidWord+"%",
                        text_colour=[255, 255, 255], back_colour=[0, 0, 0])      
    sense.clear()

# Show Atmospheric Pressure on LED
def show_Atmos(meanAtmos):
    sense.clear()
    sense.low_light = True
    atmosWord = str(meanAtmos)
    sense.show_message(atmosWord+"mbar",
                        text_colour=[255, 255, 255], back_colour=[0, 0, 0])      
    sense.clear()

# Calculate Average Temperature - Uses Last 5 Values
def calculate_Mean(arr):
    last_five_values = arr[-5:]
    mean = round(sum(last_five_values)/len(last_five_values), 2)
    return mean

# Check Internet Connectivity - Acquire Header from URL
def checkInternetHttplib(url="www.google.com",
                         timeout=3):
    connection = httplib.HTTPConnection(url,
                                        timeout=timeout)
    
    global _netCheck
    
    try:
        connection.request("HEAD", "/")
        connection.close()
        # print("Internet on..")
        _netCheck = True
        return True
    except Exception as exep:
        # print("No connection available..")
        _netCheck = False
        return False

# Joystick Controller Event Handler
def pushed_up(event):
    show_Temp(meanTemp)

def pushed_down(event):    
    if(checkInternetHttplib("www.google.com", 3) is not False):
        sense.low_light = True
        sense.show_message("Y",
                           text_colour=[255, 255, 255], back_colour=[0, 200, 0])
        sense.clear()
    else:
        sense.low_light = True
        sense.show_message("N",
                           text_colour=[255, 255, 255], back_colour=[200, 0, 0])
        sense.clear()

def pushed_left(event):
    show_Humid(meanHumid)

def pushed_right(event):
    show_Atmos(meanAtmos)

# sense.stick.direction_middle = pushed_up
sense.stick.direction_up = pushed_up
sense.stick.direction_down = pushed_down
sense.stick.direction_left = pushed_left
sense.stick.direction_right = pushed_right


if __name__ == "__main__":
    try:        
        sense.show_message("ON")
        
        while True:
            # Read and Round Sensor Data to Applicable Decimal Points + Date/Time
            temperature = round(sense.get_temperature(), 1)
            humidity = round(sense.get_humidity(), 1)
            pressure = round(sense.get_pressure(), 2)
            date = time.strftime("%Y - %m - %d ")
            t = time.strftime("%H:%M:%S")
            # Add Rounded Sensor Readings to Arrays - Run Average Calculations
            tempMean.append(int(temperature))
            meanTemp = calculate_Mean(tempMean)
            humidMean.append(int(humidity))
            meanHumid = calculate_Mean(humidMean)
            atmosMean.append(int(pressure))
            meanAtmos = calculate_Mean(atmosMean)
            
            # ***** COMMENTED OUT FOR JOYSTICK LISTENER *****
            # show_Temp(meanTemp)
            
            # Check for Internet Connection
            checkInternetHttplib("www.google.com", 3)

            # Check for Missing Sensor and Internet Connection - Save to CSV / ThingSpeak
            if(pressure is not None and _netCheck):
                # write_to_SQL()
                write_to_CSV()
                measure(channel)
            else:
                write_to_CSV()         
                
            # Joystick Event Listener
            sense.stick.get_events()

            # Repeat 15 Seconds - ThingSpeak limitation
            sleep(15)

    # Stop after Ctrl + C
    except KeyboardInterrupt:
        sense.low_light = True
        sense.show_message("OFF")
        sense.clear()
        # if conn:
        #     conn.close()
