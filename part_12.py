import random
import arcade

SPRITE_SCALING_PLAYER = 0.08
SPRITE_SCALING_FIGHTER = .08
SPRITE_SCALING_LASER = 0.8
FIGHTER_COUNT = 6
BULLET_SPEED = 10

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


EXPLOSION_TEXTURE_COUNT = 60

class Fighter(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0

    def update(self):

        self.center_x += self.change_x
        self.center_y += self.change_y

# class Explosion(arcade.Sprite):
#     """ This class creates an explosion animation """
#
#     def __init__(self, texture_list):
#         super().__init__("explosion0000.png")
#
#         # Start at the first frame
#         self.current_texture = 0
#         self.textures = texture_list
#
#     def update(self):
#         # Update to the next frame of the animation. If we are at the end
#         # of our frames, then delete this sprite.
#         self.current_texture += 1
#         if self.current_texture < len(self.textures):
#             self.set_texture(self.current_texture)
#         else:
#             self.remove_from_sprite_lists()


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Star Wars")

        self.player_list = None
        self.tie_fighter_list = None
        self.bullet_list = None

        self.player_sprite = None
        self.score = 0
        self.health = 5

        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.BLACK)

        self.laser_sound = arcade.load_sound("laser.ogg")

        # self.explosion_texture_list = []
        #
        # for i in range(EXPLOSION_TEXTURE_COUNT):
        #
        #     texture_name = f"images/explosion{i:04d}.png"
        #
        #     self.explosion_texture_list.append(arcade.load_texture(texture_name))

    def setup(self):

        self.player_list = arcade.SpriteList()
        self.tie_fighter_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        # self.explosions_list = arcade.SpriteList()

        self.score = 0
        self.health = 5

        self.player_sprite = arcade.Sprite("millennium_falcon.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        for i in range(FIGHTER_COUNT):

            tie_fighter = Fighter("tie_fighter.png", SPRITE_SCALING_FIGHTER)
            tie_fighter.center_x = random.randrange(SCREEN_WIDTH)
            tie_fighter.center_y = 500
            tie_fighter.change_x = 2
            self.tie_fighter_list.append(tie_fighter)

    def on_draw(self):

        arcade.start_render()

        self.tie_fighter_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        # self.explosions_list.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

        output = f"Health: {self.health}"
        arcade.draw_text(output, 80, 20, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):

        self.player_sprite.center_x = x
        if self.player_sprite.right > SCREEN_WIDTH:
            self.player_sprite.right = SCREEN_WIDTH

        if self.player_sprite.left < 0:
            self.player_sprite.left = 0

    def on_mouse_press(self, x, y, button, modifiers):

        bullet = arcade.Sprite("laserBlue01.png", SPRITE_SCALING_LASER)

        bullet.angle = 90

        bullet.center_x = self.player_sprite.center_x
        bullet.bottom = self.player_sprite.top
        bullet.change_y = BULLET_SPEED

        self.bullet_list.append(bullet)

        if button == arcade.MOUSE_BUTTON_LEFT:
            arcade.play_sound(self.laser_sound)

    def update(self, delta_time):

        self.tie_fighter_list.update()
        self.bullet_list.update()
        self.player_list.update()
        # self.explosions_list.update()

        # Damage to fighter
        for bullet in self.bullet_list:

            hit_list = arcade.check_for_collision_with_list(bullet, self.tie_fighter_list)

            if len(hit_list) > 0:
                # explosion = Explosion(self.explosion_texture_list)
                # explosion.center_x = hit_list[0].center_x
                # explosion.center_y = hit_list[0].center_y
                # self.explosions_list.append(explosion)
                bullet.remove_from_sprite_lists()

            for tie_fighter in hit_list:
                tie_fighter.remove_from_sprite_lists()
                self.score += 1

            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()



        # Damage to Player
        for bullet in self.bullet_list:

            hit_list = arcade.check_for_collision_with_list(bullet, self.player_list)

            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            for self.player in hit_list:
                self.health -= 1

            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

        # Tie Fighter bullets
        for tie_fighter in self.tie_fighter_list:

            if random.randrange(200) == 0:
                bullet = arcade.Sprite("laserBlue01.png")
                bullet.center_x = tie_fighter.center_x
                bullet.angle = -90
                bullet.top = tie_fighter.bottom
                bullet.change_y = -6
                self.bullet_list.append(bullet)

        self.bullet_list.update()

        # done = False

        # while not done:
        #     if self.health == 0:
        #         done = True
        # print("You have lost")

        for fighter_1 in self.tie_fighter_list:
            if fighter_1.right > SCREEN_WIDTH and fighter_1.change_x > 0:
                for fighter_2 in self.tie_fighter_list:
                    fighter_2.change_x *= -1

        # for fighter_1 in self.tie_fighter_list:
        #     if fighter_1.left > 0:
        #         for fighter_2 in self.tie_fighter_list:
        #             fighter_2.change_x *= 1

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()