var RESOLUTIONS = [];
for (var i = -7; i > -53; i--) {
  RESOLUTIONS.push(2**i);
}
var MAX_RESOLUTION = Math.max(...RESOLUTIONS);
var MAX_ZOOM = RESOLUTIONS.length-1;

var EXTENT = [-16, -8, 16, 8];
var PROJECTION = ol.proj.get("EPSG:4326");
PROJECTION.setExtent(EXTENT);

var CENTER_X = 0;
var CENTER_Y = 0;
var INITIAL_ZOOM = 0;

var mapX = CENTER_X;
var mapY = CENTER_Y;
var mapZoom = INITIAL_ZOOM;
var mapLayer = "mandelbrot";
var mapStyle = "default";
var mapCX, mapCY;

var map;

function initialize() {
    readURL();
    initializeMap();
}

function initializeMap() {
  var matrixIds = [];
  for (var i = 0; i < RESOLUTIONS.length; i++) {
    matrixIds.push(i);
  }

  if(mapCX===undefined || mapCY===undefined) {
    var layerURL = "http://localhost:8080/wmts/{Layer}/{Style}/{TileMatrix}/{TileCol}/{TileRow}.png";
  } else {
    var layerURL = "http://localhost:8080/wmts/{Layer}/{Style}/{cx}/{cy}/{TileMatrix}/{TileCol}/{TileRow}.png";
  }

  var fraktalLayer = new ol.layer.Tile({
    source: new ol.source.WMTS({
      url: layerURL,
      tileGrid: new ol.tilegrid.WMTS({
        origin: [CENTER_X,CENTER_Y],
        resolutions: RESOLUTIONS,
        matrixIds: matrixIds
      }),
      projection: PROJECTION,
      layer: mapLayer,
      style: mapStyle,
      dimensions: {
        'cx': mapCX,
        'cy': mapCY
      },
      format: 'image/png',
      requestEncoding: "REST"
    })
  })

  map = new ol.Map({
    target: 'map',
    layers: [fraktalLayer],
    view: new ol.View({
      center: [mapX, mapY],
      zoom: mapZoom,
      projection: PROJECTION,
      maxResolution: MAX_RESOLUTION,
      extent: EXTENT,
      maxZoom: MAX_ZOOM,
      constrainResolution: true
    }),
    controls: ol.control
      .defaults({
        attributionOptions: {
          collapsible: false
        }
      })
      .extend([
        new ol.control.ScaleLine({
          target: document.getElementById("scale-line"),
          units: "metric"
        })
      ]),
    logo: false
  });

/*
  fraktalLayer.on("prerender", function(evt) {
      evt.context.imageSmoothingEnabled = false;
      evt.context.webkitImageSmoothingEnabled = false;
      evt.context.mozImageSmoothingEnabled = false;
      evt.context.msImageSmoothingEnabled = false;
  });
*/

  map.on("moveend", function(evt) {
    pushURL();
  });
}


function handleLayerRowClicked(event, layerId) {
  mapLayer = layerId;
  // dirty hack to change WMTS layer, update source and refresh tiles
  map.getLayers().item(0).getSource().layer_ = layerId;
  map.getLayers().item(0).getSource().setUrls(map.getLayers().item(0).getSource().getUrls());
  map.getLayers().item(0).getSource().refresh();
  pushURL();
}


function handleStyleRowClicked(event, styleId) {
  mapStyle = styleId;
  // dirty hack to change WMTS style, update source and refresh tiles
  map.getLayers().item(0).getSource().style_ = styleId;
  map.getLayers().item(0).getSource().setUrls(map.getLayers().item(0).getSource().getUrls());
  map.getLayers().item(0).getSource().refresh();
  pushURL();
}


function handleLayersTitleClick() {
  var layersBody = document.getElementById("layers-body");
  var caret = document.getElementById("layers-caret");

  layersBody.classList.toggle("hidden");
  caret.classList.toggle("caret-up");
  caret.classList.toggle("caret-down");
}


function handleStylesTitleClick() {
  var stylesBody = document.getElementById("styles-body");
  var caret = document.getElementById("styles-caret");

  stylesBody.classList.toggle("hidden");
  caret.classList.toggle("caret-up");
  caret.classList.toggle("caret-down");
}



/**
 * Read the URL search params and set the variables according to them.
 * This makes it possible to share the link to a specific view.
 * Possible params:
 * - mapX {Number} the X Coordinate of the map center
 * - mapY {Number} the YCoordinate of the map center
 * - zoom {Number} the zoom level of the map
 */
function readURL() {
  var searchParams = new URLSearchParams(location.search);

  if (searchParams.has("x")) {
    var x = parseFloat(searchParams.get("x"));
    if (!Number.isNaN(x)) {
      mapX = x;
    }
  }

  if (searchParams.has("y")) {
    var y = parseFloat(searchParams.get("y"));
    if (!Number.isNaN(y)) {
      mapY = y;
    }
  }

  if (searchParams.has("zoom")) {
    var zoom = parseFloat(searchParams.get("zoom"));
    if (!Number.isNaN(zoom)) {
      mapZoom = zoom;
    }
  }

  if (searchParams.has("cx")) {
    var cx = parseFloat(searchParams.get("cx"));
    if (!Number.isNaN(cx)) {
      mapCX = cx;
    }
  }

  if (searchParams.has("cy")) {
    var cy = parseFloat(searchParams.get("cy"));
    if (!Number.isNaN(cy)) {
      mapCY = cy;
    }
  }

  if (searchParams.has("formula")) {
    var formula = searchParams.get("formula").toLowerCase();
    mapLayer = formula;
  }

  if (searchParams.has("style")) {
    var style = searchParams.get("style").toLowerCase();
    mapStyle = style;
  }

  if (map && map.getView()) {
    var view = map.getView();
    view.setCenter([mapX, mapY]);
    view.setZoom(mapZoom);
  }
}

/**
 * Generate the URL search params for the current view and push it to the window history
 */
function pushURL() {
  var baseUrl = location.protocol + "//" + location.host + location.pathname;

  var searchParams = new URLSearchParams();

  mapX = map.getView().getCenter()[0];
  mapY = map.getView().getCenter()[1];
  mapZoom = map.getView().getZoom();

  searchParams.set("x", mapX);
  searchParams.set("y", mapY);
  if (mapZoom != undefined) {
    searchParams.set("zoom", mapZoom);
  }
  if (mapCX != undefined) {
    searchParams.set("cx", mapCX);
  }
  if (mapCY != undefined) {
    searchParams.set("cy", mapCY);
  }
  searchParams.set("formula", mapLayer);
  searchParams.set("style", mapStyle);

  var parameter = "?" + searchParams.toString();

  var url = baseUrl + parameter;

  window.history.pushState({}, window.title, url);
}

function recenterMap() {
  var view = map.getView();
  view.setCenter([CENTER_X, CENTER_Y]);
  view.setZoom(INITIAL_ZOOM);
}


initialize();

