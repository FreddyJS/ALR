import time
from typing import Tuple

import api
import picar
import board
import wheels
import config
import adafruit_tcs34725
from sensors.LineFollower import LineFollower
from sensors.UltrasonicSensor import UltrasonicSensor

# Ultrasonic sensor
ultrasonicSensor = UltrasonicSensor(config.ULTRASONIC_SENSOR_CHANNEL)
obstacle = False

# Color sensor
i2c = board.I2C()
colorSensor = adafruit_tcs34725.TCS34725(i2c)
colorSensor.integration_time = config.COLOR_SENSOR_INTEGRATION_TIME
colorSensor.gain = config.COLOR_SENSOR_GAIN

# Line follower
lf = LineFollower()
lf.references = config.LINE_FOLLOWER_REFERENCES
max_off_track_count = config.LINE_FOLLOWER_MAX_OFF_TRACK_COUNT
off_track_count = 0

# Global variables
forward_speed = config.PICAR_MED_SPEED
backward_speed = 70
turning_angle = 90
delay = 0.0005

# PiCar Wheels
picar.setup()
fw = wheels.Front_Wheels()
bw = wheels.Back_Wheels()
fw.ready()
bw.ready()


def is_red() -> bool:
    color_temp = colorSensor.color_temperature
    return False if color_temp == None else color_temp < config.COLOR_SENSOR_RED_VALUE


def is_blue() -> bool:
    color_temp = colorSensor.color_temperature
    return False if color_temp == None else color_temp < config.COLOR_SENSOR_BLUE_VALUE and color_temp > config.COLOR_SENSOR_RED_VALUE


def follow_line() -> Tuple[bool, list]:
    """ 
        Detects the line and turns the wheels to keep the line in the center. 
        Returns a boolean indicating if the line is being followed and a list with the status of the line follower.
        Automatically stops the robot in case of an obstacle and restarts it when the obstacle is gone.
    """
    global forward_speed, off_track_count, obstacle, turning_angle

    a_step = 3
    b_step = 6
    c_step = 15
    d_step = 45

    # Measuring distance
    distance = ultrasonicSensor.distance()
    if (distance <= config.ULTRASONIC_SENSOR_MIN_DISTANCE and distance >= 0) or (distance < 0 and obstacle):
        obstacle = True
        bw.stop()
        return False, [0, 0, 0, 0, 0]
    else:
        obstacle = False
        bw.speed = forward_speed
        bw.forward()

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
            bw.speed = forward_speed
            bw.forward()
            time.sleep(0.2)

        else:
            off_track_count = 0

    fw.turn(turning_angle)
    return True, lf_status


def wait_for_crosspath():
    while True:
        _, lf_status = follow_line()
        if lf_status == [1, 1, 1, 1, 1]:
            break


def wait_end_of_crosspath():
    lf_status = lf.read_digital()
    while lf_status == [1, 1, 1, 1, 1]:
        lf_status = lf.read_digital()


def follow_route(route: list[str] = ["recto._CRUCE_1", "recto._CRUCE_2"]):
    global forward_speed
    current_hall = "pasillo0"
    room_count = 0
    in_red = False

    bw.speed = forward_speed
    bw.forward()

    while True:
        following, lf_status = follow_line()
        if not following:
            print("The robot has stopped. Probably cause an obstacle")
        else:
            # Measuring color
            red = is_red()
            if red and not in_red:
                in_red = True
                room_count += 1
                current_hall = current_hall.split(
                    "_")[0] + "_" + str(room_count)

                print("Entered room " + current_hall)
            elif not red and in_red:
                in_red = False
                print("Left room " + current_hall)

            if lf_status == [1, 1, 1, 1, 1]:
                if len(route) == 0:
                    raise KeyboardInterrupt
                action = route.pop(0)

                forward_speed = config.PICAR_CROSSPATH_SPEED
                bw.speed = forward_speed
                bw.forward()

                print("The robot has reached a crosspath")
                wait_end_of_crosspath()
                print("The robot has passed the crosspath")

                if action.startswith("recto"):
                    # We have to pass two crosspaths
                    print("Esperando a pasar el segundo cruce...")
                    wait_for_crosspath()
                    wait_end_of_crosspath()
                    print("El robot ha pasado el segundo cruce, continuando recto")

                elif action.startswith("izquierda"):
                    print("Esperando al segundo cruce para girar a la izquierda")
                    wait_for_crosspath()
                    wait_end_of_crosspath()

                    print("El robot ha pasado el segundo cruce, girando a la izquierda")
                    fw.turn(90)
                    bw.speed = 40
                    bw.left()
                    lf.wait_tile_center()

                    bw.speed = config.PICAR_CROSSPATH_SPEED
                    bw.forward()

                    print(
                        "El robot ha pasado el segundo cruce. Esperando al tercer cruce...")
                    wait_for_crosspath()
                    wait_end_of_crosspath()
                    print(
                        "El robot ha pasado el tercer cruce, continuando recto (fin de giro izquierda)")

                elif action.startswith("derecha"):
                    print("Girando a la derecha")
                    fw.turn(90)
                    bw.speed = 40
                    bw.right()
                    lf.wait_tile_center()
                    print("Saliendo del cruce")

                current_hall = "pasillo{}{}".format(action[-1], route[0][-1])
                print("Continuando recto, nuevo pasillo: " + current_hall)
                forward_speed = config.PICAR_MED_SPEED
                bw.speed = forward_speed
                bw.forward()


def destroy():
    bw.stop()
    fw.turn(90)


def processMessage(message: object):
    print("Received message: " + str(message))

    if "type" not in message:
        return

    if message["type"] == "start":
        dest_room = message["room"]
        current_route = message["route"]
        print("Starting route to room: " + dest_room)
        print("Route: " + str(current_route))


if __name__ == '__main__':
    api.start_ws()
    try:
        time.sleep(1.5)
        follow_route()
    except KeyboardInterrupt:
        api.close_ws()
        destroy()
