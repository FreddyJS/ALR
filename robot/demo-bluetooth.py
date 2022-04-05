import time

import picar
from picar import front_wheels
from picar import back_wheels
from LineFollower import LineFollower

import config
import bluetooth.scanner as scanner


# TODO: get device name from command line argument
DEVICE_NAME = "HuaweiAP"

# TODO: create flag --no-robot to test connection without robot
NO_ROBOT = False

LF_REFERENCES = config.LINE_FOLLOWER_REFERENCES
rssi_reference = 0
forward_speed = config.PICAR_MAX_SPEED
backward_speed = 70
turning_angle = 40

max_off_track_count = 40
delay = 0.0005


def processSample(message: str):
    global forward_speed, rssi_reference
    sample = int(message)

    if rssi_reference == 0:
        rssi_reference = sample
        print("rssi_reference: " + str(rssi_reference))
    else:
        print("rssi_sample: " + str(sample))
        diff = sample - rssi_reference

        if (diff > 0):
            return

        diff = abs(diff)
        if diff >= 0 and diff <= 10:
            forward_speed = 100
        elif diff > 10 and diff <= 25:
            forward_speed = 80
        elif diff > 25 and diff <= 50:
            forward_speed = 60
        elif diff > 50 and diff <= 75:
            forward_speed = 40
        else:
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

fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
lf = LineFollower()

lf.references = LF_REFERENCES
fw.ready()
bw.ready()
fw.turning_max = 45


def updateSpeed():
    bw.speed = forward_speed
    bw.forward()


def main():
    global turning_angle
    off_track_count = 0
    bw.speed = forward_speed

    a_step = 3
    b_step = 5
    c_step = 10
    d_step = 20
    bw.forward()
    while True:
        lf_status = lf.read_digital()
        print(lf_status)
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
            updateSpeed()
        # turn right
        elif lf_status in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
            off_track_count = 0
            turning_angle = int(90 - step)
            updateSpeed()
        # turn left
        elif lf_status in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
            off_track_count = 0
            turning_angle = int(90 + step)
            updateSpeed()
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
