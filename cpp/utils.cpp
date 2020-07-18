#include <iostream>
#include <opencv2/opencv.hpp>
#include <vector>
#include <map>
#include <string>

#include "distance.h"
#include "utils.h"




using namespace cv;
using namespace std;

namespace {
    Mat togray_Mat = (Mat_<double>(3, 1) << 0.2126, 0.7152, 0.0722); 
}

Mat saturate(Mat src, double low, double up) {
 
    Mat src_saturation(src.size(), CV_64FC1);
  
    for (int i = 0; i < src.rows; i++) {
        
        for (int j = 0; j < src.cols; j++) {
          
          //  bool saturation_ij = true;
            double saturation_ij = 1;
            for (int m = 0; m < 3; m++) {
                if (not((src.at<Vec3d>(i, j)[m] < up) && (src.at<Vec3d>(i, j)[m] > low))) {
                    saturation_ij = 0;
                    break;
                }
            }
            src_saturation.at<double>(i, j) = saturation_ij;
        }
    }
    return src_saturation;
}

Mat xyz2grayl(Mat xyz) {
    vector<Mat> channels;
    split(xyz, channels);
    return channels[1];
}

Mat xyz2lab(Mat xyz, IO io) { 
    vector<double> xyz_ref_white_io = illuminants[io];
    Mat lab(xyz.size(), xyz.type());
    Mat channel(cv::Size(xyz.rows, xyz.cols), CV_32FC3);
   
    for (int i = 0; i < xyz.rows; i++) {
        for (int j = 0; j < xyz.cols; j++) {       
            f_xyz2lab(xyz.at<Vec3d>(i, j)[0], xyz.at<Vec3d>(i, j)[1], xyz.at<Vec3d>(i, j)[2],//x,y,z
                     lab.at<Vec3d>(i, j)[0], lab.at<Vec3d>(i, j)[1], lab.at<Vec3d>(i, j)[2], //L,a,b
                     xyz_ref_white_io[0], xyz_ref_white_io[1], xyz_ref_white_io[2]);//Xn, Yn, Zn
        }
    }
    return lab;
}

void f_xyz2lab(double  X, double  Y, double Z,
    double& L, double& a, double& b, double Xn, double Yn, double Zn)//todo cv引用过来
{
    // CIE XYZ values of reference white point for D65 illuminant
   // static const float Xn = 0.950456f, Yn = 1.f, Zn = 1.088754f;

    // Other coefficients below:
    // 7.787f    = (29/3)^3/(29*4)
    // 0.008856f = (6/29)^3
    // 903.3     = (29/3)^3

    double x = X / Xn, y = Y / Yn, z = Z / Zn;
    auto f = [](double t) { return t > 0.008856 ? std::cbrtl(t) : (7.787 * t + 16.0 / 116.0); };
    double fx = f(x), fy = f(y), fz = f(z);
    L = y > 0.008856 ? (116.0 * std::cbrtl(y) - 16.0) : (903.3 * y);
    a = 500.0 * (fx - fy);
    b = 200.0 * (fy - fz);
}
double  r_revise(double x) {  
    return x = (x > 6.0 / 29.0) ? pow(x, 3.0) : (x - 16.0 / 116.0) * 3 * powl(6.0 / 29.0, 2);  
}

void f_lab2xyz(double l, double a, double b, double& x, double& y, double& z, double Xn, double Yn, double Zn) {
    double Y = (l + 16.0) / 116.0;
    double X = Y + a / 500.0;
    double Z = Y - b / 200.0;

    if (z < 0) {
        z = 0;
    }
    x = r_revise(X) * Xn;
    y = r_revise(Y) * Yn;
    z = r_revise(Z) * Zn;
}

Mat lab2xyz(Mat lab, IO io) {

    vector<double> xyz_ref_white_io = illuminants[io];
    Mat xyz(lab.size(), lab.type());
    for (int i = 0; i < lab.rows; i++) {
        for (int j = 0; j < lab.cols; j++) {

            f_lab2xyz(lab.at<Vec3d>(i, j)[0], lab.at<Vec3d>(i, j)[1], lab.at<Vec3d>(i, j)[2],// l, a, b,
                     xyz.at<Vec3d>(i, j)[0], xyz.at<Vec3d>(i, j)[1], xyz.at<Vec3d>(i, j)[2],//x, y, z, 
                      xyz_ref_white_io[0], xyz_ref_white_io[1], xyz_ref_white_io[2]);// Xn, Yn, Zn);
        }
    }
    return xyz;
}

Mat rgb2gray(Mat rgb) {
    Mat togray = togray_Mat;
    Mat gray(rgb.rows, rgb.cols, CV_64FC1);
    for (int i = 0; i < rgb.rows; i++) {
        for (int j = 0; j < rgb.cols; j++) {
            double res1 = rgb.at<Vec3d>(i, j)[0] * togray.at<double>(0, 0);
            double res2 = rgb.at<Vec3d>(i, j)[1] * togray.at<double>(1, 0);
            double res3 = rgb.at<Vec3d>(i, j)[2] * togray.at<double>(2, 0);
            gray.at<double>(i, j) = res1 + res2 + res3;
        }
    }
    return gray;
}

Mat xyz2xyz(Mat xyz, IO sio, IO dio) {

    if (sio.m_illuminant == dio.m_illuminant && sio.m_observer == dio.m_observer) {
        return xyz;
    }
    else {
        Mat cam(IO, IO, string);
        Mat cam_M = cam(sio, dio, "Bradford");
        Mat cam_res;
        cam_res.create(xyz.size(), xyz.type());
        for (int i = 0; i < xyz.rows; i++) {
            for (int j = 0; j < xyz.cols; j++) {
                for (int m = 0; m < 3; m++) {//矩阵乘法
                    double res1 = xyz.at<Vec3d>(i, j)[0] * cam_M.at<double>(m, 0);
                    double res2 = xyz.at<Vec3d>(i, j)[1] * cam_M.at<double>(m, 1);
                    double res3 = xyz.at<Vec3d>(i, j)[2] * cam_M.at<double>(m, 2);
                    cam_res.at<Vec3d>(i, j)[m] = res1 + res2 + res3;
                }
            }
        }
        return cam_res;
    }
}

Mat lab2lab(Mat lab, IO sio, IO dio) {
    if (sio.m_illuminant == dio.m_illuminant && sio.m_observer == dio.m_observer) {
        return lab;
    }
    return xyz2lab(xyz2xyz(lab2xyz(lab, sio), sio, dio), dio);
}

double gamma_correction_f(double f, double gamma) {//todo 3行三元表达式
    double k = f >= 0 ? pow(f, gamma) : -pow((-f), gamma);
    return k;
}

Mat gamma_correction(cv::Mat& src, float K) {
    Mat dst(src.size(),src.type());
    for (int row = 0; row < src.rows; row++) {
        for (int col = 0; col < src.cols; col++) {
            for (int m=0;m<3;m++) dst.at<Vec3d>(row, col)[m] = gamma_correction_f(src.at<Vec3d>(row, col)[m], K);
        }
    }
    return dst;
}
