from model import *


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        # skybox
        self.skybox = AdvancedSkyBox(app)

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        # add(Cube(app, tex_id=0))
        # add(Cube(app, tex_id=1, pos=(-2.5, 0, 0), rot=(45, 0, 0), scale=(1, 2, 1)))

        # add floor of boxes
        # n, s = 80, 3
        # for x in range(-n, n, s):
        #     for z in range(-n, n, s):
        #         add(Cube(app, pos=(x, -s, z)))

        add(Cube(app, pos=(0, -1, 0), scale=(30, .1, 30)))

        add(Lego(app, pos=(0, -1, -10), scale=(0.1, 0.1, 0.1)))

    def update(self):
        for obj in self.objects:
            obj.render()
        self.skybox.render() # ensure skybox is always rendered last for performance