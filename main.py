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


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(window_width, window_height, window_title)

        self.scene = None
        self.player_sprite = None
        self.player_list = []
        self.meteor_list = []
        self.laser_list = []
        self.physics_engine = None
        self.camera = None

        arcade.set_background_color(arcade.color.CHARCOAL)

    def setup(self):
        self.scene = arcade.Scene()

        #списки обектов
        self.scene.add_sprite_list('Player')
        self.scene.add_sprite_list('Meteor', use_spatial_hash=True)
        self.laser_list = arcade.SpriteList()

        self.player_list.extend(PLAYER)
        self.meteor_list.extend(METEOR)
        self.camera = arcade.Camera(self.width, self.height)

        #спрайт игрока
        self.player_sprite = arcade.Sprite(self.player_list[0], CHARACTER_SCALING)
        self.player_sprite.center_x = 300
        self.player_sprite.center_y = 50
        self.scene.add_sprite('Player', self.player_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, None)

    def on_draw(self):
        self.clear()
        self.scene['Player'].draw()
        self.scene['Meteor'].draw()
        self.laser_list.draw()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0


    def on_update(self, delta_time):
        self.laser_list.update()
        self.scene.update()
        self.physics_engine.update()

        #создание лазера
        laser = arcade.Sprite('laser/laserBlue.png')
        laser.change_y = LASER_SPEAD
        laser.center_x = self.player_sprite.center_x
        laser.bottom = self.player_sprite.top
        self.laser_list.append(laser)

        #создание метеорита
        meteor_sprite = arcade.Sprite(self.meteor_list[random.randrange(0, len(self.meteor_list) - 1)], CHARACTER_SCALING)
        meteor_sprite.center_x = random.randint(0, 600)
        meteor_sprite.center_y = 850
        meteor_sprite.change_y = -10
        self.scene.add_sprite('Meteor', meteor_sprite)

        #проверка столкновения лазера с метеоритом
        for laser in self.laser_list:
            hit_list = arcade.check_for_collision_with_list(laser, self.scene['Meteor'])
            if hit_list:
                laser.remove_from_sprite_lists()
            for meteor_sprite in hit_list:
                meteor_sprite.remove_from_sprite_lists()
            #удаление лезра за пределами игровго поля
            if laser.bottom > 800: laser.remove_from_sprite_lists()
        # удаление метеорита за пределами игровго поля
        for meteor_sprite in self.scene['Meteor']:
            if meteor_sprite.top < 0:
                meteor_sprite.remove_from_sprite_lists()


"""        meteor_check_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene['Meteor'])

        for meteor_sprite in meteor_check_list:
            meteor_sprite.remove_from_sprite_lists()"""


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
