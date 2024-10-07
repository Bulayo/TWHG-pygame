from settings import *

class Player(pygame.sprite.Sprite):

    def __init__(self, groups, pos, image, wall_collision, ball_collision):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(topleft = (pos))
        self.original_pos = pos

        self.direction = pygame.Vector2(1, 0)
        self.speed = 230
        self.wall_collision = wall_collision
        self.ball_collision = ball_collision


    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        self.rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")

    def collision(self, direction):

        for sprite in self.wall_collision:
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left

                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right

                elif direction == "vertical":
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top


        for sprite in self.ball_collision:
            if sprite.rect.colliderect(self.rect):
                    self.rect.x = self.original_pos[0]
                    self.rect.y = self.original_pos[1]

    def update(self, dt):
        self.input()
        self.move(dt)