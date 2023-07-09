#include<Arduino.h>
#include<MPU9250.h>
#include <ArduinoJson.h>
#include "helper/calib.h"
//#include "helper/handjson.h"

// wifi declaration 
#include "WiFi.h"
#include <WiFiUdp.h>

#define ssid "Ajay"
#define password "patel12335"
WiFiUDP udp;

IPAddress serverIP(192,168,190,49);  // IP address of the UDP server
unsigned int localPort = 8080;


MPU9250 mpu[] = {
  MPU9250(Wire,0x68),
  MPU9250(Wire,0x68),
  MPU9250(Wire,0x68),
  MPU9250(Wire,0x68),
  MPU9250(Wire,0x68),
  MPU9250(Wire,0x68),
 

};
const int num_mpu = sizeof(mpu)/sizeof(mpu[0]);

// define address of multiplexer 
#define TCAADDR1 0x70
#define TCAADDR2 0x71

// setection of multiplexer 
void tcaselect1(uint8_t i) {
    if (i > 7) return;
    Wire.beginTransmission(TCAADDR1);
    Wire.write(1 << i);
    Wire.endTransmission();  
}
void tcaselect2(uint8_t i){
    if(i>7) return;

    Wire.beginTransmission(TCAADDR2);
    Wire.write(1 << i);
    Wire.endTransmission(); 
  } 



const int NUM_SENSORS = 6;
const int NUM_VALUES = 6;

struct SensorData {
  float value1;
  float value2;
  float value3;
  float value4;
  float value5;
  float value6;
};


void setup(){

  Serial.begin(921600);
    //Wifi connection 
  Serial.println("Initiating WiFi...");
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);

  Serial.println("Setup done");
  WiFi.begin(ssid ,password);
  int count = 0;
  while (WiFi.status()!=WL_CONNECTED)
  {
        delay(500);
 
        Serial.println(WiFi.status());
        count++;
        if (count > 10)
        {
            Serial.println("WiFi connection failed");
            ESP.restart();
            break;
        }
  }
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println("Connected to WiFi");

    Wire.begin();
    Serial.println(F("#####################"));
  Serial.println(F("Starting Initialisation..."));
  Serial.println(F("#####################"));
  for(int i=0;i<num_mpu;i++){
    
        tcaselect1(i);
        Serial.print(F("TCAADDR: "));
        Serial.println(i);
        if(mpu[i].begin() > 0){
            Serial.println(F("MPU9250 is online..."));
            mpu[i].setAccelRange(MPU9250::ACCEL_RANGE_2G);
            mpu[i].setGyroRange(MPU9250::GYRO_RANGE_250DPS);
            mpu[i].setDlpfBandwidth(MPU9250::DLPF_BANDWIDTH_20HZ);
            mpu[i].setSrd(19);
            Serial.println(F("MPU9250 is configured..."));
            Serial.println(i);

            mpu[i].setAccelCalX(accel_bias_x[i], accel_scale_x[i]);
            mpu[i].setAccelCalY(accel_bias_y[i], accel_scale_y[i]);
            mpu[i].setAccelCalZ(accel_bias_z[i], accel_scale_z[i]);
            mpu[i].setGyroBiasX_rads(gyro_bias_x[i]*M_PI/180);
            mpu[i].setGyroBiasY_rads(gyro_bias_y[i]*M_PI/180);
            mpu[i].setGyroBiasZ_rads(gyro_bias_z[i]*M_PI/180);

            Serial.println(F("MPU9250 is calibrated..."));
            
            Wire.write(0);
            Wire.endTransmission();
        }
        else{
            Serial.println(F("MPU9250 is not online..."));
            Serial.println(F("Check your wiring..."));
            
        }
   
  }
  Serial.println(F("MPU9250 is ready to go..."));

// local connection 
udp.begin(localPort);
  

}

void loop()
{
    DynamicJsonDocument jsonDocument(1024);

    for(int i = 0; i < num_mpu; i++)
    {
        JsonObject sensorObject = jsonDocument.createNestedObject(String(i));

        tcaselect1(i);
        mpu[i].readSensor();

        float ax = mpu[i].getAccelX_mss();
        float ay = mpu[i].getAccelY_mss();
        float az = mpu[i].getAccelZ_mss();
        float gx = mpu[i].getGyroX_rads();
        float gy = mpu[i].getGyroY_rads();
        float gz = mpu[i].getGyroZ_rads();

        sensorObject["ax"] = ax;
        sensorObject["ay"] = ay;
        sensorObject["az"] = az;
        sensorObject["gx"] = gx;
        sensorObject["gy"] = gy;
        sensorObject["gz"] = gz;

        // delay(100);
    }

    String jsonString;
    serializeJson(jsonDocument, jsonString);

    // Print the JSON string
    Serial.println(jsonString);

    udp.beginPacket(serverIP, localPort);
    udp.print(jsonString);
    udp.endPacket();
}