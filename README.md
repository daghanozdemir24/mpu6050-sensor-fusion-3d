# Real-Time 6-DoF IMU Sensor Fusion & 3D Visualization

A real-time attitude and orientation tracking system developed with an **ESP8266 (NodeMCU)**, an **MPU6050 6-DoF IMU**, and an interactive 3D visualization dashboard running on **Python (VPython)**.

The system computes full 3-axis orientation (Roll, Pitch, Yaw) by fusing high-frequency gyroscope angular velocities with low-frequency accelerometer gravity vectors using a **Complementary Filter** (alpha = 0.98) to eliminate gyro drift and high-frequency motion noise.

## 🚀 Key Features
* **Full 3-Axis Attitude Estimation:** Computes Pitch, Roll, and Yaw angles in real time.
* **Complementary Filter Algorithm:** Blends gyro integration with accelerometer-derived tilt angles (Pitch and Roll) to ensure zero drift and low latency.
* **Gyro Integration for Yaw:** Integrates Z-axis angular velocity over time to track heading changes.
* **Real-Time Serial Pipeline:** Streams 6-axis raw telemetry (`ax, ay, az, gx, gy, gz`) at 115200 baud over USB UART.
* **3D Visualizer:** Real-time aircraft orientation visualizer rendered using VPython, dynamically responding to physical sensor movement.

## 📁 Repository Structure
* `esp8266_mpu6050.ino`: NodeMCU firmware reading I2C sensor registers via `MPU6050` and `Wire` libraries, streaming raw CSV telemetry over Serial.
* `imu_visualizer_3d.py`: Python script handling UART data acquisition, degree-to-radian conversions, sensor fusion calculations, and 3D scene rendering.

## 📐 Mathematical Formulation

### 1. Accelerometer Tilt Angles
* Pitch: `atan2(ay, sqrt(ax^2 + az^2))`
* Roll: `atan2(-ax, sqrt(ay^2 + az^2))`

### 2. Complementary Filter (Pitch & Roll)
* `Roll_k  = alpha * (Roll_(k-1)  + Gyro_Y_rate * dt) + (1 - alpha) * Roll_acc`
* `Pitch_k = alpha * (Pitch_(k-1) - Gyro_X_rate * dt) + (1 - alpha) * Pitch_acc`

### 3. Gyro Integration (Yaw)
* `Yaw_k = Yaw_(k-1) + Gyro_Z_rate * dt`

## 🛠️ Hardware Setup & Wiring

| MPU6050 Pin     | ESP8266 (NodeMCU) Pin | Function            |
| :---            | :---                  | :---                |
| `VCC`           | `3V3`                 | Power Supply (3.3V) |
| `GND`           | `GND`                 | Ground Reference    |
| `SCL`           | `D1 (GPIO 5)`         | I2C Clock Line      |
| `SDA`           | `D2 (GPIO 4)`         | I2C Data Line       |

## 💻 Software Setup & Execution

```bash
pip install pyserial vpython
python imu_visualizer_3d.py
```
## 👤 Author
* **Dağhan Özdemir** - [GitHub Profile](https://github.com/daghanozdemir24)
