import os
import ydlidar
import time
import sys

def main():
    # 1. Init
    ydlidar.os_init()
    
    # 2. Parameters
    laser = ydlidar.CYdLidar()
    laser.setSerialPort("/dev/ttyUSB0")
    laser.setBaudrate(115200)
    
    # --- X2 SPECIFIC CONFIGURATION ---
    laser.setLidarType(ydlidar.TYPE_TRIANGLE)
    laser.setDeviceType(ydlidar.YDLIDAR_TYPE_SERIAL)
    
    # FIX 1: Match the log's Sample Rate (4K)
    laser.setlidaropt(ydlidar.LidarPropSampleRate, 4) 
    
    # FIX 2: Set Frequency to 7Hz (Safer for X2 than 10Hz)
    laser.setlidaropt(ydlidar.LidarPropScanFrequency, 7.0)
    
    # FIX 3: Ensure Single Channel is ON
    laser.setlidaropt(ydlidar.LidarPropSingleChannel, True)

    # FIX 4: Handle the Intensity Typo (Try both to be safe)
    if hasattr(ydlidar, 'LidarPropIntensities'):
        laser.setlidaropt(ydlidar.LidarPropIntensities, False)
    elif hasattr(ydlidar, 'LidarPropIntenstiy'):
        laser.setlidaropt(ydlidar.LidarPropIntenstiy, False)
        
    # FIX 5: Range settings
    laser.setlidaropt(ydlidar.LidarPropMaxRange, 8.0)
    laser.setlidaropt(ydlidar.LidarPropMinRange, 0.12)
    laser.setlidaropt(ydlidar.LidarPropMaxAngle, 180.0)
    laser.setlidaropt(ydlidar.LidarPropMinAngle, -180.0)

    # 3. Start
    ret = laser.initialize()
    if ret:
        ret = laser.turnOn()
        scan = ydlidar.LaserScan()
        
        print("\n[INFO] Scanning... (Press Ctrl+C to stop)")
        time.sleep(1) # Warm up
        
        while ret and ydlidar.os_isOk():
            r = laser.doProcessSimple(scan)
            if r:
                # DEBUG: Bypass the wrapper to check C++ object directly
                try:
                    # Depending on SWIG generation, one of these will work:
                    raw_pts = scan.obj.points
                    
                    # Check if it's a size() method or a length property
                    count = 0
                    if hasattr(raw_pts, 'size'):
                        count = raw_pts.size()
                    else:
                        count = len(raw_pts)

                    print(f"Scan OK [Stamp:{scan.stamp}] Raw Count: {count}")
                    
                except Exception as e:
                    print(f"Wrapper Error: {e}")
                    
            else:
                print("Failed to get Lidar Data")
            
            time.sleep(0.05)
            
        laser.turnOff()
    
    laser.disconnecting()

if __name__ == "__main__":
    main()
