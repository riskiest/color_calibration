#pragma once
#include <functional>
#include <vector>
#include "opencv2\core\core.hpp"
#include "utils.h"

namespace cv {
namespace ccm {

typedef std::function<Mat(Mat)> MatFunc;

class Operation {
public:
	bool linear;
	cv::Mat M;
	MatFunc f;
	Operation() : linear(true), M(Mat()) {};
	Operation(Mat M) :linear(true), M{ M } {};
	Operation(MatFunc f) : linear(false), f(f) {};
	Mat operator()(Mat& abc) {
		if (!linear) { return f(abc); }
		if (M.empty()) { return abc; }
		return multiple(abc, M);
	};
	void add(Operation& other) {
		if (M.empty()) {
			M = other.M;
		}
		else {
			M = M * other.M;
		}
	};
	bool clear() {
		M = Mat();
	};
};

Operation identity_op( [](Mat x) {return x; } );

class Operations {
public:
	std::vector<Operation> ops;
	Operations() :ops{ } {};
	Operations(std::initializer_list<Operation> op) :ops{ op } {};
	Operations& add(const Operations& other) {
		ops.insert(ops.end(), other.ops.begin(), other.ops.end());
		return *this;
	};
	Mat run(Mat abc) {
		Operation hd;
		for (auto& op : ops) {
			if (op.linear) {
				hd.add(op);
			}
			else {
				abc = hd(abc);
				hd.clear();
				abc = op(abc);
			}
		}
		abc = hd(abc);
		return abc;
	};
};

Operations identity{ identity_op };
}
}




