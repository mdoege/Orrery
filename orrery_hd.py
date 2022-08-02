#!/usr/bin/env python

# High-res Python orrery

import pygame
import time, math, os.path
import orrp

RES  = 950      # internal resolution
SRES = 950      # window size
ANIM_SPEED = 4  # animation speed factor

pic = (
"sun.png",
"mercury.png",
"venus.png",
"earth.png",
"mars.png",
"jupiter.png",
"saturn.png",
"uranus.png",
"neptune.png",
)

# planet mean solar distances in AU
pdist = (.387, .723, 1, 1.524, 5.205, 9.576, 19.281, 30.142)

pic2 = []
for n, p in enumerate(pic):
	img = pygame.image.load(os.path.join("img", p))
	pic2.append(img)

class Orr:
	def __init__(s):
		pygame.init()
		s.res = SRES, SRES
		s.screen = pygame.display.set_mode(s.res, pygame.RESIZABLE)
		pygame.display.set_caption('Orrery')
		s.clock = pygame.time.Clock()
		s.dazz = pygame.Surface((RES, RES))
		s.plusDays = 0
		s.anim = False        # animate view?
		s.anim_start = 0
		s.old_offset = -1e6
		s.dist = False        # use true distance?
		s.zoom = 7            # default zoom level (= Neptune orbit)

	def events(s):
		for event in pygame.event.get():
			if event.type == pygame.QUIT: s.running = False
			if event.type == pygame.VIDEORESIZE:
				s.res = event.w, event.h
				s.screen = pygame.display.set_mode(s.res, pygame.RESIZABLE)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
				s.plusDays += 1
			if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
				s.plusDays -= 1

			if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
				s.plusDays += 30
			if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
				s.plusDays -= 30

			if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
				s.plusDays += 365
			if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
				s.plusDays -= 365

			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				s.plusDays = 0

			if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
				s.anim = not s.anim
				if s.anim:
					s.anim_start = time.time()
				else:
					s.plusDays += ANIM_SPEED * (time.time() - s.anim_start)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
				s.dist = not s.dist
			if event.type == pygame.KEYDOWN and event.key == pygame.K_PLUS:
				s.zoom -= 1
				s.zoom = max(0, min(s.zoom, 7))
			if event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
				s.zoom += 1
				s.zoom = max(0, min(s.zoom, 7))

	def run(s):
		s.running = True
		while s.running:
			s.clock.tick(50)
			s.events()
			s.update()
		pygame.quit()

	def update(s):
		s.dazz.fill((0, 0, 0))
		WIDTH, HEIGHT = RES, RES
		PL_CENTER = (int(WIDTH / 2), int(WIDTH / 2))
		seconds_absolute = time.time()
		plusDays = 0
		if s.anim:
			ani = ANIM_SPEED * (time.time() - s.anim_start)
		else:
			ani = 0
		offset = s.plusDays + ani
		ti = time.localtime(seconds_absolute + 86400 * offset)
		if offset != s.old_offset:
			s.old_offset = offset
			o1 = "%04u-%02u-%02u" % (ti[0], ti[1], ti[2])
			if round(offset) == 0: o2 = ""
			else: o2 = "(%+i days)" % round(offset)
			if s.anim: o3 = "(animation on)"
			else: o3 = ""
			pygame.display.set_caption("%s  %s  %s" % (o1, o2, o3))
		planets_dict = orrp.coordinates(ti[0], ti[1], ti[2], ti[3], ti[4])

		# draw Sun
		xi, yi = pic2[0].get_size()
		if not s.dist or (s.dist and s.zoom < 4):
			s.dazz.blit(pic2[0], (PL_CENTER[0] - xi//2, PL_CENTER[1] - yi//2))

		# draw orbits
		for i, el in enumerate(planets_dict):
			if s.dist:
				r = 440 / pdist[s.zoom] * pdist[i]
			else:
				r = 55 * (i + 1)
			pygame.draw.circle(s.dazz, (80, 80, 80), (PL_CENTER[0], PL_CENTER[1]), r, width = 4)

		# draw planets
		for i, el in enumerate(planets_dict):
			if s.dist:
				r = 440 / pdist[s.zoom] * pdist[i]
			else:
				r = 55 * (i + 1)
			feta = math.atan2(el[0], el[1])
			coordinates = (r * math.sin(feta), r * math.cos(feta))
			coordinates = (coordinates[0] + PL_CENTER[0], HEIGHT - (coordinates[1] + PL_CENTER[1]))
			xi, yi = pic2[i + 1].get_size()
			s.dazz.blit(pic2[i + 1], (coordinates[0] - xi//2, coordinates[1] - yi//2))

		tres = min(s.res[0], s.res[1])
		out = pygame.transform.smoothscale(s.dazz, (tres, tres))
		s.screen.blit(out, (0, 0))
		
		pygame.display.flip()

c = Orr()
c.run()

