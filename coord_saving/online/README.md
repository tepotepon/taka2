# Online coordinate saving scripts

## full.py
> this scripts allow you to save the coordenates of all objects `.txt` files.

### Setup: 

- Make sure you have all dependencies running. 

> **note:** it is **VERY important** that the foos-table looks something like this (colorwise: green-field(mandatory)/orange-ball/pink-team1/light_blue-team2):

![untitled](https://user-images.githubusercontent.com/32227452/85506883-3b825680-b5bf-11ea-8fe1-72ab7d444f7d.png)

### Use: 

- call using terminal: 
```shell
$ python full.py
```

- Commands: 
	- **spacebar**: Press to start saving coordenates - press again to stop. 

### Output: 

- The `.txt` files are inside *coords_data* folder
- example:

![image](https://user-images.githubusercontent.com/32227452/85506362-383a9b00-b5be-11ea-83e4-9a7ee72cb920.png)

- the columns denote: frame - object.ID - x_coord - y_coord. 
> **Note:** x_coords and y_coords are relative to a 1800x800 image/matrix, where (0,0) is the top-left corner. 

---

## Offline_tunning: 
> this script serves as a test for tunning the color thresholds parameters.

- call using terminal: 
```shell
$ python Offline_tunning.py example.mp4
```
- It will show you 3 windows, like this:
![image](https://user-images.githubusercontent.com/32227452/85522263-6676a580-b5d3-11ea-83ae-e974821d5d66.png)}

>**note**: In the example, the detection is not as good as it could be because of poor choice of colors. 

- Each window represent: ball, team1 and team2 detections. 

- The idea is to fine tune the thresholds parameters for each color using the trackbars and binary image as feedback. Once you have the settings you like, use those settings in `save_coords.py` 





