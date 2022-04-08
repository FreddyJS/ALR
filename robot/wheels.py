import os
import config

from picar import filedb
import picar.back_wheels as back_wheels
import picar.front_wheels as front_wheels

DBFILE = '/tmp/picar-config'


def init_db():
    if not os.path.exists(DBFILE):
        open(DBFILE, 'w').close()

    db = filedb.fileDB(DBFILE)
    db.set('turning_offset', config.PICAR_TURNING_OFFSET)
    db.set('forward_A', config.PICAR_FORWARD_A)
    db.set('forward_B', config.PICAR_FORWARD_B)


class Back_Wheels(back_wheels.Back_Wheels):
    def __init__(self, debug=False, bus_number=1):
        init_db()
        super().__init__(debug=debug, bus_number=bus_number, db=DBFILE)

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
        init_db()
        super().__init__(debug=debug, bus_number=bus_number, channel=channel, db=DBFILE)
