### BLYNK + Raspberry Pi Sensors

# Running manually
  ./ds18b20.js -r 30 -d
  
  ./dht22.js -r 30 

# Using node forever tool
  (sudo) npm install -g forever

  forever start sensors.json

