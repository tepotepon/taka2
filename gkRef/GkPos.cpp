#include "GkPos.h"

GkPos::GkPos(unsigned int N){
	NPOS = N;
	data = new cv::Point[NPOS];

	// Load initial value to the data vector. Chosen to be just 0.
	for(int i = 0; i < NPOS; i++){
		data[i] = cv::Point(0,0);
	}

	s_x 	= 0;
	s_x2	= 0;

	oldest 	= 0; 		// index of the oldest element of data.
	newest 	= NPOS-1;	// index of the newest element of data.
	diff_x	= data[newest].x-data[oldest].x;
}

GkPos::~GkPos(){
	delete[] data;
}

void GkPos::push(cv::Point p){

	// remove the oldest point from the sum terms
	s_x 	-=	data[oldest].x;
	s_x2 	-= 	data[oldest].x*data[oldest].x;

	// replace the oldest point by the new one.
	data[oldest] = p;

	// add the new point to the sum terms
	s_x 	+=	p.x;
	s_x2 	+= 	p.x*p.x;

	// Update the x-direction difference
	diff_x = p.x-data[newest].x;

	// Update the index of the newest and oldest point
	newest = oldest;
	oldest++;
	if(oldest >= NPOS)
		oldest = 0;
}


cv::Point GkPos::get_estimate(){

	// Check if the ball is moving on the right direction.
	if(diff_x > DMW){

		// Compute the regression line parameters.

		m = 0.0; b = 0.0;
		for(int i = 0; i < NPOS; i++){
			m += (NPOS*data[i].x-s_x)*data[i].y;
			b += (s_x2-s_x*data[i].x)*data[i].y;
		}

		D = NPOS*s_x2-s_x*s_x;
		m = m/D;
		b = b/D;

		// Compute the interception point between the regression line and the goalkeeper line.
		y_raw = x_gk*m+b;

		// Check if the interception is outside the table. If so, account for a
		// bounce (assuming 90 degrees) on the corresponding wall.

		if(y_raw < y_i || y_raw > y_s){
			// Look for the intercept coordinate on the wall.
			if(y_raw < y_i){ 		// Bounce was on the inferior wall
				x = (y_i-b)/m;	// Not the actual x we're looking, just a dummy.
				m = -1.0/m;		// The slope of the perpendicular line that the
								// ball should follow after the bounce
				b = y_i-m*x;	// The zero-intercept of the perpendicular line ...
			}
			else{				// Bounce was on the upper wall, same procedure.
				x = (y_s-b)/m;
				m = -1.0/m;
				b = y_s-m*x;
			}

			// Now update the interception point
			y_raw = x_gk*m+b;
		}

		// Make sure the interception point is bounded to the goalkeeper range.
		if(y_raw < y_gk_i)
			y = y_gk_i;
		else if(y_raw > y_gk_s)
			y = y_gk_s;
		else
			y = y_raw;

		return cv::Point((int)x_gk,(int)y);
	}

	//Otherwise, return the center position for the goalkeeper.

	else{
		return cv::Point((int)x_gk, (int)((y_gk_s+y_gk_i)/2));
	}
}

void GkPos::draw(cv::Mat roi){
	// Draw known ball past positions
	for(int i = 0; i < NPOS; i++)
		cv::drawMarker(roi,data[i],cv::Scalar( 0, 255, 0 ),cv::MARKER_STAR,20,3,8);

	// Draw ball trajectory estimation, similar procedure to the one on GkPos::get_estimate()
	if(diff_x > DMW){
		m = 0.0; b = 0.0;
		for(int i = 0; i < NPOS; i++){
			m += (NPOS*data[i].x-s_x)*data[i].y;
			b += (s_x2-s_x*data[i].x)*data[i].y;
		}

		D = NPOS*s_x2-s_x*s_x;
		m = m/D;
		b = b/D;

		y = x_gk*m+b;

		if(y < y_i || y > y_s){ // bounce
			if(y < y_i){
				x = (y_i-b)/m;
				cv::arrowedLine(roi, cv::Point(0,(int)b),cv::Point((int)x,(int)y_i),cv::Scalar(0,0,255),2,8,0);
				m = -1/m;
				b = y_i-m*x;
				y = x_gk*m+b;
				cv::arrowedLine(roi, cv::Point((int)x,(int)y_i),cv::Point((int)x_gk,(int)y),cv::Scalar(0,0,255),2,8,0);
			}
			else{// y > y_s
				x = (y_s-b)/m;
				cv::arrowedLine(roi, cv::Point(0,(int)b),cv::Point((int)x,(int)y_s),cv::Scalar(0,0,255),2,8,0);
				m = -1/m;
				b = y_s-m*x;
				y = x_gk*m+b;
				cv::arrowedLine(roi, cv::Point((int)x,(int)y_s),cv::Point((int)x_gk,(int)y),cv::Scalar(0,0,255),2,8,0);
			}
		}
		else{ // no bounce
			cv::arrowedLine(roi, cv::Point(0,(int)b),cv::Point((int)x_gk,(int)y),cv::Scalar(0,0,255),2,8,0);
		}
	}
}

void GkPos::printState(){
	std::cout << std::endl << "------------------------------------" << std::endl;
	std::cout << "Data: ";
	for (int i = 0; i < NPOS; i++)
		std::cout << "( " << data[i].x << ", " << data[i].y << ")  ";
	std::cout << std::endl;
	std::cout << "Oldest: " << oldest << ", Newest: " << newest << ", Diff = " << diff_x << std::endl;
	std::cout << "|x|_1 = " << s_x << ", |x|_2 = " << s_x2 << ", D = " << D << std::endl;
	std::cout << "m = " << m << ", b = " << b << ", y_raw = " << y << std::endl;
}