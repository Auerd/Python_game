import pygame as p

win_width = 800
win_height = 640


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = p.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h, = camera
    l, t = -l + win_width / 2, -t + win_height / 2

    l = min(0, l)

    l = max(-(camera.width - win_width), l)

    t = min(0, t)

    t = max(-(camera.height - win_height), t)

    return p.Rect(l, t, w, h)
