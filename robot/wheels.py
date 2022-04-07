import config

from picar import filedb
from picar.SunFounder_TB6612 import TB6612
from picar.SunFounder_PCA9685 import Servo, PCA9685

import picar.back_wheels as back_wheels
import picar.front_wheels as front_wheels


class Back_Wheels(back_wheels.Back_Wheels):
    def __init__(self, debug=False, bus_number=1):
        ''' Init the direction channel and pwm channel '''
        self.forward_A = True
        self.forward_B = True

        self.db = filedb.fileDB()
        self.db.set('turning_offset', config.PICAR_TURNING_OFFSET)
        self.db.set('forward_A', config.PICAR_FORWARD_A)
        self.db.set('forward_B', config.PICAR_FORWARD_B)

        self.forward_A = int(self.db.get('forward_A', default_value=1))
        self.forward_B = int(self.db.get('forward_B', default_value=1))

        self.left_wheel = TB6612.Motor(self.Motor_A, offset=self.forward_A)
        self.right_wheel = TB6612.Motor(self.Motor_B, offset=self.forward_B)

        self.pwm = PCA9685.PWM(bus_number=bus_number)

        def _set_a_pwm(value):
            pulse_wide = int(self.pwm.map(value, 0, 100, 0, 4095))
            self.pwm.write(self.PWM_A, 0, pulse_wide)

        def _set_b_pwm(value):
            pulse_wide = int(self.pwm.map(value, 0, 100, 0, 4095))
            self.pwm.write(self.PWM_B, 0, pulse_wide)

        self.left_wheel.pwm = _set_a_pwm
        self.right_wheel.pwm = _set_b_pwm

        self._speed = 0

        self.debug = debug
        self._debug_('Set left wheel to #%d, PWM channel to %d' %
                     (self.Motor_A, self.PWM_A))
        self._debug_('Set right wheel to #%d, PWM channel to %d' %
                     (self.Motor_B, self.PWM_B))

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed
        ''' Set moving speeds '''
        self.left_wheel.speed = self._speed
        self.right_wheel.speed = self._speed
        self._debug_('Set speed to %s' % self._speed)

    def left(self):
        self.left_wheel.backward()
        self.right_wheel.forward()
        self._debug_('Turning left')

    def right(self):
        self.left_wheel.forward()
        self.right_wheel.backward()
        self._debug_('Turning right')


class Front_Wheels(front_wheels.Front_Wheels):
    def __init__(self, debug=False, bus_number=1, channel=0):
        ''' setup channels and basic stuff '''
        self.db = filedb.fileDB()
        self.db.set('turning_offset', config.PICAR_TURNING_OFFSET)
        self.db.set('forward_A', config.PICAR_FORWARD_A)
        self.db.set('forward_B', config.PICAR_FORWARD_B)

        self._channel = channel
        self._straight_angle = 90
        self.turning_max = 45
        self._turning_offset = int(self.db.get(
            'turning_offset', default_value=0))

        self.wheel = Servo.Servo(
            self._channel, bus_number=bus_number, offset=self.turning_offset)
        self.debug = debug
        self._debug_('Front wheel PWM channel: %s' % self._channel)
        self._debug_('Front wheel offset value: %s ' % self.turning_offset)

        self._angle = {"left": self._min_angle,
                       "straight": self._straight_angle, "right": self._max_angle}
        self._debug_('left angle: %s, straight angle: %s, right angle: %s' % (
            self._angle["left"], self._angle["straight"], self._angle["right"]))
