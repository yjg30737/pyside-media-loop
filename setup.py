from setuptools import setup, find_packages

setup(
    name='pyside-media-loop',
    version='0.0.1',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_data={'pyside_media_loop.ico': ['cropEnd.png',
                                            'cropStart.png',
                                            'pause.png',
                                            'play.png',
                                            'stop.png'],
                  'pyside_media_loop.style': ['button.css',
                                              'lineedit.css',
                                              'slider.css']},
    description='PySide software which can loop the media file (audio file only currently)',
    url='https://github.com/yjg30737/pyside-media-loop.git',
    install_requires=[
        'PySide6',
        'pydub',
        'mutagen'
    ]
)