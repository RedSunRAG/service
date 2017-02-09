import jinja2
from aiohttp import web
import aiohttp_jinja2
from subprocess import PIPE, Popen, getoutput

# чтение из файла информации о состоянии чекбокса
def read_file():
    try:
        with open('checked', 'rb') as text:
            return text.read().decode('utf-8')
    except:
        pass
    return str(True)

# запись в файл состояния чекбокса
def write_file(value):
    f = open('checked', 'w')
    f.write(value)
    f.close()


# обработчик для отоброажения индексной станицы
# аботает через шаблонизатор jinja2
@aiohttp_jinja2.template('index.html')
async def handle_get(request):
    value = read_file()
    ch = ''
    dis = 'disabled'
    if value == 'True':
        ch = 'checked'
        dis = ''
    status = view_mysql_status()
    return {'name': status,'ch': ch, 'dis' : dis}


# функция определения статуса mysql
def view_mysql_status():
    n = ''
    status_desk = 'Active: active (running)'
    o,t = get_status_mysql()
    o = o.decode('utf-8')
    sd = o.__contains__(status_desk)
    if sd == True:
        n = 'работает'
    else:
        n = 'остановлен'
    return n


# обработчик для запуска службы mysql
async def start_xhr(request):
    data = {}
    start_mysql()
    return web.json_response(data)


# обработчик для перезапуска службы mysql
async def restart_xhr(request):
    data = {}
    restart_mysql()
    return web.json_response(data)


# обработчик для остановки службы mysql
async def stop_xhr(requestq):
    data = {}
    stop_mysql()
    return web.json_response(data)


# обрабатываем событие изменения состояния чекбокса
async def checkboxed_change(request):
    data = {}
    value = read_file()
    if value == 'True':
        write_file('False')
    else:
        write_file('True')
    return web.json_response(data)


# возврсщает стили
async def css_get(request):
    headers = {"Content-Type": "text/css"}
    with open("base.css", "rb") as html_body:
        response = web.Response(body=html_body.read(), headers=headers)
    return response



#def get_cur_user():
#    return getoutput('whoami')


#получение информации о статусе mysql
def get_status_mysql():
    command = '/etc/init.d/mysql status'
    p = Popen(command, shell=True, stdout=PIPE,stderr=PIPE,stdin=PIPE)
    out, err = p.communicate()
    return out, err

# запуск сервиса mysql
def start_mysql():
    out=None
    err=None
    command = 'service mysql start'
    p = Popen(command, shell=True, stderr=PIPE, stdin=PIPE)
    out,err = p.communicate()
    return out,err

# остановка сервиса mysql
def stop_mysql():
    out=None
    err=None
    command = 'service mysql stop'
    p = Popen(command, shell=True, stderr=PIPE, stdin=PIPE)
    out,err = p.communicate()
    return out,err

# перезапуск сервиса mysql
def restart_mysql():
    out=None
    err=None
    command = 'service mysql restart'
    p = Popen(command, shell=True, stderr=PIPE, stdin=PIPE)
    out,err = p.communicate()
    return out,err



# создание Application
app = web.Application()
# добавление пути для срабатывания обработчиков
# стили
app.router.add_get('/base.css', css_get)
# индексная стриница
app.router.add_get('/', handle_get)
# собственный http метод для запуска слжбы
app.router.add_route('start', '/', start_xhr)
# собственный http метод для перезапуска слжбы
app.router.add_route('restart', '/', restart_xhr)
# собственный http метод для остановки слжбы
app.router.add_route('stop', '/', stop_xhr)
# собственный http метод изменения статус чекбокса
app.router.add_route('checkboxed', '/', checkboxed_change)
# конфигурация jinja2 откуда будут браться шаблоны, в нашем случае index.html
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
# запуск web-сервера
web.run_app(app)
