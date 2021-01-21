try:
    import framebuf
except ImportError:
    from . import framebuf

from sys import exit
from multiprocessing import Process, Queue, Array
# from pygame.time import wait
from pygame import locals as L
from pygame import display as pyg_display
from pygame import event as pyg_event
from pygame import gfxdraw as pyg_gfxdraw
from pygame import image as pyg_image
from pygame.time import Clock, wait

from timeit import default_timer as timer
def timed_function(f, *args, **kwargs):
    myname = f.__name__
    def new_func(*args, **kwargs):
        print('Function [{}] Start'.format(myname))
        t = timer()
        result = f(*args, **kwargs)
        delta = timer() - t
        print('Function [{}] Time = {:6.3f}ms'.format(myname, delta))
        return result
    return new_func

from PIL import Image, ImageDraw
from io import BytesIO, SEEK_SET
def getFrameBufferImage(buffer, width:int, height:int, format:int, scale=4, invert=False, color=(255, 255, 255)):
    img = Image.new("RGB", (width * scale, height * scale), 0)
    draw = ImageDraw.Draw(img)
    fbuf = framebuf.FrameBuffer(buffer, width, height, format)
    for y in range(height):
        for x in range(width):
            c = (0, 0, 0) if fbuf.pixel(x, y) == 0 ^ invert else color # fbuf.pixel(x, y)
            pos = [x * scale, y * scale, x * scale + scale - 2, y * scale + scale - 2]
            draw.rectangle(pos, fill=c, width=0)
    img = img.resize((width*scale, height*scale), Image.NEAREST)
    fp = BytesIO()
    img.save(fp, 'bmp')
    fp.seek(0, SEEK_SET)
    return pyg_image.load_basic(fp)

QUEUE_SIZE = 1
DEFAULT_FPS = 30

class PygameScreen():
    def __init__(self, width, height, scale, shared_buffer) -> None:
        self.width = width
        self.height = height
        self.scale = scale
        self.buffer = shared_buffer
        self.frame = framebuf.FrameBuffer(shared_buffer, width, height, framebuf.MONO_VLSB)
        self.window_size = (width * scale, height * scale)
        pyg_display.init()
        pyg_display.set_caption("SSD1306_EMU")
        self.surface = pyg_display.set_mode(self.window_size, flags=L.DOUBLEBUF, vsync=1)
        self.clock = Clock()
        self.invert = False
        self.contrast = 255
        self.power = True
    
    def refresh_area(self, rect=None):
        if rect == None:
            rect = (0, 0, self.window_size[0], self.window_size[1])
        if not self.power:
            return
        color_value = int(255 - (0.4 * (255 - self.contrast)))
        color = (color_value, color_value, color_value)
        # x, y, w, h = rect
        # for xp in range(w):
        #     for yp in range(h):
        #         tx = (x + xp) * self.scale
        #         ty = (y + yp) * self.scale
        #         color = (0, 0, 0) if self.frame.pixel(x + xp, y + yp) == 0 ^ self.invert else (color_value, color_value, color_value)
        #         pyg_gfxdraw.box(self.surface, (tx, ty, self.scale-1, self.scale-1), color)
        surf = getFrameBufferImage(self.buffer, self.width, self.height, framebuf.MONO_VLSB, self.scale, self.invert, color)
        self.surface.blit(surf, rect)

    def process_requests(self, requests):
        rect = (0, 0, self.window_size[0], self.window_size[1])
        for req in requests:
            if req.action == REQUEST_ACTION_EXIT:
                exit()
            elif req.action == REQUEST_ACTION_REFRESH:
                # rect = req.rect
                pass
            elif req.action == REQUEST_ACTION_CONTRAST:
                self.contrast = req.value
            elif req.action == REQUEST_ACTION_INVERT:
                self.invert = False if req.value == 0 else True
            elif req.action == REQUEST_ACTION_POWER_ON:
                self.power = True
            elif req.action == REQUEST_ACTION_POWER_OFF:
                self.power = False
                pyg_gfxdraw.box(self.surface, (0, 0, self.window_size[0], self.window_size[1]), (0, 0, 0))
        self.refresh_area(rect)

    def process_pygame_event(self):
        # pygame event
        for event in pyg_event.get():
            if event.type == L.QUIT:
                exit()

    # @timed_function
    def do_pygame_loop_once(self, requests=[], wait_fps=-1):
        self.process_requests(requests)
        self.process_pygame_event()
        pyg_display.flip()
        if wait_fps > 0:
            self.clock.tick(wait_fps)

