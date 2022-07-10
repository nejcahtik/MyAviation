from MyServer import MyServer
from http.server import BaseHTTPRequestHandler, HTTPServer
from config import config

serverConfig=config["server"]

hostName = serverConfig["host"]
serverPort = serverConfig["port"]


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("MyAviation started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
