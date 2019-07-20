#include <opencv2/opencv.hpp>
#include <opencv2/videoio.hpp>

#include "GkPos.h"
#include "ballTracker.h"

#include <iostream>

using namespace std;
using namespace cv;

Point gk_ref, last_pos;
Mat frame, foosTable;

int main(){
    VideoCapture cap("vids/test.avi");

    // Check if camera opened successfully
    if(!cap.isOpened()){
        cout << "Error opening cam/video" << endl;
        return -1;
    }

    VideoWriter out1("vids/refGen.avi",CV_FOURCC('H','2','6','4'),30, Size(ROI_WIDTH,ROI_HEIGHT));
    // Should check if video object was created successfully, but nah...

    GkPos gk_pos(5);
    ballTracker ball_tracker;

    while(1){ // Run "forever"

        cap >> frame; // Read a new frame.

        if (frame.empty()) // Stop if the video is over.
            break;

        // Get rid of non-useful info.
        foosTable = ball_tracker.getFoosTable(frame);
        last_pos = ball_tracker.searchBall(foosTable);
        if(last_pos.x == -1 && last_pos.y ==-1){    // Invalid point! No ball found.
            // Do nothing... Maybe print something?
        }
        else{   // Add the new point, update the ref.
            gk_pos.push(last_pos);
            gk_ref = gk_pos.get_estimate();
        }

        // Goalkeeper line.
        line(foosTable, Point(x_gk, y_i),Point(x_gk, y_s),Scalar(255,0,0),1,8,0);

        // Goalkeeper limits.
        drawMarker(foosTable,Point(x_gk, y_gk_i),Scalar(255, 0, 0),0,20,3,8);
        drawMarker(foosTable,Point(x_gk, y_gk_s),Scalar(255, 0, 0),0,20,3,8);

        // Show the GoalKeeper reference.
        drawMarker(foosTable,gk_ref,Scalar( 0, 0, 255 ),0,20,3,8);

        //show results.
        imshow( "GoalKeeper Reference Demo.", foosTable);
        out1.write(foosTable);
        if(waitKey(25)==27)       //ESC to exit
            break;
    }

    // When everything done, release the video capture object
    cap.release();

    // Closes all the frames
    destroyAllWindows();

    return 0;
}
