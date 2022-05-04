import pygame as p


class Camera(object):
    def __init__(self, width, height, win_width, win_height):
        self.state = p.Rect(0, 0, width, height)
        self.win_width = win_width
        self.win_height = win_height

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def camera_configure(self, camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h, = camera
        l, t = -l + self.win_width / 2, -t + self.win_height / 2

        l = min(0, l)

        l = max(-(camera.width - self.win_width), l)

        t = min(0, t)

        t = max(-(camera.height - self.win_height), t)
        return p.Rect(l, t, w, h)

    def update(self, target):
        self.state = self.camera_configure(self.state, target.rect)
