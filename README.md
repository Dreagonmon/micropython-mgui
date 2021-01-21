# micropython-mgui
Easy to port micropython micro gui library, based on ```framebuf```
# Prepare
Make sure you are using python3.
```
pip install -r .\requirements.txt
```
If your micropython version is not match with mpy_cross version, you may need to build your own mpy-cross tools.
Follow the [offical guide](https://github.com/micropython/micropython/tree/master/mpy-cross) to build it.
Then, modify ```.mpypack.conf``` and config your mpy-cross path.

For details about mpypack, see [mpypack: A simple tool to pack up MicroPython code](https://pypi.org/project/mpypack/)

# Build
You should install mpy_cross first.
```
python -m pip install mpy_cross --user
```
Modify ```.mpypack.conf```, Then run ```build.py```

# Install

### Using Script
Modify ```.mpypack.conf```, Then run
```
build.py flash
```

### Manually Install
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
