# pyside-media-loop
PySide software which can loop the media file (mp3 audio file only currently)

You can see a lot of 30 minutes or 10 hrs loop media in Youtube, this works well if you want to make it.

My first PySide software.

The most important thing is, this package doesn't import my other package like the others such as <a href="https://github.com/yjg30737/pyqt-dark-notepad.git">Dark Notepad</a>(which will be very confusing).

## Requirements
* PySide6
* <a href="https://github.com/jiaaro/pydub">pydub</a> - for media function
* <a href="https://github.com/quodlibet/mutagen">mutagen</a> - for checking mp3

## Setup
`pip3 install git+https://github.com/yjg30737/pyside-media-loop.git --upgrade`

## Example
```python
from PySide6.QtWidgets import QApplication
from pyside_media_loop.mediaLoop import MediaLoop


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ex = MediaLoop()
    ex.show()
    app.exec()
```

## Result
Front-end

![image](https://user-images.githubusercontent.com/55078043/188292533-174d4c43-96ff-41d3-86c6-60860581e28c.png)

I will improve this software(it is not an executable file just a bunch of scripts though)'s function such as supporting various file types and present the feature of this to my Youtube channel sooner or later.


