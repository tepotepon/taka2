para compilar: 

1) mkdir build 
2) cd build
3) cmake ..
4) make
5) ./taca

Debe salir un error que diga: "GStreamer: Error opening bin: unexpected reference "prueba" - ignoring"
6) agregar "prueba.avi" en carpeta "build". Download from: 
https://drive.google.com/file/d/1pycprE_4BUgKuSTetIU_u4QtHD_sFYdg/view?usp=sharing
7) ./taca 


CPP = g++

CPPFLAGS = -L/home/jtorres/libs/opencv/4.0.1/libs -I/home/jtorres/libs/opencv/4.0.1/include -Wl,-rpath=/home/jtorres/libs/opencv/4.0.1/libs

all: test

test: main.cpp
	$(CPP) $(CPPFLAGS) $^ -o $@

