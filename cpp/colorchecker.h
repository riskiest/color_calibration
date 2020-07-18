#ifndef COLORCHECKER_H
#define COLORCHECKER_H

#include <iostream>

#include <string>
#include "colorspace.h"
#include "IO.h"


class ColorChecker
{
public:
	Mat lab;
	IO io;
	Mat rgb;
	RGB_Base* cs;
	Mat white_mask;
	Mat color_mask;
	ColorChecker() {};
	ColorChecker(Mat, string, IO, Mat);
};


class ColorCheckerMetric
{
public:
	ColorChecker cc;
	RGB_Base* cs;
	IO io;
	Mat lab;
	Mat xyz;
	Mat rgb;
	Mat rgbl;
	Mat grayl;
	Mat white_mask;
	Mat color_mask;
	ColorCheckerMetric() {};
	ColorCheckerMetric(ColorChecker colorchecker, string colorspace, IO io_);
};

/*
Mat ColorChecker2005_LAB_D50_2;
Mat ColorChecker2005_LAB_D65_2;
Mat Arange_18_24;
ColorChecker colorchecker_Macbeth;
ColorChecker colorchecker_Macbeth_D65_2;
*/

#endif
