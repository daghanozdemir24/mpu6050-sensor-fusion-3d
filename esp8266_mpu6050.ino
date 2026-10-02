
#include <MPU6050.h>
#include <Wire.h>


  MPU6050 mpu;
  int16_t ax, ay, az, gx, gy, gz; // acceleration ve gyro nun birimleri


void setup() {

Serial.begin(115200);
Wire.begin(D2,D1);   //BURADA ISTERSENİZ Wire.begin(); SEKLINDE YAZABİLİRİZ. ZATEN STANDARTA BOYLEDİR. (ESP8266 kullandıgım icin belirtmek istedim.)
mpu.initialize();    //BURADA MPU6050 sensorunu baslatıyor.


//MPU6050 sensoru bagli mi degil mi.
if(mpu.testConnection()){
  Serial.println("test başarılı");
}else{
  Serial.println("Test basarisiz. Baglanti sarunu var...");
}


}

void loop() {


//BURADA İVME VE GYRO DEGERLERİNİ OLCUYORUZ.
ax = mpu.getAccelerationX();
ay = mpu.getAccelerationY();
az = mpu.getAccelerationZ();
gx = mpu.getRotationX();              //AMA EĞER DAHA AZ KALABALIK OLSUN İSTERSEK   getMotion6(ax,ay,az,gx,gy,gz);    KULLANILABİLİR.
gy = mpu.getRotationY();              //          VEYA       getAcceleration(ax,ay,az);  ve  getRotation(gx,gy,gz);   KULLANILABILIR. 
gz = mpu.getRotationZ();



    Serial.print("Ivme olcumu    : ");
    Serial.print(ax);  Serial.print(",");
    Serial.print(ay);  Serial.print(",");
    Serial.print(az);  Serial.print(",");
    Serial.print("Jiroskop olcumu :   ");
    Serial.print(gx);  Serial.print(",");
    Serial.print(gy);  Serial.print(",");
    Serial.println(gz);

 delay(100);

}
