#include <string>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <map>
#include <tuple>
#include <cmath>
#include "distance.h"
#include "IO.h"
#include "utils.h"

using namespace cv;
using namespace std;

int main() {

   // Mat src1 = (Mat_<double>(4, 3) << 50.0000, 2.6772, -79.7751, 50.0000, 3.1571, -77.2803, 7, 8, 9, 10, 11, 12);
   // , 50.0000, 3.1571, -77.2803, 7, 8, 9, 10, 11, 12
   // Mat src2 = (Mat_<double>(3, 3) << 50.0000, 0.0000, -82.7485, 50.0000, 0.0000, -82.7485, 12, 13, 15);
  //  Mat cam(IO sio, IO dio, string method = "Bradford");
   // Mat distance_s(Mat Lab1, Mat Lab2, string distance);
  //  IO sio = IO("D65", 2);
  //  IO dio = IO("D65", 10);
    string method = "Bradford";
    Mat srcImage;
    srcImage = imread("D:/OpenCV/test.jpg");
    Mat src1 = srcImage(Range(0, 4), Range(0, 5));
    src1.convertTo(src1, CV_64F);
   // Mat src2 = srcImage(Range(3, 7), Range(4, 8));
    //src2.convertTo(src2, CV_64F);
    //System.out.println(CvType.typeToString(src));
    
    
    IO *test_sio = & A_2;
    IO *test_dio = & D65_2;


    // string distance = "distance_de00";
    //string distance = "distance_cmc";
    // string distance = "distance_de76";
    //string distance = "distance_de94";
    Mat res ;
   // cout <<"src / 255  " << (src / 255) << endl;

   // res = cam(*test_sio, *test_dio,method );
    //res = xyz2grayl(src / 255);
    //res = lab2xyz(src1/255, *test_dio);
    double low = 180.0;
    double up = 255.0;
  //  cout << src1 << endl;
    res = saturate(src1,  low,  up);
    //cout << "src1/255"<<src1 / 255 << endl;
   // cout << res << endl;
   
    //res = distance_s(src1, src2, distance);
   cout << "res.size " << res << endl;
    return 0;

}