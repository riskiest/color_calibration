#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <vector>
#include <map>
#include <string>

#include "time.h"

using namespace cv;
using namespace std;

//#include "distance.h"
//#include "utils.h"

Mat resh(Mat xyz, Mat ccm) {
    //Mat res(xyz.size(), CV_64FC3);
    int rows = xyz.rows;
    xyz = xyz.reshape(1, xyz.rows * xyz.cols);
    Mat res = xyz*ccm;
    res = res.reshape(3, rows);
    return res;
}


Mat mult(Mat xyz, Mat ccm) {
    //cout<<ccm<<endl;
    //int c = xyz.channels();

    Mat res(xyz.size(), CV_64FC3);
    //cout << "3:" << res.size() <<"," <<xyz.rows<<"," <<xyz.cols << endl;
    for (int i = 0; i < xyz.rows; i++) {
        for (int j = 0; j < xyz.cols; j++) {
            for (int m = 0; m < res.channels(); m++) {//

                res.at<Vec3d>(i,j)[m] = 0;
                for (int n = 0; n < xyz.channels(); n++) {
                    res.at<Vec3d>(i,j)[m] += xyz.at<Vec3d>(i,j)[n] * ccm.at<double>(n, m);
                    /*double res1 = xyz.at<Vec3d>(i, j)[0] * ccm.at<double>(0, m);
                    double res2 = xyz.at<Vec3d>(i, j)[1] * ccm.at<double>(1, m);
                    double res3 = xyz.at<Vec3d>(i, j)[2] * ccm.at<double>(2, m);
                    res.at<Vec3d>(i, j)[m] = res1 + res2 + res3;*/
                }

            }
            //cout << "j:" << j << endl;
        }
        //cout << "i:" << i << endl;
    }
    return res;
}

int main() {
    string imgfile = "C:/vs_workplace/Project1/Project1/input1.png";
    Mat img = imread(imgfile);
    cout << "-1:" << img.size() << "," << img.rows << "," << img.cols << endl;
    Mat img_;
    cvtColor(img, img_, COLOR_BGR2RGB);
    cout << "-2:" << img_.size() << "," << img_.rows << "," << img_.cols << endl;
    img_.convertTo(img_, CV_64FC3);
    img_ = img_ / 255.;

    Mat ccm = (Mat_<double>(3, 3) << 1.2, 0.1, -0.2, 0.4, 0.8, 0.05, 0.8, -0.9, 4.25);

    cout << "1:" << ccm.at<double>(1,1) << endl;
    clock_t start, finish;
    double  duration;
    start = clock();
    cout << "2:" << img_.size() << endl;
    Mat res(img_.size(), img_.type());

   /* for (int i = 0; i < 100; i++) {
        res = mult(img_, ccm);
        cout << "cnt:" << i << endl;
    }

    finish = clock();
    duration = (double)(finish - start) / CLOCKS_PER_SEC;
    cout << "mult time is:" << duration << endl;;

    cout << "\nwait" << endl;*/
    start = clock();

    for (int i = 0; i < 100; i++) {
        res = resh(img_, ccm);
        cout << "cnt:" << i << endl;
    }

    finish = clock();
    duration = (double)(finish - start) / CLOCKS_PER_SEC;
    cout << "resh time is:" << duration;

}