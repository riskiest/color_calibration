#include "colorspace.h"
#include "IO.h"

RGB_Base::RGB_Base(void) {
    xr = 0.6400;
    yr = 0.3300;
    xg = 0.21;
    yg = 0.71;
    xb = 0.1500;
    yb = 0.0600;
    io_base = IO("D65", 2);
    gamma = 2.2;
    _M_RGBL2XYZ_base = NULL;
    _M_RGBL2XYZ = {};
    _default_io = IO("D65", 2);
}
              

Mat RGB_Base::cal_M_RGBL2XYZ_base() {
    Mat XYZr,  XYZg, XYZb;
    XYZr = Mat(xyY2XYZ(xr, yr), true);
    XYZg = Mat(xyY2XYZ(xg, yg), true);
    XYZb = Mat(xyY2XYZ(xb, yb), true);
   
    map <IO, vector<double>> illuminants = get_illuminant();
    Mat XYZw = Mat(illuminants[io_base]); 
    Mat XYZ_rgbl;
    XYZ_rgbl.push_back(XYZr);
    XYZ_rgbl.push_back(XYZg);
    
    XYZ_rgbl.push_back(XYZb);
    XYZ_rgbl = XYZ_rgbl.reshape(0, 3);
    XYZ_rgbl = XYZ_rgbl.t();
   
    Mat S = XYZ_rgbl.inv() * XYZw;
 
    Mat Sr = S.rowRange(0, 1).clone();
    Mat Sg = S.rowRange(1, 2).clone();
    Mat Sb = S.rowRange(2, 3).clone();

   
    _M_RGBL2XYZ_base.push_back(Sr * (XYZr.t()));
    _M_RGBL2XYZ_base.push_back(Sg * (XYZg.t()));
    _M_RGBL2XYZ_base.push_back(Sb * (XYZb.t()));
    _M_RGBL2XYZ_base=_M_RGBL2XYZ_base.t();
    return _M_RGBL2XYZ_base;
}

Mat RGB_Base::M_RGBL2XYZ_base() {
    if (!_M_RGBL2XYZ_base.empty()) {
        return _M_RGBL2XYZ_base;
    }
    return cal_M_RGBL2XYZ_base();
}

IO RGB_Base::choose_io(IO io) {
    
    if (io.m_illuminant.length() != 0) {
        return io;
    }
    return _default_io;
}

void RGB_Base::set_default(IO io) {
    _default_io = io;
}

Mat RGB_Base::M_RGBL2XYZ(IO io, bool rev ) {
    io = choose_io(io);
   
    if (_M_RGBL2XYZ.count(io)==1) {
             return _M_RGBL2XYZ[io][rev ? 1 : 0];
         }
 
    if (io.m_illuminant == io_base.m_illuminant && io.m_observer == io_base.m_observer) {
        _M_RGBL2XYZ[io] = { M_RGBL2XYZ_base(), M_RGBL2XYZ_base().inv() };
        return _M_RGBL2XYZ[io][rev ? 1 : 0];
    }
    Mat M_RGBL2XYZ = cam(io_base, io) * M_RGBL2XYZ_base();
    _M_RGBL2XYZ[io] = { M_RGBL2XYZ, M_RGBL2XYZ.inv() };
    return _M_RGBL2XYZ[io][rev ? 1 : 0];
}

Mat RGB_Base::rgbl2xyz(Mat rgbl, IO io) {
    io = choose_io(io);
    Mat _rgbl2xyz(rgbl.size(), rgbl.type());
    for (int i = 0; i < rgbl.rows; i++) {
       
        for (int j = 0; j < rgbl.cols; j++) {
            for (int m = 0; m < 3; m++) {
                double res1 = rgbl.at<Vec3d>(i, j)[0] * M_RGBL2XYZ(io).at<double>(m, 0);
                double res2 = rgbl.at<Vec3d>(i, j)[1] * M_RGBL2XYZ(io).at<double>(m, 1);
                double res3 = rgbl.at<Vec3d>(i, j)[2] * M_RGBL2XYZ(io).at<double>(m, 2);
                _rgbl2xyz.at<Vec3d>(i, j)[m] = res1 + res2 + res3;
            }

        }
    }
   
    return _rgbl2xyz;
}

