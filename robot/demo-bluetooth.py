import time

import picar
from .wheels import Front_Wheels, Back_Wheels
from .sensors.LineFollower import LineFollower
from .sensors.UltrasonicSensor import UltrasonicSensor

import config
import bluetooth.scanner as scanner


# TODO: get device name from command line argument
DEVICE_NAME = "HuaweiAP"

# TODO: create flag --no-robot to test connection without robot
NO_ROBOT = False


lf = LineFollower()
lf.references = config.LINE_FOLLOWER_REFERENCES
ultrasonicSensor = UltrasonicSensor(config.ULTRASONIC_SENSOR_CHANNEL)

forward_speed = config.PICAR_MED_SPEED
backward_speed = 70
rssi_reference = 0
turning_angle = 40

max_off_track_count = 40
delay = 0.0005


def processSample(message: str):
    global rssi_reference, forward_speed
    sample = int(message.split(":")[0])

    if rssi_reference == 0:
        rssi_reference = sample
        print("rssi_reference: " + str(rssi_reference))
    else:
        print("rssi_sample: " + str(sample))
        diff = sample - rssi_reference

        if (diff > 0):
            return

        diff = abs(diff)
        if diff > 0 and diff < 5:
            forward_speed = config.PICAR_MED_SPEED
        elif diff >= 5 and diff < 10:
            forward_speed = int(config.PICAR_MED_SPEED/2)
        elif diff >= 10 and diff < 15:
            forward_speed = int(config.PICAR_MED_SPEED/3)
        elif diff >= 15:
            forward_speed = 0


# To test when no robot connected
if NO_ROBOT:
    print("No robot connected, starting only bluetooth scanner")
    scanner.start(DEVICE_NAME, processSample)
    while True:
        try:
            print("forward_speed: " + str(forward_speed))
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("Exiting program...")
            scanner.stop()
            quit()

picar.setup()
scanner.start(DEVICE_NAME, processSample)

fw = Front_Wheels()
bw = Back_Wheels()

fw.ready()
bw.ready()
fw.turning_max = 45


def updateSpeed():
    if bw.speed != forward_speed:
        bw.speed = forward_speed
        bw.forward()


def main():
    global turning_angle, forward_speed
    off_track_count = 0
    bw.speed = forward_speed
    obstacle = False

    a_step = config.PICAR_A_STEP
    b_step = config.PICAR_B_STEP
    c_step = config.PICAR_C_STEP
    d_step = config.PICAR_D_STEP
    bw.forward()
    while True:
        distance = ultrasonicSensor.distance()
        if (distance <= config.ULTRASONIC_SENSOR_MIN_DISTANCE and distance >= 0) or (distance < 0 and obstacle):
            obstacle = True
            forward_speed = 0
            bw.stop()
            continue
        else:
            obstacle = False

        updateSpeed()
        lf_status = lf.read_digital()

        # Angle calculate
        if lf_status == [0, 0, 1, 0, 0]:
            step = 0
        elif lf_status == [0, 1, 1, 0, 0] or lf_status == [0, 0, 1, 1, 0]:
            step = a_step
        elif lf_status == [0, 1, 0, 0, 0] or lf_status == [0, 0, 0, 1, 0]:
            step = b_step
        elif lf_status == [1, 1, 0, 0, 0] or lf_status == [0, 0, 0, 1, 1]:
            step = c_step
        elif lf_status == [1, 0, 0, 0, 0] or lf_status == [0, 0, 0, 0, 1]:
            step = d_step

        # Direction calculate
        if lf_status == [0, 0, 1, 0, 0]:
            off_track_count = 0
            fw.turn(90)
        # turn right
        elif lf_status in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
            off_track_count = 0
            turning_angle = int(90 - step)
        # turn left
        elif lf_status in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
            off_track_count = 0
            turning_angle = int(90 + step)
        elif lf_status == [0, 0, 0, 0, 0]:
            off_track_count += 1
            if off_track_count > max_off_track_count:
                #tmp_angle = -(turning_angle - 90) + 90
                tmp_angle = (turning_angle-90)/abs(90-turning_angle)
                tmp_angle *= fw.turning_max
                bw.speed = backward_speed
                bw.backward()
                fw.turn(tmp_angle)

                lf.wait_tile_center()
                bw.stop()

                fw.turn(turning_angle)
                time.sleep(0.2)
                bw.speed = 80
                bw.forward()
                time.sleep(0.2)

        else:
            off_track_count = 0

        fw.turn(turning_angle)
        time.sleep(delay)


def destroy():
    bw.stop()
    fw.turn(90)


if __name__ == '__main__':
    try:
        while True:
            while rssi_reference == 0:
                time.sleep(0.1)
                continue

            main()
    except KeyboardInterrupt:
        destroy()
        scanner.stop()
