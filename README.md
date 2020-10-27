# micropython-mgui
Easy to port micropython micro gui library, based on ```framebuf```
# Prepare
Make sure you are using python3.
```
pip install -r .\requirements.txt
```
If your micropython version is not match with mpy_cross version, you may need to build your own mpy-cross tools.
Follow the [offical guide](https://github.com/micropython/micropython/tree/master/mpy-cross) to build it.
Then, modify ```build.py``` and import mpy_cross from ```./lib/mpy_cross```

# Build
You should install mpy_cross first.
```
python -m pip install mpy_cross --user
```
Then run the build script.
```
python build.py
```
And you will get some *.mpy files under ```./dist/mgui/``` folder

# Install
Copy ```./dist/mgui/``` folder to one of your import path. You can check your import path using: ```print(sys.path)```.
```
e.g. import path are ['', '/lib']:
>root
|--->lib
|   |--->mgui     <--- put it there
|       |---:__init__.mpy
|       |---...
|---:boot.py
|---:main.py
|---...
```
