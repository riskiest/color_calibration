#ifndef IO_H
#define IO_H
#include <string>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <map>
#include <tuple>
#include <opencv2/core/mat.hpp>

using namespace std;
using namespace cv;
//extern Mat 

class IO
{
    public:
	string m_illuminant;
	int m_observer;
    public:
	IO() {};
	IO(string, int);
	~IO();
	bool operator<(const IO& other)const;
	

};


//map <IO, vector<double>> get_xyz_ref_white();
//vector<double> xyY2XYZ(double x, double y);
vector<double> xyY2XYZ(double x, double y, double Y=1);
map <IO, vector<double>> get_illuminant();

Mat cam(IO , IO ,string method = "Bradford");
extern map<IO, vector<double> >  illuminants;
static IO A_2("A", 2), A_10("A", 10), D50_2("D50", 2), D50_10("D50", 10), D55_2("D55", 2), D55_10("D55", 10), D65_2("D65", 2), D65_10("D65", 10), D75_2("D75", 2), D75_10("D75", 10), E_2("E", 2), E_10("E", 10);

#endif