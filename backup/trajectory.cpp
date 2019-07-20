#include "trajectory.h"

Point predictNextPosition(const vector<Point> &positions) {
    Point predictedPosition;        // this will be the return value
    int numPositions;

    numPositions = positions.size();

    if (numPositions == 0) {

        cout << "error, predictNextPosition was called with zero points\n";

    } else if (numPositions == 1) {

        return(positions[0]);

    } else if (numPositions == 2) {

        int deltaX = positions[1].x - positions[0].x;
        int deltaY = positions[1].y - positions[0].y;

        predictedPosition.x = positions.back().x + deltaX;
        predictedPosition.y = positions.back().y + deltaY;

    } else if (numPositions == 3) {

        int sumOfXChanges = ((positions[2].x - positions[1].x) * 2) +
            ((positions[1].x - positions[0].x) * 1);

        int deltaX = (int)round((float)sumOfXChanges / 3.0);

        int sumOfYChanges = ((positions[2].y - positions[1].y) * 2) +
            ((positions[1].y - positions[0].y) * 1);

        int deltaY = (int)round((float)sumOfYChanges / 3.0);

        predictedPosition.x = positions.back().x + deltaX;
        predictedPosition.y = positions.back().y + deltaY;

    } else if (numPositions == 4) {

        int sumOfXChanges = ((positions[3].x - positions[2].x) * 3) +
            ((positions[2].x - positions[1].x) * 2) +
            ((positions[1].x - positions[0].x) * 1);

        int deltaX = (int)round((float)sumOfXChanges / 6.0);

        int sumOfYChanges = ((positions[3].y - positions[2].y) * 3) +
            ((positions[2].y - positions[1].y) * 2) +
            ((positions[1].y - positions[0].y) * 1);

        int deltaY = (int)round((float)sumOfYChanges / 6.0);

        predictedPosition.x = positions.back().x + deltaX;
        predictedPosition.y = positions.back().y + deltaY;

    } else if (numPositions >= 5) {

        int sumOfXChanges = ((positions[numPositions - 1].x - positions[numPositions - 2].x) * 4) +
            ((positions[numPositions - 2].x - positions[numPositions - 3].x) * 3) +
            ((positions[numPositions - 3].x - positions[numPositions - 4].x) * 2) +
            ((positions[numPositions - 4].x - positions[numPositions - 5].x) * 1);

        int deltaX = (int)round((float)sumOfXChanges / 10.0);

        int sumOfYChanges = ((positions[numPositions - 1].y - positions[numPositions - 2].y) * 4) +
            ((positions[numPositions - 2].y - positions[numPositions - 3].y) * 3) +
            ((positions[numPositions - 3].y - positions[numPositions - 4].y) * 2) +
            ((positions[numPositions - 4].y - positions[numPositions - 5].y) * 1);

        int deltaY = (int)round((float)sumOfYChanges / 10.0);

        predictedPosition.x = positions.back().x + deltaX*5;
        predictedPosition.y = positions.back().y + deltaY*5;

    } else {
        // should never get here
    }
    return(predictedPosition);
}