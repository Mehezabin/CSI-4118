import socket

HOST= '127.0.0.1'

PORT = 8989

my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
my_socket.bind((HOST,PORT))
my_socket.listen(1)

print('Serving on port ',PORT)

while True:
    clientconnection,address = my_socket.accept()
    request = clientconnection.recv(1024).decode('utf-8')
    # Split request from spaces
    string_list = request.split(' ')     
    print(request)
    method = string_list[0]
    requested_file = string_list[1]

    print('Client request ', requested_file)

    filename = requested_file.split('?')[0] 
    # get rid of the / to get the filename
    filename = filename.lstrip('/')
    
    try:
        file = open(filename,'rb') # read file in byte format
        response = file.read()
        file.close()

        header = 'HTTP/1.1 200 OK\n'

        # determining the file type to render in the browser
        if(filename.endswith(".jpg")):
            mimetype = 'image/jpg'
        elif(filename.endswith(".css")):
            mimetype = 'text/css'
        elif(filename.endswith(".mp4")):
            mimetype = 'video/mp4'
        elif(filename.endswith(".mp3")):
            mimetype = 'audio/mp3'
        else:
            mimetype = 'text/html'

        header += 'Content-Type: '+str(mimetype)+'\n\n'

    except Exception as e:
        #when the file is not found by the server
        # display error message
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><h1>404 Not Found</h1></body></html>'.encode('utf-8')

    final_response = header.encode('utf-8')
    final_response += response
    clientconnection.send(final_response)
    clientconnection.close()
