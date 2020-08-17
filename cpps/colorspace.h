#pragma once
//#include "utils.h"
#include "io.h"
#include "operations.h"
#include "utils.h"
#include <vector>
#include <string>
#include <iostream>

//using namespace std;

namespace cv {
namespace ccm{

class ColorSpace {
public:
	IO io;
	std::string type;
	bool linear;
	Operations to;
	Operations from;
	ColorSpace* l = 0;
	ColorSpace* nl = 0;

	ColorSpace() {};
	//ColorSpace(IO io) :io(io) {};
	//ColorSpace(bool linear):linear(linear) {};
	//ColorSpace(IO io, std::string type, bool linear) :io(io), type(type), linear(linear){
	//	io.out();
	//};
	ColorSpace(IO io, std::string type, bool linear) :io(io),type(type), linear(linear) {};

	virtual bool relate(ColorSpace other) {
		return (type == other.type) && (io == other.io);
	};
	virtual Operations relation(ColorSpace other) {
		return identity;
	};

	bool operator<(const ColorSpace& other)const {
		if (io < other.io) {
			return true;
		}
		if (type < other.type) {
			return true;
		}
		if (linear < other.linear) {
			return true;
		}
	}
};

class RGB_Base_ : public ColorSpace {
public:
	//IO io;
	//std::string type = "RGB";
	//bool linear;
	RGB_Base_* l = 0;
	RGB_Base_* nl = 0;
	double xr;
	double yr;
	double xg;
	double yg;
	double xb;
	double yb;
	//Operations to;
	//Operations from;
	MatFunc toL;
	MatFunc fromL;
	Mat M_to;
	Mat M_from;

	using ColorSpace::ColorSpace;

	virtual Operations relation(RGB_Base_ other) {
		if (linear == other.linear) { return identity; }
		if (linear) { return Operations({ Operation(fromL) }); }
		return Operations({ Operation(toL) });
	};

	void init() {
		//_set_base(linear);
		_set_parameter();
		_cal_linear();
		_cal_M();
		_cal_operations();
	}

	virtual void _set_parameter() {};

	virtual void _cal_M() {
		Mat XYZr, XYZg, XYZb, XYZ_rgbl, Srgb;
		XYZr = Mat(xyY2XYZ({ xr, yr }), true);
		XYZg = Mat(xyY2XYZ({ xg, yg }), true);
		XYZb = Mat(xyY2XYZ({ xb, yb }), true);
		merge(std::vector<Mat>{ XYZr, XYZg, XYZb }, XYZ_rgbl);
		XYZ_rgbl = XYZ_rgbl.reshape(1, XYZ_rgbl.rows);
		//std::cout << XYZ_rgbl << std::endl;
		//std::cout << io.illuminant << " " << io.observer << std::endl;

		Mat XYZw = Mat(illuminants[io], true);
		//std::cout << XYZw << std::endl;
		solve(XYZ_rgbl, XYZw, Srgb);
		merge(std::vector<Mat>{ Srgb.at<double>(0)* XYZr, 
			Srgb.at<double>(1)* XYZg, 
			Srgb.at<double>(2)* XYZb }, M_to);
		M_to = M_to.reshape(1, M_to.rows);
		M_from = M_to.inv();		
		//std::cout << M_to << std::endl;
		//std::cout << M_from << std::endl;
	};

	virtual void _cal_operations() {
		toL = [this](Mat rgb) {return _toL(rgb); };
		fromL = [this](Mat rgbl) {return _fromL(rgbl); };
		if (linear) {
			to = Operations({ Operation(M_to.t()) });
			from = Operations({ Operation(M_from.t()) });
		}
		else {
			to = Operations({ Operation(toL), Operation(M_to.t()) });
			from = Operations({ Operation(M_from.t()), Operation(fromL) });
		}
	}

	virtual void _cal_linear() {}

	virtual Mat _toL(Mat rgb) { return Mat(); };
	virtual Mat _fromL(Mat rgbl) { return Mat(); };

	void bind(RGB_Base_& rgbl) {
		init();
		rgbl.init();
		l = &rgbl;
		rgbl.l = &rgbl;
		nl = this;
		rgbl.nl = this;
	}

};

class AdobeRGB_Base_ : public RGB_Base_ {
public:
	using RGB_Base_::RGB_Base_;
	double gamma;
	virtual Mat _toL(Mat rgb) {
		return gamma_correction(rgb, gamma);
	}
	virtual Mat _fromL(Mat rgbl) {
		return gamma_correction(rgbl, 1. / gamma);
	}
};

class sRGB_Base_ : public RGB_Base_ {
public:
	using RGB_Base_::RGB_Base_;
	//sRGB_Base_(IO io, std::string type, bool linear, double xr, double yr, double xg, double yg, double xb, double yb, double a, double gamma) :
	//	test_(io.out()),a(a), gamma(gamma), RGB_Base_(io, type, linear, xr, yr, xg, yg, xb, yb) {};
	double a;
	double gamma;
	double alpha;
	double beta;
	double phi;
	double K0;
	//bool test_;

