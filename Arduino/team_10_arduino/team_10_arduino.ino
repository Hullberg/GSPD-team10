
#include <DHT.h>
#include <DHT_U.h>
#include <Adafruit_SI1145.h>
#include <SoftwareSerial.h>

#define DHTPIN 2     // connect pin 2 to this pin
#define DHTTYPE DHT22   // DHT 22  

// Connect pin 1 (on the left) of the sensor to +5V
// NOTE: If using a board with 3.3V logic like an Arduino Due connect pin 1
// to 3.3V instead of 5V!
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND


// Initialize DHT sensor.
DHT dht(DHTPIN, DHTTYPE);

Adafruit_SI1145 uv = Adafruit_SI1145();

SoftwareSerial BT_Serial(10, 11); // RX, TX

String message; //string that stores the incoming message


void setup() {
  BT_Serial.begin(57600);  //BT adapter serial
  Serial.begin(9600); //debug serial (hardware/USB)

  dht.begin();
  uv.begin();

  Serial.println("OK!");
  BT_Serial.println("BT established!");
}

void loop() {
   while(BT_Serial.available()>0)
  {//while there is data available on the serial monitor
    message+=char(BT_Serial.read());//store string from serial command
  
  
  if(!BT_Serial.available())
  {
    Serial.println(message); 
    if(message!=""){//if data is available
        float result = -1;
            
      if(message == "t"){       

        Serial.println("read temperat");
        result = dht.readTemperature(); // Read temperature as Celsius (the default)         
      
      } else if(message == "h"){

        Serial.println("read relative humidity");
        result = dht.readHumidity();
        
      }else if(message == "v" ){

        Serial.println("read visible light"); 
        result = uv.readVisible();  
        
      }else if(message == "u"){   

        Serial.println("read UV");
        result = uv.readUV();       
     
      }else{
        
        // if nothing else matches, do the default
        Serial.println("command does not match! " + message);

      }

      BT_Serial.println(result);
      message=""; //clear the data
    }
  }

  // Wait a few seconds between measurements.
  delay(2000);
}
  /*
  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)){
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
 */

}