def _pygame_loop(queue: Queue, width, height, scale, buffer):
    screen = PygameScreen(width, height, scale, buffer)
    try:
        while True:
            # queue event
            requests = []
            while not queue.empty():
                requests.append(queue.get_nowait())
            screen.do_pygame_loop_once(requests, DEFAULT_FPS)
    except KeyboardInterrupt:
        pass

REQUEST_ACTION_EXIT = 0x00
REQUEST_ACTION_POWER_ON = 0x01
REQUEST_ACTION_POWER_OFF = 0x02
REQUEST_ACTION_INVERT = 0x03
REQUEST_ACTION_CONTRAST = 0x04
REQUEST_ACTION_REFRESH = 0x05
class RefreshRequest():
    action = REQUEST_ACTION_EXIT
    value = 0
    rect = (0, 0, 0, 0) # (x, y, w, h)
    data = bytearray()

class SSD1306_Emu(framebuf.FrameBuffer):
    def __init__(self, width, height, *args, main_process=False, **kws):
        self.width = width
        self.height = height
        self.__scale = 8
        self.__main_process = main_process
        # sub process
        self.__loop = None
        self.__loop_queue = None
        # main process
        self.__request_list = []
        self.__screen = None
        # internal
        self.__power = True
        
        # init buffer
        self.pages = self.height // 8
        if height % 8 != 0:
            self.pages = self.pages + 1
        self.buffer = bytearray(self.pages * self.width)
        if self.__main_process:
            self.__screen_buffer = bytearray(self.pages * self.width)
        else:
            self.__screen_buffer = Array('b', self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.__screen_frame = framebuf.FrameBuffer(self.__screen_buffer, self.width, self.height, framebuf.MONO_VLSB)
        # init display
        self.init_display()

    def __del__(self):
        self._pygame_stop()

    def __pygame_signal(self, signal, value=0, rect=(0, 0, 0, 0), data=bytearray()):
        req = RefreshRequest()
        req.action = signal
        req.value = value
        req.rect = rect
        req.data = data
        if self.__main_process:
            if self.__screen == None:
                return
            self.__request_list.append(req)
        else:
            if self.__loop_queue == None:
                return
            if not self.__loop_queue.full():
                self.__loop_queue.put_nowait(req)

    def init_display(self):
        if self.__main_process:
            if self.__screen != None:
                return
            self.__screen = PygameScreen(self.width, self.height, self.__scale, self.__screen_buffer)
        else:
            if self.__loop != None:
                return
            # start loop
            self.__loop_queue = Queue(QUEUE_SIZE)
            self.__loop = Process(
                target=_pygame_loop,
                args=(self.__loop_queue, self.width, self.height, self.__scale, self.__screen_buffer),
                daemon=False
            )
            self.__loop.start()

    def poweroff(self): # default on
        self.__power = False
        self.__pygame_signal(REQUEST_ACTION_POWER_OFF)

    def poweron(self): # default on
        self.__power = True
        self.__pygame_signal(REQUEST_ACTION_POWER_ON)

    def contrast(self, contrast): # default 255
        assert 0 <= contrast and 256 > contrast
        self.__pygame_signal(REQUEST_ACTION_CONTRAST, value=contrast)

    def invert(self, invert): # default False
        self.__pygame_signal(REQUEST_ACTION_INVERT, value=1 if invert else 0)

    def show(self):
        if not self.__power:
            return
        else:
            self.__screen_buffer[:] = self.buffer
            self.__pygame_signal(REQUEST_ACTION_REFRESH, rect=(0, 0, self.width, self.height))
        # sleep(0.05) # emu refresh speed
        wait(50)

    def refresh(self, x, y, w, h):
        if not self.__power:
            return
        else:
            for xp in range(w):
                for yp in range(h):
                    color = self.pixel(x + xp, y + yp)
                    self.__screen_frame.pixel(x + xp, y + yp, color)
            self.__pygame_signal(REQUEST_ACTION_REFRESH, rect=(x, y, w, h))
        # sleep(0.02)
        wait(20)
    
    def pygame_loop(self, wait=True):
        if self.__screen == None:
            return
        self.__screen.do_pygame_loop_once(self.__request_list, DEFAULT_FPS if wait else -1)
        self.__request_list.clear()

    def _pygame_stop(self):
        if self.__loop == None:
            return
        if not self.__loop.is_alive():
            self.__loop == None
            return
        while not self.__loop_queue.empty():
            self.__loop_queue.get_nowait() # clean queue
        try:
            self.__pygame_signal(REQUEST_ACTION_EXIT)
            self.__loop.join(1)
        except:
            print("killing pygame process...")
            self.__loop.terminate()
        self.__loop_queue.cancel_join_thread()
        self.__loop = None
