from settings import *

class Collision_Sprite(pygame.sprite.Sprite):

    def __init__(self, groups, pos, image):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(topleft = pos)

class Ball_Sprite(pygame.sprite.Sprite):

    def __init__(self, groups, pos, image, state, ball_type, collision_sprite):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(topleft = pos)

        if ball_type == "blue":
            self.direction = pygame.Vector2(1, 0)
        if ball_type == "red":
            self.direction = pygame.Vector2(0, 1)

        self.speed = 500
        self.state = state
        self.ball_type = ball_type
        self.collision_sprite = collision_sprite

    
    def update(self, dt):

        if self.ball_type == "blue":
            for sprite in self.collision_sprite:
                if sprite.rect.colliderect(self.rect):
                    if self.rect.left < sprite.rect.right and self.rect.right > sprite.rect.right:
                        self.rect.left = sprite.rect.right

                    elif self.rect.right > sprite.rect.left  and self.rect.left < sprite.rect.left:
                        self.rect.right = sprite.rect.left

                    self.direction.x *= -1

            if self.state % 2 == 0:
                self.rect.center += self.direction * self.speed * dt

            else:
                self.rect.center -= self.direction * self.speed * dt

        if self.ball_type == "red":
            for sprite in self.collision_sprite:
                if sprite.rect.colliderect(self.rect):
                    if self.rect.top < sprite.rect.bottom and self.rect.bottom > sprite.rect.bottom:
                        self.rect.top = sprite.rect.bottom

                    elif self.rect.bottom > sprite.rect.top and self.rect.top < sprite.rect.top:
                        self.rect.bottom = sprite.rect.top
                    self.direction.y *= -1

            if self.state % 2 == 0:
                self.rect.center += self.direction * self.speed * dt

            else:
                self.rect.center -= self.direction * self.speed * dt

        

class Sprites(pygame.sprite.Sprite):

    def __init__(self, groups, pos, image):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(topleft = (pos))
        
