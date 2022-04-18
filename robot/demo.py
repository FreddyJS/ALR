import json
import time
from typing import List, Tuple

import api
import picar
import board
import config
import adafruit_tcs34725
from wheels import Front_Wheels, Back_Wheels
from sensors.LineFollower import LineFollower
from sensors.UltrasonicSensor import UltrasonicSensor


# Ultrasonic sensor
def on_obstacle(blocked):
    global obstacle
    obstacle = blocked


obstacle = False
ultrasonicSensor = UltrasonicSensor(
    config.ULTRASONIC_SENSOR_CHANNEL, on_obstacle, config.ULTRASONIC_SENSOR_MIN_DISTANCE)
ultrasonicSensor.start()

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
fw = Front_Wheels()
bw = Back_Wheels()
fw.ready()
bw.ready()

route = None


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
    global forward_speed, off_track_count, obstacle, turning_angle, max_off_track_count

    a_step = config.PICAR_A_STEP
    b_step = config.PICAR_B_STEP
    c_step = config.PICAR_C_STEP
    d_step = config.PICAR_D_STEP

    # Measuring distance
    if obstacle:
        bw.stop()
        return False, []
    else:
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
    angle = 89 if turning_angle >= 90 else 91
    if lf_status == [0, 0, 1, 0, 0]:
        off_track_count = 0
        fw.turn(angle)
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
            print("off_track_count:", off_track_count)
            print("last_status:", lf_status)
            raise KeyboardInterrupt
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
    while True:
        _, lf_status = follow_line()
        if lf_status != [1, 1, 1, 1, 1]:
            break


def turn_left():
    fw.turn(90 - 45)
    lf.wait_tile_status(status=[0, 0, 0, 0, 1])
    lf.wait_tile_center()


def turn_right():
    fw.turn(90 + 45)
    lf.wait_tile_status(status=[1, 0, 0, 0, 0])
    lf.wait_tile_center()


def follow_route(route: List[str] = ["derecha._CRUCE_1", "izquierda._CRUCE_2", "derecha._CRUCE_3", "izquierda._CRUCE_4", "0._HABITACION_5"]):
    global forward_speed
    current_hall = "pasillo0"
    room_count = 0
    in_red = False

    bw.speed = forward_speed
    bw.forward()

    if "vuelta" in route[0] and "False" in route[0]:
        route.pop(0)

    while True:
        following, lf_status = follow_line()
        if not following:
            print("The robot has stopped. Probably cause an obstacle")
        else:
            # Measuring color
            red = is_red()
            if red and not in_red:
                room_count += 1
                in_red = True

                current_hall = current_hall.split("_")[0]
                current_hall = current_hall + "_" + str(room_count)
                print("Detected room, current_hall: " + current_hall)
                api.update_current_hall(current_hall)

                if "HABITACION" in route[0]:
                    action = route.pop(0)
                    if "recto" not in action:
                        print("Reched the destiny room!")
                        bw.stop()
                        return

            elif not red and in_red:
                in_red = False
                print("Passed room: " + current_hall)

            if lf_status == [1, 1, 1, 1, 1]:
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

                    turn_left()

                    print(
                        "El robot ha pasado el segundo cruce. Esperando al tercer cruce...")
                    wait_for_crosspath()
                    wait_end_of_crosspath()
                    print(
                        "El robot ha pasado el tercer cruce, continuando recto (fin de giro izquierda)")

                elif action.startswith("derecha"):
                    print("Girando a la derecha")
                    turn_right()
                    print("Saliendo del cruce")

                elif action.startswith("vuelta"):
                    print("Pasillo con salida. Girando a la izquierda dos veces...")
                    wait_for_crosspath()
                    wait_end_of_crosspath()

                    turn_left()

                    wait_for_crosspath()
                    wait_end_of_crosspath()

                    print("El robot ha pasado el segundo cruce, girando a la izquierda")
                    turn_left()

                    wait_for_crosspath()
                    wait_end_of_crosspath()
                    print("El robot ha pasado el tercer cruce, continuando recto")
                else:
                    print("Unexpected action for crosspath: " + action)
                    raise KeyboardInterrupt

                forward_speed = config.PICAR_MED_SPEED
                for step in route:
                    if "CRUCE" in step:
                        current_hall = f"pasillo{action[-1]}{step[-1]}"
                        break

                api.update_current_hall(current_hall)
                print("Continuando recto, nuevo pasillo: " + current_hall)


def destroy():
    bw.stop()
    fw.turn(90)


def processMessage(message: object):
    global route
    print("Received message: " + str(message))

    if "type" not in message:
        return

    if message["type"] == "start":
        route = message["route"]


if __name__ == '__main__':
    api.start_ws(processMessage)
    try:
        while True:
            while route is None:
                time.sleep(0.25)

            print("Starting route to room: " + route["dest_room"])
            follow_route(route=route["route"])

            print("Finished route. Returning to hall...")
            time.sleep(5)
            follow_route(route=route["return_route"])
            print("Finished return route")

            route = None
    except KeyboardInterrupt:
        api.close_ws()
        ultrasonicSensor.kill()
        destroy()
