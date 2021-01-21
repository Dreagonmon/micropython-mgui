import asyncio, threading, os, json
from aiohttp import web
from . import framebuf

class MonoScreenEmu(framebuf.FrameBuffer):
    def __init__(self,width,height,name="main"):
        # assert width <= 128 and width >= 2
        # assert height <= 64 and height >= 2
        self.width = width
        self.height = height
        self.pages = self.height // 8
        self.buffer = memoryview(bytearray(self.pages * self.width))
        self.screen = memoryview(bytearray(self.pages * self.width))
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.name = name
        self.is_invert = True # True means black background and white color
        self.__buttons = [None] * 15
        self.__callback = {}
        self.init_display()
    
    def __button_callback(self,key,op):
        if key in self.__callback:
            self.__callback[key](key,op)

    def init_display(self):
        start()
        setup_screen(self.name,self.width,self.height,self.screen,invert=self.is_invert,buttons=self.__buttons,button_callback=self.__button_callback)
        pass

    def show(self):
        for x in range(self.width):
            for p in range(self.pages):
                self.screen[p*self.width + x] = self.buffer[p*self.width + x]
        update_screen(self.name,self.screen)
    def register_key(self,pos,key=None,callback=None):
        assert pos >= 0 and pos <= 14, "key position must in [0,14]"
        assert (key == None) or (not key in self.__buttons), "key name should be different"
        self.unregister_key(pos)
        self.__buttons[pos] = key
        if callback != None and key != None:
            self.__callback[key] = callback
        self.init_display()
    def unregister_key(self,pos):
        assert pos >= 0 and pos <= 14, "key position must in [0,14]"
        if self.__buttons[pos] != None:
            # clear callback
            name = self.__buttons[pos]
            if name in self.__callback:
                del self.__callback[name]
            self.__buttons[pos] = None
        setup_screen(self.name,self.width,self.height,self.screen,invert=self.is_invert,buttons=self.__buttons,button_callback=self.__button_callback)
    def is_key_down(self,key):
        '''this function is only for emu, you must use another implement in micropython'''
        return remote_is_key_down(self.name,key)

# screen server
index_html = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SSD1306 SCREEN LIST</title>
  <script>
    var screens = JSON.parse(`{screens:s}`)
    function renderButtons() {
      console.log(screens)
      let container = document.querySelector("#screens")
      for (let k in screens){
        let name = screens[k]
        let link = document.createElement("a")
        link.innerText = name
        link.href = `/${name}`
        container.append(link)
      }
    }
    // 浏览器事件
    window.onload = () => {
      renderButtons()
    }
  </script>
  <style>
    #container {
      margin: 0 auto;
      max-width: 512px;
      display: flex;
      flex-direction: column;
      align-items: center;
      background: lightskyblue;
    }
    #screens {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
  </style>
</head>
<body id="container">
  <h3>Screen List</h3>
  <div id="screens"></div>
