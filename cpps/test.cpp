#include "color.h"
#include "opencv2/core.hpp"
#include <iostream>

using namespace cv;
using namespace std;
using namespace cv::ccm;

void test_cs(void) {
	Color color(ColorChecker2005_LAB_D50_2, Lab_D50_2);
	//cout << "sRGB.M_to: " << sRGB.M_to << endl;
	//cout << "AdobeRGB.M_to: " << AdobeRGB.M_to << endl;
	//cout << "WideGamutRGB.M_to: " << WideGamutRGB.M_to << endl;
	//cout << "ProPhotoRGB.M_to: " << ProPhotoRGB.M_to << endl;
	//cout << "XYZ::_cam(D50_2, D65_2): " << XYZ_D65_2._cam(D50_2, D65_2) << endl;
	//cout << "XYZ::_cam(D55_2, D50_2, VON_KRIS): " << XYZ_D65_2._cam(D55_2, D50_2, VON_KRIS) << endl;
	//cout << "XYZ::_cam(D65_2, D65_2): " << XYZ_D65_2._cam(D65_2, D65_2) << endl;
	cout << "XYZ::_cam(D65_2, D50_2, IDENTITY): " << XYZ_D65_2._cam(D65_2, D50_2, IDENTITY) << endl;
}

void test_color(void) {
	Mat colors = (Mat_<Vec3d>(1, 1) <<
		Vec3d(0.3, 0.2, 0.5));

	Color color(colors, sRGB);
	Color color_rgb = color.to(sRGB);
	print(color_rgb.colors, "color_rgb");
	Color color_rgbl = color.to(sRGBL);
	print(color_rgbl.colors, "color_rgbl");
	Color color_xyz = color.to(XYZ_D65_2);
	print(color_xyz.colors, "color_xyz");
	Color color_lab = color.to(Lab_D65_2);
	print(color_lab.colors, "color_lab");
	Color color_xyz_d50 = color.to(XYZ_D50_2); 
	print(color_xyz_d50.colors, "color_xyz_d50");
	Color color_lab_d50 = color.to(Lab_D50_2);
	print(color_lab_d50.colors, "color_lab_d50");
	print(sRGB.M_to, "sRGB.M_to");
	Mat m = XYZ_D65_2._cam(D65_2, D50_2);
	print(m, "m");
	Mat s =m* sRGB.M_to;
	cout << s << endl;
}

class A {
public:
	virtual int out(void) {
		return 1;
	}
};

class B:public A {
public:
	virtual int out(void) {
		return 2;
	}
};

class C: public B {

};

class D {
public:
	int foo(A a) {
		return a.out();
	}
};

class E {
public:
	template<typename T>
	int foo(T a) {
		return a.out();
	}
};

class F {
public:
	A a;
	//template<typename T>
	F(A a) :a(a) {};
	int foo(){
		return a.out();
	}
};

class G {
public:
	A* a;
	G(A* a) :a(a) {};
	//template<typename T>
	int foo() {
		return a->out();
	}
};

class H {
public:
	A& a;
	H(A& a) :a(a) {};
	//template<typename T>
	int foo() {
		return a.out();
	}
};

class I {
public:
	A a;
	//template<typename T>
	I(A a) :a(a) {};
	int foo() {
		return (&a)->out();
	}
};

void test_test() {
	A a;
	B b;
	C c;
	D d;
	cout << "D" << endl; //1
	cout << d.foo(a) << endl; //1
	cout << d.foo(b) << endl; //1
	cout << d.foo(c) << endl; //1
	E e;
	cout << "E" << endl; //1
	cout << e.foo(a) << endl; //1
	cout << e.foo(b) << endl; //2
	cout << e.foo(c) << endl; //2
	F fa(a), fb(b), fc(c);
	cout << "F" << endl; //1
	cout << fa.foo() << endl; //1
	cout << fb.foo() << endl; //1
	cout << fc.foo() << endl; //1
	G ga(&a), gb(&b), gc(&c);
	cout << "G" << endl; //1
	cout << ga.foo() << endl; //1
	cout << gb.foo() << endl; //2
	cout << gc.foo() << endl; //2
	H ha(a), hb(b), hc(c);
	cout << "H" << endl; //1
	cout << ha.foo() << endl; //1
	cout << hb.foo() << endl; //2
	cout << hc.foo() << endl; //2
	I ia(a), ib(b), ic(c);
	cout << "I" << endl; //1
	cout << ia.foo() << endl; //1
	cout << ib.foo() << endl; //1
	cout << ic.foo() << endl; //1
}

int main() {
	test_color();
	//test_test();
	return 1;
}