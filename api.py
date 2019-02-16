from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import json
#create,update,view,list,delete
def readFromFile():
    TODOS=list()
    f=open('read.txt','r')
    filedata=f.read().splitlines()[1:]
    f.close()

    for i in filedata:
        item=i.split(':')
        dictItem=dict(id=item[0],string=item[1])
        TODOS.append(dictItem)
    return TODOS

def writeToFile():
    f=open("read.txt",'w')
    f.write("ID:STRING\n")
    for i in TODOS:
        f.write(str(i['id'])+":"+i['string']+"\n")
    f.close

class RestHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/list':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({'data': TODOS}))
            return
        elif self.path=='/view':
            _id=self.headers['id']
            for i in TODOS:
                if str(i['id'])==str(_id):
                    self.wfile.write(i['string'])
                    break
            self.send_response(200)
            self.end_headers()
            return
        else:
            self.wfile.write("This page doesn't exist")
            self.send_response(404)
            self.end_headers() 

    def do_POST(self):
        if self.path =='/create':
            postedData = cgi.FieldStorage(fp=self.rfile,
                           environ={
                                'REQUEST_METHOD':'POST', 
                                'CONTENT_TYPE':self.headers['Content-Type']
                           })
            new_string = postedData['string'].value
            new_id=postedData['id'].value
            new_todo = {'id':new_id, 'string': new_string}
            TODOS.append(new_todo)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(new_todo))
            writeToFile()
            return
        elif self.path=='/update':
            postedData = cgi.FieldStorage(fp=self.rfile,
                           environ={
                                'REQUEST_METHOD':'POST', 
                                'CONTENT_TYPE':self.headers['Content-Type']
                           })
            given_id = postedData['id'].value
            given_string=postedData['string'].value
            for i in TODOS:
                if str(i['id'])==str(given_id):
                    i['string']=given_string
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(TODOS))
            writeToFile()
        elif self.path=='/delete':
            postedData = cgi.FieldStorage(fp=self.rfile,
                           environ={
                                'REQUEST_METHOD':'POST', 
                                'CONTENT_TYPE':self.headers['Content-Type']
                           })
            given_id = postedData['id'].value
            for i in TODOS:
                if str(i['id'])==str(given_id):
                    TODOS.remove(i)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(TODOS))
            writeToFile()
        else:
            self.wfile.write("This page doesn't exist")
            self.send_response(404)
            self.end_headers() 
TODOS=readFromFile()
httpd = HTTPServer(('localhost', 8000), RestHTTPRequestHandler)
httpd.serve_forever()