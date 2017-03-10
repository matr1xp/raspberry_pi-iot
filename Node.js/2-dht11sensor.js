/**
 * DHT11 Humidity and Temperature sensor
 * requires:
 *   npm install rpi-dht-sensor
 * run with:
 *   node dht11sensor.js
 **/
var DhtSensor = require('rpi-dht-sensor');
var Dht11 = new DhtSensor.DHT11(4);

function read() {
   var readout = Dht11.read();
   console.log('Temperature: ' + readout.temperature.toFixed(2) + 'C');
   console.log('Humidity: ' + readout.humidity.toFixed(2) + '%');
   setTimeout(read, 5000);
}

read();
