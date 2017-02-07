import jinja2
from aiohttp import web
import aiohttp_jinja2


def read_file():
    try:
        with open('checked', 'rb') as text:
            return text.read().decode('utf-8')
    except:
        pass
    return str(True)


def write_file(value):
    f = open('checked', 'w')
    f.write(value)
    f.close()


# async def handle_get(request):
#     headers = {"Content-Type": "text/html"}
#     with open("index.html", "rb") as html_body:
#         response = web.Response(body=html_body.read(), headers=headers)
#     return response
@aiohttp_jinja2.template('index.html')
async def handle_get(request):
    value = read_file()
    ch = ''
    if value == 'True':
        ch = 'checked'

    return {'name': 'vvvv', 'ch': ch}


async def start_xhr(request):
    data = {}
    return web.json_response(data)


async def restart_xhr(request):
    data = {}
    return web.json_response(data)


async def stop_xhr(request):
    data = {}
    return web.json_response(data)


async def checkboxed_change(request):
    data = {}
    value = read_file()
    if value == 'True':
        write_file('False')
    else:
        write_file('True')
    return web.json_response(data)


# @aiohttp_jinja2.template('tmpl.jinja2')
# def handler(request):
#     return {''}


async def button_get(request):
    headers = {"Content-Type": "text/css"}
    with open("base.css", "rb") as html_body:
        response = web.Response(body=html_body.read(), headers=headers)
    return response


app = web.Application()

app.router.add_get('/base.css', button_get)
app.router.add_get('/', handle_get)

app.router.add_route('start', '/', start_xhr)
app.router.add_route('restart', '/', restart_xhr)
app.router.add_route('stop', '/', stop_xhr)
app.router.add_route('checkboxed', '/', checkboxed_change)

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

web.run_app(app)
