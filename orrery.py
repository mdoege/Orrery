#!/usr/bin/env python

# Python orrery

import pygame
import time, math
import orrp

RES  = 150		# internal resolution
SRES = 600		# window size
ANIM_SPEED = 4	# animation speed factor

class Orr:
	def __init__(s):
		pygame.init()
		s.res = SRES, SRES
		s.screen = pygame.display.set_mode(s.res, pygame.RESIZABLE)
		pygame.display.set_caption('Orrery')
		s.clock = pygame.time.Clock()
		s.dazz = pygame.Surface((RES, RES))
		s.plusDays = 0
		s.anim = False
		s.anim_start = 0

	def events(s):
		for event in pygame.event.get():
			if event.type == pygame.QUIT: s.running = False
			if event.type == pygame.VIDEORESIZE:
				s.res = event.w, event.h
				s.screen = pygame.display.set_mode(s.res, pygame.RESIZABLE)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
				s.plusDays += 1
				pygame.display.set_caption("%+i days" % s.plusDays)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
				s.plusDays -= 1
				pygame.display.set_caption("%+i days" % s.plusDays)

			if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
				s.plusDays += 30
				pygame.display.set_caption("%+i days" % s.plusDays)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
				s.plusDays -= 30
				pygame.display.set_caption("%+i days" % s.plusDays)

			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				s.plusDays = 0
				pygame.display.set_caption("Today")

			if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
				s.anim = not s.anim
				if s.anim:
					s.anim_start = time.time()
					pygame.display.set_caption("Animation on")
				else:
					pygame.display.set_caption("Animation off")

	def run(s):
		s.running = True
		while s.running:
			s.clock.tick(5)
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
		ti = time.localtime(seconds_absolute + 86400 * (s.plusDays + ani))
		planets_dict = orrp.coordinates(ti[0], ti[1], ti[2], ti[3], ti[4])
		pygame.draw.circle(s.dazz, (255, 255, 0), (PL_CENTER[0], PL_CENTER[1]), 4)
		for i, el in enumerate(planets_dict):
			r = 8 * (i + 1) + 2
			pygame.draw.circle(s.dazz, (80, 80, 80), (PL_CENTER[0], PL_CENTER[1]), r, width = 1)
			feta = math.atan2(el[0], el[1])
			coordinates = (r * math.sin(feta), r * math.cos(feta))
			coordinates = (coordinates[0] + PL_CENTER[0], HEIGHT - (coordinates[1] + PL_CENTER[1]))
			for ar in range(0, len(orrp.planets_a[i][0]), 5):
				x = orrp.planets_a[i][0][ar] - 50 + coordinates[0]
				y = orrp.planets_a[i][0][ar + 1] - 50 + coordinates[1]
				if x >= 0 and y >= 0:
					c = (orrp.planets_a[i][0][ar + 2], orrp.planets_a[i][0][ar + 3],
									orrp.planets_a[i][0][ar + 4])
					pygame.draw.line(s.dazz, c, (int(x), int(y)), (int(x), int(y)))

		tres = s.res[0], s.res[1]
		out = pygame.transform.scale(s.dazz, tres)
		s.screen.blit(out, (0, 0))
		
		pygame.display.flip()

c = Orr()
c.run()

