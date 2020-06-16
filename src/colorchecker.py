import numpy as np
from .colorspace import *

class ColorChecker:
	def __init__(self, color, colorspace, colorflag, ill, obs, whites=None):
		'''
		color: colors of colorchecker patches;
		colorspace: 'LAB' or a kind of 'RGB' color space;
		ill: if colorspace is 'LAB', then ill is the illuminant of color defined on;
		obs: if colorspace is 'LAB', then obs is the observer of color defined on;
		whites: sometimes needed for linearization
		'''
		# self.color = color
		self._lab, self._xyz, self._rgb, self._rgbl = None, None, None, None
		self.rgb_cs = colorspace
		if colorspace == 'LAB':
			self._lab = color
		elif colorspace == 'RGBL':
			self._rgbl = color
		else:
			self._rgb = color
			
		# self.colorspace = colorspace
		self.ill = ill
		self.obs = obs
		# self.dist_ill = dist_ill
		# self.dist_obs = dist_obs
		self.whites = whites
		self.white_mask = np.ones(color.shape, dtype=bool)
		self.white_mask[whites] = False
		self.color_mask = ~self.white_mask


class ColorCheckerMetric:
	def __init__(self, colorchecker, colorspace):
		'''
		dist_ill: distance illuminant; needed when calculating xyz, lab
		dist_obs: distance observer; needed when calculating xyz, lab
		'''

		self.cc = colorchecker
		self._lab, self._xyz, self._rgb, self._rgbl = \
			self.cc._lab, self.cc._xyz, self.cc._rgb, self.cc._rgbl
		
		self._grayl, self._l = None, None
		self.cs = self.cc.rgb_cs
		self.dist_ill = dist_ill
		self.dist_obs = dist_obs

	@property
	def lab(self):
		if not self._lab:
			self._lab = xyz2lab(self.xyz)
		return self._lab

	@property
	def rgb(self):
		if not self._rgb:
			self._rgb = self.cs.rgbl2rgb(self.rgbl)
		return self._rgb

	@property
	def rgbl(self):
		if not self._rgbl:
			if self._rgb:
				self._rgbl = self.cs.rgb2rgbl(self._rgb)
			else:
				self._rgbl = self.cs.xyz2rgbl(self.xyz, self.dist_ill, self.dist_obs)
		return self._rgbl

	@property
	def xyz(self):
		if not self._xyz:
			if self._lab:
				self._xyz = lab2xyz(self.lab, self.dist_ill, self.dist_obs)
			else:
				self._xyz = self.cs.rgbl2xyz(self.rgbl, self.dist_ill, self.dist_obs)
		return self._xyz

	@property
	def grayl(self):
		if not self._grayl:
			self._grayl = xyz2grayl(self.xyz)
		return self._grayl
	
	# @property
	# def l(self):
	# 	if not self._l:
	# 		self._l = 

	
	# @property
	# def whites_grayl(self):
	# 	if not self._grayl:
	# 		self._grayl = xyz2grayl(self.xyz)
	# 	return self._grayl


# class ColorChecker:
#     def __init__(self, rgb):
#         rgbl = rgb2rgbl(rgb)
#         lab = rgbl2lab(rgbl)
#         # lab = ColorChecker2005_LAB_D65_2
#         xyz = lab2xyz(lab)
#         rgbl = xyz2rgbl(xyz)
#         rgb = rgbl2rgb(rgbl)
#         # rgbl = rgb2rgbl(rgb)
#         gray = rgb2gray(rgb)
#         grayl = rgb2rgbl(gray)        

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

colorchecker_Macbeth = ColorChecker(ColorChecker2005_LAB_D50_2, 'LAB', 'D50', '2', np.arange(18,24))

# class ColorChecker_Macbeth:
#     ColorChecker2005_LAB_D50_2 = np.array([[37.986, 13.555, 14.059],
#             [65.711, 18.13, 17.81],
#             [49.927, -4.88, -21.925],
#             [43.139, -13.095, 21.905],
#             [55.112, 8.844, -25.399],
#             [70.719, -33.397, -0.199],
#             [62.661, 36.067, 57.096],
#             [40.02, 10.41, -45.964],
#             [51.124, 48.239, 16.248],
#             [30.325, 22.976, -21.587],
#             [72.532, -23.709, 57.255],
#             [71.941, 19.363, 67.857],
#             [28.778, 14.179, -50.297],
#             [55.261, -38.342, 31.37],
#             [42.101, 53.378, 28.19],
#             [81.733, 4.039, 79.819],
#             [51.935, 49.986, -14.574],
#             [51.038, -28.631, -28.638],
#             [96.539, -0.425, 1.186],
#             [81.257, -0.638, -0.335],
#             [66.766, -0.734, -0.504],
#             [50.867, -0.153, -0.27],
#             [35.656, -0.421, -1.231],
#             [20.461, -0.079, -0.973]])

