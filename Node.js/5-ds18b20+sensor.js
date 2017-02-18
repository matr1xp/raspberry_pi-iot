/**
 * DS18B20 sensor 
 * requires: 
 *   npm install ds18b20
 * run with:
 *   node ds18b20.js
 **/
var ds18b20 = require('ds18b20')
var sensor_id = null;
ds18b20.sensors(function(err, ids) {
   //Get sensor IDs
   if (ids.length > 0) {
      //Loop in case there are multiple sensors
      for (i=0; i<ids.length; i++) {
        sensor_id = ids[i];
	setInterval(function() { 
           ds18b20.temperature(sensor_id, {parser: 'hex'}, function(err, value) {
                var cToFahr = value * 9 / 5 + 32;
      		console.log(i+': Temperature is', value.toFixed(2) + '\xB0C' + ' or ' + cToFahr.toFixed(2) + '\xB0F');
  	   });
        }, 2000);
      }	
   } else {
      console.log("No DS18B20 sensor found!");
   } 
});

