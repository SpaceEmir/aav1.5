from pygame import *
import random

init()

level = 1

# GAMESPRITE CLASS

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, vx, vy, x=60, y=60, angle=0, do=False):
        super().__init__()

        self.original_image = transform.scale(image.load(player_image), (x, y))
        self.image = self.original_image

        self.angle = angle
        self.vx = vx
        self.vy = vy

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

        self.width = x
        self.height = y

        self.rspeed = random.randint(-3, 3)
        self.img_name = player_image

        if do:
            self.rect = self.image.get_rect(center=(size[0]//2, size[1]//2))

    def rotate(self, amount):
        self.angle += amount

        center = self.rect.center
        self.image = transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=center)
    
    def resize(self, x, y):
        center = self.rect.center
        self.original_image = transform.scale(image.load(self.img_name), (x, y))
        self.image = transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=center)
        self.width = x
        self.height = y
    
    def photo(self, img):
        center = self.rect.center
        self.original_image = transform.scale(image.load(img), (self.width, self.height))
        self.image = transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=center)
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# ASTEROID CLASS

class Asteroid(GameSprite):
    def zerteilen(self, n):
        if self.width in [30, 25]:
            asteroids.remove(self  )
            self.kill()

        else:
            self.resize(self.width // 2, self.height // 2)
            asteroid = Asteroid(asteroid_photo, 0, 0, 0, 0, x=30, y=30)
            asteroid.start(do=(self.rect. x + 30, self.rect.y + 30))
            asteroids.add(asteroid)

    def start(self, do=None):
        self.vx = random.randint(1, level + 1)
        self.vy = random.randint(1, level + 1)

        if do == None:
            choice = random.randint(0, 3)

            if choice == 0:
                self.rect.x = 0
                self.rect.y = random.randint(5, size[1] - 5)
        
            if choice == 1:
                self.rect.y = 0
                self.rect.x = random.randint(5, size[0] - 5)
            
            if choice == 2:
                self.rect.y = size[1]
                self.rect.x = random.randint(5, size[0] - 5)

            if choice == 3:
                self.rect.x= size[0]
                self.rect.y=random.randint(5, size[1])
            
            w = random.choice([30, 60, 100])
            self.resize(w, w)
        
        else:
            self.rect.y = do[1]
            self.rect.x = do[0]
        
    def controls(self):
        global lived

        if self.rect.y >= size[1] - self.width // 2:
            self.start(do=(self.rect.x, 0))
        
        if self.rect.y <= self.width // 2:
            self.start(do=(self.rect.x, self.rect.y))

        if self.rect.x >= size[0] - self.height // 2:
            self.start(do=(0, self.rect.y))
        
        if self.rect.x <= self.height // 2:
            self.start(do=(self.rect.x, self.rect.y))

    def update(self):
        self.controls()
        self.rect.x += self.vx
        self.rect.y += self.vy

# PLAYER CLASS

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, vx, vy, x=60, y=60, angle=0):
        super().__init__(player_image, player_x, player_y, vx, vy, x, y, angle)

        self.normal_image = transform.scale(image.load(player_photo), (x, y))
        self.fire_image = transform.scale(image.load("feuer.png"), (x, y))

    def set_photo(self, img):
        center = self.rect.center
        self.original_image = img
        self.image = transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=center)

    def start(self):
        self.rect.x = size[0] // 2
        self.rect.y = size[1] // 2
        self.speed = 4 * level
        self.lives = 3
    
    def controls(self):
        if self.rect.x > size[0]:
            self.rect.x = 0
        
        if self.rect.x < 0:
            self.rect.x = size[0]
        
        if self.rect.y > size[1]:
            self.rect.y = 0
        
        if self.rect.y < 0:
            self.rect.y = size[1]

    def move(self):
        global bullet_cooldown
        keys = key.get_pressed()

        if keys[K_RIGHT]:
            self.rotate(-10)
        
        if keys[K_LEFT]:
            self.rotate(10)

        moving = False

        if keys[K_UP]:
            import math

            rad = math.radians(self.angle)

            self.vx = -math.sin(rad) * self.speed
            self.vy = -math.cos(rad) * self.speed

            self.rect.x += self.vx
            self.rect.y += self.vy
            moving = True

        if moving:
            self.set_photo(self.fire_image)
        else:
            self.set_photo(self.normal_image)
        
        if keys[K_a]:
            self.rotate(-5)
        
        if keys[K_d]:
            self.rotate(5)

        if keys[K_SPACE]:
            if bullet_cooldown == 0:
                player.fire()
                bullet_cooldown += 1
 
    def update(self):
        self.move()
        self.controls()
    
    def fire(self):
        import math

        speed = 8 + level * 2

        rad = math.radians(self.angle)

        vx = -math.sin(rad) * speed
        vy = -math.cos(rad) * speed

        bullet = Bullet(ufo_bullet_photo, 0, 0, 0, 0, x=10, y=10)
        bullet.start(
            vx,
            vy,
            self.rect.centerx + vx * 4,
            self.rect.centery + vy * 4
        )
        bullets.add(bullet)

