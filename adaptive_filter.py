from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import random
import math


def plot_image(image1, image2):
    fig, ax = plt.subplots(1,2)
    ax[0].imshow(image1, cmap='gray')
    ax[0].set_title('Orginal Image')
    ax[1].imshow(image2, cmap = 'gray')
    ax[1].set_title('Filtered image')
    plt.tight_layout()
    plt.show()

def adaptive_filer(image):
	size = image.size
	print(size)

	noise = Image.new("L", image.size)
	temp = Image.new("L", image.size)
	output = Image.new("L", image.size)

	iset = 0
	rand = -1
	var = 1000

	for i in range(0, size[0]):
		for j in range(0, size[1]):
			if(iset == 0):
				r = 0
				while(r >= 1.0 or r == 0):
					temp1 = random.uniform(-1,1)
					temp2 = random.uniform(-1,1)
					r = temp1 ** 2 + temp2 ** 2;
				fac = (-2.0 * math.log(r) / r) ** 0.5;
				rand = int(temp1 * fac * (var ** 0.5));
				rand2 = int(temp2 * fac * (var ** 0.5));
				iset = 1;
				l = image.getpixel((i, j)) + rand2
				noise.putpixel((i,j), rand2)
			if(iset == 1):
				iset = 0;
				l = image.getpixel((i, j)) + rand
				noise.putpixel((i,j), rand)
			temp.putpixel((i,j), l)
	ignore = int((3 - 1) / 2)

	for i in range(0 + ignore, size[0] - ignore):
		for j in range(0 + ignore, size[1] - ignore):
			p1 = temp.getpixel((i-1,j-1))
			p2 = temp.getpixel((i,j-1))
			p3 = temp.getpixel((i+1,j-1))
			p4 = temp.getpixel((i-1,j))
			p5 = temp.getpixel((i,j))
			p6 = temp.getpixel((i+1,j))
			p7 = temp.getpixel((i-1,j+1))
			p8 = temp.getpixel((i,j+1))
			p9 = temp.getpixel((i+1,j+1))
			ap = (p1+p2+p3+p4+p5+p6+p7+p8+p9)/9
			ap2 = (p1**2+p2**2+p3**2+p4**2+p5**2+p6**2+p7**2+p8**2+p9**2)/9
			vp2 = ap2 - ap ** 2
			interval = 1000
			if(vp2 < var):
				l = temp.getpixel((i,j)) - (var / vp2) * (temp.getpixel((i,j)) - ap)
			elif(vp2 < var + interval):
				l = temp.getpixel((i,j)) - (var / vp2) * (temp.getpixel((i,j)) - ap)
			else:
				l = temp.getpixel((i,j))
			output.putpixel((i,j), int(l))

	return output, temp, noise

image = Image.open('Fig0507(b)(ckt-board-gauss-var-400).tif').convert('L')
output,temp,noise= adaptive_filer(image)
output.save("output_adaptive_filer.png")
temp.save("temp_adaptive_filer.png")
noise.save("noise_adaptive_filer.png")


plot_image(np.array(image),np.array(output))
