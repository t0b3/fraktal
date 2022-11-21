from flask import Flask, Response, request, send_from_directory

from fraktal import Drawing


app = Flask(__name__)


@app.route('/', defaults={'filename': 'index.html'})
@app.route('/<path:filename>')
def srv_app(filename):
    resp = send_from_directory('app', filename)
    resp.access_control_allow_origin='*'
    return resp


@app.route('/wmts/<path:path>')
def wmts(path):
    p = path.rstrip('.png').split('/')
    par = { "x_row": int(p[-2]),
            "y_row": int(p[-1]),
            "zoomlevel": int(p[-3]),
            "style": p[1],
            "fractal": p[0] }
    if (len(p)==7):
        if (p[2]=='undefined'):
            par["c"]=0
        else:
            par["c"]=complex(float(p[2]),
                    float(p[3]))

    png = Drawing.generate_image_wmts_tile(par)

    resp = Response(png, mimetype='image/png')
    resp.access_control_allow_origin='*'
    return resp



@app.route('/wms/')
def wms():
    p = request.args

    #def filter_neg_dict(d: dict, keys: list):
    #    return {k: v for k, v in d.items() if k not in keys}
    #
    #p = filter_neg_dict(p, ['SERVICE','VERSION','REQUEST'])
    #p = filter_neg_dict(p, ['FORMAT','TRANSPARENT','CRS'])

    par = { "fractal": p["LAYERS"],
            "style": p["STYLES"],
            "width": int(p["WIDTH"]),
            "height": int(p["HEIGHT"]) }
    par["xmin"], par["ymin"], par["xmax"], par["ymax"] = map(float, p["BBOX"].split(','))
    if (("CX" and "CY") in p.keys()):
        par["c"] = complex(float(p["CX"]),
                           float(p["CY"]))

    png = Drawing.generate_image_wms(par)

    resp = Response(png, mimetype='image/png')
    resp.access_control_allow_origin='*'
    return resp


if __name__ == "__main__":
    app.run()
