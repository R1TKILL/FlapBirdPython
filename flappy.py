import pygame, random

from pygame.locals import *
from sys import exit

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 700

JUMPS_SPEED = 12  # Pulo
GRAVITY = 1  # Gravidade
GAME_SPEED = 10  # Velocidade do jogo - (Canos, chão.)

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 60
PIPE_HEIGHT = 500

#Espaço entre os canos.
PIPE_GAP = 110

color_bird = ['blue', 'red', 'yellow']
select_bird = random.randint(0, 2)

# Estas classes herdando o pygame te oferece facilidades em sprites e objetos para o jogo.
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        # Classes que tem o pygame precisam chamar o construtor do pygame no inicio.
        pygame.sprite.Sprite.__init__(self)

        #Sons do voô.
        self.sound_up = pygame.mixer.Sound('../FlapBird/assets/audio/wing.wav')

        self.jump_speed = JUMPS_SPEED

        # Objetos que terão suas imagens cicladas no update
        self.images =\
        [
            pygame.image.load(f'../FlapBird/assets/sprites/{color_bird[select_bird]}bird-upflap.png'),
            pygame.image.load(f'../FlapBird/assets/sprites/{color_bird[select_bird]}bird-midflap.png'),
            pygame.image.load(f'../FlapBird/assets/sprites/{color_bird[select_bird]}bird-downflap.png')
        ]

        # O contador para alterar.
        self.current_image = 0

        '''Convert alpha ajuda na melhor interpretação dos bits transparentes em imagens no pygame
        útil para definir melhor colisões, não contando os bits transparentes, image rect nesse contexto
        não são variaveis, mas funções do construtor pygame, não alteralos o nome.'''

        # imagem inicial.
        self.image = pygame.image.load(f'../FlapBird/assets/sprites/{color_bird[select_bird]}bird-upflap.png').convert_alpha()
        #Faz uma mascara para colisão dos sprites.
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        # Posição das imagens fica no rect.
        self.rect[0] = SCREEN_WIDTH / 2 - 100
        self.rect[1] = SCREEN_HEIGHT / 2 + 50

        self.angle_down = -15

    # Toda classe que recebe o pygame junto com os outros métodos tem o update pra informar o pygame das sprites.
    def update(self, activaty_gravity):
        # Para cada update mudar a imagem.
        # Ao fianl ele pega o resto dessa divisão o fazendo receber o inicio.
        self.current_image = (self.current_image + 1) % 3
        # Mudando de fato.
        self.image = self.images[self.current_image]

        if self.rect[1] >= (SCREEN_HEIGHT - 120):
            activaty_gravity = False
            self.rect[1] = (SCREEN_HEIGHT - 120)

        if activaty_gravity:
            # 3 -  Aplicando a gravidade de volta para descer cada vez mais rapido.
            self.jump_speed += GRAVITY
            # 1 - Aplico seu corpo descendo.
            self.rect[1] += self.jump_speed
            self.angle_down -= 2

        # Invertendo o ângulo quando cair e voar.
        if self.jump_speed > 0:
            self.image = pygame.transform.rotate(self.image, self.angle_down)
        elif self.jump_speed < 0:
            self.image = pygame.transform.rotate(self.image, 10)

    # Para o pulo/voo do passaro.
    def jump(self):
        self.angle_down = 10
        # 2 - Aqui inverto a velocidade descendo para subir no pulo.
        self.jump_speed = -JUMPS_SPEED
        self.sound_up.play()


color_pipe = ['../FlapBird/assets/sprites/pipe-red.png', '../FlapBird/assets/sprites/pipe-green.png']
select_pipe = random.randint(0, 1)


#Classe dos canos.
class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(color_pipe[select_pipe]).convert_alpha()

        #Enlargando um pouco o cano para caber certo na tela
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        #Se o inverted for True o cano invert o eixo y ao contrário.
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            # 2 - Já ao contrário sua o altura menos sua posição y, para esconder.
            self.rect[1] = -(self.rect[3] - ysize)
        else:
            # 1 - O cano sera do tamanho da tela menos tamanho definido, para  aparecer.
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        #Vai se mover na velocidade do chão.
        self.rect[0] -= GAME_SPEED


