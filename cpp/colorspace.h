#ifndef COLORSPACE_H
#define COLORSPACE_H

#include "utils.h"
#include "IO.h"

using namespace std;
using namespace cv;

class RGB_Base
{
public:
    double xr;
    double yr;
    double xg;
    double yg;
    double xb;
    double yb;
    IO io_base;
    double gamma;
    Mat _M_RGBL2XYZ_base;
    map<IO, vector<Mat>> _M_RGBL2XYZ;
    IO _default_io;

    RGB_Base();

    virtual Mat cal_M_RGBL2XYZ_base();
    virtual Mat M_RGBL2XYZ_base();
    virtual IO choose_io(IO io);
    virtual void set_default(IO io);
    virtual Mat M_RGBL2XYZ(IO io, bool rev = false);
    virtual Mat rgbl2xyz(Mat rgbl, IO io);
    virtual Mat xyz2rgbl(Mat xyz, IO io);
    virtual Mat rgb2rgbl(Mat rgb);
    virtual Mat rgbl2rgb(Mat rgbl);
    virtual Mat rgb2xyz(Mat rgb, IO io);
    virtual Mat xyz2rgb(Mat xyz, IO io);
    virtual Mat rgbl2lab(Mat rgbl, IO io);
    virtual Mat rgb2lab(Mat rgb, IO io);
};


class sRGB_Base : public RGB_Base
{
public:
    double xr;
    double yr;
    double xg;
    double yg;
    double xb;
    double yb;
    double alpha;
    double beta;
    double phi;
    double gamma;
    double _K0;

    sRGB_Base();

    double K0();
    double _rgb2rgbl_ele(double x);
    Mat rgb2rgbl(Mat rgb);
    double _rgbl2rgb_ele(double x);
    Mat rgbl2rgb(Mat rgbl);
};


class sRGB : public sRGB_Base
{
public:
    Mat _M_RGBL2XYZ_base;
    sRGB() : sRGB_Base() {
        Mat _M_RGBL2XYZ_base = (Mat_<double>(3, 3) <<
            0.41239080, 0.35758434, 0.18048079,
            0.21263901, 0.71516868, 0.07219232,
            0.01933082, 0.11919478, 0.95053215);
    }
};


class AdobeRGB : public RGB_Base {
public:
    using RGB_Base::RGB_Base;
};


class WideGamutRGB : public RGB_Base {
public:
    WideGamutRGB() : RGB_Base() {
        xr = 0.7347;
        yr = 0.2653;
        xg = 0.1152;
        yg = 0.8264;
        xb = 0.1566;
        yb = 0.0177;
        io_base = IO("D65", 2);
    }
};


class ProPhotoRGB : public RGB_Base {
public:
    ProPhotoRGB() : RGB_Base() {
        xr = 0.734699;
        yr = 0.265301;
        xg = 0.159597;
        yg = 0.820403;
        xb = 0.036598;
        yb = 0.000105;
        io_base = IO("D65", 2);
    }
};


class DCI_P3_RGB : public RGB_Base {
public:
    DCI_P3_RGB() : RGB_Base() {
        xr = 0.680;
        yr = 0.32;
        xg = 0.265;
        yg = 0.69;
        xb = 0.15;
        yb = 0.06;
    }
};


class AppleRGB : public RGB_Base {
public:
    AppleRGB() : RGB_Base() {
        xr = 0.626;
        yr = 0.34;
        xg = 0.28;
        yg = 0.595;
        xb = 0.155;
        yb = 0.07;
        gamma = 1.8;
    }
};


class REC_709_RGB : public sRGB_Base {
public:
    REC_709_RGB() : sRGB_Base() {
        xr = 0.64;
        yr = 0.33;
        xg = 0.3;
        yg = 0.6;
        xb = 0.15;
        yb = 0.06;
        alpha = 1.099;
        beta = 0.018;
        phi = 4.5;
        gamma = 1 / 0.45;
    }
};


class REC_2020_RGB : public sRGB_Base {
public:
    REC_2020_RGB() : sRGB_Base() {
        xr = 0.708;
        yr = 0.292;
        xg = 0.17;
        yg = 0.797;
        xb = 0.131;
        yb = 0.046;
        alpha = 1.09929682680944;
        beta = 0.018053968510807;
        phi = 4.5;
        gamma = 1 / 0.45;
    }
};


RGB_Base* get_colorspace(string colorspace);


#endif