#ifndef TRAJECTORY
#define TRAJECTORY

#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

/*
Predice la posición de la pelota en función de un vector de N puntos.
*/
Point predictNextPosition(const vector<Point> &positions);


#endif // TRAJECTORY
