#pragma once
#include <QThread>
#include <QMessageBox>
#include <QMutex>
#include <QTime>

#include "opencv2\imgproc.hpp"
#include "fl/Headers.h"
//#include "fl/fuzzylite.h"

#include <iostream>

using namespace std;

class thread_ANFIS : public QThread {

	Q_OBJECT

public:
	thread_ANFIS(cv::Point *BallPos, cv::Point *GoalKeeperPos);
	~thread_ANFIS();

	enum Estado {
		PLAY,
		PAUSE,
		STOP
	};

	Estado estado = STOP;
	QMutex mutex;

	cv::Point newBallPos;
	cv::Point *BallPos;
	cv::Point *GoalKeeperPos;

	bool newData = false;

	void Play();
	void Pause();
	void Stop();

	void run();

	vector<cv::Point> posiciones;

	fl::Engine* engine;

	fl::OutputVariable* xref;
	fl::OutputVariable* yref;

	fl::InputVariable* x1;
	fl::InputVariable* y1;
	fl::InputVariable* x2;
	fl::InputVariable* y2;
	fl::InputVariable* x3;
	fl::InputVariable* y3;
	fl::InputVariable* x4;
	fl::InputVariable* y4;
	fl::InputVariable* x5;
	fl::InputVariable* y5;
	fl::InputVariable* x6;
	fl::InputVariable* y6;
	fl::InputVariable* x7;
	fl::InputVariable* y7;
	fl::InputVariable* x8;
	fl::InputVariable* y8;
	fl::InputVariable* x9;
	fl::InputVariable* y9;
	fl::InputVariable* x10;
	fl::InputVariable* y10;

	signals:
		void newRef();
	public slots :
		void new_BallPos();
private:

};
