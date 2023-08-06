# Python module for simple ASUS tinkerboard camera

## Overview
This repository documentation for simple asus tinkerboard camera control. Test create python module and upload python pypi. May with a lots of bug :)

## Test Environment

* device: [ASUS Tinkerboard](https://www.asus.com/us/Networking-IoT-Servers/AIoT-Industrial-Solution/All-series/Tinker-Board/)
* image: v2.2.2
* camera: OV5647 (Raspiberry Camera V1, 5MP)
  * IMX219 (Raspiberry Camera V2, 8MP), another tinkerboard supported camera is not tested
* python version: 3.5

## Usage
* preview
```console
$ from stkcam import TKCam, CamType
$ cam = TKCam(CamType.OV5647)
$ cam.preview()
```
* take a picture
```console
$ from stkcam import TKCam, CamType
$ cam = TKCam(CamType.OV5647)
$ cam.take_image('/home/linaro/Desktop\image.jpg') # image path
```