	virtual void _cal_linear() {
		alpha = a + 1;
		K0 = a / (gamma - 1);
		phi = (pow(alpha, gamma) * pow(gamma - 1, gamma - 1)) / (pow(a, gamma - 1) * pow(gamma, gamma));
		beta = K0 / phi;
	}

	double _toL_ew(double x) {
		if (x > K0) {
			return pow(((x + alpha - 1) / alpha), gamma);
		}
		else if (x >= -K0) {
			return x / phi;
		}
		else {
			return -(pow(((-x + alpha - 1) / alpha), gamma));
		}
	}

	Mat _toL(Mat rgb) {
		return _elementwise(rgb, [this](double a)->double {return _toL_ew(a); });
	}

	double _fromL_ew(double x) {
		if (x > beta) {
			return alpha * pow(x, 1 / gamma) - (alpha - 1);
		}
		else if (x >= -beta) {
			return x * phi;
		}
		else {
			return -(alpha * pow(-x, 1 / gamma) - (alpha - 1));
		}

	}

	Mat _fromL(Mat rgbl) {
		return _elementwise(rgbl, [this](double a)->double {return _fromL_ew(a); });
	}
};

class sRGB_ :public sRGB_Base_ {
public:
	sRGB_(bool linear):sRGB_Base_(D65_2, "sRGB", linear) {};

	void _set_parameter() {
		xr = 0.64;
		yr = 0.33;
		xg = 0.3;
		yg = 0.6;
		xb = 0.15;
		yb = 0.06;
		a = 0.055;
		gamma = 2.4;
	}
};

class AdobeRGB_ : public AdobeRGB_Base_ {
public:
	AdobeRGB_(bool linear = false) :AdobeRGB_Base_(D65_2, "AdobeRGB", linear) {};
	
	void _set_parameter() {
		xr = 0.64;
		yr = 0.33;
		xg = 0.21;
		yg = 0.71;
		xb = 0.15;
		yb = 0.06;
		gamma = 2.2;
	}

};

class WideGamutRGB_ : public AdobeRGB_Base_ {
public:
	//using AdobeRGB_Base_::AdobeRGB_Base_;
	WideGamutRGB_(bool linear = false) :AdobeRGB_Base_(D50_2, "WideGamutRGB", linear) {};
	
	void _set_parameter() {
		xr = 0.7347;
		yr = 0.2653;
		xg = 0.1152;
		yg = 0.8264;
		xb = 0.1566;
		yb = 0.0177;
		gamma = 2.2;
	}

};


class ProPhotoRGB_ : public AdobeRGB_Base_ {
public:
	//using AdobeRGB_Base_::AdobeRGB_Base_;
	ProPhotoRGB_(bool linear = false) :AdobeRGB_Base_(D50_2, "ProPhotoRGB", linear) {};

	void _set_parameter() {
		xr = 0.734699;
		yr = 0.265301;
		xg = 0.159597;
		yg = 0.820403;
		xb = 0.036598;
		yb = 0.000105;
		gamma = 1.8;
	}

	//IO io = D50_2;
	//std::string type = "WideGamutRGB";
	//bool linear;
	//double xr = 0.734699;
	//double yr = 0.265301;
	//double xg = 0.159597;
	//double yg = 0.820403;
	//double xb = 0.036598;
	//double yb = 0.000105;
	//double gamma = 1.8;
};


class DCI_P3_RGB_ : public AdobeRGB_Base_ {
public:
	DCI_P3_RGB_(bool linear = false) :AdobeRGB_Base_(D65_2, "DCI_P3_RGB", linear) {};

	void _set_parameter() {
		xr = 0.68;
		yr = 0.32;
		xg = 0.265;
		yg = 0.69;
		xb = 0.15;
		yb = 0.06;
		gamma = 2.2;
	}

	//using AdobeRGB_Base_::AdobeRGB_Base_;

	//IO io = D65_2;
	//std::string type = "DCI_P3_RGB";
	//bool linear;
	//double xr = 0.68;
	//double yr = 0.32;
	//double xg = 0.265;
	//double yg = 0.69;
	//double xb = 0.15;
	//double yb = 0.06;
	//double gamma = 2.2;
};


class AppleRGB_ : public AdobeRGB_Base_ {
public:
	AppleRGB_(bool linear = false) :AdobeRGB_Base_(D65_2, "AppleRGB", linear) {};

