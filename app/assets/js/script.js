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

var map;

function initialize() {
    initializeMap();
    readURL();
}

function initializeMap() {
  var matrixIds = [];
  for (var i = 0; i < RESOLUTIONS.length; i++) {
    matrixIds.push(i);
  }

  var fraktalLayer = new ol.layer.Tile({
    source: new ol.source.WMTS({
      url:
        "http://localhost:8080/wmts/{Layer}/default/{TileMatrix}/{TileCol}/{TileRow}.png",
      tileGrid: new ol.tilegrid.WMTS({
        origin: [0,0],
        resolutions: RESOLUTIONS,
        matrixIds: matrixIds
      }),
      projection: PROJECTION,
      layer: "mandelbrot",
      requestEncoding: "REST"
    })
  })

  map = new ol.Map({
    target: 'map',
    layers: [fraktalLayer],
    view: new ol.View({
      center: [mapX, mapY],
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

  if (searchParams.has("mapX")) {
    var x = parseFloat(searchParams.get("mapX"));
    if (!Number.isNaN(x)) {
      mapX = x;
    }
  }

  if (searchParams.has("mapY")) {
    var y = parseFloat(searchParams.get("mapY"));
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

  searchParams.set("mapX", mapX);
  searchParams.set("mapY", mapY);
  if (mapZoom != undefined) {
    searchParams.set("zoom", mapZoom);
  }

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