</body>
</html>
'''
screen_html = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SSD1306 SCREEN {name:s}</title>
  <script>
    var sse_nm = undefined
    var buttons = JSON.parse(`{buttons:s}`)
    var keylist = ["r","t","y","u","i","f","g","h","j","k","c","v","b","n","m"]
    var keyEventList = {}
    function drawScreen(data,width,height,imgData){
      let rows = Math.ceil(data.length / width)
      for (let row=0;row<rows;row++){
        for (let col=0;col<width;col++){
          for (let bit=7;bit>-1;bit--){
            // parse byte
            y = row*8 + bit
            pos = y*width + col
            pat = 0x01 << bit
            // console.log(col,y)
            if ((data[row*width + col] & pat) > 0){
              imgData.data[pos*4] = 0x00 //R
              imgData.data[pos*4+1] = 0x00 //G
              imgData.data[pos*4+2] = 0x00 //B
              imgData.data[pos*4+3] = 0xff //A
            }else{
              imgData.data[pos*4] = 0xff //R
              imgData.data[pos*4+1] = 0xff //G
              imgData.data[pos*4+2] = 0xff //B
              imgData.data[pos*4+3] = 0xff //A
            }
          }
        }
      }
      // console.log(imgData.data)
      return imgData
    }
    function screenUpdate(event) {
      // update screen
      let screen = JSON.parse(event.data)
      window.data = screen
      // 调整canvas尺寸
      let canvas = document.querySelector("#screen-img")
      let cwidth = canvas.clientWidth
      let cheight = Math.ceil(cwidth * screen.height / screen.width)
      canvas.style.height = `${cheight}px`
      canvas.width = screen.width
      canvas.height = screen.height
      // 绘制图像
      let ctx = canvas.getContext("2d");
      ctx.fillStyle = "#000";
      ctx.imageSmoothingEnabled = false; // 像素风
      ctx.fillRect(0,0,screen.width,screen.height)
      let imgData = ctx.getImageData(0,0,screen.width,screen.height)
      imgData = drawScreen(screen.data,screen.width,screen.height,imgData)
      ctx.putImageData(imgData,0,0)
      //
    }
    function startService() {
      // 关闭现有的连接
      if (sse_nm != undefined)
        sse_nm.close()
      sse_nm = new EventSource("/screen_event/{name:s}")
      sse_nm.addEventListener("screen_update", screenUpdate)
      sse_nm.onerror = () => {
        stopService()
        // 3秒后重试连接，防止频繁请求服务器
        setTimeout(startService, 3000);
      }
    }
    function stopService() {
      if (sse_nm != undefined)
        sse_nm.close()
    }
    // 按钮事件
    function keyOp(key,op,event){
      event.preventDefault()
      // effect
      let btn = document.querySelector(`#btn-${key}`)
      if (op == "down"){
        btn.style.background = `rgba(255, 255, 255, 0.2)`
      }else{
        btn.style.background = ""
      }
      let url = `/keypad_event/{name:s}/${key}/${op}`
      navigator.sendBeacon(url)
      // console.log(url)
    }
    function renderButtons(){
      // 设置样式
      const COLS = 5
      let container = document.querySelector("#buttons")
      container.innerHTML = ""
      let rows = Math.ceil(buttons.length / COLS)
      let cwidth = container.clientWidth
      let cheight = rows * (cwidth / COLS)
      container.style.gridTemplateColumns = `repeat(5, 1fr)`;
      container.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
      container.style.height = `${cheight}px`
      // 布局按钮
      keyEventList = {}
      for (let i in buttons){
        let keyName = buttons[i]
        let keyboard = keylist[i]
        let btn = document.createElement("button")
        btn.innerText = keyName
        if (keyName != null && keyName != ""){
          btn.id = `btn-${keyName}`
          btn.onmousedown = btn.ontouchstart = keyOp.bind(this,keyName,"down")
          btn.onmouseup = btn.ontouchend = keyOp.bind(this,keyName,"up")
          keyEventList[keyboard] = keyName;
        }else{
          btn.ontouchstart = btn.ontouchend = btn.onclick = (event)=>{event.preventDefault()}
          btn.style.background = "none"
          btn.style.border = "none"
        }
        container.append(btn)
      }
    }
    // 浏览器事件
    window.onload = ()=>{
      startService()
      renderButtons()
    }
    window.onresize = renderButtons
    window.onkeydown = (event)=>{
      let code = event.key.toLowerCase()
      if ((code in keyEventList) && !event.repeat){
        keyOp(keyEventList[code],"down",event)
      }
    }
    window.onkeyup = (event)=>{
      let code = event.key.toLowerCase()
      if ((code in keyEventList) && !event.repeat){
        keyOp(keyEventList[code],"up",event)
      }
    }
  </script>
  <style>
    #container {
      margin: 0 auto;
      max-width: 512px;
      display: flex;
      flex-direction: column;
      align-items: center;
      background: #000;
      color: #FFF;
    }
    #screen-img {
      image-rendering: optimizeSpeed;
      image-rendering: -moz-crisp-edges;
      image-rendering: -o-crisp-edges;
      image-rendering: -webkit-crisp-edges;
      image-rendering: crisp-edges;
      image-rendering: -webkit-optimize-contrast;
      image-rendering: pixelated;
      -ms-interpolation-mode: nearest-neighbor;
      width: 80%;
    }
    #buttons {
      margin-top: 1rem;
      width: 100%;
      display: grid;
      gap: 0.3rem;
    }
    #buttons button{
      background: transparent;
      border-radius: 0.5rem;
      border: 1px solid #FFF;
      color: #FFF;
    }
    #info {
      font-family: monospace;
      font-size: 2rem;
    }
  </style>
</head>
<body id="container">
  <div>{name:s}</div>
  <canvas id="screen-img"></canvas>
  <div id="buttons"></div>
  <div>you can use the follow key to control keyEvent:</div>
  <div id="info">
    <div>R T Y U I</div>
    <div>F G H J K</div>
    <div>C V B N M</div>
  </div>
</body>
</html>
'''


# config
__HOST = "0.0.0.0"
__PORT = 8848

# global var
__server_thread = None
__httpd = None
__loop = None
__stop = False
__screens = {}
__lock_table = {} # screen_name -> lock
__resp_list = []

def start():
    global  __server_thread
    # 不要重复启动服务
    if __server_thread != None and __server_thread.is_alive():
        return
    __server_thread = threading.Thread(target=__start_server)
    __server_thread.setDaemon(True)
    __server_thread.start()

def setup_screen(name,width,height,buffer,invert=True,buttons=[],button_callback=None):
    assert buffer != None
    # assert width <= 128 and width >= 2
    # assert height <= 64 and height >= 2
    __screens[name] = {"buffer":buffer,"width":width,"height":height,"invert":invert,"buttons":buttons,"keypad":{},"callback":button_callback}

def remove_screen(name):
    if name in __screens:
        del __screens[name]

def update_screen(name,buffer):
    if __loop == None:
        return
    if name in __screens:
        __screens[name]["buffer"] = buffer
    asyncio.run_coroutine_threadsafe(__notify(name),__loop)

def remote_is_key_down(name,key):
    if name in __screens and key in __screens[name]["keypad"]:
        return __screens[name]["keypad"][key]
    return False

def stop():
    global __stop
    __stop = True

