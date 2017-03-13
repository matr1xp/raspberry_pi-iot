/**
 * BMP180 - Barometric Pressure and Temperature sensor
 * requires:
 *   npm install raspi-sensors
 * run with:
 *   node 4-bmp180-sensor.js
 **/
var RaspiSensors = require('raspi-sensors');

var interval = 15;

var BMP180 = new RaspiSensors.Sensor({
	type: "BMP180",
	address: 0x77,
    }, "BMP180");

BMP180.fetchInterval(function(err,data) { 
    if (err) {
 	console.error("Error:",err.cause);
	return;
    }
    console.log(data);
}, interval);

