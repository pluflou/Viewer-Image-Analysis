import numpy as np
from skimage import io
import matplotlib.pyplot as plt


class Image:    
    def __init__(self, image):
        self.raw = np.asarray(image)
        self.shape= self.raw.shape
        self.x_size= self.shape[1]
        self.y_size= self.shape[0]
        self.subtracted_data= np.array([[0 for x in range(self.x_size)] for y in range(self.y_size)])

    def __getitem__(self,index):
        return self.raw[index]

    def __setitem__(self,index,value):
        self.raw[index] = value

    def subtract_bg(self,bg):
        print("Subtracting background...")
        if (bg.shape == self.shape):
            for i in range(self.y_size):
                for j in range (self.x_size):
                    self.subtracted_data[i][j]= int(self.raw[i][j]) - int(bg.raw[i][j])
                    #print(self.raw[i][j], bg.raw[i][j],self.subtracted_data[i][j] )
            return self.subtracted_data
        else:
            print("Error: Background image size does not match data size.")

path_to_image= '/home/sara/Documents/SECAR/Diagnostics/Viewer-Image-Analysis/images/stability_FP2/D1568_8_28_19_overnight_stability_006.tiff'
bg_image = io.imread('/home/sara/Documents/SECAR/Diagnostics/Viewer-Image-Analysis/images/stability_FP2/light_bg/BG_crop.tiff')
image_file = io.imread(path_to_image)



image=Image(image_file)
bg = Image(bg_image)
#print(bg.raw)
image.subtract_bg(bg)

bg = bg.raw#[0:10,0:10]
raw= image.raw#[0:10,0:10]
image = image.subtracted_data#[0:10,0:10]
#print(raw, bg, image)

import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable

gs = gridspec.GridSpec(1,3)

plt.figure(figsize=(9,4))
ax = plt.subplot(gs[0,0])
plt.imshow(raw, cmap='jet')
plt.title("Raw")

ax = plt.subplot(gs[0,1])
plt.imshow(bg, cmap='jet')
plt.title("BG")

ax = plt.subplot(gs[0,2])
plt.imshow(image, cmap='jet')
plt.title("Subtracted")

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(cax=cax, orientation='vertical')

plt.tight_layout()

plt.savefig("im6_raw_bg_subtract_f", dpi = 300)