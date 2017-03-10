#!/usr/bin/python
'''
 Environment Sensors to ThingSpeak using MQTT
 Hardware:
    DS18B20
    BMP180
    DHT22
 Software:
    Adafruit DHT library (https://github.com/adafruit/Adafruit_Python_DHT)
    Adafruit BMP library (https://github.com/adafruit/Adafruit_Python_BMP)
 Services:
    ThingSpeak (https://thingspeak.com/)
'''
import signal, json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import os, sys, time, glob
import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085

INTERVAL = 60   # sensor reading interval in seconds

def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    sys.exit(0)

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

def mqtt_start():
  global mqttHost, useUnsecuredTCP, useUnsecuredWebsockets, useSSLWebsockets, mqttc
  # MQTT ThingSpeak Settings 
  useUnsecuredTCP = True 
  useUnsecuredWebsockets = False
  useSSLWebsockets = False
  mqttHost = "mqtt.thingspeak.com"
  # MQTT Reporting Status
  mqttc = mqtt.Client()
  mqttc.connect("localhost", 1883, 60)
  mqttc.loop_start()
  mqttc.publish("thingspeak/sensors", json.dumps({'file': __file__, 'status':'Running','host':mqttHost,'interval':INTERVAL}),2)

def mqtt_stop():
  mqttc.publish("thingspeak/sensors", json.dumps({'file': __file__, 'status':'Exited'}),2)
  mqttc.loop_stop()
  mqttc.disconnect()
      
def ThingSpeak():
  # ThingSpeak Channel Settings
  ThingSpeakChannelID = "236028"
  ThingSpeakAPIKey = "D58X9PXTCT6CGCLR"
  # Topic string
  topic = "channels/" + ThingSpeakChannelID + "/publish/" + ThingSpeakAPIKey
  return topic

if __name__ == "__main__":
 try:
    # Catch kill signal so we can exit gracefully
    signal.signal(signal.SIGTERM, sigterm_handler)
    mqtt_start()  
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
    
    Topic = ThingSpeak()

    while True:
      tPayload1 = ''    # BMP180
      tPayload2 = ''    # DHT22
      tPayload3 = ''    # DS18B20 
      
      # Get BMP180 sensor reading
      tPayload1 = "field1={:.2f}&field2={}&field3={:.2f}".format(bmp_sensor.read_temperature(), bmp_sensor.read_pressure(), bmp_sensor.read_altitude())
      
      # Get a DHT sensor reading
      humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)
      # Try until you get a reading 
      if humidity is not None and temperature is not None:
        tPayload2 = "&field4={:.2f}&field5={:.2f}".format(temperature, humidity)
      else:
        print('Error: Failed to get DHT22 sensor reading!')
      
      # Get DS18B20 sensor reading
      tPayload3 = "&field6={:.2f}".format(read_ds_temp())
      
      # Send data to ThingSpeak
      publish.single(Topic, payload=tPayload1+tPayload2+tPayload3, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
      time.sleep(INTERVAL)
 except KeyboardInterrupt:
      print("<Ctrl+C> pressed... exiting.")
 except Exception as inst:
      mqttc.publish("thingspeak/sensors", json.dumps({'file': __file__, 'status':'Error','message':'{}'.format(inst)}),2)
      print("Error: {}".format(inst))
 finally:
      # Graceful exit
      mqtt_stop()
      print(__file__, "Program terminated gracefully.")
 