class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('../FlapBird/assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        #O chão vai ser do tamnho da tela menos o seu tamanho.
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        #Rotacionando o chão para traz.
            self.rect[0] -= GAME_SPEED


#Método que fara o retorno do chão.
def out_screen(sprite):
   # Retorna a posição do sprite quando seu canto esquedo [0], for menor que sua própia largura.
    return sprite.rect[0] < -(sprite.rect[2])

#Função que vai gerar as posições para os canos.
def get_random_pipes(xpos):
    size = random.randint(160, 400)
    pipe = Pipe(False, xpos, size)

    #No invertido será o tamanho da tela - menos o cano de baixo mais um espaço definido.
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return ((pipe, pipe_inverted))


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

music_point = pygame.mixer.Sound('../FlapBird/assets/audio/point.wav')


# Sorteia o fundo.
wallaper = ['../FlapBird/assets/sprites/background-day.png', '../FlapBird/assets/sprites/background-night.png']
select_wallaper = random.choice(wallaper)

BACKGROUND = pygame.image.load(select_wallaper)
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

FORENGROUND = pygame.image.load('../FlapBird/assets/sprites/message.png')
FORENGROUND = pygame.transform.scale(FORENGROUND, ((SCREEN_WIDTH / 2 + 50), SCREEN_HEIGHT / 2))

GameOver_image = pygame.image.load('../FlapBird/assets/sprites/gameover.png')
GameOver_image = pygame.transform.scale(GameOver_image, ((SCREEN_WIDTH / 2 + 100), SCREEN_HEIGHT / 2 - 250))

# Grupo de sprites do tipo passaro, ajuda a gerenciar melhor os tipos de sprites pra jogo.
bird_group = pygame.sprite.Group()

ground_group = pygame.sprite.Group()
# Fazendo o loop infinito do chão.
for i in range(2):
    '''
    Na primeira iteração o i vale 0, recebendo a largura da tela,
    multiplicada por i que 0,fazendo-o ficar no começo, na segunda como
    o i vale 1, vai ficar atrás do primeiro chão.
    '''
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

FPS = pygame.time.Clock()


def GameOver():
    bird = Bird()
    bird_group.add(bird)

    sound_death = pygame.mixer.Sound('../FlapBird/assets/audio/die.wav')
    sound_death.play()

    while True:
        FPS.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    bird.kill()
                    menu()

        screen.blit(BACKGROUND, (0, 0))
        screen.blit(GameOver_image, (50, 250))


        pygame.display.update()


def game():
    bird = Bird()
    bird_group.add(bird)
    score = 0

    #Placar do jogo.
    textFormatScore = pygame.font.SysFont('NDS12', 40, True, False)

    pipe_group = pygame.sprite.Group()
    for i in range(2):
        # Pra não ter cano logo de cara.
        pipes = get_random_pipes(SCREEN_WIDTH * i + 450)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    # Som do impacto no chão.
    sound_collider_ground = pygame.mixer.Sound('../FlapBird/assets/audio/hit.wav')

    while True:
        FPS.tick(20)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    bird.jump()

        screen.blit(BACKGROUND, (0, 0))

        #Fazendo de fato o loop.
        #Se o primeiro chão ta fora da tela.
        if out_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0]) # 1 - Removo.
            new_ground = Ground(GROUND_WIDTH - 120) # Crio um novo jogando lá pra frente da tela.
            ground_group.add(new_ground) # E o adiciono no grupo do chão.

        #loop dos canos.
        if out_screen(pipe_group.sprites()[0]):
            #Remove os dois canos juntos que são essa posição no grupo.
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])

            new_pipes = get_random_pipes(SCREEN_WIDTH * 2 - 200)
            pipe_group.add(new_pipes[0])
            pipe_group.add(new_pipes[1])

            if (bird.rect[0] > (new_pipes[0].rect[2])):
                score += 1
                music_point.play()


        bird_group.update(True)  # Para atualizar o que aconteçe entre as imagens na tela.
        ground_group.update()
        pipe_group.update()

        # Onde vai desenhar esse grupo.
        ground_group.draw(screen)
        pipe_group.draw(screen)
        bird_group.draw(screen)

        #Vericando se houve colisão.
        #collide_mask, faz com que todos os pixes transparentes sejam desconsiderados nas colisões.
        if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask)) or \
           (pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
            sound_collider_ground.play()
            bird.kill()
            bird.update(False)
            GameOver()

        labelScore = f"{score}"
        formatScore = textFormatScore.render(labelScore, True, (255, 255, 255))

        screen.blit(formatScore, (170, 100))

        pygame.display.update()

def menu():
    bird = Bird()
    bird_group.add(bird)

    textFormatDeveloper = pygame.font.SysFont('NDS12', 20, True, False)
    labelDeveloper = "Developed by R1TKILL"
    formatDeveloper = textFormatDeveloper.render(labelDeveloper, True, (230, 0, 0))

    while True:
        FPS.tick(20)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:

                if event.key == K_SPACE:
                    bird.kill()
                    bird.jump()
                    game()

        screen.blit(BACKGROUND, (0, 0))
        screen.blit(FORENGROUND, (70, 150))

        if out_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDTH - 20)
            ground_group.add(new_ground)

        bird_group.update(False)
        ground_group.update()

        bird_group.draw(screen)
        ground_group.draw(screen)

        screen.blit(formatDeveloper, (95, 650))

        pygame.display.update()


menu()