	void _set_parameter() {
		xr = 0.625;
		yr = 0.34;
		xg = 0.28;
		yg = 0.595;
		xb = 0.155;
		yb = 0.07;
		gamma = 1.8;
	}

	//using AdobeRGB_Base_::AdobeRGB_Base_;

	//IO io = D65_2;
	//std::string type = "AppleRGB";
	//bool linear;
	//double xr = 0.625;
	//double yr = 0.34;
	//double xg = 0.28;
	//double yg = 0.595;
	//double xb = 0.155;
	//double yb = 0.07;
	//double gamma = 1.8;
};


class REC_709_RGB_ : public sRGB_Base_ {
public:
	REC_709_RGB_(bool linear) :sRGB_Base_(D65_2, "REC_709_RGB", linear) {};

	void _set_parameter() {
		xr = 0.64;
		yr = 0.33;
		xg = 0.3;
		yg = 0.6;
		xb = 0.15;
		yb = 0.06;
		a = 0.099;
		gamma = 1 / 0.45;
	}

	//REC_709_RGB_(bool linear) :sRGB_Base_(io = D65_2, type = "sRGB", linear = linear, xr = 0.65, yr = 0.33,
	//	xg = 0.3, yg = 0.6, xb = 0.15, yb = 0.06, a = 0.055, gamma = 2.4) {};

	//using sRGB_Base_::sRGB_Base_;

	//IO io = D65_2;
	//std::string type = "REC_709_RGB";
	//bool linear;
	//double xr = 0.64;
	//double yr = 0.33;
	//double xg = 0.3;
	//double yg = 0.6;
	//double xb = 0.15;
	//double yb = 0.06;
	//double a = 0.099;
	//double gamma = 1 / 0.45;
};


class REC_2020_RGB_ : public sRGB_Base_ {
public:
	//REC_2020_RGB_(bool linear) :sRGB_Base_(io = D65_2, type = "sRGB", linear = linear, xr = 0.65, yr = 0.33,
	//	xg = 0.3, yg = 0.6, xb = 0.15, yb = 0.06, a = 0.055, gamma = 2.4) {};

	REC_2020_RGB_(bool linear) :sRGB_Base_(D65_2, "REC_2020_RGB", linear) {};

	void _set_parameter() {
		xr = 0.708;
		yr = 0.292;
		xg = 0.17;
		yg = 0.797;
		xb = 0.131;
		yb = 0.046;
		a = 0.09929682680944;
		gamma = 1 / 0.45;
	}

	//using sRGB_Base_::sRGB_Base_;

	//IO io = D65_2;
	//std::string type = "REC_2020_RGB";
	//bool linear;
	//double xr = 0.708;
	//double yr = 0.292;
	//double xg = 0.17;
	//double yg = 0.797;
	//double xb = 0.131;
	//double yb = 0.046;
	//double a = 0.09929682680944;
	//double gamma = 1 / 0.45;
};

sRGB_ sRGB(false), sRGBL(true);
AdobeRGB_ AdobeRGB(false), AdobeRGBL(true);
WideGamutRGB_ WideGamutRGB(false), WideGamutRGBL(true);
ProPhotoRGB_ ProPhotoRGB(false), ProPhotoRGBL(true);
DCI_P3_RGB_ DCI_P3_RGB(false), DCI_P3_RGBL(true);
AppleRGB_ AppleRGB(false), AppleRGBL(true);
REC_709_RGB_ REC_709_RGB(false), REC_709_RGBL(true);
REC_2020_RGB_ REC_2020_RGB(false), REC_2020_RGBL(true);

class _ColorSpaceInitial {
public:
	_ColorSpaceInitial() {
		sRGB.bind(sRGBL);
		AdobeRGB.bind(AdobeRGBL);
		WideGamutRGB.bind(WideGamutRGBL);
		ProPhotoRGB.bind(ProPhotoRGBL);
		DCI_P3_RGB.bind(DCI_P3_RGBL);
		AppleRGB.bind(AppleRGBL);
		REC_709_RGB.bind(REC_709_RGBL);
		REC_2020_RGB.bind(REC_2020_RGBL);
	}
};

_ColorSpaceInitial color_space_initial;

enum CAM {
	IDENTITY,
	VON_KRIS,
	BRADFORD
};

class XYZ :public ColorSpace {
public:
	//IO io;
	//std::string type = "XYZ";
	//Operations to;
	//Operations from;

	std::map <std::tuple<IO, IO, CAM>, cv::Mat > CAMs;
	//const static Mat Von_Kries;
	//const static Mat Bradford;
	//const static std::map <CAM, std::vector< Mat >> MAs;