Mat RGB_Base::xyz2rgbl(Mat xyz, IO io) {
    io = choose_io(io);
    Mat _rgbl2xyz(xyz.size(), xyz.type());
    for (int i = 0; i < xyz.rows; i++) {

        for (int j = 0; j < xyz.cols; j++) {
            for (int m = 0; m < 3; m++) {
                double res1 = xyz.at<Vec3d>(i, j)[0] * M_RGBL2XYZ(io, true).at<double>(m, 0);
                double res2 = xyz.at<Vec3d>(i, j)[1] * M_RGBL2XYZ(io, true).at<double>(m, 1);
                double res3 = xyz.at<Vec3d>(i, j)[2] * M_RGBL2XYZ(io, true).at<double>(m, 2);
                _rgbl2xyz.at<Vec3d>(i, j)[m] = res1 + res2 + res3;
            }

        }
    }
   
    return _rgbl2xyz;
   
}

Mat RGB_Base::rgb2rgbl(Mat rgb) {
    return gamma_correction(rgb, gamma);
}

Mat RGB_Base::rgbl2rgb(Mat rgbl) {
    return gamma_correction(rgbl, 1 / gamma);
}

Mat RGB_Base::rgb2xyz(Mat rgb, IO io) {
    io = choose_io(io);
    return rgbl2xyz(rgb2rgbl(rgb), io);
}

Mat RGB_Base::xyz2rgb(Mat xyz, IO io) {
    io = choose_io(io);
    return rgbl2rgb(xyz2rgbl(xyz, io));
}

Mat RGB_Base::rgbl2lab(Mat rgbl, IO io) {
    io = choose_io(io);
    return xyz2lab(rgbl2xyz(rgbl, io), io);
}

Mat RGB_Base::rgb2lab(Mat rgb, IO io) {
    io = choose_io(io);
    return rgbl2lab(rgb2rgbl(rgb), io);
}

sRGB_Base::sRGB_Base(void) {
    xr = 0.6400;
    yr = 0.3300;
    xg = 0.3000;
    yg = 0.6000;
    xb = 0.1500;
    yb = 0.0600;
    alpha = 1.055;
    beta = 0.0031308;
    phi = 12.92;
    gamma = 2.4;
}


double sRGB_Base::K0() {
    if (_K0) {
        return _K0;
    }
    return beta * phi;
}


double  sRGB_Base::_rgb2rgbl_ele(double x) {
    if (x > K0()) {
        return pow(((x + alpha - 1) / alpha), gamma);
    }

    else if (x >= -K0()) {
        return x / phi;
    }

    else {
        return -(pow(((-x + alpha - 1) / alpha), gamma));
    }

}


Mat  sRGB_Base::rgb2rgbl(Mat rgb) {
    int height = rgb.rows;
    int width = rgb.cols;
    int nc = rgb.channels();
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++) {
           
            for (int nc_ = 0; nc_ < nc; nc_++)
                rgb.at<Vec3d>(row, col)[nc_] = _rgb2rgbl_ele(rgb.at<Vec3d>(row, col)[nc_]);
        }
    }
    return rgb;
}


double  sRGB_Base::_rgbl2rgb_ele(double x) {
    if (x > beta) {
        return alpha*pow(x ,1/ gamma)-(alpha-1);
    }
    else if (x >= -beta) {
        return x * phi;
    }

    else {
        return -(alpha * pow(-x, 1 / gamma) - (alpha - 1));
    }

}


Mat  sRGB_Base::rgbl2rgb(Mat rgbl) {
    int height = rgbl.rows;
    int width = rgbl.cols;
    int nc = rgbl.channels();
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++) {
            for (int nc_ = 0; nc_ < nc; nc_++)
                rgbl.at<Vec3d>(row, col)[nc_] = _rgbl2rgb_ele(rgbl.at<Vec3d>(row, col)[nc_]);
        }
    }
    return rgbl;
}


RGB_Base* get_colorspace(string colorspace) {
    RGB_Base* p = new RGB_Base;
    if (colorspace == "RGB_Base") {
        p = new RGB_Base;
    }
    else if (colorspace == "sRGB_Base") {
        p = new sRGB_Base;
    }
    else if (colorspace == "sRGB") {
        p = new sRGB;
    }
    else if (colorspace == "AdobeRGB") {
        p = new AdobeRGB;
    }
    else if (colorspace == "WideGamutRGB") {
        p = new WideGamutRGB;
    }
    else if (colorspace == "ProPhotoRGB") {
        p = new ProPhotoRGB;
    }
    else if (colorspace == "DCI_P3_RGB") {
        p = new DCI_P3_RGB;
    }
    else if (colorspace == "AppleRGB") {
        p = new AppleRGB;
    }
    else if (colorspace == "REC_709_RGB") {
        p = new REC_709_RGB;
    }
    else if (colorspace == "REC_2020_RGB") {
        p = new REC_2020_RGB;
    }
    return p;
}