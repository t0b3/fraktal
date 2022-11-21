import os
from http.server import SimpleHTTPRequestHandler
from urllib import parse
from http.server import ThreadingHTTPServer as HTTPServer

from fraktal import Drawing


class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server, cache: bool = False):
        self.cache = cache
        super().__init__(request, client_address, server)

    def list_directory(self, path):
        self.send_error(403, "Request forbidden")

    def do_GET(self):
        """Respond to a GET request."""

        def send_response(response, mimetype):
            # serve image directly
            self.send_response(200)
            self.send_header("content-type", mimetype)
            self.send_header("access-control-allow-origin", "*")
            self.end_headers()
            self.wfile.write(response)

        def save_to_file(content, filename):
            basedir = os.path.dirname(filename)
            if not (os.path.isdir(basedir)):
                # create basedir if not exists
                os.makedirs(basedir)
            fh = open(filename, "wb")
            fh.write(content)
            fh.close()

        # serve static files
        static_routes = (
            self.path in ('/', '/favicon.ico', '/manifest.json'),
            self.path.startswith('/?'),
            self.path.startswith('/assets'))
        if any(static_routes):
            self.path = '/app' + self.path
            super().do_GET()

        # serve WMTS tile requests
        elif (self.path.startswith('/wmts/')):
            real_path = super().translate_path('/cache' + self.path)

            if (os.path.isfile(real_path)):
            # file exists: serve from cache
                super().do_GET()

            else:
            # file does not exist: calculate
                # parse input params
                p = self.path.rstrip('.png').rsplit('wmts/')[-1].split('/')
                par = {"x_row": int(p[-2]),
                       "y_row": int(p[-1]),
                       "zoomlevel": int(p[-3]),
                       "style": p[1],
                       "fractal": p[0]}
                if (len(p)==7):
                    if (p[2]=='undefined'):
                        par["c"]=0
                    else:
                        par["c"]=complex(float(p[2]),
                                         float(p[3]))

                png = Drawing.generate_image_wmts_tile(par)

                send_response(png, mimetype="image/png")

                # save image to WMTS cache (optionally)
                if (self.cache):
                    save_to_file(png, real_path)

        # serve WMS get image requests
        elif (self.path.startswith("/wms")):
            p = dict(parse.parse_qsl(parse.urlsplit(self.path).query))

            def filter_neg_dict(d: dict, keys: list):
                return {k: v for k, v in d.items() if k not in keys}
            # TODO: implement service error handling
            p = filter_neg_dict(p, ['SERVICE','VERSION','REQUEST'])
            p = filter_neg_dict(p, ['FORMAT','TRANSPARENT','CRS'])

            par = {"fractal": p["LAYERS"],
                   "style": p["STYLES"],
                   "width": int(p["WIDTH"]),
                   "height": int(p["HEIGHT"])}
            par["xmin"] = float(p["BBOX"].split(',')[0])
            par["ymin"] = float(p["BBOX"].split(',')[1])
            par["xmax"] = float(p["BBOX"].split(',')[2])
            par["ymax"] = float(p["BBOX"].split(',')[3])
            if (("CX" and "CY") in p.keys()):
                par["c"] = complex(float(p["CX"]),
                                   float(p["CY"]))

            png = Drawing.generate_image_wms(par)

            send_response(png, mimetype="image/png")

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