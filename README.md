# micropython-mgui
Easy to port micropython micro gui library, based on micropython ```framebuf```module

# Prepare
Make sure you are using python3.8 and higher
```
pip install -r .\requirements.txt
```
If your micropython version is not match with mpy_cross version, you may need to build your own mpy-cross tools.
Follow the [offical guide](https://github.com/micropython/micropython/tree/master/mpy-cross) to build it.
Then, modify ```.mpypack.conf``` and config your mpy-cross path.

For details about mpypack, see [mpypack: A simple tool to pack up MicroPython code](https://pypi.org/project/mpypack/)

# Build
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

# Useage

### The Class
- MGuiView is the base class. Any view extends this class.
  - examples in mgui_component.py
- MGuiLayout is layout base class. Any view that has children should extends this class.
  - examples in mgui_layout.py
- MGuiRoot is the MGUI root class. This class handle the loop, context, and start passing an event.
- MGuiScreen is the abstract screen class. Used by MGuiRoot to refresh screen.

### Event System
The event passed from parent to children. if any children return True, then the event stop passing.
