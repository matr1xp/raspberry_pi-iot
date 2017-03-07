#!/usr/bin/python
'''
 Environment Sensors to ThingSpeak using MQTT
 Hardware:
    DS18B20
    BMP180
    DHT22
 Software:
    Adafruit DHT library (https://github.com/adafruit/Adafruit_Python_DHT)
    Adafruit BMP library (https://github.com/adafruit/Adafruit_Python_BMP.git)
'''
import paho.mqtt.publish as publish
import os, sys, time, glob
import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085

def read_raw_ds_temp():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_ds_temp():
    lines = read_raw_ds_temp()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.5)
        lines = read_raw_ds_temp()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_str = lines[1][equals_pos+2:]
        temp_c = float(temp_str) / 1000.0
        return temp_c

try:
    INTERVAL = 30   # sensor reading interval in seconds

    # DHT22 sensor
    dht_sensor = Adafruit_DHT.DHT22 
    dht_pin = 18
    # DS18B20 sensor
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    device_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(device_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    # BMP180 sensor
    bmp_sensor = BMP085.BMP085()
   
    # MQTT Settings 
    useUnsecuredTCP = True 
    useUnsecuredWebsockets = False
    useSSLWebsockets = False
    mqttHost = "mqtt.thingspeak.com"

    # Set up the connection parameters based on the connection type
    if useUnsecuredTCP:
       tTransport = "tcp"
       tPort = 1883
       tTLS = None

    if useUnsecuredWebsockets:
       tTransport = "websockets"
       tPort = 80
       tTLS = None

    if useSSLWebsockets:
       import ssl
       tTransport = "websockets"
       tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
       tPort = 443
    
    # ThingSpeak Channel Settings
    ThingSpeakChannelID = "236028"
    ThingSpeakAPIKey = "D58X9PXTCT6CGCLR"
     
    # Topic string
    topic = "channels/" + ThingSpeakChannelID + "/publish/" + ThingSpeakAPIKey

    while True:
      tPayload1 = ''    # BMP180
      tPayload2 = ''    # DHT22
      tPayload3 = ''    # DS18B20 

      # Get BMP180 sensor reading
      tPayload1 = "field1={}&field2={}&field3={}".format(bmp_sensor.read_temperature(), bmp_sensor.read_pressure(), bmp_sensor.read_altitude())
      
      # Get a DHT sensor reading
      humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)
      # Try until you get a reading 
      if humidity is not None and temperature is not None:
        tPayload2 = "&field4={}&field5={}".format(temperature, humidity)
      else:
        print('Error: Failed to get DHT22 sensor reading!')
      
      # Get DS18B20 sensor reading
      tPayload3 = "&field6={}".format(read_ds_temp())

      publish.single(topic, payload=tPayload1+tPayload2+tPayload3, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
      time.sleep(INTERVAL)
except KeyboardInterrupt:
      print("<Ctrl+C> pressed... exiting.")
      sys.exit(0) 
except:
      print("Error: {0} {1}".format(sys.exc_info()[0], sys.exc_info()[1]))
