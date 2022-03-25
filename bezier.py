import copy
import math

import pygame
import sys

from data.classes.Points import Points

pygame.init()

screen_width, screen_height = 1024, 576
screen = pygame.display.set_mode((screen_width, screen_height))

points = Points()
bezier = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

clock = pygame.time.Clock()


def draw_line(origin, endpoint, surface):
    delta_x = endpoint.x - origin.x
    delta_y = endpoint.y - origin.y
    error = 0

    if delta_x == 0:
        return None
    delta_error = math.fabs(delta_y / delta_x)

    y = int(origin.y)
    for x in range(int(origin.x), int(endpoint.x)):
        surface.set_at((x, y), (0, 0, 0))
        error += delta_error
        if error >= 0.5:
            y += 1
            error -= 1.0


def draw_curve(surface):
    for i in range(0, 101):
        curve_points = points.get_point(i / 100)

        last_point = copy.deepcopy(curve_points[0])
        last_point.x, last_point.y = screen_width // 2 + last_point.x, screen_height // 2 - last_point.y

        for curve_point in curve_points:
            rendered_curve_point = copy.deepcopy(curve_point)
            rendered_curve_point.x, rendered_curve_point.y = screen_width // 2 + curve_point.x, screen_height // 2 - curve_point.y

            surface.set_at((int(rendered_curve_point.x), int(rendered_curve_point.y)), (0, 0, 0))
            draw_line(last_point, curve_point, surface)

            last_point = copy.deepcopy(curve_point)

    return surface


while True:
    screen.fill((255, 255, 255))
    screen.blit(bezier, (0, 0))

    mouse_pos = pygame.mouse.get_pos()
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = mouse_pos[0] - screen_width // 2,  - (mouse_pos[1] - screen_height // 2)
            points.add_anchor_point(mouse_pos)

    bezier = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

    bezier = draw_curve(bezier)

    points.update()

    for point in points.points:
        poin = copy.deepcopy(point)
        poin.pos.x, poin.pos.y = screen_width // 2 + poin.pos.x, screen_height // 2 - poin.pos.y
        pygame.draw.circle(screen, (255, 0, 0), poin.pos, 3)

    pygame.display.update()
    clock.tick(60)
