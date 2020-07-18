#ifndef LINEARIZE_H
#define LINEARIZE_H

#include "utils.h"
#include "colorchecker.h"

using namespace std;
using namespace cv;

class Linear
{
public:
    Linear() {}
    Linear(float gamma_, int deg, Mat src, ColorCheckerMetric cc, vector<double> saturated_threshold) {}
    virtual void calc(void) {}
    virtual Mat linearize(Mat inp);
    virtual void value(void) {}
    Mat polyfit(Mat src_x, Mat src_y, int order);
    Mat poly1d(Mat src, Mat w, int deg);
    Mat _polyfit(Mat src, Mat dst, int deg);
    Mat _lin(Mat p, Mat x, int deg);
    Mat mask_copyto(Mat src, Mat mask);
    Mat mask_copyto_gray(Mat src, Mat mask);

};


class Linear_identity : public Linear
{
public:
    using Linear::Linear;
};


class Linear_gamma : public Linear
{
public:
    float gamma;
    Linear_gamma() {};
    Linear_gamma(float gamma_, int deg, Mat src, ColorCheckerMetric cc, vector<double> saturated_threshold);
    Mat linearize(Mat inp);
};


class Linear_color_polyfit : public Linear
{
public:
    int deg;
    Mat mask;
    Mat src;
    Mat dst;
    Mat pr, pg, pb;
    
    Linear_color_polyfit() {};
    Linear_color_polyfit(float gamma, int deg, Mat src, ColorCheckerMetric cc, vector<double> saturated_threshold);
    void calc(void);
    Mat linearize(Mat inp);

};


class Linear_color_logpolyfit : public Linear
{
public:
    int deg;
    Mat mask;
    Mat src;
    Mat dst;
    Mat pr, pg, pb;
    Linear_color_logpolyfit() {};
    Linear_color_logpolyfit(float gamma, int deg, Mat src, ColorCheckerMetric cc, vector<double> saturated_threshold);
    void calc(void);
    Mat linearize(Mat inp);
   // Mat _polyfit(Mat src, Mat dst, int deg);
   // Mat _lin(Mat p, Mat x);
};


class Linear_gray_polyfit : public Linear
{
public:
    int deg;
    Mat mask;
    Mat src;
    Mat dst;
    Mat p;
    Linear_gray_polyfit() {};
    Linear_gray_polyfit(float gamma, int deg, Mat src, ColorCheckerMetric cc, vector<double> saturated_threshold);
    void calc(void);
    Mat linearize(Mat inp);
};


class Linear_gray_logpolyfit : public Linear
{
public:
    int deg;
    Mat mask;
    Mat src;
    Mat dst;
    Mat p;
    Linear_gray_logpolyfit() {};
    Linear_gray_logpolyfit(float gamma, int deg, Mat src, ColorCheckerMetric cc, vector<double> saturated_threshold);
    void calc(void);
    Mat linearize(Mat inp);
   // Mat _polyfit(Mat src, Mat dst, int deg);
   // Mat _lin(Mat p, Mat x);
};



Linear* get_linear(string linear);
#endif
