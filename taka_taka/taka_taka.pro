QT += core
QT -= gui

TARGET = taka_taka
CONFIG += console
CONFIG -= app_bundle
CONFIG += link_pkgconfig
CONFIG += c++11 console

TEMPLATE = app

SOURCES += main.cpp

INCLUDEPATH += /usr/local/include/opencv4

LIBS += -L/usr/lib/
LIBS += -L/usr/local/lib -lopencv_videoio -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_features2d -lopencv_video -lopencv_tracking
LIBS += `pkg-config \
    --cflags \
    --libs`
