#pragma once


#include <string>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <map>
#include <tuple>
#include <cmath>


using namespace std;
using namespace cv;



struct LAB
{
	/* Lightness */
	double l;
	/* Color-opponent a dimension */
	double a;
	/* Color-opponent b dimension */
	double b;
};
using LAB = struct LAB;

double deltaE_cie76(const LAB& lab1, const LAB& lab2);

double to_rad(double degree);

double to_deg(double rad);

double deltacE_cmc(const LAB& lab1, const LAB& lab2, double kL , double kC );

double deltacE_ciede94(const LAB& lab1, const LAB& lab2, double kH, double kC, double kL, double k1, double);

double deltacE_ciede2000(const LAB& lab1, const LAB& lab2, double kL , double kC , double kH );

Mat distance_s(Mat Lab1, Mat Lab2, string distance);