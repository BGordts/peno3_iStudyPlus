// Example testing sketch for various DHT humidity/temperature sensors
// Written by ladyada, public domain

#include "DHT.h"
#define DHTPIN 2     // what pin we're connected to
#define PHOTOSENSE_ANA_PIN A0
#define SOUNDSENSE_ANA_PIN A1
#define DHTTYPE DHT11   // DHT 11 
  
                          


const int sendFreq = 1000; //
unsigned int sample;

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600); 
  dht.begin();
}

void loop() {
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  unsigned long startMillis= millis();  // Start of sample window
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  int l = analogRead(PHOTOSENSE_ANA_PIN);
  unsigned int peakToPeak = 0;   // peak-to-peak level
  unsigned int signalMax = 0;
  unsigned int signalMin = 1024;
   // collect data for sendFreq - elapsedTime mS
  while (millis() - startMillis < sendFreq)
  {
     sample = analogRead(SOUNDSENSE_ANA_PIN);
     //Serial.println(sample);
     if (sample < 1024)  // toss out spurious readings
     {
        if (sample > signalMax)
        {
           signalMax = sample;  // save just the max levels
        }
        else if (sample < signalMin)
        {
           signalMin = sample;  // save just the min levels
        }
     }
  }
  peakToPeak = signalMax - signalMin;  // max - min = peak-peak amplitude
  double s = (peakToPeak * 3.3) / 1024;  // convert to volts
  
  Serial.print(l);
  Serial.print("\t");
  Serial.print(h);
  Serial.print("\t");
  Serial.print(t);
  Serial.print("\t");
  Serial.println(s);

}

