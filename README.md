### How to run:

just run the following script:
* `chmod +x run.sh && ./run.sh`

If there will be any issues with Matplotlib try this:
* sudo apt install python3-tk

### Configuration
you can set the following config varibles by creating .env file:


* ARUCO_MARKER_TYPE - the type of Aruco marker. By default is "APRILTAG_16H5"

* VIDEO_PATH - path to the video you want to process. By default it gets ArucoVideo.mp4 from test_videos folder


### What it does?

For now, it draws an animated 2D and 3D graphs of the Aruco Marker movement and outputs processed video in realtime

<img src="https://github.com/ge6rgii/aruco_marker_detector/blob/main/test_videos/screenshot.png" width=500px>
