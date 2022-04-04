#!/usr/bin/env python

import sys
import time

import picar
import board
import adafruit_tcs34725
from picar import front_wheels
from picar import back_wheels
from LineFollower import LineFollower

import api
import config

# picar.setup()
azul = config.COLOR_SENSOR_BLUE_VALUE
rojo = config.COLOR_SENSOR_RED_VALUE

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_tcs34725.TCS34725(i2c)
off_track_count = 0

LF_REFERENCES = config.LINE_FOLLOWER_REFERENCES
# Change sensor integration time to values between 2.4 and 614.4 milliseconds
sensor.integration_time = config.COLOR_SENSOR_INTEGRATION_TIME
# Change sensor gain to 1, 4, 16, or 60
sensor.gain = config.COLOR_SENSOR_GAIN

forward_speed = 96
backward_speed = 38
velocidadGiro = 33
turning_angle = 86
'''
a_step = 4
b_step = 7
c_step = 12
d_step = 15
'''

a_step = 3
b_step = 6
c_step = 15
d_step = 45


aDos = 8
bDos = 12
cTres = 16
dTres = 20


giroCruce = 46
velocidadCruce = 46
direccAux = ""
dir2 = ""
firstDetectRed = False
max_off_track_count = 70

delay = 0.0005
# recto,derecha,derecha
# derecha,izquierda
# izquierda,izquierda
# CONTADOR RUTAS

#rutas = ["recto","derecha","derecha"]

# rutas=["derecha","izquierda"]

# rutas=["recto","izquierda","izquierda"]

# rutas=["izquierda","derecha"]
# rutas=["izquierda","recto","derecha"]

# rutas=["derecha","izquierda"]
# for i in argsk
rutas = ["recto", "recto", "recto", "recto"]

nCruces = len(rutas)

fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
lf = LineFollower()

lf.references = LF_REFERENCES
fw.ready()
bw.ready()
fw.turning_max = 45

# tcs = Adafruit_TCS34725.TCS34725(integration_time=Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_154MS,
#                                  gain=Adafruit_TCS34725.TCS34725_GAIN_1X, address=0x29, busnum=1)


def destroy():
    bw.stop()
    fw.turn(90)
    sys.exit(1)


def stopVehicle(fin):
    if(fin):
        bw.stop()
        print('HA LLEGADO A SU DESTINO')
        time.sleep(2)
        return
    bw.stop()


def selectStep(lf_status, step_a, step_b, step_c, step_d):
    step = None
    if lf_status == [0, 0, 1, 0, 0]:
        step = 0
    elif lf_status == [0, 1, 1, 0, 0] or lf_status == [0, 0, 1, 1, 0]:
        step = step_a
    elif lf_status == [0, 1, 0, 0, 0] or lf_status == [0, 0, 0, 1, 0]:
        step = step_b
    elif lf_status == [1, 1, 0, 0, 0] or lf_status == [0, 0, 0, 1, 1]:
        step = step_c
    elif lf_status == [1, 0, 0, 0, 0] or lf_status == [0, 0, 0, 0, 1]:
        step = step_d

    return step


