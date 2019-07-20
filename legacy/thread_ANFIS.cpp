#include "thread_ANFIS.h"


thread_ANFIS::thread_ANFIS(cv::Point *BallPos, cv::Point *GoalKeeperPos) {

	this->BallPos = BallPos;
	this->GoalKeeperPos = GoalKeeperPos;

	engine = fl::FisImporter().fromFile(".//fis_files//fis6.fis");

	x1 = engine->getInputVariable("x1");
	y1 = engine->getInputVariable("y1");

	x2 = engine->getInputVariable("x2");
	y2 = engine->getInputVariable("y2");

	x3 = engine->getInputVariable("x3");
	y3 = engine->getInputVariable("y3");BallPos

	x4 = engine->getInputVariable("x4");
	y4 = engine->getInputVariable("y4");

	x5 = engine->getInputVariable("x5");
	y5 = engine->getInputVariable("y5");

	x6 = engine->getInputVariable("x6");
	y6 = engine->getInputVariable("y6");

	x7 = engine->getInputVariable("x7");
	y7 = engine->getInputVariable("y7");

	x8 = engine->getInputVariable("x8");
	y8 = engine->getInputVariable("y8");

	x9 = engine->getInputVariable("x9");
	y9 = engine->getInputVariable("y9");

	x10 = engine->getInputVariable("x10");
	y10 = engine->getInputVariable("y10");

	if (engine->isReady()) cout << "Fuzzy rdy" << endl;

	printf("Hola from ANFIS constructor\n");
}

thread_ANFIS::~thread_ANFIS() {

	this->requestInterruption();

	if (estado != PLAY) {
		mutex.unlock();
	}
}

void thread_ANFIS::Play() {
	if (estado != PLAY) {
		mutex.unlock();
		estado = PLAY;
	}
}
void thread_ANFIS::Pause() {
	estado = PAUSE;
}
void thread_ANFIS::Stop() {
	estado = STOP;
}
void thread_ANFIS::new_BallPos() {
	if (estado == PLAY)
		newData = true;
}
void thread_ANFIS::run() {

	printf("Hola from run ANFIS\n");

	while (!this->isInterruptionRequested()) {

		if (estado != PLAY) {
			mutex.lock();
		}
		else if (newData) {
			newData = false;

			newBallPos = *BallPos;

			if (newBallPos != cv::Point(0, 0)) {
				//cout << "Ball Pos: " << new_ball_pos << endl;
				posiciones.push_back(newBallPos);
			}

			if (posiciones.size() > 10) {

				posiciones.erase(posiciones.begin());

				x1->setValue(posiciones[0].x);
				y1->setValue(posiciones[0].y);

				x2->setValue(posiciones[1].x);
				y2->setValue(posiciones[1].y);

				x3->setValue(posiciones[2].x);
				y3->setValue(posiciones[2].y);

				x4->setValue(posiciones[3].x);
				y4->setValue(posiciones[3].y);

				x5->setValue(posiciones[4].x);
				y5->setValue(posiciones[4].y);

				x6->setValue(posiciones[5].x);
				y6->setValue(posiciones[5].y);

				x7->setValue(posiciones[6].x);
				y7->setValue(posiciones[6].y);

				x8->setValue(posiciones[7].x);
				y8->setValue(posiciones[7].y);

				x9->setValue(posiciones[8].x);
				y9->setValue(posiciones[8].y);

				x10->setValue(posiciones[9].x);
				y10->setValue(posiciones[9].y);

				engine->process();

				xref = engine->getOutputVariable("xref");
				yref = engine->getOutputVariable("yref");

				GoalKeeperPos->x = (int)xref->getValue();
				GoalKeeperPos->y = (int)yref->getValue();

				if (GoalKeeperPos->x != GoalKeeperPos->x || GoalKeeperPos->y != GoalKeeperPos->y) {
					//cout << "no es un numero" << endl;
					// El resultado de GoalKeeperPos->x arroja "nan"
					// que al compararlo con sigo mismo da "false"
				}
				else if (GoalKeeperPos->x < 0 || GoalKeeperPos->y < 0) {
					//cout << "fuera de los limites" << endl;
				}
				else {
					//cout << "xr: " << GoalKeeperPos->x << " yr: " << GoalKeeperPos->y << endl;	//Valor de salida.
					// Todo Ok
					emit newRef();
				}
			}

			//cout << "ANFIS: " << time->elapsed() << " ms\n" << std::flush;

			//printf("ANFIS: %d\n", *frameCounter);
		
		}
	}
}