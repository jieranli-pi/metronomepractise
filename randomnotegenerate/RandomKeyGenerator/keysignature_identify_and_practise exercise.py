from matplotlib import pyplot as plt
from matplotlib import image as mpimg 
import simpleaudio as sa #toplay audio
import time
import random

key_lists=["Ab","A","B","Bb","Cb","C#","C","Db",
           "D","Eb","E","F","F#","G","Gb"]
for i in range(0,1000):
    a=random.randint(0,14)
    image = mpimg.imread(key_lists[a]+".png")
    plt.imshow(image)
    plt.show()
    time.sleep(2)
    # define an object to play
    wave_object = sa.WaveObject.from_wave_file(key_lists[a]+'.wav') 
     # define an object to control the play
    play_object = wave_object.play()
    play_object.wait_done()

    
    print("The previous key was "+key_lists[a]+" ")


