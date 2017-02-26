#!/usr/bin/env node
/**
 * DS18B20 sensor with Blynk app
 * requires: 
 *   npm install ds18b20
 *   npm install blynk-library
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

var Blynk = require('blynk-library');
var AUTH = '7bf8f88d595f47f199874f10bd6a55ed';
var app = new Blynk.Blynk(AUTH, options = {
  connector : new Blynk.TcpClient( options = { addr:"127.0.0.1", port:8442 } )
});

var ds18b20 = require('ds18b20');
var refresh_rate = 0;
var x;

class DS18Blynk {
  constructor(app) {
    this.tempC = new app.VirtualPin(2);
    this.tempF = new app.VirtualPin(8);
    this.status = new app.VirtualPin(4);
    this.rate = new app.VirtualPin(6);
  }
}


ds18b20.sensors(function(err, ids) {
   //Get sensor IDs
   if (ids.length > 0) {
      //We're concerned of 1st sensor only
      var sensor = ids[0];
      x = read_timed(sensor, new DS18Blynk(app), INTERVAL);
   } else {
      console.log("No DS18B20 sensor found!");
   } 
});

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
             read_temperature(sensor, blynky);
           }, rate);
}

function read_temperature(sensor, blynky) {
    ds18b20.temperature(sensor, {parser: 'hex'},
      function(err, value) {
          var cToFahr = value * 9 / 5 + 32;
          //Write temp values to Blynk Pins
          blynky.tempC.write(value.toFixed(2));
          blynky.tempF.write(cToFahr.toFixed(2));
          if (DEBUG) {
            console.log("Temperature: "+value.toFixed(2)+'\xB0C', " or "+cToFahr.toFixed(2)+'\xB0F');
          }
          //Light up our status LED
          setTimeout(function() {
             blynky.status.write(0);
          }, 1000);
          blynky.status.write(1023);
     });
}