def is_running():
    return __server_thread != None and __server_thread.is_alive()

async def __stop_server():
    global __stop, __httpd
    __stop = False
    while not __stop:
        await asyncio.sleep(0.5)
    print("停止服务...")
    await __httpd.cleanup()
    loop = asyncio.get_event_loop()
    loop.call_soon(lambda loop: loop.stop(),loop)

async def __run_server():
    global __httpd
    app = web.Application()
    # 添加启动时任务
    app.on_startup.append(__before_server_start)
    # 添加应用关闭时回调
    app.on_shutdown.append(__before_server_stop)
    app.add_routes([
        web.post("/screen_event/{name}",__screen_event),
        web.get("/screen_event/{name}",__screen_event),
        web.post("/keypad_event/{name}/{key}/{op}",__keypad_event),
        web.get("/keypad_event/{name}/{key}/{op}",__keypad_event),
        web.get("/{name}",__screen_page),
        web.get("/",__index_page),
    ])
    __httpd = web.AppRunner(app)
    await __httpd.setup()
    site = web.TCPSite(__httpd, __HOST, __PORT)
    await site.start()
    print("服务启动在 {:s}:{:d}\n浏览器访问以获取ssd1306屏幕内容".format(__HOST,__PORT))
async def __before_server_start(app):
    app['keep_alive'] = asyncio.ensure_future(__keep_alive_task())
async def __before_server_stop(app):
    app['keep_alive'].cancel()
    await app['keep_alive']

def __start_server():
    global __loop
    __loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.get_event_loop_policy().set_event_loop(__loop)
    asyncio.run_coroutine_threadsafe(__run_server(),__loop)
    asyncio.run_coroutine_threadsafe(__stop_server(),__loop)
    __loop.run_forever()

# web请求相关方法
# 主页
async def __index_page(request):
    html = index_html.replace("{screens:s}",json.dumps(list(__screens.keys())))
    return web.Response(content_type="text/html",body=html)
# 屏幕页
async def __screen_page(request):
    name = request.match_info["name"]
    if name not in __screens:
        return web.Response(content_type="text/html",body="<h1>Screen Not Exist</h1>")
    html = screen_html.replace("{name:s}",name).replace("{buttons:s}",json.dumps(__screens[name]["buttons"]))
    return web.Response(content_type="text/html",body=html)
# 屏幕事件
def __get_lock(name):
    if not name in __lock_table:
        __lock_table[name] = asyncio.Condition()
    return __lock_table[name]
async def __notify(name):
    if not name in __lock_table:
        return False
    lock = __lock_table[name]
    await lock.acquire()
    try:
        lock.notify_all()
        return True
    except:
        return False
    finally:
        lock.release()
def __get_image_data(name):
    if not name in __screens.keys():
        return ""
    screen = __screens[name]
    width = screen["width"]
    height = screen["height"]
    data = []
    for byt in screen["buffer"]:
        if screen["invert"]:
            data.append(~byt & 0xFF)
        else:
            data.append(byt & 0xFF)
    data = {
        "width":width,
        "height":height,
        "data":data
    }
    return json.dumps(data)
async def __keep_alive_task():
    # 定时发送消息，防止连接关闭
    try:
        while True:
            await asyncio.sleep(30) #30s
            for resp in __resp_list:
                try:
                    await resp.write(":ping\r\n".encode("utf-8"))
                except:
                    __resp_list.remove(resp)
    except asyncio.CancelledError:
        pass
async def __screen_event(request):
    name = request.match_info["name"]
    resp = web.StreamResponse()
    # 设置响应头
    resp.headers['Content-Type'] = 'text/event-stream'
    resp.headers['Cache-Control'] = 'no-cache'
    resp.headers['Connection'] = 'keep-alive'
    resp.headers['X-Accel-Buffering'] = 'no'
    resp.enable_chunked_encoding()
    # 开始ServeSendEvent
    await resp.prepare(request)
    lock = __get_lock(name)
    __resp_list.append(resp)
    try:
        await resp.write(":connected\r\n".encode("utf-8"))
        # 激活一次事件
        await resp.write("event: {:s}\r\ndata: {:s}\r\n\r\n".format("screen_update",__get_image_data(name)).encode("utf-8"))
        while True:
            await lock.acquire()
            try:
                # 等待事件唤醒
                await lock.wait()
                await resp.write("event: {:s}\r\ndata: {:s}\r\n\r\n".format("screen_update",__get_image_data(name)).encode("utf-8"))
            finally:
                lock.release()
    finally:
        __resp_list.remove(resp)
    # 结束
    await resp.write_eof()
    return resp
# 按钮事件
async def __keypad_event(request):
    name = request.match_info["name"]
    key = request.match_info["key"]
    op = request.match_info["op"]
    assert op == "down" or op == "up"
    if name in __screens:
        if op == "down":
            __screens[name]["keypad"][key] = True
        else:
            __screens[name]["keypad"][key] = False
        # 如果设置过回调则调用
        if __screens[name]["callback"] != None:
            __screens[name]["callback"](key,op)
        return web.Response(body="ok")
    return web.Response(body="failed")