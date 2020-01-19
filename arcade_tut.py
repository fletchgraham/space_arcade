import arcade
import random

WIDTH = 800
HEIGHT = 600
TITLE = 'Arcade Tutorial'
SCALE = .2

class TutorialWindow(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.enemies_list = arcade.SpriteList()
        self.asteroids_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()
        self.setup()


    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)

        self.player = arcade.Sprite("images/jet.png", SCALE)
        self.player.center_x = self.width / 2
        self.player.bottom = 10
        self.all_sprites.append(self.player)

        arcade.schedule(self.add_enemy, .25)
        arcade.schedule(self.add_asteroid, 1.0)

    def add_enemy(self, delta_time: float):
        enemy = FlyingSprite('images/enemy.png', SCALE / 2)
        enemy.top = random.randint(self.height + 40, self.height + 80)
        enemy.left = random.randint(10, self.width - 10)
        enemy.velocity = (0, random.randint(-8, -6))
        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)

    def add_asteroid(self, delta_time: float):
        asteroid = FlyingSprite('images/asteroid.png', SCALE)
        asteroid.top = random.randint(self.height + 40, self.height + 80)
        asteroid.left = random.randint(10, self.width - 10)
        asteroid.velocity = (0, random.randint(-3, -1))
        self.asteroids_list.append(asteroid)
        self.all_sprites.append(asteroid)

    def on_update(self, delta_time: float):
        self.all_sprites.update()

    def on_draw(self):
        arcade.start_render()
        self.all_sprites.draw()

class FlyingSprite(arcade.Sprite):

    def update(self):

        # Move the sprite
        super().update()

        # Remove if off the screen
        if self.right < 0:
            self.remove_from_sprite_lists()
        

if __name__ == '__main__':
    app = TutorialWindow(WIDTH, HEIGHT, TITLE)
    arcade.run()