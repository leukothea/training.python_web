import socket
import sys
import os
import mimetypes

def resolve_uri(uri):
    """Write a new function resolve_uri that handles looking up resources on
  disk using the URI."""
    root= '/Users/catherine/Desktop/training.python_web/assignments/session02/webroot'
    path = root + uri
    if os.path.exists(path):
        if os.path.isdir(path):
            list = os.listdir(path)
            mimetype = "text/plain"
            return " ".join(list), mimetype
        elif os.path.isfile(root + uri):
            body = open(path, 'rb').read()
            extension = os.path.splitext(path)[1]
            mimetype = mimetypes.types_map[extension]
            return body, mimetype
    else:
        raise ValueError("URI does not exist")    


def response_not_found():
    """Write a new function response_not_found that returns a 404 response if the
  resource does not exist."""
    resp = []
    resp.append("HTTP/1.1 404 Not Found")
    resp.append("")
    return "\r\n".join(resp)

def response_ok(body, mimetype):
    """Update the response_ok function so that it accepts a body and mimetype
  argument and properly includes these in the response it generates."""
    resp = []
    resp.append("HTTP/1.1 200 OK")
    resp.append("Content-Type: %s" % mimetype)
    resp.append("")
    resp.append(body)
    return "\r\n".join(resp)

def response_method_not_allowed():
    """returns a 405 Method Not Allowed response"""
    resp = []
    resp.append("HTTP/1.1 405 Method Not Allowed")
    resp.append("")
    return "\r\n".join(resp)

def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    method, uri, protocol = first_line.split()
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    print >>sys.stderr, 'request is okay'
    return uri


def server():
    """Update the code in the server loop to use the new and changed functions you
  completed for the tasks above."""
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print >>sys.stderr, "making a server on %s:%s" % address
    sock.bind(address)
    sock.listen(1)
    
    try:
        while True:
            print >>sys.stderr, 'waiting for a connection'
            conn, addr = sock.accept() # blocking
            try:
                print >>sys.stderr, 'connection - %s:%s' % addr
                request = ""
                while True:
                    data = conn.recv(1024)
                    request += data
                    if len(data) < 1024 or not data:
                        break

                try:
                    uri = parse_request(request)
                except NotImplementedError:
                    response = response_method_not_allowed()
                except LookupError:
                    response = response_not_found()
                else:
                    try:
                        body, mimetype = resolve_uri(uri)
                    except ValueError:
                        response = response_not_found()
                    else:
                        response = response_ok(body, mimetype)

                print >>sys.stderr, 'sending response'
                conn.sendall(response)
            finally:
                conn.close()
            
    except KeyboardInterrupt:
        sock.close()
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
