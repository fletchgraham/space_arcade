import arcade
import random

WIDTH = 800
HEIGHT = 800
TITLE = 'Arcade Tutorial'
SCALE = .2

class TutorialWindow(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.enemies_list = arcade.SpriteList()
        self.asteroids_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()
        self.alive = True
        self.paused = False
        self.score = 0
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

        if self.paused or not self.alive:
            return

        if (
            self.player.collides_with_list(self.enemies_list)
            or self.player.collides_with_list(self.asteroids_list)
        ):
            self.alive = False
            

        self.all_sprites.update()

        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

        self.score += delta_time

    def on_draw(self):
        arcade.start_render()
        self.all_sprites.draw()
        
        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {int(self.score * 100) / 100}"
        arcade.draw_text(score_text, 10, 10,
                         arcade.csscolor.WHITE, 18)
        
        if not self.alive:
            arcade.draw_text('YOU DIED', 10, HEIGHT - 82,
                            arcade.csscolor.WHITE, 72)

    def on_key_press(self, symbol, modifiers):
        speed = 5
        if symbol == arcade.key.Q:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol == arcade.key.I or symbol == arcade.key.UP:
            self.player.change_y = speed

        if symbol == arcade.key.K or symbol == arcade.key.DOWN:
            self.player.change_y = -1 * speed

        if symbol == arcade.key.J or symbol == arcade.key.LEFT:
            self.player.change_x = -1 * speed

        if symbol == arcade.key.L or symbol == arcade.key.RIGHT:
            self.player.change_x = speed

    def on_key_release(self, symbol: int, modifiers: int):

        if (
            symbol == arcade.key.I
            or symbol == arcade.key.K
            or symbol == arcade.key.UP
            or symbol == arcade.key.DOWN
        ):
            self.player.change_y = 0

        if (
            symbol == arcade.key.J
            or symbol == arcade.key.L
            or symbol == arcade.key.LEFT
            or symbol == arcade.key.RIGHT
        ):
            self.player.change_x = 0

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