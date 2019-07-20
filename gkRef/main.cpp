#include <opencv2/opencv.hpp>
#include <opencv2/videoio.hpp>

#include "GkPos.h"
#include "ballTracker.h"

#include <iostream>
#include <chrono>

using namespace std;
using namespace std::chrono;
using namespace cv;

Point gk_ref, last_pos;
Mat frame, foosTable;

int frames = 0;

int main(){
    VideoCapture cap("vids/test.avi");

    // Check if camera opened successfully
    if(!cap.isOpened()){
        cout << "Error opening cam/video" << endl;
        return -1;
    }

    GkPos gk_pos(5);
    ballTracker ball_tracker;

    // Save starting time.
    high_resolution_clock::time_point t1 = high_resolution_clock::now();
    while(1){ // Run "forever"

        frames++; // Keep track of the number of processed frames.

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
    }

    high_resolution_clock::time_point t2 = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>( t2 - t1 ).count();
    double fps  = 1000000*frames / duration;
    cout << "time[uS]: " << duration << "\t" << "frames: " << frames << "\t" << "FPS: " << fps << endl;

    // When everything done, release the video capture object
    cap.release();

    // Closes all the frames
    destroyAllWindows();

    return 0;
}
