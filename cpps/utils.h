#pragma once
#include <functional>
#include <vector>
#include "opencv2\core\core.hpp"

namespace cv {
namespace ccm {

//typedef double (*DoubleFunc)(double);

template<typename F>
Mat _elementwise(Mat src, F&& lambda) {
    Mat dst = src.clone();
    MatIterator_<Vec3d> it, end;
    for (it = dst.begin<Vec3d>(), end = dst.end<Vec3d>(); it != end; ++it) {
        for (int j = 1; j < 3; j++) {
            (*it)[j] = lambda((*it)[j]);
        }
    }
    return dst;
}

template<typename F>
Mat _channelwise(Mat src, F&& lambda) {
    Mat dst = src.clone();
    MatIterator_<Vec3d> it, end;
    for (it = dst.begin<Vec3d>(), end = dst.end<Vec3d>(); it != end; ++it) {
        *it = lambda(*it);
    }
    return dst;
}

template<typename F>
Mat _distancewise(Mat src, Mat ref, F&& lambda) {
    Mat dst = Mat(src.size(), src.depth());
    MatIterator_<Vec3d> it_src = src.begin<Vec3d>(), end_src = src.end<Vec3d>(), 
                it_ref= ref.begin<Vec3d>(), end_ref=ref.end<Vec3d>();
    MatIterator_<double> it_dst = dst.begin<Vec3d>(), end_dst= dst.end<Vec3d>();
    for (; it_src!=end_src; ++it_src,++it_ref,++it_dst) {
        *it_dst = lambda(*it_src, *it_ref);
    }
    return dst;
}


double _gamma_correction(double element, double gamma) {
    return (element >= 0 ? pow(element, gamma) : -pow((-element), gamma));
}

Mat gamma_correction(Mat src, double gamma) {
    return _elementwise(src, [gamma](double element)->double {return _gamma_correction(element, gamma); });
}

Mat mask_copyto(Mat src, Mat mask) {
    Mat src_(countNonZero(mask), 1, src.type());
    int countone = 0;

    for (int i = 0; i < mask.rows; i++) {
        if (mask.at<double>(i, 0)) {
            for (int c = 0; c < src.channels(); c++) {
                src_.at<Vec3d>(countone, 0)[c] = src.at<Vec3d>(i, 0)[c];
            }
            countone++;
        };
    }
    return src_;
}

Mat multiple(Mat xyz, Mat ccm) {
    Mat tmp = xyz.reshape(1, xyz.rows * xyz.cols);
    Mat res = tmp*ccm;
    res = res.reshape(res.cols, xyz.rows);
    return res;
}

//Mat multiple2(Mat xyz, Mat ccm) {
//    Mat tmp = xyz.reshape(1, xyz.rows * xyz.cols);
//    Mat res = tmp * ccm;
//    //res = res.reshape(3, xyz.rows);
//    return res;
//}


Mat saturate(Mat src, double low, double up) {
    Mat src_saturation(src.size(), CV_64FC1);
    for (int i = 0; i < src.rows; ++i) {
        for (int j = 0; j < src.cols; ++j) {
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

Mat M_gray = (Mat_<double>(3, 1) << 0.2126, 0.7152, 0.0722);

Mat rgb2gray(Mat rgb) {
    return multiple(rgb, M_gray);
}

}
}