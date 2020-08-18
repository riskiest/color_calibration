#pragma once
#pragma once
#include "colorspace.h"
#include "distance.h"
#include "utils.h"
#include <map>

namespace cv {
namespace ccm {

class Color {
public:
	Mat colors;
	ColorSpace cs;
	Mat grays;
	Mat colored;
	std::map<ColorSpace, Color*> _history;

	Color(Mat colors, ColorSpace cs) :colors(colors), cs(cs) {};

	Color to(const ColorSpace& other, CAM method = BRADFORD, bool save = true) {
	/*	if (_history.count(other) == 1) {
			return *_history[other];
		}*/
		if (cs.relate(other)) {
			return Color(cs.relation(other).run(colors), other);
		}
		Operations ops;
		ops.add(cs.to).add(XYZ(cs.io).cam(other.io, method)).add(other.from);
		Color color(ops.run(colors), other);
		//if (save) {
		//	_history[other] = &color;
		//}
		return color;
	}

	Mat channel(Mat M, int i) {
		Mat dChannels[3];
		split(M, dChannels);
		return dChannels[i];
	}

	Mat toGray(IO io, CAM method = BRADFORD, bool save = true) {
		return channel(this->to(XYZ(io), method, save).colors, 1);
	}

	Mat toLuminant(IO io, CAM method = BRADFORD, bool save = true) {
		return channel(this->to(Lab(io), method, save).colors, 0);
	}

	Mat diff(Color& other, DISTANCE_TYPE method = CIE2000) {
		return diff(other, cs.io, method);
	}

	Mat diff(Color& other, IO io, DISTANCE_TYPE method = CIE2000) {
		switch (method)
		{
		case cv::ccm::CIE76:
		case cv::ccm::CIE94_GRAPHIC_ARTS:
		case cv::ccm::CIE94_TEXTILES:
		case cv::ccm::CIE2000:
		case cv::ccm::CMC_1TO1:
		case cv::ccm::CMC_2TO1:
			return distance(to(Lab(io)).colors, other.to(Lab(io)).colors, method);
			break;
		case cv::ccm::RGB:
			return distance(to(*cs.nl).colors, other.to(*cs.nl).colors, method);
			break;
		case cv::ccm::RGBL:
			return distance(to(*cs.l).colors, other.to(*cs.l).colors, method);
			break;
		default:
			break;
		}
	}

	void get_gray(double JDN = 2.0) {
		Mat lab = to(Lab_D65_2).colors;
		Mat gray(colors.size(), colors.type());
		int fromto[] = { 0,0, -1,1, -1,2 };
		mixChannels(&lab, 1, &gray, 1, fromto, 3);
		Mat d = distance(lab, gray, CIE2000);
		this->grays = d < JDN;
		this->colored = ~grays;
	}

	Color operator[](Mat mask) {
		return Color(mask_copyto(colors, mask), cs);
	}
};

static Mat ColorChecker2005_LAB_D50_2 = (Mat_<Vec3d>(24, 1) <<
	Vec3d(37.986, 13.555, 14.059),
	Vec3d(65.711, 18.13, 17.81),
	Vec3d(49.927, -4.88, -21.925),
	Vec3d(43.139, -13.095, 21.905),
	Vec3d(55.112, 8.844, -25.399),
	Vec3d(70.719, -33.397, -0.199),
	Vec3d(62.661, 36.067, 57.096),
	Vec3d(40.02, 10.41, -45.964),
	Vec3d(51.124, 48.239, 16.248),
	Vec3d(30.325, 22.976, -21.587),
	Vec3d(72.532, -23.709, 57.255),
	Vec3d(71.941, 19.363, 67.857),
	Vec3d(28.778, 14.179, -50.297),
	Vec3d(55.261, -38.342, 31.37),
	Vec3d(42.101, 53.378, 28.19),
	Vec3d(81.733, 4.039, 79.819),
	Vec3d(51.935, 49.986, -14.574),
	Vec3d(51.038, -28.631, -28.638),
	Vec3d(96.539, -0.425, 1.186),
	Vec3d(81.257, -0.638, -0.335),
	Vec3d(66.766, -0.734, -0.504),
	Vec3d(50.867, -0.153, -0.27),
	Vec3d(35.656, -0.421, -1.231),
	Vec3d(20.461, -0.079, -0.973));

static Mat ColorChecker2005_LAB_D65_2 = (Mat_<Vec3d>(24, 1) <<
	Vec3d(37.542, 12.018, 13.33),
	Vec3d(65.2, 14.821, 17.545),
	Vec3d(50.366, -1.573, -21.431),
	Vec3d(43.125, -14.63, 22.12),
	Vec3d(55.343, 11.449, -25.289),
	Vec3d(71.36, -32.718, 1.636),
	Vec3d(61.365, 32.885, 55.155),
	Vec3d(40.712, 16.908, -45.085),
	Vec3d(49.86, 45.934, 13.876),
	Vec3d(30.15, 24.915, -22.606),
	Vec3d(72.438, -27.464, 58.469),
	Vec3d(70.916, 15.583, 66.543),
	Vec3d(29.624, 21.425, -49.031),
	Vec3d(55.643, -40.76, 33.274),
	Vec3d(40.554, 49.972, 25.46),
	Vec3d(80.982, -1.037, 80.03),
	Vec3d(51.006, 49.876, -16.93),
	Vec3d(52.121, -24.61, -26.176),
	Vec3d(96.536, -0.694, 1.354),
	Vec3d(81.274, -0.61, -0.24),
	Vec3d(66.787, -0.647, -0.429),
	Vec3d(50.872, -0.059, -0.247),
	Vec3d(35.68, -0.22, -1.205),
	Vec3d(20.475, 0.049, -0.972));

static Color Macbeth_D50_2(ColorChecker2005_LAB_D50_2, Lab_D50_2);
static Color Macbeth_D65_2(ColorChecker2005_LAB_D65_2, Lab_D65_2);

}
}






