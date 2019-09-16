import socket, _thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 80))
s.listen(10)


# greq will return a string (example: www.example.com/exe -> exe)
def greq(d):
    if 'GET' == d[:3] and ' HTTP' in d:
        d = d.split('GET /')[1]
        d = d.split(' HTTP')[0]
        return d
    elif 'POST' == d[:4] and ' HTTP' in d:
        d = d.split('POST /')[1]
        d = d.split(' HTTP')[0]
        return d
    else:
        return ""


# postval will return a dictionary of post forms value
def postval(d):
    print(d)
    vals = {}
    d = d.split('\\r\\n')[-1].strip()
    d = d.split('&')
    try:
        for i in d:
            a, b = i.split('=')
            vals.update({a: b})
    except:
        return {}
    return vals


# getget will return a dictionary of get forms value
def getget(r):
    dic = {}
    r = r.split('?')[-1]
    r = r.split('&')
    for i in r:
        s = i.split('=')
        dic.update({s[0]: s[1]})
    return dic


# gcookie will return a dictionary of cookies on client browser
def gcookie(d):
    dic = {}
    if '\\r\\nCookie: ' in d:
        d = d.split('\\r\\nCookie: ')[1]
        d = d.split('\\r\\n')[0]
        d = d.split('; ')
        for i in d:
            a, b = i.split('=')
            dic.update({a: b})
    else:
        return {}
    return dic


# set cookie will return a string wich can be used in makeres function as header
def setcookie(dic):
    header = 'Set-Cookie: '
    for i in dic:
        header += i + '=' + dic[i] + ';'
    return header[:-1]


# render will return a strin of a text file like html or txt
def render(dir):
    f = open(dir, 'r')
    return f.read()


# binrender is like render but it will return bytes of a binary file like png or jpeg or zip or...
def binrender(dir):
    f = open(dir, 'rb')
    return f.read()


# makeres return a http response (type is bytes)
def makeres(status_code, content, content_type, *headers):
    if type(content) == bytes:
        if headers == []:
            l = 'HTTP/1.1 ' + status_code + '\r\nContent-type: ' + content_type + '\r\nContent-Length: ' + str(
                len(content)) + '\r\n\r\n'
            l = l.encode() + content + b'\r\n'
        else:
            l = 'HTTP/1.1 ' + status_code + '\r\nContent-type: ' + content_type + '\r\nContent-Length: ' + str(
                len(content)) + '\r\n'
            for i in headers:
                l += i + '\r\n'
            l += '\r\n'
            l = l.encode() + content + b'\r\n'
    else:
        if not headers:
            l = 'HTTP/1.1 ' + status_code + '\r\nContent-type: ' + content_type + '\r\nContent-Length: ' + str(
                len(content.encode())) + '\r\n\r\n' + content + '\r\n'
            l = l.encode()
        else:
            l = 'HTTP/1.1 ' + status_code + '\r\nContent-type: ' + content_type + '\r\nContent-Length: ' + str(
                len(content)) + '\r\n'
            for i in headers:
                l += i + '\r\n'
            l += '\r\n' + content + '\r\n'
            l = l.encode()
    return l


def conn(x, b):
    ip = b[0]
    header = ''
    data = str(x.recv(1024))[2:-1]
    req = greq(data)

    # You can import and use your functions here!

    content = render('home.html')
    status_code = '200 OK'
    content_type = 'text/html'
    res = makeres(status_code, content, content_type, header)
    x.send(res)
    x.close()


while True:
    # Do not change it if you are making a simple website
    a, b = s.accept()
    _thread.start_new_thread(conn, (a, b))
