# Offline coordinate saving scripts

### Setup: 

- Place video to be processed in this folder. (Download this <a href="https://drive.google.com/file/d/1Rr45scmC6dsU8pffWDMVBm23K8V49MeR/view?usp=sharing" target="_blank">**example**</a>)

> **note:** it is **very important** that the foos-table looks something like this (colorwise: green-field/orange-ball/pink-team1/light_blue-team2): ![untitled](https://user-images.githubusercontent.com/32227452/85506883-3b825680-b5bf-11ea-8fe1-72ab7d444f7d.png)

- call using terminal: 
```shell
$ python save_ball_coords.py example.mp4
```
### Use: 

- Executing the script will show you this:

![WhatsApp Image 2020-06-24 at 01 31 48](https://user-images.githubusercontent.com/32227452/85505084-7e422f80-b5bb-11ea-890e-ed1aa09eabae.jpeg)

- Commands: 
	- **P**: Pause video. 
	- **spacebar**: Press to start saving coordenates - press again to stop. 
	- **esc**: to exit.

- Bars allow you to *fine tune* the ball color thresholds parameters (see [Offline_tunning](#Offline_tunning)) 

- Last bar (binary: on/off) allow you to see the color detection binary mask.

### Output: 

- The `Data.txt` file is inside *coords_data* folder
- example:

![image](https://user-images.githubusercontent.com/32227452/85506362-383a9b00-b5be-11ea-83e4-9a7ee72cb920.png)
	- the columns denote: frame - object.ID - x_coord - y_coord. 
> **Note:** x_coords and y_coords are relative to a 1800x800 image/matrix, where (0,0) is the top-left corner. 

## Offline_tunning: 

- this script serves as a test for tunning the color thresholds parameters. 
