import serial
import time
import math
from vpython import *

# --- BAĞLANTI AYARLARI ---
# Port ismini kendi bilgisayarına göre düzeltmelisin (örn: COM3)
arduino_port = 'COM3' 
baud_rate = 115200

try:
    ser = serial.Serial(arduino_port, baud_rate)
    print(f"{arduino_port} üzerinden veri bekleniyor...")
except:
    print("HATA: Port bulunamadı. Kodu durdurup portu kontrol et.")
    exit()

# --- 3D SAHNE ---
scene.title = "MPU6050 - Sensor Fusion Demo"
scene.width = 1500
scene.height = 1050
scene.background = color.gray(0.1)
scene.range = 5

# Uçak benzeri bir şekil oluşturalım ki yönü belli olsun
govde = box(length=4, width=1, height=0.5, color=color.green)
kanat = box(length=1, width=4, height=0.1, pos=vector(0, 0, 0), color=color.blue)
kuyruk = box(length=1, width=1.5, height=0.5, pos=vector(-1.5, 0.5, 0), color=color.purple)

# Tüm parçaları tek bir nesne gibi hareket ettirmek için 'compound' kullanıyoruz
sensor_obj = compound([govde, kanat, kuyruk])

# Eksen Okları
#x_arrow = arrow(length=3, color=color.red, axis=vector(1,0,0))   # X Ekseni
#y_arrow = arrow(length=3, color=color.green, axis=vector(0,1,0)) # Y Ekseni
#z_arrow = arrow(length=3, color=color.blue, axis=vector(0,0,1))  # Z Ekseni

# --- DEĞİŞKENLER VE SABİTLER ---
# Başlangıç açıları
roll = 0.0
pitch = 0.0
yaw = 0.0

# Zaman hesabı için (İntegral alırken dt lazım)
onceki_zaman = time.time()

# Filtre Katsayısı (Abiye anlatacağın kısım burası)
# 0.98 -> Jiroskopa güven (Hızlı tepki)
# 0.02 -> İvmeölçere güven (Drifti/Kaymayı düzelt)
alpha = 0.98 

print("Sistem başlatıldı. Veri akışı bekleniyor...")

while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            data = line.split(',')

            if len(data) == 6:
                # Şu anki zamanı al ve geçen süreyi (dt) hesapla
                simdi = time.time()
                dt = simdi - onceki_zaman
                onceki_zaman = simdi

                # 1. HAM VERİLERİ ÇEK
                ax = float(data[0])
                ay = float(data[1])
                az = float(data[2])
                gx = float(data[3])
                gy = float(data[4])
                gz = float(data[5])

                # 2. İVMEÖLÇERDEN AÇI HESABI (Radyan)
                # İvmeölçer sadece yerçekimini referans alır
                acc_pitch = math.atan2(ay, math.sqrt(ax*ax + az*az))
                acc_roll = math.atan2(-ax, math.sqrt(ay*ay + az*az))

                # 3. JİROSKOP VERİSİNİ DÖNÜŞTÜRME
                # MPU6050'den gelen ham veriyi derece/saniye'ye çevirmek gerekir.
                # Varsayılan hassasiyet ayarında (250dps) bu bölen 131.0'dır.
                gyro_x_rate = gx / 131.0
                gyro_y_rate = gy / 131.0
                gyro_z_rate = gz / 131.0

                # Radyan/saniye cinsine çevir (VPython radyan sever)
                gyro_x_rad =math.radians(gyro_x_rate)
                gyro_y_rad = math.radians(gyro_y_rate)
                gyro_z_rad = math.radians(gyro_z_rate)

                # 4. COMPLEMENTARY FILTER (BÜTÜNLEYEN FİLTRE)
                # Formül: Yeni_Açı = alpha * (Eski_Açı + Jiroskop_Hızı * dt) + (1-alpha) * İvmeölçer_Açısı
                
                # Pitch ve Roll için hem jiroskop hem ivmeölçer birleştirilir
                roll = alpha * (roll + gyro_y_rad * dt) + (1 - alpha) * acc_roll
                pitch = alpha * (pitch - gyro_x_rad * dt) + (1 - alpha) * acc_pitch
                
                # Yaw (Z ekseni dönüşü) için sadece jiroskop kullanabiliriz (Pusula yoksa)
                # Bu yüzden zamanla biraz kayabilir ama kısa sürede sorun olmaz.
                yaw = yaw + gyro_z_rad * dt

                # --- 5. GÖRSELİ GÜNCELLE 
                # Nesnenin açısını sıfırlayıp yeniden ayarlıyoruz
                sensor_obj.up = vector(0, 1, 0)
                sensor_obj.axis = vector(1, 0, 0)
                
                # Hesaplanan açılarla döndür
                sensor_obj.rotate(angle=yaw, axis=vector(0,1,0))   # Z ekseni (Yaw)
                sensor_obj.rotate(angle=pitch, axis=vector(0,0,1)) # Y ekseni (Pitch)
                sensor_obj.rotate(angle=roll, axis=vector(1,0,0))  # X ekseni (Roll)

                # Animasyon hızı
                rate(100)

    except Exception as e:
        # Bazen seri porttan bozuk karakter gelebilir, program çökmesin diye pass geçiyoruz
        pass 