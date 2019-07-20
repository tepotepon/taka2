#include "ballTracker.h"

using namespace cv;

ballTracker::ballTracker(){
	element1 = getStructuringElement( 2,Size( 3, 3 ),Point( 1, 1 ));
	element2 = getStructuringElement( 2,Size( 2*7 + 1, 2*7+1 ),Point( 5, 5 ));
	roi = Rect(ROI_X, ROI_Y, ROI_WIDTH, ROI_HEIGHT);
}

ballTracker::~ballTracker(){
	//Nothing to delete (90% sure...)
}

cv::Mat ballTracker::getFoosTable(Mat frame){
	return frame(roi);
}

cv::Point ballTracker::searchBall(Mat foosTable){
	// RGB to HSV
    cvtColor(foosTable,src_hsv, COLOR_BGR2HSV);

    // Orange threshold
    inRange(src_hsv, Scalar(6, 150, 200), Scalar(15, 250, 255), red_yellow_image);

    // Blob completion and noise filtering
    erode(red_yellow_image, red_yellow_image, element1);
    dilate(red_yellow_image, red_yellow_image, element2);

    // Find contours
    std::vector<std::vector<Point> > contours;
    findContours( red_yellow_image, contours, RETR_TREE, CHAIN_APPROX_SIMPLE );

    // Fit a circle around it and find its center.
    std::vector<std::vector<Point> > contours_poly( contours.size() );
    std::vector<Rect> boundRect( contours.size() );
    std::vector<Point2f>centers( contours.size() );
    std::vector<float>radius( contours.size() );

    for( size_t i = 0; i < contours.size(); i++ ){
        approxPolyDP( contours[i], contours_poly[i], 3, true );
        boundRect[i] = boundingRect( contours_poly[i] );
        minEnclosingCircle( contours_poly[i], centers[i], radius[i] );
    }

    // If a ball has been found...
    if(centers.size() != 0){
        // Pass its position to the Goalkeeper algorithm
        return Point(centers[0].x,centers[0].y);
    }
    else{
    	return Point(-1,-1);
    }
}