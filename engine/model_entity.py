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

        self._ship_category = ship_category
        self._ship_type = ship_type

    # event listener
    def on_tick(self, e):
        raise NotImplementedError

    def on_move(self, e):
        raise NotImplementedError


class Player(ShipEntity, Controllable):
    def __init__(self,
                 *ship_entity_properties,
                 ship_category=EntityCategory.MECH, ship_type=ShipType.PLAYER,
                 **movable_properties):
        Controllable.__init__(self, **movable_properties)
        super(Player, self).__init__(*ship_entity_properties, ship_category=ship_category, ship_type=ship_type)

        self._event_mgr.add(TickEvent, WeakBoundMethod(self.on_tick))
        self._event_mgr.add(InputMoveEvent, WeakBoundMethod(self.on_move))

    def fire(self):
        pass

    def on_tick(self, e):
        self.update_position()
        self._event_mgr.post(UpdateSpritePosEvent(pos=self._position.get_tuple()))

    def on_move(self, e):
        data = e.get_data()
        event = None

        if data:
            # player_controlled = data['is_player']
            direction = data['direction']
            magnitude = data['magnitude']

            if direction is not None and magnitude is not None:
                self.set_move_state(direction)
                self.update_angle(direction, magnitude)

                # if player_controlled:

                # else:
                #     """
                #     Reserved for AI movement algorithm
                #     """
                #     print("Moving AI")

            else:
                print(f'{data}')
                print("direction/magnitude not found")

        else:
            print("data not found...")

        if event:
            self._event_mgr.post(event)


# class Bullet(Entity):
#     def __init__(self, event_mgr, **kwargs):
#         super(Bullet, self).__init__(event_mgr, **kwargs)
#
#         self._bullet_type = None
#         self._dmg = None
#         self._owner = None


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