def recorrido(x):
    global turning_angle
    global a_step
    global b_step
    global c_step
    global d_step
    global giroCruce
    global nCruces
    global direccAux
    global dir2
    global rutas

    if(x == 0):
        print('Iniciando ruta a la estacion base')
        rutas = ["derecha"]
        nCruces = len(rutas)
        bw.speed = forward_speed
        bw.forward()
    if(x == 2):
        print('VUELtA!!!')
        rutas = ["derecha", "derecha", "recto", "recto"]
        nCruces = len(rutas)
        bw.speed = forward_speed
        bw.forward()
    if(x == 1):
        rutas = ["recto", "recto", "recto", "recto"]
        nCruces = len(rutas)

    print('iniciorecorrido')
    off_track_count = 0
    bw.speed = forward_speed
    dir2 = ""
    bw.forward()
    global firstDetectRed

    while True:
        temp = sensor.color_temperature
        # print(temp)
        # print(temp)
        if(str(temp) == "None"):
            temp = 5500
        if(temp < rojo):
            print('CRUCE INMINENTE!')
            if(not firstDetectRed):
                firstDetectRed = not firstDetectRed
                direccAux = rutas.pop(0)
                print('direccion a tomar: '+direccAux)
                dir2 = direccAux
                bw.speed = forward_speed - 29  # reduce velocidad por llegar a un cruce
                bw.forward()
                nCruces -= 1
                if(cruce(nCruces, direccAux)):
                    return True

        firstDetectRed = False
        lt_status_now = lf.read_digital()
        step = selectStep(lt_status_now, a_step, b_step, c_step, d_step)

        # Direction calculate
        if lt_status_now == [0, 0, 1, 0, 0]:
            off_track_count = 0
            # fw.turn(86)
            turning_angle = 87
            # turning_angle=0
        # turn right
        elif lt_status_now in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
            off_track_count = 0
            turning_angle = int(90 - step)
        # turn left
        elif lt_status_now in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
            off_track_count = 0
            turning_angle = int(90 + step)
        elif lt_status_now == [0, 0, 0, 0, 0]:
            off_track_count += 1
            if off_track_count > max_off_track_count:
                # tmp_angle = -(turning_angle - 90) + 90
                tmp_angle = (turning_angle-86)/abs(86-turning_angle)
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
        time.sleep(delay)


