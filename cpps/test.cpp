#include "color.h"
#include "opencv2/core.hpp"
#include <iostream>

using namespace cv;
using namespace std;
using namespace cv::ccm;

int main() {
	Color color(ColorChecker2005_LAB_D50_2, Lab_D50_2);
	cout << "sRGB.M_to: " << sRGB.M_to << endl;
	cout << "AdobeRGB.M_to: " << AdobeRGB.M_to << endl;
	cout << "WideGamutRGB.M_to: " << WideGamutRGB.M_to << endl;
	cout << "ProPhotoRGB.M_to: " << ProPhotoRGB.M_to << endl;
	cout << "XYZ::_cam(D50_2, D65_2): " << XYZ_D65_2._cam(D50_2, D65_2) << endl;
	cout << "XYZ::_cam(D55_2, D50_2, VON_KRIS): " << XYZ_D65_2._cam(D55_2, D50_2, VON_KRIS) << endl;
	cout << "XYZ::_cam(D65_2, D65_2): " << XYZ_D65_2._cam(D65_2, D65_2) << endl;
	cout << "XYZ::_cam(D65_2, D50_2, IDENTITY): " << XYZ_D65_2._cam(D65_2, D50_2, IDENTITY) << endl;

	
}