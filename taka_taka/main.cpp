#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "opencv2/tracking.hpp"
#include <opencv2/features2d.hpp>

#include <time.h>
#include <iostream>
#include <stdlib.h>
#include <stdio.h>

using namespace std;
using namespace cv;

/// Global variables
Mat frame,src_hsv,img_gray;
Mat red_threshold,red2_threshold,yellow_threshold;
Mat red_image, red_yellow_image;
Mat element1 = getStructuringElement( 2,Size( 5, 5 ),Point( 3, 3 ));
Mat element2 = getStructuringElement( 2,Size( 2*7 + 1, 2*7+1 ),Point( 5, 5 ));

Rect roi(120, 80, 780, 400);
time_t start, ending;

int frames;

int main(){

  VideoCapture cap("Vid.mp4");

  // Check if camera opened successfully
  if(!cap.isOpened()){
    cout << "Error opening video stream or file" << endl;
    return -1;
  }

  time(&start);

  while(1){
      Mat ry_img;
      frames++;

      cap >> frame;
      if (frame.empty())
        break;

      //resize just for practicality
      resize(frame, frame, Size(), 0.5, 0.5);

      //get rid of non-useful info.
      Mat image_roi = frame(roi);

      //RGB to HSV
      cvtColor(image_roi,src_hsv, COLOR_BGR2HSV);

      //HSV COLOR THRESHOLD (yellow - RED1 - RED2
      inRange(src_hsv, Scalar(23, 100, 100), Scalar(30, 255, 255), yellow_threshold);
      inRange(src_hsv, Scalar(0, 100, 100), Scalar(10, 255, 255), red_threshold);
      inRange(src_hsv, Scalar(160, 100, 100), Scalar(179, 255, 255), red2_threshold);

      //add together for a single binary image.
      addWeighted(red_threshold,1.0,red2_threshold,1.0, 0.0,red_image);
      addWeighted(yellow_threshold,1.0,red_image,1.0, 0.0,red_yellow_image);

      //Apply morf. operations.
      erode(red_yellow_image, red_yellow_image, element1);
      dilate(red_yellow_image, red_yellow_image, element2);

      //find contours.
      vector<vector<Point> > contours;
      findContours( red_yellow_image, contours, RETR_TREE, CHAIN_APPROX_SIMPLE );

      vector<vector<Point> > contours_poly( contours.size() );
      vector<Rect> boundRect( contours.size() );
      vector<Point2f>centers( contours.size() );
      vector<float>radius( contours.size() );

      for( size_t i = 0; i < contours.size(); i++ )
      {
          approxPolyDP( contours[i], contours_poly[i], 3, true );
          boundRect[i] = boundingRect( contours_poly[i] );
          minEnclosingCircle( contours_poly[i], centers[i], radius[i] );
      }

      //draw contours into original image.
      for(unsigned i=0;i<boundRect.size();i++)
        rectangle( image_roi, boundRect[i], Scalar( 0, 255, 0 ), 2, 1 );

      //show results.
      imshow( "Detection results.", image_roi);
      imshow( "binary mask", red_yellow_image);

      // Press  ESC on keyboard to exit
      char c=(char)waitKey(25);
      if(c==27)
        break;

  }

  time(&ending);
  double seconds = difftime(ending, start);
  double fps  = frames / seconds;

  cout << "time: " << seconds
       << "\t" << "frames: " << frames
       << "\t" << "FPS: " << fps << endl;

  // When everything done, release the video capture object
  cap.release();

  // Closes all the frames
  destroyAllWindows();

  return 0;
}
