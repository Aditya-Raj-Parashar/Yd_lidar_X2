import ydlidar
import time
import matplotlib
matplotlib.use('TkAgg') #<-- work whrn used in linux
import matplotlib.pyplot as plt
import numpy as np

def main():
    # 1. Initialize Lidar
    ydlidar.os_init()
    laser = ydlidar.CYdLidar()
    laser.setlidaropt(ydlidar.LidarPropSerialPort, "/dev/ttyUSB0")
    laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 115200)
    laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
    laser.setlidaropt(ydlidar.LidarPropSingleChannel, True)
    laser.setlidaropt(ydlidar.LidarPropSampleRate, 3)

    # 2. Setup Plot
    plt.ion() # Turn on interactive mode
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='polar')
    ax.set_title("YDLidar X2 Live Scan", fontsize=15)
    
    # Create the scatter plot object (we'll update its data in the loop)
    # Using 'ro' for red dots, size 2
    points_plot, = ax.plot([], [], 'ro', markersize=2)
    
    # Set limit to 8 meters (X2 range)
    ax.set_ylim(0, 8) 

    if laser.initialize() and laser.turnOn():
        scan = ydlidar.LaserScan()
        print("Starting Radar View...")
        
        try:
            while ydlidar.os_isOk() and plt.fignum_exists(fig.number):
                if laser.doProcessSimple(scan):
                    # Extract angles and ranges
                    # Filter: ignore 0.0 distance (failed reads)
                    angles = [p.angle for p in scan.points if p.range > 0]
                    ranges = [p.range for p in scan.points if p.range > 0]
                    
                    # Update plot data
                    points_plot.set_data(angles, ranges)
                    
                    # Redraw the plot
                    fig.canvas.draw()
                    fig.canvas.flush_events()
                    
                time.sleep(0.01) # Small delay to prevent CPU hogging
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            laser.turnOff()
            laser.disconnecting()
            plt.close()

if __name__ == "__main__":
    main()
