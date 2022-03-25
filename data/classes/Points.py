from pygame import Vector2
from data.utils.utils import cubic_bezier
from copy import deepcopy


class Point:
    def __init__(self, pos):
        self.pos = pos


class Points:
    def __init__(self):
        self.points = [Point(Vector2(-50, -50)), Point(Vector2(-50, 50)), Point(Vector2(50, 50)), Point(Vector2(50, -50))]

    def add_anchor_point(self, pos):
        self.points.append(Point(self.points[-1].pos))
        self.points.append(Point(Vector2(pos)))
        self.points.append(Point(Vector2(pos)))

    def get_point(self, t):
        curve_points = []

        p0 = Vector2()
        p1 = Vector2()
        p2 = Vector2()
        p3 = Vector2()

        state = 1

        for index, point in enumerate(self.points):
            exec(f'p{state - 1}.x, p{state - 1}.y = {point.pos}')

            if state % 4 == 0:
                curve_points.append(cubic_bezier(p0, p1, p2, p3, t))
                p0 = deepcopy(p3)
                state = 1

            state += 1

        return curve_points

    def update(self):
        for index, point in enumerate(self.points):
            # first anchor point
            if index == 0:
                pass
            # first control point
            elif index == 1:
                pass
            # last anchor point
            elif index == len(self.points) - 1:
                pass
            # last control point
            elif index == len(self.points) - 2:
                pass
            # generic anchor point
            elif index % 3 == 0:
                pass
            # generic left control point
            elif index % 3 == 2:
                # self.points[index] = Point(self.points[index + 1].pos)
                last_anchor_point = self.points[index - 2].pos
                current_anchor_point = self.points[index + 1].pos
                next_anchor_point = self.points[index + 4].pos

                dir_to_last_anchor_point = (last_anchor_point - current_anchor_point)
                dir_to_next_anchor_point = (next_anchor_point - current_anchor_point)

                left_control_point_dir = (dir_to_last_anchor_point.normalize() - dir_to_next_anchor_point.normalize()).normalize()

                left_control_point = left_control_point_dir * (dir_to_last_anchor_point.magnitude() / 2)
                left_control_point += current_anchor_point

                self.points[index] = Point(left_control_point)
            # generic right control point
            elif index % 3 == 1:
                # self.points[index] = Point(self.points[index - 1].pos)
                last_anchor_point = self.points[index - 4].pos
                current_anchor_point = self.points[index - 1].pos
                next_anchor_point = self.points[index + 2].pos

                dir_to_last_anchor_point = (last_anchor_point - current_anchor_point)
                dir_to_next_anchor_point = (next_anchor_point - current_anchor_point)

                right_control_point_dir = (dir_to_next_anchor_point.normalize() - dir_to_last_anchor_point.normalize()).normalize()

                right_control_point = right_control_point_dir * (dir_to_next_anchor_point.magnitude() / 2)
                right_control_point += current_anchor_point

                self.points[index] = Point(right_control_point)

            # Pause

            # first control point
            if index == 1:
                attached_anchor_point = self.points[index - 1].pos
                next_control_point = self.points[index + 1].pos

                control_point_dir = (next_control_point - attached_anchor_point)
                control_point_dir_norm = control_point_dir.normalize()

                control_point = control_point_dir_norm * (control_point_dir.magnitude() / 2)
                control_point += attached_anchor_point

                self.points[index] = Point(control_point)
            # last control point
            elif index == len(self.points) - 2:
                attached_anchor_point = self.points[index + 1].pos
                last_control_point = self.points[index - 1].pos

                control_point_dir = (last_control_point - attached_anchor_point)
                control_point_dir_norm = control_point_dir.normalize()

                control_point = control_point_dir_norm * (control_point_dir.magnitude() / 2)
                control_point += attached_anchor_point

                self.points[index] = Point(control_point)