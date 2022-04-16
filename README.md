# Aruco Marker Pose Estimation
The purpose of this project is to reconstruct the 2d/3d pose of the marker from videos.

## Environment variables

* ARUCO_MARKER_TYPE - a type of detecting aruco marker, by default set to "APRILTAG_16H5".
* CAM_CALIBRATION_PATH - a path to the file with camera calibration data, by default we get from the root of this repository.
* VIDEO_PATH - a path to the video to process. By default it gets the video from "test_videos" folder.
* MARKER_PLANE - a plane you want to see on 2d plot; available values: FRONT, SAGITTAL and TRANSVERSE; not used for 3d plots.

## How to run

Just run the following command:

```bash
pipenv install && pipenv run python main.py
```
