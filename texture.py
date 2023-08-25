import io
import pygame as pg
import moderngl as mgl
from urllib.request import urlopen


class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path=r'textures\grassy_texture.jpg')
        self.textures[1] = self.get_texture(path=r'textures\notfound.png')
        self.textures[2] = self.get_internet_texture(url="https://play-lh.googleusercontent.com/IeNJWoKYx1waOhfWF6TiuSiWBLfqLb18lmZYXSgsH1fvb8v1IYiZr5aYWe0Gxu-pVZX3")
        self.textures['lego'] = self.get_texture(path=r'objects\legoman\Face_04.png')
        self.textures['skybox'] = self.get_texture_cube(dir_path='textures\\skybox\\', ext='png')

    def get_texture_cube(self, dir_path, ext='png'):
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        # textures = [pg.image.load(dir_path + f'{face}.{ext}').convert() for face in faces]
        textures = []
        for face in faces:
            texture = pg.image.load(dir_path + f'{face}.{ext}').convert()
            if face in ['right', 'left', 'front', 'back']:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)
        
        return texture_cube
    
    def get_internet_texture(self, url):
        # load images from url
        img_str = urlopen(url).read()
        img_file = io.BytesIO(img_str)

        texture = pg.image.load(img_file).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                 data=pg.image.tostring(texture, 'RGB'))
        
        # mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        # AF
        texture.anisotropic = 32.0
        return texture


    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                 data=pg.image.tostring(texture, 'RGB'))
        
        # mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        # AF
        texture.anisotropic = 32.0
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]