from settings import *
import pygame as pg
from tiles import AnimatedTile, StaticTile
from support import import_folder
from random import choice, randint

class Sky:
	def __init__(self,horizon,style = 'level'):
		self.top = pg.image.load('graphics/decoration/sky/sky_top.png').convert()
		self.bottom = pg.image.load('graphics/decoration/sky/sky_bottom.png').convert()
		self.middle = pg.image.load('graphics/decoration/sky/sky_middle.png').convert()
		self.horizon = horizon

		# stretch 
		self.top = pg.transform.scale(self.top,(WIDTH,TILESIZE))
		self.bottom = pg.transform.scale(self.bottom,(WIDTH,TILESIZE))
		self.middle = pg.transform.scale(self.middle,(WIDTH,TILESIZE))

		self.style = style
		if self.style == 'overworld':
			palm_surfaces = import_folder('graphics/overworld/palms')
			self.palms = []

			for surface in [choice(palm_surfaces) for image in range(10)]:
				x = randint(0,WIDTH)
				y = (self.horizon * TILESIZE) + randint(50,100)
				rect = surface.get_rect(midbottom = (x,y))
				self.palms.append((surface,rect))

			cloud_surfaces = import_folder('graphics/overworld/clouds')
			self.clouds = []

			for surface in [choice(cloud_surfaces) for image in range(10)]:
				x = randint(0,WIDTH)
				y = randint(0,(self.horizon * TILESIZE) - 100)
				rect = surface.get_rect(midbottom = (x,y))
				self.clouds.append((surface,rect))
				
	def draw(self,surface):
		for row in range(VERTICAL_TILE_NUMBER):
			y = row * TILESIZE
			if row < self.horizon:
				surface.blit(self.top,(0,y))
			elif row == self.horizon:
				surface.blit(self.middle,(0,y))
			else:
				surface.blit(self.bottom,(0,y))

		if self.style == 'overworld':
			for palm in self.palms:
				surface.blit(palm[0],palm[1])
			for cloud in self.clouds:
				surface.blit(cloud[0],cloud[1])

class Water:
	def __init__(self,top,level_width):
		water_start = -WIDTH
		water_tile_width = 192
		tile_x_amount = int((level_width + WIDTH * 2) / water_tile_width)
		self.water_sprites = pg.sprite.Group()

		for tile in range(tile_x_amount):
			x = tile * water_tile_width + water_start
			y = top
			sprite = AnimatedTile(water_tile_width,x,y,'graphics/decoration/water')
			self.water_sprites.add(sprite)

	def draw(self,surface,shift):
		self.water_sprites.update(shift)
		self.water_sprites.draw(surface)

class Clouds:
	def __init__(self,horizon,level_width,cloud_number):
		cloud_surf_list = import_folder('graphics/decoration/clouds')
		min_x = -WIDTH
		max_x = level_width + WIDTH
		min_y = 0
		max_y = horizon
		self.cloud_sprites = pg.sprite.Group()

		for cloud in range(cloud_number):
			cloud = choice(cloud_surf_list)
			x = randint(min_x,max_x)
			y = randint(min_y,max_y)
			sprite = StaticTile(0,x,y,cloud)
			self.cloud_sprites.add(sprite)

	def draw(self,surface,shift):
		self.cloud_sprites.update(shift)
		self.cloud_sprites.draw(surface)
