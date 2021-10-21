from engine.event import *
from engine.base_model import *
from engine.helper import *


class GameEntity(Listener):
    def __init__(self, event_mgr=None):
        super(GameEntity, self).__init__(event_mgr=event_mgr)

    def update(self, *args, **kwargs):
        pass

    # event listener
    def on_tick(self, *e):
        raise NotImplementedError

    def on_move(self, *e):
        raise NotImplementedError


class ShipEntity(GameEntity, Destructible, Projectile, Shooter):
    def __init__(self, event_mgr, hp, sp, dmg, weapon,
                 ship_category=None, ship_type=None):
        GameEntity.__init__(self, event_mgr=event_mgr)
        Destructible.__init__(self, hp=hp, sp=sp)
        Projectile.__init__(self, dmg=dmg)
        Shooter.__init__(self, weapon=weapon)

        self._ship_category = ship_category
        self._ship_type = ship_type

    # event listener
    def on_tick(self, *e):
        raise NotImplementedError

    def on_move(self, *e):
        raise NotImplementedError

    def on_fire(self, *e):
        raise NotImplementedError

    def fire_weapon(self, **kwargs):
        raise NotImplementedError


class Player(ShipEntity, Controllable):
    def __init__(self,
                 *ship_entity_properties,
                 ship_category=EntityCategory.MECH, ship_type=ShipType.PLAYER,
                 **movable_properties):
        Controllable.__init__(self, **movable_properties)
        super(Player, self).__init__(*ship_entity_properties, ship_category=ship_category, ship_type=ship_type)

        self._event_mgr.add(TickEvent, WeakBoundMethod(self.on_tick))
        self._event_mgr.add(InputEvent, WeakBoundMethod(self.on_input))

    def fire_weapon(self, firing=False, auto_fire=False):
        if self._weapon:
            if auto_fire:
                self._weapon.set_auto_fire_state(auto_fire)
            self._weapon.set_fire_state(firing)

        else:
            print('Unable to fire: cannot find weapon!')

    def on_tick(self, e):
        self.update_position()
        self._event_mgr.post(UpdateSpritePosEvent(pos=self._position.get_tuple()))

    def on_input(self, e):
        data = e.get_data()
        event = None

        if data:
            if data['movement_vector'] is not None:
                self.on_move(data['movement_vector'])

            if data['fire_state'] is not None:
                self.on_fire(data['fire_state'])

        else:
            pass

        if event:
            self._event_mgr.post(event)

    def on_move(self, vector):
        direction, magnitude = list(vector.items())[0]
        self.set_move_state(direction)
        self.update_angle(direction, magnitude)

    def on_fire(self, fire_state):
        if AUTO in fire_state:
            self.fire_weapon(auto_fire=fire_state[AUTO])
        else:
            self.fire_weapon(firing=fire_state[MANUAL])


class BulletEntity(GameEntity, Movable, Projectile):
    def __init__(self, event_mgr,
                 dmg=0.0,
                 **movable_properties):
        GameEntity.__init__(self, event_mgr=event_mgr)
        Movable.__init__(self, **movable_properties)
        Projectile.__init__(self, dmg=dmg)

        self._owner = None

    def calculate_damage(self):
        pass

    def update_position(self, *args, **kwargs):
        pass

    def update_angle(self, *args, **kwargs):
        pass

    # event listener
    def on_tick(self, e):
        raise NotImplementedError

    def on_move(self, e):
        raise NotImplementedError


# todo decompose; base classes potentially exists
class Weapon(Listener):
    def __init__(self, event_mgr, atk_spd=0.0, atk_rate=1000, firing=False, auto_firing=False,
                 bullet_factory=None):
        super(Weapon, self).__init__(event_mgr=event_mgr)
        self._attack_speed = atk_spd
        self._curr_attack_rate = atk_rate
        self._true_atk_rate = self._curr_attack_rate
        self._last_shot_tick = 0
        self._is_firing = firing
        self._is_auto_firing = auto_firing

        self._bullet_factory = bullet_factory
        self._bullet_stack = list()

        self._event_mgr.add(TickEvent, WeakBoundMethod(self.on_tick))

    def on_tick(self, e):
        self.fire()

    def fire(self, *args, **kwargs):
        pass

    def set_auto_fire_state(self, auto_fire):
        self._is_auto_firing = self._is_auto_firing ^ auto_fire

    def set_fire_state(self, firing):
        if self._is_auto_firing:
            self._is_firing = self._is_auto_firing

        else:
            self._is_firing = firing
