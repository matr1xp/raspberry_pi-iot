/**
 * DHT22 - Temperature and Humidity sensor
 * requires:
 *   npm install raspi-sensors
 * run with:
 *   node 2-dht22-sensor.js
 **/
var RaspiSensors = require('raspi-sensors');

var interval = 15;

var DHT22 = new RaspiSensors.Sensor({
	type: "DHT22",
	pin: 0x0,
    }, "DHT22");

DHT22.fetchInterval(function(err,data) { 
    if (err) {
 	console.error("Error:",err.cause);
	return;
    }
    console.log(data);
}, interval);

