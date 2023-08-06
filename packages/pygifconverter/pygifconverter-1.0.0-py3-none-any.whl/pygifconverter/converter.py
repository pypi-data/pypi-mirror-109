"""
Given static images, make them into a GIF file.
"""

import glob
from PIL import Image

class GifConverter:
    def __init__(self, path_in=None, path_out=None, resize=(320,240)):
        self.path_in = path_in or './*.png'
        self.path_out = path_out or './output.gif'
        self.resize = resize
        
    def convert_gif(self):
        """
        Process image converting into GIF.
        """
        img, *images = [Image.open(f).resize(self.resize, Image.ANTIALIAS) \
                       for f in glob.glob(self.path_in)]
        
        try:
            img.save(
                fp=self.path_out,
                format='GIF',
                append_images=images,
                save_all=True,
                duration=500,
                loop=0,
            )
        except IOError:
            print("Cannot convert!", img)
            

if __name__ == '__main__':
    c = GifConverter('./project/images/*.png', './project/image_out/result.gif')
    c.convert_gif()