from engine.event import *
from engine.base_model import *


class GameEntity(Listener):
    def __init__(self, event_mgr=None):
        super(GameEntity, self).__init__(event_mgr=event_mgr)

    def update(self, *args, **kwargs):
        pass

    # event listener
    def on_tick(self, e):
        raise NotImplementedError

    def on_move(self, e):
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
    def on_tick(self, e):
        raise NotImplementedError

    def on_move(self, e):
        raise NotImplementedError

    def fire(self, **kwargs):
        raise NotImplementedError


class Player(ShipEntity, Controllable):
    def __init__(self,
                 *ship_entity_properties,
                 ship_category=EntityCategory.MECH, ship_type=ShipType.PLAYER,
                 **movable_properties):
        Controllable.__init__(self, **movable_properties)
        super(Player, self).__init__(*ship_entity_properties, ship_category=ship_category, ship_type=ship_type)

        self._event_mgr.add(TickEvent, WeakBoundMethod(self.on_tick))
        self._event_mgr.add(InputEvent, WeakBoundMethod(self.on_move))

    def fire(self, firing, auto_fire=False):
        if self._weapon:
            self._weapon.fire(firing=firing, auto_fire=auto_fire)

        else:
            print('cannot find weapon!')

    def on_tick(self, e):
        self.update_position()
        self._event_mgr.post(UpdateSpritePosEvent(pos=self._position.get_tuple()))

    def on_move(self, e):
        data = e.get_data()
        event = None

        if data:
            # player_controlled = data['is_player']
            movement_vector = data['movement_vector']
            auto_firing = data['auto_firing']
            firing = data['firing']

            if movement_vector:
                direction, magnitude = list(movement_vector.items())[0]
                self.set_move_state(direction)
                self.update_angle(direction, magnitude)

            else:
                print(f'{data}')
                print("direction/magnitude not found")

            if firing or auto_firing:
                self.fire(firing=firing, auto_fire=auto_firing)

        else:
            print("data not found...")

        if event:
            self._event_mgr.post(event)


class BulletEntity(GameEntity, Movable, Projectile):
    def __init__(self, event_mgr, dmg,
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


class Weapon(Listener):
    def __init__(self, event_mgr, atk_spd=0.0, atk_rate=1000, auto_fire=False,
                 bullet_factory=None):
        super(Weapon, self).__init__(event_mgr=event_mgr)
        self._attack_speed = atk_spd
        self._curr_attack_rate = atk_rate
        self._true_atk_rate = self._curr_attack_rate
        self._last_shot_tick = 0
        self._is_firing = auto_fire

        self._bullet_factory = bullet_factory
        self._bullet_stack = list()

        self._event_mgr.add(TickEvent, WeakBoundMethod(self.on_tick))

    def on_tick(self, e):
        self.fire()

    def fire(self, *args, **kwargs):
        pass

    def set_fire_state(self, firing=False, auto_fire=False):
        self._is_firing = (self._is_firing ^ auto_fire) or firing
