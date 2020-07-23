import numpy as np
from .colorspace import *
from .utils import *

'''
Difference between ColorChecker and ColorCheckerMetric

The instance of ColorChecker describe the colorchecker by color values,
color space and gray indice, which are stable for a colorchecker.

The instance of ColorCheckerMetric adds the color space which is associated with 
the color distance function and the colorchecker converts to.
'''

# class ColorChecker:
# 	def __init__(self, color, colorspace, io, whites=None):
# 		'''
# 		the colorchecker;

# 		color: reference colors of colorchecker;
# 		colorspace: 'LAB' or some 'RGB' color space;
# 		io: only valid if colorspace is 'LAB';
# 		whites: the indice list of gray colors of the reference colors;
# 		'''
# 		# color and correlated color space
# 		self.lab, self.rgb = None, None
# 		self.cs, self.io = None, None
# 		if colorspace == 'LAB':
# 			self.lab = color
# 			self.io = io
# 		else:
# 			self.rgb = color
# 			self.cs = get_colorspace(colorspace)

# 		# white_mask & color_mask
# 		self.white_mask = np.zeros(color.shape[0], dtype=bool)
# 		if whites is not None:
# 			self.white_mask[whites] = True
# 		self.color_mask = ~self.white_mask

# class ColorCheckerMetric:
# 	def __init__(self, colors, cs):
# 		'''
# 		the colorchecker adds the color space for conversion for color distance;
# 		'''

# 		# colorchecker
# 		self.cc = colors

# 		# color space
# 		self.cs = cs

# 		self.lab = self.cc.to(Lab(self.cs.io))
# 		self.rgbl = self.cc.to(self.cs.l)
# 		self.rgb = self.rgbl.fromL()
# 		self.grayl = self.cc.to()
		


# 		# colors after conversion
# 		# if self.cc.lab is not None:
# 		# 	self.lab = lab2lab(self.cc.lab, self.cc.io, io)
# 		# 	self.xyz = lab2xyz(self.lab, io)
# 		# 	self.rgbl = self.cs.xyz2rgbl(self.xyz, io)
# 		# 	self.rgb = self.cs.rgbl2rgb(self.rgbl)
# 		# else:
# 		# 	self.rgb = colorconvert(self.cc.rgb, self.cc.cs, self.cs)
# 		# 	self.rgbl = self.cs.rgb2rgbl(self.rgb)
# 		# 	self.xyz = self.cs.rgbl2xyz(self.rgbl)
# 		# 	self.lab = xyz2lab(self.xyz)
# 		# self.grayl = xyz2grayl(self.xyz)

# 		# gray_mask & color_mask
# 		self.gray_mask = self.cc.grays
# 		self.color_mask = ~self.cc.grays