	Mat Von_Kries = (Mat_<double>(3, 3) << 0.40024, 0.7076, -0.08081, -0.2263, 1.16532, 0.0457, 0., 0., 0.91822);
	Mat Bradford = (Mat_<double>(3, 3) << 0.8951, 0.2664, -0.1614, -0.7502, 1.7135, 0.0367, 0.0389, -0.0685, 1.0296);
	std::map <CAM, std::vector< Mat >> MAs = {
		{IDENTITY , {Mat::eye(cv::Size(3,3),CV_64FC1) , Mat::eye(cv::Size(3,3),CV_64FC1)} },
		{VON_KRIS, { Von_Kries ,Von_Kries.inv() }},
		{BRADFORD, { Bradford ,Bradford.inv() }}
	};


	//using ColorSpace::ColorSpace;
	XYZ(IO io) : ColorSpace(io, "XYZ", true) {};

	Mat _cam(IO sio, IO dio, CAM method = BRADFORD) {
		if (sio == dio) {
			return Mat::eye(cv::Size(3, 3), CV_64FC1);
		}
		if (CAMs.count(std::make_tuple(dio, sio, method)) == 1) {
			return CAMs[std::make_tuple(dio, sio, method)];
		}

		Mat XYZws = Mat(illuminants[dio]);
		Mat XYZWd = Mat(illuminants[sio]);
		Mat MA = MAs.at(method)[0];
		Mat MA_inv = MAs.at(method)[1];
		//print(XYZws, "XYZws");
		//print(XYZWd, "XYZWd");
		//print(MA, "MA");
		//print(MA_inv, "MA_inv");
		//Mat tmp1 = MA * (XYZws);
		//print(tmp1, "tmp1");
		//Mat tmp2 = MA * (XYZWd);
		//print(tmp2, "tmp2");
		//Mat tmp3 = tmp1 / tmp2;
		//print(tmp3, "tmp3");
		//Mat tmp4 = Mat::diag(tmp3);
		////tmp4.diag(tmp3);
		//print(tmp4, "tmp4");
		//Mat M = MA_inv * tmp4 * MA;
		//print(M, "M");

		Mat M = MA_inv * Mat::diag((MA * XYZws) / (MA * XYZWd)) * MA;

		CAMs[std::make_tuple(dio, sio, method)] = M;
		CAMs[std::make_tuple(sio, dio, method)] = M.inv();
		return M;
	}

	Operations cam(IO dio, CAM method = BRADFORD) {
		return (io == dio) ? Operations() : Operations({ Operation(_cam(io,dio,method).t()) });
	}
};



XYZ XYZ_D65_2(D65_2);
XYZ XYZ_D50_2(D50_2);

class Lab :public ColorSpace {
public:
	//IO io;
	//std::string type = "Lab";
	//Operations to{ Operation([this](Mat src) {return _to(src); }) };
	//Operations from{ Operation([this](Mat src) {return _from(src); }) };

	Lab(IO io) : ColorSpace(io, "XYZ", true) {
		to = { Operation([this](Mat src) {return _to(src); }) };
		from = { Operation([this](Mat src) {return _from(src); }) };
	}


	//using ColorSpace::ColorSpace;
	//Lab(IO io) :io(io) {};
private:
	static constexpr double delta = (6./29.);
	static constexpr double m = 1. / (3. * delta * delta);
	static constexpr double t0 = delta*delta*delta;
	static constexpr double c = 4. / 29.;
	//static const 

public:
	Vec3d __from(Vec3d xyz) {
		double x = xyz[0] / illuminants[io][0], y = xyz[1] / illuminants[io][1], z = xyz[2] / illuminants[io][2];
		auto f = [this](double t) { return t > t0 ? std::cbrtl(t) : (m * t + c); };
		double fx = f(x), fy = f(y), fz = f(z);
		return { 116. * fy - 16. ,500 * (fx - fy),200 * (fy - fz) };		
	}

	Mat _from(Mat src) {
		return _channelwise(src, [this](Vec3d a)->Vec3d {return __from(a); });
	}

	Vec3d __to(Vec3d lab) {
		auto f_inv = [this](double t) {return t > delta ? pow(t, 3.0) : (t - c) / m; };
		double L = (lab[0] + 16.) / 116., a = lab[1] / 500., b = lab[2] / 200.;
		return { illuminants[io][0] * f_inv(L + a),illuminants[io][1] * f_inv(L),illuminants[io][2] * f_inv(L - b) };
	}

	Mat _to(Mat src) {
		return _channelwise(src, [this](Vec3d a)->Vec3d {return __to(a); });
	}

};

Lab Lab_D65_2(D65_2);
Lab Lab_D50_2(D50_2);

}
}
