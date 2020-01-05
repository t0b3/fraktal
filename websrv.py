import os
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler
try:
    # with python >= 3.7 use multithreaded HTTPServer
    from http.server import ThreadingHTTPServer as HTTPServer
except:
    from http.server import HTTPServer

from fraktal import Drawing
import shutil, io


class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server, cache: bool = False):
        self.cache = cache
        super().__init__(request, client_address, server)

    def list_directory(self, path):
        self.send_error(403, "Request forbidden")

    def do_GET(self):
        """Respond to a GET request."""
        # serve static index file
        if (self.path in ('/', '/favicon.ico')):
            self.path = '/srv' + self.path
            super().do_GET()

        # serve static app files
        elif (self.path.startswith('/app')):
            super().do_GET()

        # serve WMTS tile requests
        elif (self.path.startswith('/wmts/')):
            self.path = '/cache' + self.path
            real_path = super().translate_path(self.path)

            if (os.path.isfile(real_path)):
            # file exists: serve from cache
                super().do_GET()

            else:
            # file does not exist: calculate
                # parse input params
                p = real_path.rstrip('.png').rsplit('wmts/')[-1].split('/')
                par = {"x_row": int(p[-2]),
                       "y_row": int(p[-1]),
                       "zoomlevel": int(p[-3]),
                       "style": p[1],
                       "fractal": p[0]}
                if (len(p)==7):
                    par["c_x"]=complex(float([2]),
                                       float(p[3]))

                image = Drawing.generate_wmts_tile(par)

                # serve image directly
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.end_headers()
                f = io.BytesIO()
                image.save(f, "PNG")
                f.seek(0)
                shutil.copyfileobj(f, self.wfile)
                f.close()

                # save image to WMTS cache (optionally)
                if (self.cache):
                    basedir = os.path.dirname(real_path)
                    if not (os.path.isdir(basedir)):
                        create basedir if not exists
                        os.makedirs(basedir)
                    image.save(real_path)
                    if (verbose):
                        print("image saved:", real_path)
                image.close()

        # serve WMS get image requests
        elif (self.path.startswith("/wms")):
            self.send_error(501)

        # respond with failure to unexpected requests
        else:
            self.send_error(500)


# start HTTP server
def start_webservice(server_address = ('127.0.0.1', 8080), server_class=HTTPServer, handler_class=MyHandler):
    httpd = server_class(server_address, handler_class)
    print("listening at http://"+server_address[0]+":"+str(server_address[1]))
    httpd.serve_forever()

if __name__ == "__main__":
    start_webservice()