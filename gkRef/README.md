To compile, from the taka2/gkRef directory:

cd build && cmake -DSRC=main .. && make && cd ../

OpenCV ver >= 3.0 is required. To compile in demo or debug modes, change the argument from the command to -DSRC=demo or -DSRC=debug accordingly.

Output will be the gkRef.app executable located on taka2/gkRef. Run as ./gkRef

A sample video named test.avi should be located inside the taka2/vids directory in order to run the code. Output videos -if there are any- will be generated on the same directory.

A sample video can be downloaded from [here](https://drive.google.com/file/d/1pycprE_4BUgKuSTetIU_u4QtHD_sFYdg/view?usp=sharing)
