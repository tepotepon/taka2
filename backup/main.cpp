#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/features2d.hpp>
#include "trajectory.h"

/*
#include <pylon/PylonIncludes.h>
#ifdef PYLON_WIN_BUILD
#    include <pylon/PylonGUI.h>
#endif
*/

#include <unistd.h>
#include <time.h>
#include <iostream>
#include <stdlib.h>
#include <stdio.h>

using namespace std;
using namespace cv;
//using namespace Pylon;

/// Global variables
Mat frame,src_hsv,img_gray;
Mat red_threshold,red2_threshold,yellow_threshold;
Mat red_image, red_yellow_image;
Mat element1 = getStructuringElement( 2,Size( 3, 3 ),Point( 1, 1 ));
Mat element2 = getStructuringElement( 2,Size( 2*7 + 1, 2*7+1 ),Point( 5, 5 ));

Rect roi(100, 10, 600, 580);
time_t start, ending;

int frames;
Point ballPosition(0, 0);
Rect portero;

int main(){

  vector<Point> ballPositions;
  Point predictedballPosition;
  VideoCapture cap("vids/test.avi");

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

      //RGB to HSV
      cvtColor(image_roi,src_hsv, COLOR_BGR2HSV);

      // Combinación de colores para seguir jugadores + pelota.
      /*
      //HSV COLOR THRESHOLD (yellow - RED1 - RED2
      inRange(src_hsv, Scalar(23, 100, 100), Scalar(30, 255, 255), yellow_threshold); //black cvScalar(0, 0, 0), cvScalar(180, 255, 30),
      inRange(src_hsv, Scalar(0, 100, 100), Scalar(10, 255, 255), red_threshold);
      inRange(src_hsv, Scalar(160, 100, 100), Scalar(179, 255, 255), red2_threshold); /

      //add together for a single binary image.
      addWeighted(red_threshold,1.0,red2_threshold,1.0, 0.0,red_image);
      addWeighted(yellow_threshold,1.0,red_image,1.0, 0.0,red_yellow_image);*/

      inRange(src_hsv, Scalar(6, 150, 200), Scalar(15, 250, 255), red_yellow_image); //orange

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
      line(image_roi, Point(510,0),Point(520,image_roi.rows),Scalar(255,0,0),1,8,0);

      //rectangle( image_roi, boundRect[i], Scalar( 0, 255, 0 ), 2, 1 );
      if(centers.size() != 0){
        ballPosition = Point(centers[0].x,centers[0].y);
        ballPositions.push_back(ballPosition);
        predictedballPosition = predictNextPosition(ballPositions);
        drawMarker(image_roi,centers[0],Scalar( 0, 255, 0 ),0,20,3,8);
        drawMarker(image_roi,predictedballPosition,Scalar( 255, 0, 0 ),0,20,3,8);

        // portero con limites
        /*
            if(int(predictedballPosition.y)-15 >400){
                portero = Rect(500,400-15, 30,30);
                rectangle(image_roi,portero, Scalar(0,0,255), FILLED,8,0);
            }
            else if(int(predictedballPosition.y)-15 < 180){
                portero = Rect(500,180-15, 30,30);
                rectangle(image_roi,portero, Scalar(0,0,255), FILLED,8,0);
            }
            else {
                portero = Rect(500,int(predictedballPosition.y)-15, 30,30);
                rectangle(image_roi,portero, Scalar(0,0,255), FILLED,8,0);
            }
        }*/

        portero = Rect(500,int(predictedballPosition.y)-15, 30,30);
        rectangle(image_roi,portero, Scalar(0,0,255), FILLED,8,0);
      }

      cout << "current position        = " << ballPositions.back().x << ", " << ballPositions.back().y << "\n";
      cout << "next predicted position = " << predictedballPosition.x << ", " << predictedballPosition.y << "\n";
      cout << "--------------------------------------------------\n";

      //show results.
      imshow( "Detection results.", image_roi);
      //imshow( "binary mask", red_yellow_image);

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
