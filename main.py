import pygame as pg
import moderngl as mgl
import sys
from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
from scene_renderer import SceneRenderer

class GraphicsEngine:
    fps = 0
    def __init__(self, win_size=(1600,900)):
        pg.init()
        # set window size
        self.WIN_SIZE = win_size
        # opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # title window
        pg.display.set_caption(f"3d Engine :D - {self.fps} FPS")
        # set icon
        icon = pg.image.load('shield.png')
        pg.display.set_icon(icon)
        # opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        # mouse controls
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        # detect existing opengl context
        self.ctx = mgl.create_context()
        # uncomment to show inside faces of the cube
        # self.ctx.front_face = 'cw'
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        # create time object
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        # light
        self.light = Light(position=(3, 3, -3), color=(1, 1, 1))
        # camera
        self.camera = Camera(self)
        # mesh
        self.mesh = Mesh(self)
        # create scene
        self.scene = Scene(self)
        # renderer
        self.scene_renderer = SceneRenderer(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                self.scene_renderer.destroy()
                pg.quit()
                sys.exit()
        
    def render(self):
        # clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # render scene
        # self.scene.render()
        self.fps = self.clock.get_fps()
        pg.display.set_caption(f"3d Engine :D - {round(self.fps, 0)} FPS")
        self.scene_renderer.render()
        # swap buffer
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001
    
    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)

if __name__ == "__main__":
    app = GraphicsEngine()
    app.run()
