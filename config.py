import ydlidar
import time
import math

def main():
    ydlidar.os_init()
    laser = ydlidar.CYdLidar()
    laser.setlidaropt(ydlidar.LidarPropSerialPort, "/dev/ttyUSB0")
    laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 115200)
    laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
    laser.setlidaropt(ydlidar.LidarPropSingleChannel, True)
    laser.setlidaropt(ydlidar.LidarPropSampleRate, 3)

    if laser.initialize() and laser.turnOn():
        scan = ydlidar.LaserScan()
        try:
            while ydlidar.os_isOk():
                if laser.doProcessSimple(scan):
                    # Filter out zero-distance points (missed reflections)
                    valid_points = [p for p in scan.points if p.range > 0.1]
                    
                    if valid_points:
                        # Find closest and furthest objects in the WHOLE room
                        closest = min(valid_points, key=lambda p: p.range)
                        furthest = max(valid_points, key=lambda p: p.range)
                        
                        # Convert radians to degrees for easier reading
                        c_angle = math.degrees(closest.angle)
                        f_angle = math.degrees(furthest.angle)
                        
                        print(f"--- Full Scan ({len(valid_points)} points) ---")
                        print(f"Closest Object: {closest.range:.2f}m at {c_angle:.1f}°")
                        print(f"Furthest Object: {furthest.range:.2f}m at {f_angle:.1f}°")
                        print("-" * 30)
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        laser.turnOff()
    laser.disconnecting()

if __name__ == "__main__":
    main()
