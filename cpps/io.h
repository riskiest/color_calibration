#pragma once

#include <string>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <map>

namespace cv {
namespace ccm {

class IO
{
public:
	std::string illuminant;
	std::string observer;
	IO() {};
	IO(std::string illuminant, std::string observer) :illuminant(illuminant), observer(observer) {};
	bool operator<(const IO& other)const { 
		return (illuminant < other.illuminant || ((illuminant == other.illuminant) && (observer < other.observer))); 
	}
	bool operator==(IO& other) const{
		return illuminant == other.illuminant && observer == other.observer;
	};
};

static IO A_2("A", "2"), A_10("A", "10"),
	D50_2("D50", "2"), D50_10("D50", "10"),
	D55_2("D55", "2"), D55_10("D55", "10"),
	D65_2("D65", "2"), D65_10("D65", "10"),
	D75_2("D75", "2"), D75_10("D75", "10"),
	E_2("E", "2"), E_10("E", "10");

std::map<IO, std::vector<double>> illuminants_xy = {
	{A_2, { 0.44757, 0.40745 }}, {A_10, { 0.45117, 0.40594 }},
	{D50_2, { 0.34567, 0.35850 }}, {D50_10, { 0.34773, 0.35952 }},
	{D55_2, { 0.33242, 0.34743 }}, {D55_10, { 0.33411, 0.34877 }},
	{D65_2, { 0.31271, 0.32902 }}, {D65_10, { 0.31382, 0.33100 }},
	{D75_2, { 0.29902, 0.31485 }}, {D75_10, { 0.45117, 0.40594 }},
	{E_2, { 1 / 3, 1 / 3 }}, {E_10, { 1 / 3, 1 / 3 }},
};

std::vector<double> xyY2XYZ(std::vector<double> xyY) {
	double Y = xyY.size() >= 3 ? xyY[2] : 1;
	return { Y*xyY[0]/xyY[1],Y,Y/xyY[1]*(1-xyY[0]-xyY[1]) };
}

std::map <IO, std::vector<double>> get_illuminant() {
	std::map <IO, std::vector<double> >  illuminants;
    for (auto it = illuminants_xy.begin(); it != illuminants_xy.end(); it++)
    {

        illuminants[it->first] = xyY2XYZ(it->second);
    }
    return illuminants;
}

std::map<IO, std::vector<double> >  illuminants = get_illuminant();

}
}



