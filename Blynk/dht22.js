#!/usr/bin/env node
/**
 * DHT22 sensor with Blynk app
 * requires: 
 *   npm install blynk-library
 *   npm install node-dht-sensor
 **/
var DEBUG = false;
var INTERVAL = 30000;                 //default to 30 seconds

if (process.argv.length <= 2) {
  console. log("Usage: " + __filename + " [-d,DEBUG] [-r rate(sec)]");
  process. exit(-1);
} else {
  arguments = process.argv.join(' ');
  //Get debug mode args
  debug_regex = /(-[d|DEBUG])/g;
  if (match = debug_regex.exec(arguments)) {
      DEBUG = true;
      console.log("Running in DEBUG mode.");
  }
  //Get rate from args
  rate_regex = /(-r) ([0-9]+)/g;
  if (match = rate_regex.exec(arguments)) {
      INTERVAL = match[2] * 1000;
      console.log("Setting refresh rate of", match[2]+" seconds");
  }
}

var sensor = require('node-dht-sensor');
var DHT = 22;
var GPIO = 17;

var Blynk = require('blynk-library');
var AUTH = '7bf8f88d595f47f199874f10bd6a55ed';

var app = new Blynk.Blynk(AUTH, options = {
  connector : new Blynk.TcpClient( options = { addr:"127.0.0.1", port:8442 } )
});

class DH22Blynk {
  constructor(app) {
    this.tempC = new app.VirtualPin(0);
    this.humidity = new app.VirtualPin(1);
    this.tempF = new app.VirtualPin(7);
    this.status = new app.VirtualPin(3);
    this.rate = new app.VirtualPin(5);
  }
}

var x = read_timed(sensor, new DH22Blynk(app), INTERVAL);

app.on('connect', function() { console.log("Blynk ready."); });
app.on('disconnect', function() { console.log("DISCONNECT"); });

function read_timed(sensor, blynky, rate) {
   blynky.rate.on('write', function(param) {
        new_rate = param[0] * 1000;
        if ( new_rate != rate) {
          rate = new_rate;
          if (DEBUG) {
            console.log("Setting new rate to", rate/1000 + " seconds.");
          }
          x = read_timed(sensor, blynky, new_rate);
          return x;
        }
   });
   if (x) {
       clearInterval(x);
   }
   return setInterval(function() {
             get_reading(sensor, blynky);
           }, rate);
}

function get_reading(sensor, blynky) {
  sensor.read(DHT, GPIO, function(err, temperature, humidity) {
      if (!err) {
          //Write values to Blynk Pins
          blynky.tempC.write(temperature.toFixed(2));
          blynky.humidity.write(humidity.toFixed(1));
          var Ftemp = temperature * 9 / 5 + 32;
	        blynky.tempF.write(Ftemp.toFixed(2));
          if (DEBUG) {
            console.log("Temperature: "+temperature.toFixed(2)+'\xB0C', " or "+Ftemp.toFixed(2)+'\xB0F');
          }
          setTimeout(function() {
             blynky.status.write(0);
	        }, 1000);
      	  blynky.status.write(1023);
      }
  });
}
