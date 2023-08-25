import glm
import pygame as pg

# FOV = 10 # degrees
NEAR = 0.1
FAR = 500 # essentially this is the render distance
# SPEED = 0.02
SENSITIVITY = 0.04

class Camera:
    def __init__(self, app, position=(0, 0, 4), yaw=-90, pitch=0, SPEED=0.02, FOV=50):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch
        self.SPEED = SPEED
        self.FOV = FOV
        # view matrix
        self.m_view = self.get_view_matrix()
        # projection matrix
        self.m_proj = self.get_projection_matrix()
        # ortho matrix
        self.m_ortho = self.get_ortho_projection_matrix()

    def rotate(self):
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY # += is inverted camera controls
        self.pitch = max(-89, min(89, self.pitch))

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self):
        self.move()
        self.rotate()
        self.check_inputs()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()

    def check_inputs(self):
        for event in pg.event.get():
            # print(event.type, event)
            if event.type == pg.MOUSEWHEEL:
                print(event.x, event.y)
            if event.type == pg.KEYDOWN:
                print("should change")
                # self.FOV = 10

    def move(self):
        velocity = self.SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.position += self.forward * velocity
            self.SPEED+=.001
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_SPACE]:
            self.position += self.up * velocity
        if keys[pg.K_LSHIFT]:
            self.position -= self.up * velocity
        if keys[pg.K_c]:
            self.FOV = 10
            print(self.FOV)
        if keys[pg.K_z]:
            self.FOV = 50
            print(self.FOV)

    def get_view_matrix(self):
        # this is where the 3rd person changes will come in, can change the vec3(0) to be a player's location
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(self.FOV), self.aspect_ratio, NEAR, FAR)
    
    def get_ortho_projection_matrix(self):
        return glm.ortho(0, 0, 1, 1, 1, 10)