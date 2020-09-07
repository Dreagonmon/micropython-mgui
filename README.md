# micropython-mgui
Easy to port micropython micro gui library, based on ```framebuf```

# Build
You should install mpy_cross first.
```
python3 -m pip install mpy_cross --user
```
Then run the build script.
```
python3 build.py
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
