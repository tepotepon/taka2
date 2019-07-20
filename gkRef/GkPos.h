#include <opencv2/opencv.hpp>

#define y_i 	0		// y coordinate of the lower horizontal wall of the table.
#define y_s 	470		// y coordinate of the upper horizontal wall of the table.
#define x_gk	475		// x coordinate of the goalkeeper vertical line trayectory.
#define y_gk_i	120		// y coordinate of the upper bound for the puppet reference.
#define y_gk_s	350		// y coordinate of the upper bound for the puppet reference.
#define DMW 	10		// Don't Move Window: Minimum value of diff_x for which to consider ball movement.

class GkPos{

public:

	GkPos(unsigned int N);
	~GkPos();

	void push(cv::Point p);
	cv::Point get_estimate(void);
	void draw(cv::Mat roi); // Print lines and points over the roi.
	void printState(); 		// Print relevant variables for debuggind purposes

private:

	unsigned int NPOS; 			// Number of positions to be considered in the prediction.
	cv::Point* data; 			// Array to hold the NPOS past points to be used in the regression.

	unsigned int oldest;		// Index of the oldest point.
	unsigned int newest; 		// Index of the newest point.

	int diff_x; 				// Diference between the x-coordinate of the last two stored points.
	float s_x, s_x2; 			// Sum terms required by the estimate formulas.

	float D, m, b, x, y, y_raw;// Temporary variables for the goalkeeper position estimation.
};

/*
	TO-DO:	Extend the bounce prediction to the multi-bounce case.
*/

/*
	TO-DO:	Support an arbitrary reference system through x0 and y0. Also provide support for non completely
			horizontal/vertical lines on the walls.
*/

/*
	NOTE:	I'm assuming that the table is not rotated with respect to the camera,
			i.e. walls and puppet trayectories are all completely horizontal or vertical lines.
*/

/*
	NOTE: 	I'm currently using a simple criterion for ball direction inference: if the ball position is
			increasing on the x direction, then I'm executing the algorithm.
*/

/*
	TODO:	Somehow add a "threat severity" term to exaggerate/relax the reference
*/

/*
	RELEVANT LINKS:
		http://www.cplusplus.com/doc/tutorial/structures/
		https://codereview.stackexchange.com/questions/60484/stl-vector-implementation
		http://www.cplusplus.com/doc/oldtutorial/templates/
		https://stackoverflow.com/questions/33590792/two-threads-sharing-variable-c
		https://stackoverflow.com/questions/41505451/c-multi-threading-communication-between-threads
*/