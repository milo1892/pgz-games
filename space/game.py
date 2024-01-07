from pygame.time import get_ticks

WIDTH = 480
HEIGHT = 600
TITLE = '---=== SPACE INVADERS ===---'

class Cannon(Actor):
    def __init__(self, sprite, position):
        super(Cannon, self).__init__(sprite, position)
        self.speed = 5
        self.last_fire = 0
        self.firing_interval = 300
        self.score = 0

    def move_right(self):
        self.x += self.speed
        if self.right >= WIDTH - 40:
            self.right = WIDTH - 40

    def move_left(self):
        self.x -= self.speed
        if self.left <= 40:
            self.left = 40

class Bullet(Actor):
    def __init__(self, sprite, position):
        super(Bullet, self).__init__(sprite, position)
        self.speed = 20

    def update(self):
        self.y -= self.speed

    def is_dead(self):
        return self.bottom <= 0

class Alien(Actor):
    def __init__(self, sprite, position):
        super(Alien, self).__init__(sprite, position)
        self.movement = 20
        self.max_movement = 40
        self.x_speed = 1
        self.y_speed = 7
        self.lives = 3

    def update(self):
        self.x += self.x_speed
        self.movement += self.x_speed
        if abs(self.movement) >= self.max_movement:
            self.x_speed *= -1
            self.y += self.y_speed
            self.movement = 0

    def is_dead(self):
        return self.lives == 0

cannon = Cannon('cannon', (WIDTH / 2, 560))
bullets = []
aliens = []

alien_x = 60
alien_y = 40
for i in range(5):
    for i in range(7):
        aliens.append(Alien('alien', (alien_x, alien_y)))
        alien_x += 60
    alien_x = 60
    alien_y += 40

def update():
    if keyboard.right:
        cannon.move_right()
    elif keyboard.left:
        cannon.move_left()

    if keyboard.space:
        if get_ticks() - cannon.last_fire > cannon.firing_interval:
            bullets.append(Bullet('bullet', cannon.pos))
            sounds.shot.play()
            cannon.last_fire = get_ticks()

    for bullet in bullets[:]:
        bullet.update()
        if bullet.is_dead():
            bullets.remove(bullet)

    for alien in aliens[:]:
        alien.update()
        for bullet in bullets[:]:
            if alien.colliderect(bullet):
                alien.lives -= 1
                if alien.is_dead():
                    aliens.remove(alien)
                    sounds.explosion.play()
                    cannon.score += 100
                bullets.remove(bullet)

def draw():
    screen.clear()
    cannon.draw()

    for bullet in bullets:
        bullet.draw()

    for alien in aliens:
        alien.draw()

    screen.draw.text("SCORE: %d" % cannon.score, (20, 20), fontname="space_invaders", fontsize=20)
