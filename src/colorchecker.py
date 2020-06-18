import numpy as np
from .colorspace import *
from .utils import *

class ColorChecker:
	def __init__(self, color, colorspace, io, whites=None):
		'''
		color: colors of colorchecker patches;
		colorspace: 'LAB' or a kind of 'RGB' color space;
		io: needed if colorspace is 'LAB';
		whites: sometimes needed for linearization;
		'''
		# colorspace and color
		self.lab, self.rgb = None, None
		self.cs, self.io = None, None
		if colorspace == 'LAB':
			self.lab = color
			self.io = io
		else:
			self.rgb = color
			self.cs = get_colorspace(colorspace)

		# white_mask & color_mask
		if whites is None:
			self.white_mask = np.zeros(color.shape[0], dtype=bool)
		else:
			self.white_mask = np.ones(color.shape[0], dtype=bool)
			self.white_mask[whites] = False
		self.color_mask = ~self.white_mask

class ColorCheckerMetric:
	def __init__(self, colorchecker, colorspace, io):
		'''
		dio: needed when calculating xyz, lab
		'''

		self.cc = colorchecker
		self.cs = get_colorspace(colorspace)
		self.io = io

		if self.cc.lab is not None:
			self.lab = lab2lab(self.cc.lab, self.cc.io, io)
			self.xyz = lab2xyz(self.lab, io)
			self.rgbl = self.cs.xyz2rgbl(self.xyz, io)
			self.rgb = self.cs.rgbl2rgb(self.rgbl)
		else:
			self.rgb = colorconvert(self.cc.rgb, self.cc.cs, self.cs)
			self.rgbl = self.cs.rgb2rgbl(self.rgb)
			self.xyz = self.cs.rgbl2xyz(self.rgbl)
			self.lab = xyz2lab(self.xyz)
		self.grayl = xyz2grayl(self.xyz)

		# white_mask & color_mask
		self.white_mask = self.cc.white_mask
		self.color_mask = self.cc.color_mask
		 

ColorChecker2005_LAB_D50_2 = np.array([[37.986, 13.555, 14.059],
		[65.711, 18.13, 17.81],
		[49.927, -4.88, -21.925],
		[43.139, -13.095, 21.905],
		[55.112, 8.844, -25.399],
		[70.719, -33.397, -0.199],
		[62.661, 36.067, 57.096],
		[40.02, 10.41, -45.964],
		[51.124, 48.239, 16.248],
		[30.325, 22.976, -21.587],
		[72.532, -23.709, 57.255],
		[71.941, 19.363, 67.857],
		[28.778, 14.179, -50.297],
		[55.261, -38.342, 31.37],
		[42.101, 53.378, 28.19],
		[81.733, 4.039, 79.819],
		[51.935, 49.986, -14.574],
		[51.038, -28.631, -28.638],
		[96.539, -0.425, 1.186],
		[81.257, -0.638, -0.335],
		[66.766, -0.734, -0.504],
		[50.867, -0.153, -0.27],
		[35.656, -0.421, -1.231],
		[20.461, -0.079, -0.973]])

ColorChecker2005_LAB_D65_2 = np.array([[37.542, 12.018, 13.33],
		[65.2, 14.821, 17.545],
		[50.366, -1.573, -21.431],
		[43.125, -14.63, 22.12],
		[55.343, 11.449, -25.289],
		[71.36, -32.718, 1.636],
		[61.365, 32.885, 55.155],
		[40.712, 16.908, -45.085],
		[49.86, 45.934, 13.876],
		[30.15, 24.915, -22.606],
		[72.438, -27.464, 58.469],
		[70.916, 15.583, 66.543],
		[29.624, 21.425, -49.031],
		[55.643, -40.76, 33.274],
		[40.554, 49.972, 25.46],
		[80.982, -1.037, 80.03],
		[51.006, 49.876, -16.93],
		[52.121, -24.61, -26.176],
		[96.536, -0.694, 1.354],
		[81.274, -0.61, -0.24],
		[66.787, -0.647, -0.429],
		[50.872, -0.059, -0.247],
		[35.68, -0.22, -1.205],
		[20.475, 0.049, -0.972]])

colorchecker_Macbeth = ColorChecker(ColorChecker2005_LAB_D50_2, 'LAB', D50_2, np.arange(18,24))
colorchecker_Macbeth_D65_2 = ColorChecker(ColorChecker2005_LAB_D65_2, 'LAB', D65_2, np.arange(18,24))