# BULLET CLASS

class Bullet(GameSprite):
    def start(self, vx, vy, x, y):
        self.vx = vx
        self.vy = vy
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
       
class UFO(GameSprite):
    def __init__(self, player):
        super().__init__(UFO_photo, 0, 0, 0, 0, do=False)
        self.player = player
        self.angle = 0  # Initialer Winkel

    def start(self, do=None):
        self.vx = random.randint(1, level + 1) / 2
        self.vy = random.randint(1, level + 1) / 2
        if do is None:
            choice = random.randint(0, 3)
            if choice == 0:
                self.rect.x = 0
                self.rect.y = random.randint(5, size[1] - 5)
            elif choice == 1:
                self.rect.y = 0
                self.rect.x = random.randint(5, size[0] - 5)
            elif choice == 2:
                self.rect.y = size[1]
                self.rect.x = random.randint(5, size[0] - 5)
            elif choice == 3:
                self.rect.x = size[0]
                self.rect.y = random.randint(5, size[1])
        else:
            self.rect.x = do[0]
            self.rect.y = do[1]

    def controls(self):
        if self.rect.y >= size[1] + self.height // 2:
            self.rect.y = -self.height // 2
        if self.rect.y <= -self.height // 2:
            self.rect.y = size[1] + self.height // 2
        if self.rect.x >= size[0] + self.width // 2:
            self.rect.x = -self.width // 2
        if self.rect.x <= -self.width // 2:
            self.rect.x = size[0] + self.width // 2

    def turn(self):
        import math
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        # Winkel in Grad berechnen (für die Rotation des Bildes)
        self.angle = math.degrees(math.atan2(-dy, dx))
        # Bild rotieren (UFO-Bild zeigt standardmäßig nach unten, daher -90°)
        self.image = transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def fire(self, bullet_group, bullet_img):
        import math
        speed = 8
        # WICHTIG: Denselben Winkel wie in turn() verwenden (inkl. -90°)
        angle_rad = math.radians(self.angle - 90)
        vx = -math.sin(angle_rad) * speed
        vy = -math.cos(angle_rad) * speed
        bullet = Bullet(bullet_img, 0, 0, 0, 0, x=10, y=10)
        bullet.start(vx, vy, self.rect.centerx, self.rect.centery)
        bullet_group.add(bullet)

    def update(self):
        self.controls()
        self.turn()
        # Bewegung zum Spieler
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        dist = (dx**2 + dy**2)**0.5
        if dist > 0:
            self.rect.x += (dx / dist) * self.vx
            self.rect.y += (dy / dist) * self.vy
        # Schießen
        if waiting % (FPS // level) == 0:
            self.fire(ufo_bullets, bullet_photo)

# SETTINGS

# Window settings

caption = "SPACE GAME"
size = (1920, 1080)

# Photo settings

player_photo = "rocket.png"
asteroid_photo = "asteroid.png"
background_photo = "background.png"
bullet_photo = "bullet.png"
ufo_bullet_photo = "ufo_bullet.png"
UFO_photo = "UFO.png"

# Game-in settings

num_asteroids = 30 + level ** 2
num_ufos = 2 ** (level -1)
game = True

FPS = 32
clock = time.Clock()

points = 0
num_clicks = 0

bullet_cooldown = 0
limit = FPS // 2

on = True

waiting = 0

# Font settings

lose_show = False
win_show = False

font_size = 100

# Time settings

counter = 0
start = 0
wait_time = 3 # s

# Music settings

mixer.init()

mixer.music.load("spacemusic.wav")
mixer.music.play(-1)

game_over = mixer.Sound("game_over.wav")

# HILFSFUNKTIONEN

def update_asteroid_num():
    asteroids.empty()
    global free
    
    free = list(range(1, size[0]))

    for i in range(num_asteroids):
        asteroid = Asteroid(asteroid_photo, 0, 0, 0, 0)
        asteroid.start()
        asteroids.add(asteroid)

def update_ufo_num():
    ufos.empty()

    for i in range(num_ufos):
        ufo = UFO(player)
        ufo.start()
        ufos.add(ufo)

def add_ast(num):
    for i in range(num):
        ast = Asteroid(asteroid_photo, 0, 0, 0, 0)
        ast.start()
        asteroids.add(ast)

def LOSE():
    global lose_show, start, lived, lose, points, num_clicks, on
    lose = font1.render(f"GAME OVER!", True, (255, 0, 0))
    point_show = font1.render(f"""             {points} POINTS,
Hold SPACE to play again.""", True, (255, 255, 0))
    
    if on:
        window.blit(lose, (size[0] //2-250,size[1] // 2-300))
    window.blit(point_show, (size[0] //2-250 - 250, size[1] // 2 + 100 -200))

    if start == 0:
        game_over.play()

    keys = key.get_pressed()
    if keys[K_SPACE]:
        num_clicks += 1
    
    if num_clicks == 3:
        points = 0
        lose_show = False
        start = 0
        num_clicks = 0
        update_asteroid_num()
        update_ufo_num()
        bullets.empty()
        ufo_bullets.empty()
            
        player.start()

    if start % (FPS // 2) == 0:
        if on:
            on = False
        
        else:
            on = True
    
    if start % (FPS*3) == 0:
        game_over.play()
    
    start += 1

def events_control():
    global game, bullet_cooldown

    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game = False

def game_in_controls():
    global lose_show

    for asteroid in asteroids:
        small_rect = asteroid.rect.inflate(-30, -30)

        if small_rect.colliderect(player.rect):
            lose_show = True
        
        asteroid.rotate(asteroid.rspeed)

def update_all():
    asteroids.update()
    bullets.update()
    ufos.update()
    ufo_bullets.update()
    player.update()

def draw_all():
    asteroids.draw(window)
    bullets.draw(window)
    ufos.draw(window)
    ufo_bullets.draw(window)
    player.reset()

def main_controls():
    global points, win_show, lose_show
    events_control()

    if not lose_show:
        update_all()
        game_in_controls()

    if len(asteroids) < 20:
        add_ast(10)
    
    hits = sprite.groupcollide(asteroids, bullets, False, True)

    for asteroid in hits:
        for bullet in hits[asteroid]:
            bullets.remove(bullet)
            bullet.kill()
        if asteroid.width in [30, 25]:
            points += 15
        
        elif asteroid.width in [60, 50]:
            points += 10

        else:
            points += 5
        n = 1
        if asteroid.width == 30:
            n=2

        asteroid.zerteilen(n)
    
    hits = sprite.groupcollide(asteroids, ufo_bullets, False, True)

    for asteroid in hits:
        for bullet in hits[asteroid]:
            bullets.remove(bullet)
            bullet.kill()
        if asteroid.width in [30, 25]:
            points += 15
        
        elif asteroid.width in [60, 50]:
            points += 10

        else:
            points += 5
        n = 1
        if asteroid.width == 30:
            n=2

        asteroid.zerteilen(n)
    
    for b in ufo_bullets:
        if sprite.collide_rect(b, player):
            lose_show = True

def main():
    global counter, bullet_cooldown
    window.blit(background, (0, 0))
    main_controls()
    if not lose_show:
        draw_all()
    
    if lose_show:
        LOSE()

    display.update()
    clock.tick(FPS)

    counter += 1
    if bullet_cooldown > 0:
        bullet_cooldown += 1
    
    if bullet_cooldown == limit:
        bullet_cooldown = 0


# FENSTER ERSTELLEN

window = display.set_mode(size)
display.set_caption(caption)

# TEXTS

# Fonts

font.init()

font1 = font.Font(None, font_size)

# Labels
lose = font1.render("GAME OVER!", True, (255, 0, 0))

# SPRITES

# Asteroiden

asteroids = sprite.Group()

for i in range(0):
    asteroid = Asteroid(asteroid_photo, 0, 0, 0, 0)
    asteroid.start()
    asteroids.add(asteroid)


# Bullets
bullets = sprite.Group()
ufo_bullets = sprite.Group()

# Player

player = Player(player_photo, 0, 0, 0, 0)
player.start()

# UFOs

ufos = sprite.Group()

update_ufo_num()

# Background

background = transform.scale(
    image.load(background_photo),
    size
)

# GAME LOOP

while game:
    main()
    waiting += 1