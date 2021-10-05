from event import *
from util.enums import *
from helper.helper import WeakBoundMethod


class Entity(Listener):
    def __init__(self, event_mgr,
                 pos=(0, 0), pos_off=(0, 0), accel=(0, 0), mov_spd=3.0):
        super(Entity, self).__init__(
            event_mgr=event_mgr)

        self._pos = pos
        self._pos_off = pos_off
        self._accel_vector = accel
        self._mov_spd = mov_spd

    def update_pos(self, *args, **kwargs):
        pass

    def update_accel(self, *args, **kwargs):
        pass


class Ship(Entity):
    def __init__(self, event_mgr,
                 ship_weapon=None, ship_stats=None, ship_type=None,
                 ship_category=None, ship_status=None,
                 is_player=False,
                 **kwargs):
        super(Ship, self).__init__(event_mgr, **kwargs)

        self._event_mgr.add(TickEvent, WeakBoundMethod(self.on_tick_event))
        self._event_mgr.add(InputMoveEvent, WeakBoundMethod(self.on_entity_move))

        self._ship_weapon = ship_weapon
        self._ship_stats = ship_stats
        self._ship_type = ship_type
        self._ship_category = ship_category
        self._ship_status = ship_status

        self._is_player = is_player
        self._move_state = {
            LEFT: False,
            RIGHT: False,
            UP: False,
            DOWN: False,
        }

    def on_tick_event(self, e):
        self.update_pos()
        self._event_mgr.post(UpdateSpritePosEvent(pos=self._pos))

    def on_entity_move(self, e):
        data = e.get_data()
        event = None

        if data:
            player_controlled = data['is_player']
            direction = data['direction']
            magnitude = data['magnitude']

            if not(direction is None and magnitude is None):
                if player_controlled:
                    self.set_move_state(direction)
                    self.update_accel(direction, magnitude)

                else:
                    """
                    Reserved for AI movement algorithm
                    """
                    print("Moving AI")

            else:
                print(f'{data}')
                print("direction/magnitude not found")

        else:
            print("data not found...")

        if event:
            self._event_mgr.post(event)

    def update_pos(self):
        self._pos[X_AXIS] = self._pos[X_AXIS] + (self._accel_vector[X_AXIS] * self._mov_spd)
        self._pos[Y_AXIS] = self._pos[Y_AXIS] + (self._accel_vector[Y_AXIS] * self._mov_spd)

    def update_accel(self, direction, magnitude):
        if magnitude == STOP:
            if (direction == LEFT or direction == RIGHT) and \
                    not (self._move_state[LEFT] or self._move_state[RIGHT]):
                self._accel_vector[X_AXIS] = magnitude

            elif (direction == UP or direction == DOWN) and \
                    not (self._move_state[UP] or self._move_state[DOWN]):
                self._accel_vector[Y_AXIS] = magnitude

        else:
            if direction == LEFT or direction == RIGHT:
                self._accel_vector[X_AXIS] = magnitude

            elif direction == UP or direction == DOWN:
                self._accel_vector[Y_AXIS] = magnitude

    def set_move_state(self, direction):
        self._move_state[direction] = not self._move_state[direction]


class Bullet(Entity):
    def __init__(self, event_mgr, **kwargs):
        super(Bullet, self).__init__(event_mgr, **kwargs)

        self._bullet_type = None
        self._dmg = None
        self._owner = None
