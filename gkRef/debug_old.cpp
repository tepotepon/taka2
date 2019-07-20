#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/videoio.hpp>

#include "GkPos.h"

#include <iostream>

#include <time.h>

#define ROI_X 140
#define ROI_Y 70
#define ROI_WIDTH 520
#define ROI_HEIGHT 470

using namespace std;
using namespace cv;

/// Global variables
Mat frame,src_hsv, red_yellow_image;
Mat element1 = getStructuringElement( 2,Size( 3, 3 ),Point( 1, 1 ));
Mat element2 = getStructuringElement( 2,Size( 2*7 + 1, 2*7+1 ),Point( 5, 5 ));

Rect roi(ROI_X, ROI_Y, ROI_WIDTH, ROI_HEIGHT);

Rect portero;
Point gk_ref, last_pos;

time_t start, ending;
int frames = 0;

//char pause = 1;

int main(){
  GkPos gk_pos(5);

  VideoCapture cap("vids/test.avi");
  //namedWindow( "GoalKeeper Reference Generation Test.", WINDOW_AUTOSIZE );// Create a window for display.

  // Check if camera opened successfully
  if(!cap.isOpened()){
    cout << "Error opening cam" << endl;
    return -1;
  }

  time(&start);
  while(1){
      frames++;
      cap >> frame;
      if (frame.empty())
        break;

      //get rid of non-useful info.
      Mat image_roi = frame(roi);

      // RGB to HSV
      cvtColor(image_roi,src_hsv, COLOR_BGR2HSV);

      // Orange threshold
      inRange(src_hsv, Scalar(6, 150, 200), Scalar(15, 250, 255), red_yellow_image);

      // Blob completion and noise filtering
      erode(red_yellow_image, red_yellow_image, element1);
      dilate(red_yellow_image, red_yellow_image, element2);

      // Find contours
      vector<vector<Point> > contours;
      findContours( red_yellow_image, contours, RETR_TREE, CHAIN_APPROX_SIMPLE );

      // Fit a circle around it and find its center.
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

      // Goalkeeper line.
      line(image_roi, Point(475,0),Point(475,image_roi.rows),Scalar(255,0,0),1,8,0);

      // Goalkeeper limits.
      drawMarker(image_roi,Point(475,120),Scalar( 255, 0, 0 ),0,20,3,8);
      drawMarker(image_roi,Point(475,350),Scalar( 255, 0, 0 ),0,20,3,8);

      // If a ball has been found...
      if(centers.size() != 0){
        // Pass its position to the Goalkeeper algorithm
        last_pos = Point(centers[0].x,centers[0].y);
      }
      gk_pos.push(last_pos);
      gk_ref = gk_pos.get_estimate();
      // Show the GoalKeeper reference.
      drawMarker(image_roi,gk_ref,Scalar( 0, 0, 255 ),0,20,3,8);
      gk_pos.draw(image_roi);

      //show results.
      imshow("GoalKeeper Reference", image_roi);

      // Press  ESC on keyboard to exit
      /*
      char c=(char)waitKey(20);
      if(c==27)       //ESC
        break;
      else if(c==32)  // space
        pause = 1;

      while(pause == 1){
        char c=(char)waitKey(100);
        if(c==83)       // right arrow
          break;
        else if(c==84)  // down arrow
          gk_pos.printState();
        else if(c==32)  // space
          pause = 0;
      }
      */
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
