#include "IO.h"
#include <string>
#include <iostream>
namespace {
    vector<double> illuminants_xy_A_2 = { 0.44757, 0.40745 };
    vector<double> illuminants_xy_A_10 = { 0.45117, 0.40594 };
    vector<double> illuminants_xy_D50_2 = { 0.34567, 0.35850 };
    vector<double> illuminants_xy_D50_10 = { 0.34773, 0.35952 };
    vector<double> illuminants_xy_D55_2 = { 0.33242, 0.34743 };
    vector<double> illuminants_xy_D55_10 = { 0.33411, 0.34877 };
    vector<double> illuminants_xy_D65_2 = { 0.31271, 0.32902 };
    vector<double> illuminants_xy_D65_10 = { 0.31382, 0.33100 };
    vector<double> illuminants_xy_D75_2 = { 0.29902, 0.31485 };
    vector<double> illuminants_xy_E_2 = { 1 / 3, 1 / 3 };
    vector<double> illuminants_xy_E_10 = { 1 / 3, 1 / 3 };
    Mat  Von_Kries_Mat = (Mat_<double>(3, 3) << 0.40024, 0.7076, -0.08081,-0.2263, 1.16532, 0.0457,0., 0., 0.91822);
    Mat Bradford_Mat = (Mat_<double>(3, 3) << 0.8951, 0.2664, -0.1614, -0.7502, 1.7135, 0.0367, 0.0389, -0.0685, 1.0296);
}

 map<IO, vector<double> >  illuminants=get_illuminant();

vector<double>(*xyY)(double, double, double);

 IO::IO(string illuminant, int observer) {
    m_illuminant = illuminant;
    m_observer = observer;


}
IO::~IO() {}




bool IO::operator<(const IO& other)const {//todo why<
    {
        return (m_illuminant < other.m_illuminant || ((m_illuminant == other.m_illuminant) && (m_observer < other.m_observer)));
    }
}


vector<double> xyY2XYZ(double x, double y, double Y) {
    
    double X;
    double Z;
    X = Y * x / y;
    Z = Y / y * (1 - x - y);
    vector <double>  xyY2XYZ(3);
    xyY2XYZ[0] = X;
    xyY2XYZ[1] = Y;
    xyY2XYZ[2] = Z;

    return xyY2XYZ;
}

map <IO, vector<double>> get_illuminant() {
    map<IO, vector<double> >  illuminants_xy;
    illuminants_xy[A_2] = illuminants_xy_A_2;
    illuminants_xy[A_10] = illuminants_xy_A_10;
    illuminants_xy[D50_2] = illuminants_xy_D50_2;
    illuminants_xy[D50_10] = illuminants_xy_D50_10;
    illuminants_xy[D55_2] = illuminants_xy_D55_2;
    illuminants_xy[D55_10] = illuminants_xy_D55_10;
    illuminants_xy[D65_2] = illuminants_xy_D65_2;
    illuminants_xy[D65_10] = illuminants_xy_D65_10;
    illuminants_xy[D75_2] = illuminants_xy_D75_2;
    illuminants_xy[E_2] = illuminants_xy_E_2;
    illuminants_xy[E_10] = illuminants_xy_E_10;
    map <IO, vector<double> >  illuminants1;
    map<IO, vector<double>>::iterator it;
    it = illuminants_xy.begin();
    for (it; it != illuminants_xy.end(); it++)
    {

        double x = it->second[0];
        double y = it->second[1];
        double Y = 1;
        vector<double> res;
        res = xyY2XYZ(x, y, Y);
        illuminants1[it->first] = res;

    }

    illuminants1[D65_2] = { 0.95047, 1.0, 1.08883 };   
    illuminants1[D65_10] = { 0.94811, 1.0, 1.07304 };
    return illuminants1;
}
map <tuple<IO, IO, string>, cv::Mat > CAMs;

Mat cam(IO sio, IO dio, string method) {
   
    Mat  Von_Kries = Von_Kries_Mat;
    Mat Bradford = Bradford_Mat;
    map <String, vector< cv::Mat >> MAs;
    MAs["Identity"] = { Mat::eye(cv::Size(3,3),CV_64FC1) , Mat::eye(cv::Size(3,3),CV_64FC1) };
    MAs["Von_Krie"] = { Von_Kries ,Von_Kries.inv() };
    MAs["Bradford"] = { Bradford ,Bradford.inv() };

    if (CAMs.count(make_tuple(dio, sio, method)) == 1) {//todo count? 
        return CAMs[make_tuple(dio, sio, method)];
    }

    Mat XYZws = Mat(illuminants[dio]);
    Mat XYZWd = Mat(illuminants[sio]);
    Mat MA = MAs[method][0];
    Mat MA_inv = MAs[method][1];
    Mat MA_res1 = MA * XYZws;
    Mat MA_res2 = MA * XYZWd;
    Mat MA_res3 = MA_res1 / MA_res2;
    cv::Mat me = cv::Mat::eye(cv::Size(3, 3), CV_64FC1);
    for (int i = 0; i < 3; i++) {
        me.at<double>(i, i) = MA_res3.at<double>(i, 0);
    }

    Mat M = MA_inv * (me);
    CAMs[make_tuple(dio, sio, method)] = M;
    return M;


}



