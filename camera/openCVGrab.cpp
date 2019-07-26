#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <pylon/PylonIncludes.h>

#include <sstream>
#include <unistd.h>
#include <time.h>
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <chrono>

using namespace Pylon;
using namespace GenApi;
using namespace cv;
using namespace std;
using namespace std::chrono;

/// Global variables
Mat frame;

int main(int argc, char* argv[])
{
    // Automagically call PylonInitialize and PylonTerminate to ensure the pylon runtime system
    // is initialized during the lifetime of this object.
    Pylon::PylonAutoInitTerm autoInitTerm;
    high_resolution_clock::time_point t1;
    high_resolution_clock::time_point t9;

    try
    {
        // Create an instant camera object with the camera device found first.
	      cout << "Creating Camera..." << endl;
	      CInstantCamera camera(CTlFactory::GetInstance().CreateFirstDevice());
	      cout << "Camera Created." << endl;

        // Print the model name of the camera.
        cout << "Using device " << camera.GetDeviceInfo().GetModelName() << endl;

        // The parameter MaxNumBuffer can be used to control the count of buffers
        // allocated for grabbing. The default value of this parameter is 10.
        camera.MaxNumBuffer = 100;

	      // create pylon image format converter and pylon image
	      CImageFormatConverter formatConverter;
	      formatConverter.OutputPixelFormat= PixelType_BGR8packed;
	      CPylonImage pylonImage;

	       // Create an OpenCV image
        // Start the grabbing images.
        // The camera device is parameterized with a default configuration which
        // sets up free-running continuous acquisition.
        camera.StartGrabbing();

        // This smart pointer will receive the grab result data.
        CGrabResultPtr ptrGrabResult;

        // Camera.StopGrabbing() is called automatically by the RetrieveResult() method
        // when c_countOfImagesToGrab images have been retrieved.
        t1 = high_resolution_clock::now();
        while ( camera.IsGrabbing())
        {
            // Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            camera.RetrieveResult( 5000, ptrGrabResult, TimeoutHandling_ThrowException);

            // Image grabbed successfully?
            if (ptrGrabResult->GrabSucceeded())
            {
                // Access the image data.
                //cout << "SizeX: " << ptrGrabResult->GetWidth() << endl;
                //cout << "SizeY: " << ptrGrabResult->GetHeight() << endl;
                const uint8_t *pImageBuffer = (uint8_t *) ptrGrabResult->GetBuffer();
                //cout << "Gray value of first pixel: " << (uint32_t) pImageBuffer[0] << endl << endl;
		            // Convert the grabbed buffer to pylon imag
		            formatConverter.Convert(pylonImage, ptrGrabResult);
		            // Create an OpenCV image out of pylon image
                frame = cv::Mat(ptrGrabResult->GetHeight(), ptrGrabResult->GetWidth(), CV_8UC3, (uint8_t *) pylonImage.GetBuffer());
                //imshow( "frame", frame);
            }

            else
            {
                cout << "Error: " << ptrGrabResult->GetErrorCode() << " " << ptrGrabResult->GetErrorDescription() << endl;
            }
        t9 = high_resolution_clock::now();
        auto d_full_while = duration_cast<microseconds>( t9 - t1 ).count();
        // Get the resulting frame rate
        //double d = camera.ResultingFrameRate.GetValue();
        cout << "d_full_while[uS]: " << d_full_while << "\t" << endl; 
        //<< "ResultingFrameRate" << d << endl;

        }
        
    }

    catch (GenICam::GenericException &e)
    {
        // Error handling.
        cerr << "An exception occurred." << endl
        << e.GetDescription() << endl;
        return 0;
    }

    // Comment the following two lines to disable waiting on exit.
    cerr << endl << "Press Enter to exit." << endl;
    while( cin.get() != '\n');

    return 0;
}
