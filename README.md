# What	is	Vision	Audio?</br>
A gesture-controlled audio player built for the purpose of demonstrating the capabilities of computer vision. The program is built with python programming language with the help of several external libraries used for image processing & computer vision.
</br></br>




# How	to	Configure?
### 1.Anaconda environment</br></br>
***Step1:** Clone the repo*</br></br>

***Step2:** Open the Anaconda Prompt and navigate to the cloned repo location (vision_audio)*</br></br>

***Step3:** Execute the following commands to create and activate a virtual environment*</br>
```
conda create -n vision_audio python=3.9 pip
```
```
conda activate vision_audio
```
</br></br>

***Step4:** Execute following commands to install required modules and run the main script*
```
pip install -r requirements.txt
```
```
python main.py
```
</br></br>


### 2.Pycharm</br></br>
***Step1:** Clone the repo and open the project with pycharm*</br></br>

***Step2:** Install the following modules*
- mediapipe
- opencv-python
- pygame</br></br>

***Step3:** Run "main.py" file*</br></br>


# How	to	play	with	Vision	Audio?

The songs are already loaded but you can add a folder using *load songs* button. The player will load all the mp3 files in a given folder.

### To Start/continue  ->   *Raise all five fingers*</br></br>
![play_ex](https://user-images.githubusercontent.com/60750424/122570201-24a70080-d069-11eb-9f4c-c9243ac30ebe.PNG)</br></br></br></br></br>


### To pause:  ->   *all the fingers*</br></br>
![paused_ex](https://user-images.githubusercontent.com/60750424/122570250-31c3ef80-d069-11eb-84ec-b452c4af8dd9.PNG)</br></br></br></br></br>

### To change the volume  ->   *Raise your thumb and index finger and adjust the distance between them*</br></br>
![Change_volume_ex](https://user-images.githubusercontent.com/60750424/122570293-3d171b00-d069-11eb-8a76-b376ae2c27b8.PNG)</br></br></br></br></br>




### To play the previous track  ->   *Raise all the fingers except your thumb and move them to the left*</br></br>
![Play_prev](https://user-images.githubusercontent.com/60750424/122571972-eca0bd00-d06a-11eb-981a-187f5c512aa0.png)</br></br></br></br></br>

### To play the next track  ->   *Raise all the fingers except your thumb and move them to the right*</br></br>
![Play_next](https://user-images.githubusercontent.com/60750424/122572022-f9251580-d06a-11eb-8fb3-3ff2d4b5c64a.gif)











