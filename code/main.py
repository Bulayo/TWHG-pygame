from settings import *
from player import Player
from sprites import *
from random import randint
from pytmx.util_pygame import load_pygame

class Game:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.WINDOW = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption("The World's Hardest Game Pygame")
        self.clock = pygame.time.Clock()

        # Sound
        theme_music = pygame.mixer.Sound(join("sound", "music.mp3"))
        theme_music.set_volume(0.5)
        theme_music.play(loops= -1)

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.ball_sprites = pygame.sprite.Group()

        # Current Level
        self.current_level = 1
        self.map = load_pygame(join("data", f"level{self.current_level}.tmx"))


        self.limit_spawn = 0        
        self.running = True


    def run(self):

        while self.running:
            dt = self.clock.tick(60) / 1000
            
            if self.limit_spawn > 1:
                self.limit_spawn = 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.current_level -= 1
                        self.limit_spawn -= 1
                        self.all_sprites.empty()
                        self.ball_sprites.empty()
                        self.collision_sprites.empty()
                    
                    elif event.key == pygame.K_e:
                        self.current_level += 1
                        self.limit_spawn -= 1
                        self.all_sprites.empty()
                        self.ball_sprites.empty()
                        self.collision_sprites.empty()

            # update
            self.all_sprites.update(dt)
            if self.limit_spawn < 1:
                self.level_setup()
            
            # draw
            self.WINDOW.fill("#B4B5FE")
            self.all_sprites.draw(self.WINDOW)

            pygame.display.flip()

            self.limit_spawn += 1

        pygame.mixer.quit()
        pygame.quit()


    def level_setup(self):
        
        self.map = load_pygame(join("data", f"level{self.current_level}.tmx"))

        for x, y, image in self.map.get_layer_by_name("Walls").tiles():
            Collision_Sprite((self.all_sprites, self.collision_sprites), (x * TILE_SIZE, y * TILE_SIZE), image)

        for x, y, image in self.map.get_layer_by_name("Floor").tiles():
            Sprites((self.all_sprites), (x * TILE_SIZE, y * TILE_SIZE), image)

        for x, y, image in self.map.get_layer_by_name("Start").tiles():
            Sprites((self.all_sprites), (x * TILE_SIZE, y * TILE_SIZE), image)

        for x, y, image in self.map.get_layer_by_name("End").tiles():
            Sprites((self.all_sprites), (x * TILE_SIZE, y * TILE_SIZE), image)
        
        for i, (x, y, image) in enumerate(self.map.get_layer_by_name("Blue_Balls").tiles()):
            Ball_Sprite((self.all_sprites, self.ball_sprites), (x * TILE_SIZE + 8, y * TILE_SIZE + 8), pygame.transform.scale(image, (32, 32)), i % 2 + 1, "blue",self.collision_sprites)
        
        for i, (x, y, image) in enumerate(self.map.get_layer_by_name("Red_Balls").tiles()):
            Ball_Sprite((self.all_sprites, self.ball_sprites), (x * TILE_SIZE + 8, y * TILE_SIZE + 8), pygame.transform.scale(image, (32, 32)), i % 2 + 1, "red",self.collision_sprites)

        for x, y, image in self.map.get_layer_by_name("Player").tiles():
            Player(self.all_sprites, (x * TILE_SIZE, y * TILE_SIZE), image, self.collision_sprites)
        
        for obj in self.map.get_layer_by_name("Coins"):
            Sprites((self.all_sprites), (obj.x, obj.y), pygame.transform.scale(obj.image, (32, 32)))


        
        
if __name__ == "__main__":
    game = Game()
    game.run()