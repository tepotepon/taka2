#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>

#define ROI_X 		140
#define ROI_Y 		70
#define ROI_WIDTH	520
#define ROI_HEIGHT	470

class ballTracker{

public:

	ballTracker();
	~ballTracker();

	cv::Mat getFoosTable(cv::Mat frame);
	cv::Point searchBall(cv::Mat foosTable);

private:

	cv::Mat src_hsv, red_yellow_image, element1, element2;
	cv::Rect roi;

};