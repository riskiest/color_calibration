#include <iostream>
#include <opencv2/opencv.hpp>
#include <vector>
#include <map>
#include <string>
#include "IO.h"
#include "distance.h"
//#include "colorspace.h"


using namespace cv;
using namespace std;

//LAB  f_xyz2lab(double  X, double  Y, double Z,LAB lab, double Xn, double Yn, double Zn);
void f_xyz2lab(double  X, double  Y, double Z,double& L, double& a, double& b, double Xn, double Yn, double Zn);
double gamma_correction_f(double  f, double gamma);

Mat  saturate(Mat src, double low, double up);

Mat xyz2grayl(Mat xyz);

Mat xyz2lab(Mat xyz, IO io);

double  r_revise(double x);

void f_lab2xyz(double l, double a, double b, double& x, double& y, double& z, double Xn, double Yn, double Zn);

Mat lab2xyz(Mat lab, IO io);

Mat rgb2gray(Mat rgb);

Mat xyz2xyz(Mat xyz, IO sio, IO dio);

Mat lab2lab(Mat lab, IO sio, IO dio);

Mat gamma_correction(cv::Mat& src, float K);

double gamma_correction_f(double f, double gamma);
