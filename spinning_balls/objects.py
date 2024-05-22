# Импорт модулей: math для математических функций
import math
# random для генерации случайных чисел
import random
# pygame для создания игры
import pygame

# Установка размеров экрана: WIDTH и HEIGHT задают размер экрана, CENTER вычисляет центр экрана
SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2

# Установка радиусов: Максимальный и минимальный радиус для кругов
MAX_RADIUS = 120
MIN_RADIUS = 90

# Конструктор: Инициализация атрибутов круга, загрузка изображения и получение прямоугольной области изображения
class Circle(pygame.sprite.Sprite):
	def __init__(self, i):
		super(Circle, self).__init__()
		self.i = i
		self.base = 0
		self.radius = 0
		self.theta = 0
		self.angle = 0

		self.dt = 1
		self.rotate = True
		self.max_rotation = 30
		self.complete = False
		self.shrink = False

		self.image = pygame.image.load('Images/circle.png')
		self.rect = self.image.get_rect()

	# Метод update: Обновляет состояние круга. Управляет радиусом, углом поворота и положением в зависимости от текущего состояния круга
	def update(self, shrink):
		self.shrink = shrink

		if not self.complete:
			if self.radius < MAX_RADIUS:
				self.radius += 5
			if self.radius == MAX_RADIUS:
				if self.theta < 30:
					self.theta += 1
				else:
					self.complete = True
			self.angle = (self.base + self.i * self.theta) * math.pi / 180

		if self.complete:
			if self.shrink:
				self.radius -= 1
				if self.radius < MIN_RADIUS:
					self.radius = MIN_RADIUS
			else:
				self.radius += 1
				if self.radius > MAX_RADIUS:
					self.radius = MAX_RADIUS

			if self.rotate and self.radius in (MAX_RADIUS, MIN_RADIUS):
				if abs(self.base) > self.max_rotation:
					self.base = 0
					self.rotate = False
				
				self.base += self.dt
				self.angle += math.radians(self.dt)

		self.x = math.cos(self.angle) * self.radius + CENTER[0]
		self.y = math.sin(self.angle) * self.radius + CENTER[1]

		self.rect = self.image.get_rect(center=(self.x, self.y))
		self.mask = pygame.mask.from_surface(self.image)

	# Метод draw: Рисует круг на экране
	def draw(self, win):
		win.blit(self.image, self.rect)

# Конструктор: Инициализирует игрока, загружает его изображение и получает прямоугольную область изображения
class Player():
	def __init__(self):
		self.reset()

		self.image = pygame.image.load('Images/player.png')
		self.rect = self.image.get_rect()

	# Метод reset: Сбрасывает состояние игрока к начальным значениям.
	def reset(self):
		self.radius = 30
		self.theta = 0
		self.rotate = True
		self.speed = 5
		self.dr = self.speed
		self.alive = True

	# Метод update: Обновляет состояние игрока. Управляет радиусом, углом поворота и положением в зависимости от текущего состояния игрока
	def update(self, rotate):
		if not rotate:
			self.rotate = False
		if self.rotate:
			self.theta = (self.theta + 2 ) % 360
		else:
			self.radius += self.dr
			if self.radius <= 30:
				self.dr *= -1
				self.rotate = True

		angle = self.theta * math.pi / 180
		self.x = math.cos(angle) * self.radius + CENTER[0]
		self.y = math.sin(angle) * self.radius + CENTER[1]

		self.rect = self.image.get_rect(center=(self.x, self.y))
		self.mask = pygame.mask.from_surface(self.image)

	# Метод draw: Рисует игрока на экране
	def draw(self, win):
		win.blit(self.image, self.rect)

# Конструктор: Инициализирует объект игрок с фиксированным радиусом
class Dot():
	def __init__(self):
		self.radius = 8

	# Метод update: Обновляет положение и рисует точку на экране
	def update(self, x, y, win, color):
		pygame.draw.circle(win, color, (x, y), self.radius)

# Конструктор: Инициализирует снежинку, загружает изображение, если оно предоставлено, или создает поверхность, если изображение отсутствует
class Leaf(pygame.sprite.Sprite):
	def __init__(self, x, y, image=None):
		super(Leaf, self).__init__()

		self.color = (128, 128, 128)
		self.speed = 3
		self.angle = 0

		self.side = random.randint(15, 40)
		self.image = None
		if image:
			self.image = pygame.image.load(image)
			self.image = pygame.transform.scale(self.image, (self.side, self.side))
			self.rect = self.image.get_rect(center=(x, y))
		else:
			self.surface = pygame.Surface((self.side, self.side), pygame.SRCALPHA)
			self.surface.set_colorkey((20,20,20))
			self.rect = self.surface.get_rect(center=(x, y))

	# Метод update: Обновляет состояние снежинки, вращает ее, изменяет положение и удаляет ее, если она выходит за пределы экрана
	def update(self, win):
		center = self.rect.center
		self.angle = (self.angle + self.speed) % 360
		if self.image:
			image = pygame.transform.rotate(self.image , self.angle)
			self.rect.x += random.randint(-1, 1)
		else:
			image = pygame.transform.rotate(self.surface , self.angle)
		self.rect = image.get_rect()
		self.rect.center = center

		self.rect.y += 1.5

		if self.rect.top >= HEIGHT:
			self.kill()

		if not self.image:
			pygame.draw.rect(self.surface, self.color, (0,0, self.side, self.side), 4)
		win.blit(image, self.rect)