#     ColorChecker2005_LAB_D65_2 = np.array([[37.542, 12.018, 13.33],
#             [65.2, 14.821, 17.545],
#             [50.366, -1.573, -21.431],
#             [43.125, -14.63, 22.12],
#             [55.343, 11.449, -25.289],
#             [71.36, -32.718, 1.636],
#             [61.365, 32.885, 55.155],
#             [40.712, 16.908, -45.085],
#             [49.86, 45.934, 13.876],
#             [30.15, 24.915, -22.606],
#             [72.438, -27.464, 58.469],
#             [70.916, 15.583, 66.543],
#             [29.624, 21.425, -49.031],
#             [55.643, -40.76, 33.274],
#             [40.554, 49.972, 25.46],
#             [80.982, -1.037, 80.03],
#             [51.006, 49.876, -16.93],
#             [52.121, -24.61, -26.176],
#             [96.536, -0.694, 1.354],
#             [81.274, -0.61, -0.24],
#             [66.787, -0.647, -0.429],
#             [50.872, -0.059, -0.247],
#             [35.68, -0.22, -1.205],
#             [20.475, 0.049, -0.972]])

#     ColorChecker2005_LAB_D65_10 = np.array([[37.086, 12.274, 12.592],
#             [64.955, 12.807, 18.014],
#             [51.203, -3.956, -20.394],
#             [42.383, -10.369, 21.193],
#             [56.335, 6.77, -24.024],
#             [71.66, -31.103, 3.212],
#             [59.938, 34.888, 53.167],
#             [42.806, 8.124, -41.883],
#             [49.419, 42.259, 12.808],
#             [30.787, 20.529, -22.491],
#             [71.039, -19.617, 58.211],
#             [69.138, 20.686, 64.194],
#             [32.216, 10.126, -44.708],
#             [55.035, -34.836, 34.155],
#             [39.846, 45.894, 24.146],
#             [79.145, 5.463, 79.267],
#             [51.445, 42.995, -17.301],
#             [53.848, -29.91, -22.353],
#             [96.515, -0.816, 1.635],
#             [81.287, -0.651, -0.134],
#             [66.802, -0.639, -0.367],
#             [50.871, -0.005, -0.243],
#             [35.714, -0.265, -1.176],
#             [20.505, -0.036, -0.959]])

#     ColorChecker2005_LAB_D50_10 = np.array([[37.596, 13.534, 13.456],
#             [65.52, 15.904, 18.42],
#             [50.642, -6.748, -21.139],
#             [42.521, -9.343, 21.259],
#             [55.938, 4.723, -24.484],
#             [71.024, -31.547, 1.404],
#             [61.465, 37.284, 55.609],
#             [41.802, 2.959, -43.447],
#             [50.735, 44.326, 15.266],
#             [30.806, 18.861, -21.8],
#             [71.382, -16.777, 57.652],
#             [70.449, 23.406, 66.164],
#             [31.021, 4.503, -46.761],
#             [54.8, -32.907, 32.669],
#             [41.488, 48.83, 27.056],
#             [80.208, 9.344, 79.885],
#             [52.236, 43.304, -15.231],
#             [52.604, -32.947, -25.158],
#             [96.525, -0.499, 1.449],
#             [81.269, -0.642, -0.239],
#             [66.78, -0.694, -0.449],
#             [50.866, -0.076, -0.269],
#             [35.685, -0.432, -1.214],
#             [20.486, -0.145, -0.968]])    

#     lab = ColorChecker2005_LAB_D65_2
#     xyz = lab2xyz(lab)
#     rgbl = xyz2rgbl(xyz)
#     rgb = rgbl2rgb(rgbl)
#     gray = rgb2gray(rgb)
#     grayl = rgb2rgbl(gray)