def cruce(nCruceCount, direccion):
    # solo para seguir recto?
    segundaCruceta = False
    global firstDetectRed
    salirAux = False
    global turning_angle
    global off_track_count

    if("recto" in direccion):
        print("Avanzando por el pasillo... direccion a seguir=recto")
        primeraCrucetaRecto = False
        flagAux = False
        while not salirAux:
            # siguiendo linea, atravesando rojo
            print("Avanzando por el pasillo... sobre el primer rojo")

            lt_status_now = lf.read_digital()
            step = selectStep(lt_status_now, a_step, b_step, c_step, d_step)

            # Direction calculate
            if lt_status_now == [0, 0, 1, 0, 0]:
                off_track_count = 0
                fw.turn(87)
            # turn right
            elif lt_status_now in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
                off_track_count = 0
                turning_angle = int(87 - step)
            # turn left
            elif lt_status_now in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
                off_track_count = 0
                turning_angle = int(87 + step)
           # elif lt_status_now == [0, 0, 0, 0, 0]:
            #    off_track_count += 1
             #   if off_track_count > max_off_track_count:
                # tmp_angle = -(turning_angle - 90) + 90
              #      tmp_angle = (turning_angle-90)/abs(90-turning_angle)
               #     tmp_angle *= fw.turning_max
                #    bw.speed = backward_speed
                #   bw.backward()
                #  fw.turn(tmp_angle)
                # lf.wait_tile_center()
                # bw.stop()
                # fw.turn(turning_angle)
                # time.sleep(0.2)
                #bw.speed = forward_speed
                # bw.forward()
                # time.sleep(0.2)
            # elif lt_status_now == [1 1 1 1 1]:
                # primeraCrucetaReccto=True

            else:
                off_track_count = 0
            fw.turn(turning_angle)
            time.sleep(delay)

            temp = sensor.color_temperature
            if(str(temp) == "None"):
                temp = 5500

            if(temp > rojo):
                # vuelvo a estar en blanco
                bw.speed = velocidadCruce
                bw.forward()
                while True:
                    #print("El robot esta avanzando por el cruce, ha atravesado el primer rojo")
                    time.sleep(0.0005)
                    lt_status_now = lf.read_digital()
                    step = selectStep(lt_status_now, a_step,
                                      b_step, c_step, d_step)

                    # Direction calculate
                    if lt_status_now == [0, 0, 1, 0, 0]:
                        off_track_count = 0
                        fw.turn(90)
                    # turn right
                    elif lt_status_now in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
                        off_track_count = 0
                        turning_angle = int(90 - step)
                    # turn left
                    elif lt_status_now in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
                        off_track_count = 0
                        turning_angle = int(90 + step)

                    # elif lt_status_now == [0, 0, 0, 0, 0]:
                     #   off_track_count += 1
                      #  if off_track_count > max_off_track_count:
                       #     # tmp_angle = -(turning_angle - 90) + 90
                        #    tmp_angle = (turning_angle-90)/abs(90-turning_angle)
                        #   tmp_angle *= fw.turning_max
                        #  bw.speed = backward_speed
                        # bw.backward()
                        # fw.turn(tmp_angle)
                        # lf.wait_tile_center()
                        # bw.stop()
                        # fw.turn(turning_angle)
                        # time.sleep(0.2)
                        #bw.speed = forward_speed
                        # bw.forward()
                        # time.sleep(0.2)

                    elif lt_status_now == [1, 1, 1, 1, 1]:
                        off_track_count = 0
                        while(True):
                            time.sleep(delay)
                            lt_status_now = lf.read_digital()
                            print(lt_status_now)
                            if lt_status_now == [0, 0, 1, 0, 0]:
                               # print('sali de la cruceta')
                                step = 0
                                flagAux = True  # he salido de la primera cruceta
                            elif lt_status_now == [0, 1, 1, 0, 0] or lt_status_now == [0, 0, 1, 1, 0]:
                                #print('sali de la cruceta')
                                step = a_step
                                flagAux = True

                            elif lt_status_now == [0, 1, 0, 0, 0] or lt_status_now == [0, 0, 0, 1, 0]:
                                #print('sali de la cruceta')
                                step = b_step
                                flagAux = True

                            elif lt_status_now == [1, 1, 0, 0, 0] or lt_status_now == [0, 0, 0, 1, 1]:
                                #print('sali de la cruceta')
                                step = c_step
                                flagAux = True

                            elif lt_status_now == [1, 0, 0, 0, 0] or lt_status_now == [0, 0, 0, 0, 1]:
                                #print('sali de la cruceta')
                                step = d_step
                                flagAux = True

                            # Direction calculate
                            if lt_status_now == [0, 0, 1, 0, 0]:
                                off_track_count = 0
                                turning_angle = 86
                            # turn right
                            elif lt_status_now in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
                                off_track_count = 0
                                turning_angle = int(86 - step)
                            # turn left
                            elif lt_status_now in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
                                off_track_count = 0
                                turning_angle = int(86 + step)
                            elif lt_status_now == [0, 0, 0, 0, 0]:
                                off_track_count += 1
                                if off_track_count > max_off_track_count:
                                    # tmp_angle = -(turning_angle - 90) + 90
                                    tmp_angle = (turning_angle-90) / \
                                        abs(90-turning_angle+1)
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
                            time.sleep(delay)
                            if(flagAux):
                                if(lt_status_now == [1, 1, 1, 1, 1]):
                                    salirAux = True
                                    break
                    else:
                        off_track_count = 0
                    fw.turn(turning_angle)
                    time.sleep(delay)

                    if(salirAux):
                        break

    if("derecha" in direccion):
        # ya hemos reducido la velocidad antes de escoger direccion
        # en caso de ir a la derecha: hemos detectado rojo, se redujo velocidad, buscamos cruceta y giramos derecha
        # para reenganchar la linea de nuevo
        print('SE ACERCA GIRO DERECha')

        while(True):
            lt_status_now = lf.read_digital()
            step = selectStep(lt_status_now, a_step, b_step, c_step, d_step)

            # Direction calculate
            if lt_status_now == [0, 0, 1, 0, 0]:
                off_track_count = 0
                turning_angle = 86
            # turn right
            elif lt_status_now in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
                off_track_count = 0
                turning_angle = int(86 - step)
            # turn left
            elif lt_status_now in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
                off_track_count = 0
                turning_angle = int(86 + step)
            elif lt_status_now == [0, 0, 0, 0, 0]:
                off_track_count += 1
                if off_track_count > max_off_track_count:
                    # tmp_angle = -(turning_angle - 90) + 90
                    tmp_angle = (turning_angle-90)/abs(90-turning_angle+1)
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

            # cruceta, es el momento de realizar el giro a la derecha
            elif lt_status_now == [1, 1, 1, 1, 1]:
                off_track_count = 0
                print('CRUCETA!')
                # time.sleep(2)
                # time.sleep(0.5)
                bw.speed = velocidadGiro
                bw.forward()
                step = giroCruce
                fw.turn(int(86+step+10+5))  # - izquierda + derecha
                time.sleep(3.28)  # tiempo para que gire y reenganche la linea
                break
            else:
                off_track_count = 0
            fw.turn(turning_angle)
            time.sleep(delay)
    if("izquierda" in direccion):
        bw.speed = velocidadCruce
        bw.forward()
        flagAux = False
        while(True):
            lt_status_now = lf.read_digital()
            step = selectStep(lt_status_now, a_step, b_step, c_step, d_step)

            # Direction calculate
            if lt_status_now == [0, 0, 1, 0, 0]:
                off_track_count = 0
                turning_angle = 86
            # turn right
            elif lt_status_now in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
                off_track_count = 0
                turning_angle = int(86 - step)
            # turn left
            elif lt_status_now in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
                off_track_count = 0
                turning_angle = int(86 + step)
            elif lt_status_now == [0, 0, 0, 0, 0]:
                off_track_count += 1
                if off_track_count > max_off_track_count:
                    # tmp_angle = -(turning_angle - 90) + 90
                    tmp_angle = (turning_angle-90)/abs(90-turning_angle+1)
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

            # cruceta, es el momento de realizar el giro a la derecha
            elif lt_status_now == [1, 1, 1, 1, 1]:
                off_track_count = 0
                while(True):
                    time.sleep(delay)
                    lt_status_now = lf.read_digital()
                    print(lt_status_now)
                    if lt_status_now == [0, 0, 1, 0, 0]:
                        #print('sali de la cruceta')
                        step = 0
                        flagAux = True  # he salido de la primera cruceta
                    elif lt_status_now == [0, 1, 1, 0, 0] or lt_status_now == [0, 0, 1, 1, 0]:
                        #print('sali de la cruceta')
                        step = a_step
                        flagAux = True

                    elif lt_status_now == [0, 1, 0, 0, 0] or lt_status_now == [0, 0, 0, 1, 0]:
                        #print('sali de la cruceta')
                        step = b_step
                        flagAux = True

                    elif lt_status_now == [1, 1, 0, 0, 0] or lt_status_now == [0, 0, 0, 1, 1]:
                        #print('sali de la cruceta')
                        step = c_step
                        flagAux = True

                    elif lt_status_now == [1, 0, 0, 0, 0] or lt_status_now == [0, 0, 0, 0, 1]:
                        #print('sali de la cruceta')
                        step = d_step
                        flagAux = True

                    # Direction calculate
                    if lt_status_now == [0, 0, 1, 0, 0]:
                        off_track_count = 0
                        turning_angle = 86
                    # turn right
                    elif lt_status_now in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
                        off_track_count = 0
                        turning_angle = int(86 - step)
                    # turn left
                    elif lt_status_now in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
                        off_track_count = 0
                        turning_angle = int(86 + step)
                    elif lt_status_now == [0, 0, 0, 0, 0]:
                        off_track_count += 1
                        if off_track_count > max_off_track_count:
                            # tmp_angle = -(turning_angle - 90) + 90
                            tmp_angle = (turning_angle-90) / \
                                abs(90-turning_angle+1)
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
                    time.sleep(delay)
                    if(flagAux):
                        if(lt_status_now == [1, 1, 1, 1, 1]):
                            bw.speed = velocidadGiro
                            bw.forward()
                            step = giroCruce
                            fw.turn(int(86-step-10))  # - izquierda + derecha
                            # tiempo para que gire y reenganche la linea
                            time.sleep(2.05)
                            break
                break
            else:
                off_track_count = 0
            fw.turn(turning_angle)
            time.sleep(delay)

    primeraCruceta = False
    bw.speed = forward_speed
    bw.forward()
    print('NUEVO PASILLO')
    firstDetectRed = False

    if(nCruceCount == 0):
        print('ULTIMO PASILLO')
        contador = 1  # contador de habitaciones; numero de azules atravesados
        fff = False  # flag transicion azul suelo
        firstDetect = False
        habitacion = 1

        while(True):
            time.sleep(0.0005)
            lt_status_now = lf.read_digital()
            step = selectStep(lt_status_now, a_step, b_step, c_step, d_step)

            # Direction calculate
            if lt_status_now == [0, 0, 1, 0, 0]:
                off_track_count = 0
                fw.turn(90)
            # turn right
            elif lt_status_now in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
                off_track_count = 0
                turning_angle = int(90 - step)
            # turn left
            elif lt_status_now in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
                off_track_count = 0
                turning_angle = int(90 + step)
            elif lt_status_now == [0, 0, 0, 0, 0]:
                off_track_count += 1
                if off_track_count > max_off_track_count:
                    # tmp_angle = -(turning_angle - 90) + 90
                    tmp_angle = (turning_angle+1-90)/abs(90-turning_angle+1)
                    tmp_angle *= fw.turning_max
                    bw.speed = backward_speed
                    bw.backward()
                    fw.turn(tmp_angle)
                    lf.wait_tile_center()
                    bw.stop()
                    fw.turn(turning_angle)
                    time.sleep(0.2)
                    #bw.speed = forward_speed - 20
                    bw.forward()
                    time.sleep(0.2)

            else:
                off_track_count = 0
            fw.turn(turning_angle)
            time.sleep(delay)

            temp = sensor.color_temperature
            # print(temp)
            if (temp < rojo):
                if(not firstDetect):
                    print('Aproximandonos a una habitacion, reduciendo la velocidad.')
                    if(contador == habitacion):
                        # va a finalizar el programa, gracias al True
                        stopVehicle(True)
                        return True
                    else:
                        firstDetect = not firstDetect
                        bw.speed = forward_speed-39
                        bw.forward()
                        fff = True
            else:
                if(fff):
                    print(
                        'Hemos pasado por una habitacion que no es el destino todavia')
                    bw.speed = forward_speed
                    bw.forward()
                    contador += 1
                    firstDetect = not firstDetect
                    fff = False
    # return False


class RobotState:
    IDLE = 0
    GUIDING = 1
    RETURNING = 2


current_state = RobotState.IDLE
current_route = None
dest_room = None


def processMessage(message: object):
    global current_state, current_route, dest_room
    print("Received message: " + str(message))

    if "type" not in message:
        # Ignore message if it does not have a type, probably debug message
        return

    if message["type"] == "start":
        dest_room = message["room"]
        current_route = message["route"]
        current_state = RobotState.GUIDING


# Start websocket client to receive updates from the backend
api.start_ws(processMessage)

try:
    while(True):
        # Wait for a new route to be sent from the backend to start navigating
        if current_state == RobotState.IDLE:
            time.sleep(0.1)

        # Navigate to the room using the current_route
        elif current_state == RobotState.GUIDING:
            print("Navigating to room `{}`".format(dest_room))
            recorrido(1)

            # Set the state to returning to the docking station
            current_state = RobotState.RETURNING

        # Return to the docking station
        elif current_state == RobotState.RETURNING:
            print("Returning to docking station")
            recorrido(2)

            # We should wait in IDLE state until the backend sends a new route
            current_state = RobotState.IDLE
            # for now just exit the program
            sys.exit(0)

except KeyboardInterrupt:
    api.close_ws()
    destroy()