# Конструктор: Инициализирует частицу, задает начальные координаты, цвет, скорость и срок жизни
class Particle(pygame.sprite.Sprite):
	def __init__(self, x, y, color, win):
		super(Particle, self).__init__()
		self.x = x
		self.y = y
		self.color = color
		self.win = win
		self.size = random.randint(4,7)
		xr = (-3,3)
		yr = (-3,3)
		f = 26
		self.life = 40
		self.x_vel = random.randrange(xr[0], xr[1]) * f
		self.y_vel = random.randrange(yr[0], yr[1]) * f
		self.lifetime = 0

	# Метод update: Обновляет состояние частицы, уменьшает размер, изменяет положение и удаляет частицу, если срок жизни истек
	def update (self):
		self.size -= 0.1
		self.lifetime += 1
		if self.lifetime <= self.life:
			self.x += self.x_vel
			self.y += self.y_vel
			s = int(self.size)
			pygame.draw.rect(self.win, self.color, (self.x, self.y,s,s))
		else:
			self.kill()

# Конструктор: Инициализирует карточку счета, загружает шрифт и создает изображения для текста и тени
class Score:
	def __init__(self, x, y, size, style, color,  win):
		self.size = size
		self.color = color
		self.win = win

		self.inc = 1
		self.animate = False
		
		self.style = style
		self.font= pygame.font.Font(self.style, self.size)

		self.image = self.font.render("0", True, self.color)
		self.rect = self.image.get_rect(center=(x,y))
		self.shadow_rect = self.image.get_rect(center=(x+2, y+2))

	# Метод update: Обновляет текст счета и рисует его на экране вместе с тенью
	def update(self, score):
		if self.animate:
			self.size += self.inc
			self.font = pygame.font.Font(self.style, self.size)
			if self.size <= 50 or self.size >= 55:
				self.inc *= -1
				
			if self.size == 50:
				self.animate = False
		self.image = self.font.render(f"{score}", False, self.color)
		shadow = self.font.render(f"{score}", True, (54, 69, 79))
		
		self.win.blit(shadow, self.shadow_rect)
		self.win.blit(self.image, self.rect)

# Конструктор: Инициализирует сообщение, создает изображения для текста и тени
class Message:
	def __init__(self, x, y, size, text, font, color, win):
		self.win = win
		self.color = color
		self.x, self.y = x, y
		if not font:
			self.font = pygame.font.SysFont("Verdana", size)
			anti_alias = True
		else:
			self.font = pygame.font.Font(font, size)
			anti_alias = False
		self.image = self.font.render(text, anti_alias, color)
		self.rect = self.image.get_rect(center=(x,y))
		if self.color == (200, 200, 200):
				self.shadow_color = (255, 255, 255)
		else:
			self.shadow_color = (54,69,79)
		self.shadow = self.font.render(text, anti_alias, self.shadow_color)
		self.shadow_rect = self.image.get_rect(center=(x+2,y+2))

	# Метод update: Обновляет текст сообщения и рисует его на экране вместе с тенью
	def update(self, text=None, color=None, shadow=True):
		if text:
			if not color:
				color = self.color
			self.image = self.font.render(f"{text}", False, color)
			self.rect = self.image.get_rect(center=(self.x,self.y))
			self.shadow = self.font.render(f"{text}", False, self.shadow_color)
			self.shadow_rect = self.image.get_rect(center=(self.x+2,self.y+2))
		if shadow:
			self.win.blit(self.shadow, self.shadow_rect)
		self.win.blit(self.image, self.rect)

# Конструктор: Инициализирует кнопку, загружает изображение, масштабирует его и устанавливает координаты
class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()
		
		self.scale = scale
		self.image = pygame.transform.scale(img, self.scale)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

	# Метод update_image: Обновляет изображение кнопки
	def update_image(self, img):
		self.image = pygame.transform.scale(img, self.scale)

	# Метод draw: Рисует кнопку на экране и проверяет нажатие кнопки мыши. Возвращает True, если кнопка была нажата.
	def draw(self, win):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False

		win.blit(self.image, self.rect)
		return action

# Конструктор: Наследует все атрибуты и методы класса Message, добавляет индекс и флаг для отображения текста
class BlinkingText(Message):
	def __init__(self, x, y, size, text, font, color, win):
		super(BlinkingText, self).__init__(x, y, size, text, font, color, win)
		self.index = 0
		self.show = True

	# Метод update: Обновляет состояние текста, чередует его отображение и рисует его на экране, если show равно True
	def update(self):
		self.index += 1
		if self.index % 40 == 0:
			self.show = not self.show

		if self.show:
			self.win.blit(self.image, self.rect)