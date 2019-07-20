#include <opencv2/opencv.hpp>
#include <opencv2/videoio.hpp>

#include "GkPos.h"
#include "ballTracker.h"

#include <iostream>

using namespace std;
using namespace cv;

Point gk_ref, last_pos;
Mat frame, foosTable;

int frames = 0;
unsigned char pause = 1;

int main(){
    VideoCapture cap("vids/test.avi");

    // Check if camera opened successfully
    if(!cap.isOpened()){
        cout << "Error opening cam/video" << endl;
        return -1;
    }

    VideoWriter out1("vids/refGen.avi",CV_FOURCC('H','2','6','4'),30, Size(ROI_WIDTH,ROI_HEIGHT));
    VideoWriter out2("vids/refGen_SlowMo.avi",CV_FOURCC('H','2','6','4'),5, Size(ROI_WIDTH,ROI_HEIGHT));
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
        gk_pos.draw(foosTable);

        //show results.
        imshow( "GoalKeeper Reference Generation Test.", foosTable);
        out1.write(foosTable);
        out2.write(foosTable);

        // Press  ESC on keyboard to exit or SPACE to pause
        char c = (char)waitKey(25);
        if(c == 27)
            break;
        else if(c == 32)
            pause = 1;

        // If paused, then right arrow to move one frame or down arrow to print state. SPACE again to exit pause.
        while(pause == 1){
            char c=(char)waitKey(25);
            if(c == 83)
                break;
            else if(c == 84)
                gk_pos.printState();
            else if(c == 32)
                pause = 0;
        }
    }

    // When everything done, release the video capture object
    cap.release();

    // Closes all the frames
    destroyAllWindows();

    return 0;
}
