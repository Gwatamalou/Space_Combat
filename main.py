import random

import arcade
import glob

window_width = 600
window_height = 800
window_title = 'Space_Combat'

CHARACTER_SCALING = 1

PLAYER_MOVEMENT_SPEED = 5
LASER_SPEAD = 10

PLAYER = glob.glob('player/*')
METEOR = glob.glob('meteor/*')
LASER = glob.glob('laser/*')


class Entity(arcade.Sprite):
    def __init__(self, sprite_list, center_x=0, center_y=0, change_x=0, change_y=0, bottom=None):
        super().__init__()
        self.sprite_list = arcade.Sprite(sprite_list, CHARACTER_SCALING)
        self.sprite_list.change_x = change_x
        self.sprite_list.change_y = change_y
        self.sprite_list.center_x = center_x
        self.sprite_list.center_y = center_y
        if bottom: self.sprite_list.bottom = bottom


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(window_width, window_height, window_title)

        self.scene = None
        self.player_list = []
        self.meteor_list = []
        self.laser_list = []
        self.physics_engine = None
        self.camera = None

        arcade.set_background_color(arcade.color.CHARCOAL)

    def setup(self):
        self.scene = arcade.Scene()

        # списки обектов
        self.scene.add_sprite_list('Player')
        self.scene.add_sprite_list('Meteor', use_spatial_hash=True)
        self.scene.add_sprite_list('Laser', use_spatial_hash=True)

        self.player_list.extend(PLAYER)
        self.meteor_list.extend(METEOR)
        self.laser_list.extend(LASER)

        self.player_sprit = Entity(self.player_list[0], 300, 50)

        self.camera = arcade.Camera(self.width, self.height)
        self.scene.add_sprite('Player', self.player_sprit.sprite_list)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprit, None)

    def on_draw(self):
        self.clear()
        self.scene['Player'].draw()
        self.scene['Meteor'].draw()
        self.scene['Laser'].draw()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprit.sprite_list.change_x = -PLAYER_MOVEMENT_SPEED
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprit.sprite_list.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprit.sprite_list.change_x = 0
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprit.sprite_list.change_x = 0

    def on_update(self, delta_time):
        self.scene.update()
        self.physics_engine.update()

        # создание лазера
        self.laser_sprit = Entity(self.laser_list[0], center_x=self.player_sprit.sprite_list.center_x,
                                  change_y=LASER_SPEAD, bottom=self.player_sprit.sprite_list.top)
        self.scene.add_sprite('Laser', self.laser_sprit.sprite_list)

        # создание метеорита

        self.meteor_sprite = Entity(self.meteor_list[random.randrange(0, len(self.meteor_list) - 1)],
                                    center_x=random.randint(0, 600),
                                    center_y=850,
                                    change_y=-(random.randint(1, 6)),
                                    change_x=random.randint(-3, 3))
        self.scene.add_sprite('Meteor', self.meteor_sprite.sprite_list)

        # проверка столкновения лазера с метеоритом
        for laser in self.scene['Laser']:
            hit_list = arcade.check_for_collision_with_list(laser, self.scene['Meteor'])
            if hit_list:
                laser.remove_from_sprite_lists()
            for meteor_sprite in hit_list:
                meteor_sprite.remove_from_sprite_lists()
            # удаление лезра за пределами игровго поля
            if laser.bottom > 800: laser.remove_from_sprite_lists()
        # удаление метеорита за пределами игровго поля
        for meteor_sprite in self.scene['Meteor']:
            if meteor_sprite.top < 0:
                meteor_sprite.remove_from_sprite_lists()


        # meteor_check_list = arcade.check_for_collision_with_list(self.player_sprit.sprite_list, self.scene['Meteor'])
        #
        # for meteor_sprite in meteor_check_list:
        #     meteor_sprite.remove_from_sprite_lists()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
