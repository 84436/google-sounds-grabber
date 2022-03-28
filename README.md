# Google Sounds Grabber

This Python script takes a decoded dump of a Google Sounds APK (`com.google.android.soundpicker`) and generates an `aria2` job file that downloads every alarm, notification and ring tones available from the descriptions of that APK.

Ideal for people who don't have a Pixel phone (or who just want to use the tone files for something/somewhere else idk) and can't be bothered to install the Google Sounds app.




## Ingredients

* [**Apktool**](https://ibotpeaches.github.io/Apktool/): for decompiling the APK
  
  * Java 8+

* [**Beautiful Soup 4**](https://beautiful-soup-4.readthedocs.io/en/latest/) with LXML: for parsing `strings.xml` and other interesting stuff in the APK
  
  * Python 3+

* [**aria2**](https://aria2.github.io/): for mass downloading stuff

* **Google Sounds APK** (you can grab one from [APKMirror](https://www.apkmirror.com/apk/google-inc/sounds/))




## Quick Start

```
apktool d com.google.android.soundpicker.apk

python google_sounds_grabber.py com.google.android.soundpicker google_sounds

aria2c -i google_sounds.aria2.txt
```




## Sample Result

```
> tree /f 
C:.
├───Alarms
│   ├───Classical Harmonies      
│   │       Carnival.ogg
│   │       Crusade.ogg
│   │       Dreamy Nights.ogg    
│   │       Morning Calm.ogg     
│   │       Mozart Wakes.ogg     
│   │       New Horizon.ogg      
│   │       Renaissance.ogg      
│   │       The Four Seasons.ogg 
│   │       Variations II.ogg    
│   │       Variations.ogg       
│   │
│   ├───Material Adventures      
│   │       Balafon Sunrise.ogg  
│   │       Blades of Grass.ogg  
│   │       Blast Off.ogg        
│   │       Butterfly Trails.ogg 
│   │       Dustscape.ogg        
│   │       Forest Beat.ogg      
│   │       Funkyard.ogg
│   │       Horizon.ogg
│   │       Knick Knack.ogg      
│   │       Piano in the Sky.ogg 
│   │       Piano Taps.ogg       
│   │       Step Out.ogg
│   │       Temple of Dreams.ogg 
│   │       Zebra Stripes.ogg    
│   │
...
```




> this is what happens when you are unhinged and still up @ nearly 3am
