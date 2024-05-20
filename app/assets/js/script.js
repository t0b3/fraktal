const RESOLUTIONS = [];
for (let i = -7; i > -53; i--) {
  RESOLUTIONS.push(2**i);
}
const MAX_RESOLUTION = Math.max(...RESOLUTIONS);
const MAX_ZOOM = RESOLUTIONS.length-1;

const EXTENT = [-16, -8, 16, 8];
//var PROJECTION = ol.proj.get("EPSG:4326");
//PROJECTION.setExtent(EXTENT);
//var PROJECTION = new ol.proj.Projection({code:'0',units:'meters',extent:EXTENT,global:false,metersPerUnit:1,worldExtent:EXTENT});
const PROJECTION = null;

const CENTER_X = 0;
const CENTER_Y = 0;
const INITIAL_ZOOM = 0;

var mapX = CENTER_X;
var mapY = CENTER_Y;
var mapZoom = INITIAL_ZOOM;
var mapLayer = "mandelbrot";
var mapStyle = "default";
var mapCX, mapCY;

var map;
var wmtsLayer;
var wmsLayer;

function initialize() {
    readURL();
    initializeMap();
    handleLayerRowClicked(null, mapLayer);
    handleStyleRowClicked(null, mapStyle);
    document.getElementById("share-mailto").addEventListener("click", ()=>{open("mailto:?subject=Fraktal&body="+encodeURIComponent(location.href))});
    document.getElementById("share-qr").addEventListener("click", ()=>{open("https://chart.googleapis.com/chart?cht=qr&chs=180x180&choe=UTF-8&chld=L|1&chl="+encodeURIComponent(location.href))});
    if ('ontouchstart' in window) {
        document.getElementById("ol-touch").classList.toggle("ol-touch")
    }
}


// override ol.control.ScaleLine class with custom updateElement method
ol.control.ScaleLine.prototype.updateElement_ = function () {
  const DEFAULT_DPI = 25.4 / 0.28;
  const LEADING_DIGITS = [1, 2, 5];

  const viewState = this.viewState_;

  if (!viewState) {
    if (this.renderedVisible_) {
      this.element.style.display = 'none';
      this.renderedVisible_ = false;
    }
    return;
  }

  let pointResolution = ol.proj.getPointResolution(
    viewState.projection,
    viewState.resolution,
    viewState.center,
    'm',
  );

  const minWidth =
    (this.minWidth_ * (this.dpi_ || DEFAULT_DPI)) / DEFAULT_DPI;

  const maxWidth =
    this.maxWidth_ !== undefined
      ? (this.maxWidth_ * (this.dpi_ || DEFAULT_DPI)) / DEFAULT_DPI
      : undefined;

  let nominalCount = minWidth * pointResolution;
  nominalCount *= 1.1; // compensate rounding issue;
  let suffix;
  if (nominalCount < 1e-12) {
    suffix = ' &centerdot; 10<sup>-15</sup>';
    pointResolution *= 1e15;
  } else if (nominalCount < 1e-9) {
    suffix = ' &centerdot; 10<sup>-12</sup>';
    pointResolution *= 1e12;
  } else if (nominalCount < 1e-6) {
    suffix = ' &centerdot; 10<sup>-9</sup>';
    pointResolution *= 1e9;
  } else if (nominalCount < 0.001) {
    suffix = ' &centerdot; 10<sup>-6</sup>';
    pointResolution *= 1000000;
  } else if (nominalCount < 1) {
    suffix = ' &centerdot; 10<sup>-3</sup>';
    pointResolution *= 1000;
  } else if (nominalCount < 1000) {
    suffix = '';
  } else {
    suffix = ' &centerdot; 10<sup>3</sup>';
    pointResolution /= 1000;
  }

  let i = 3 * Math.floor(Math.log(minWidth * pointResolution) / Math.log(10));
  let count, width, decimalCount;
  let previousCount, previousWidth, previousDecimalCount;
  while (true) {
    decimalCount = Math.floor(i / 3);
    const decimal = Math.pow(10, decimalCount);
    count = LEADING_DIGITS[((i % 3) + 3) % 3] * decimal;
    width = Math.round(count / pointResolution);
    if (isNaN(width)) {
      this.element.style.display = 'none';
      this.renderedVisible_ = false;
      return;
    }
    if (maxWidth !== undefined && width >= maxWidth) {
      count = previousCount;
      width = previousWidth;
      decimalCount = previousDecimalCount;
      break;
    } else if (width >= minWidth) {
      break;
    }
    previousCount = count;
    previousWidth = width;
    previousDecimalCount = decimalCount;
    ++i;
  }
  const html = this.scaleBar_
    ? this.createScaleBar(width, count, suffix)
    : count.toFixed(decimalCount < 0 ? -decimalCount : 0) + ' ' + suffix;

  if (this.renderedHTML_ != html) {
    this.innerElement_.innerHTML = html;
    this.renderedHTML_ = html;
  }

  if (this.renderedWidth_ != width) {
    this.innerElement_.style.width = width + 'px';
    this.renderedWidth_ = width;
  }

  if (!this.renderedVisible_) {
    this.element.style.display = '';
    this.renderedVisible_ = true;
  }
}


function initializeMap() {

  const matrixIds = [];
  for (let i = 0; i < RESOLUTIONS.length; i++) {
    matrixIds.push(i);
  }

  // TODO: read & build layers list and their params dynamically
  function getLayerURL() {
    if(mapCX===undefined || mapCY===undefined) {
      return layerURL = "/wmts/{Layer}/{Style}/{TileMatrix}/{TileCol}/{TileRow}.png";
    } else {
      return layerURL = "/wmts/{Layer}/{Style}/{CX}/{CY}/{TileMatrix}/{TileCol}/{TileRow}.png";
    }
  };

  wmtsLayer = new ol.layer.Tile({
    source: new ol.source.WMTS({
      url: getLayerURL(),
      tileGrid: new ol.tilegrid.WMTS({
        origin: [CENTER_X,CENTER_Y],
        resolutions: RESOLUTIONS,
        matrixIds: matrixIds
      }),
      projection: PROJECTION,
      layer: mapLayer,
      style: mapStyle,
      dimensions: {
        'CX': mapCX,
        'CY': mapCY
      },
      format: 'image/png',
      attributions: '<a target="new" href="/about/">fraktal</a>',
      requestEncoding: "REST"
    })
  })

  wmsLayer = new ol.layer.Image({
    extent: EXTENT,
    source: new ol.source.ImageWMS({
      url: "/wms/",
      params: {
        LAYERS: mapLayer,
        FORMAT: "image/png",
        STYLES: mapStyle,
        VERSION: "1.3.0",
        CX: mapCX,
        CY: mapCY
      },
      serverType: "mapserver",
      attributions: '<a target="new" href="/about/">fraktal</a>',
    })
  });

  map = new ol.Map({
    target: 'map',
    layers: [wmtsLayer],
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
      .defaults.defaults({
        rotate: false,
        attributionOptions: {
          collapsible: false
        }
      })
      .extend([
        new ol.control.ZoomToExtent({
          label: '',
          extent: EXTENT
        })
      ])
      .extend([
        new ol.control.MousePosition({
          coordinateFormat: ol.coordinate.createStringXY(16),
//          projection: PROJECTION,
          // comment the following two lines to have the mouse position
          // be placed within the map.
          className: 'custom-mouse-position',
          target: document.getElementById('mouse-position'),
          undefinedHTML: '&nbsp;'
        })
      ])
      .extend([
        new ol.control.ScaleLine({
          target: document.getElementById("scale-line"),
          units: "metric",
          minWidth: 256
        })
      ]),
    interactions: ol.interaction
      .defaults.defaults({
        altShiftDragRotate:false,
        pinchRotate:false
      }),
    logo: false
  });
/*
  map.on('pointermove', function(event) {
    //console.log(event.coordinate);
  });
*/
  map.on('contextmenu', function(event) {
    event.preventDefault();
    [mapCX, mapCY] = event.coordinate;
    if(map.getLayers().item(0) == wmtsLayer) {
    // WMTS
      map.getLayers().item(0).getSource().setUrl(getLayerURL());
      map.getLayers().item(0).getSource().updateDimensions({'CX': mapCX, 'CY': mapCY});
    } else {
    // WMS
      map.getLayers().item(0).getSource().updateParams({'CX': mapCX, 'CY': mapCY});
    }
    pushURL();
  });

  document.getElementById('map').setAttribute('data-long-press-delay', '500');
  document.getElementById('map').addEventListener('long-press', function(event) {
    [mapCX, mapCY] = map.getCoordinateFromPixel([event.detail.clientX, event.detail.clientY]);
    if(map.getLayers().item(0) == wmtsLayer) {
    // WMTS
      map.getLayers().item(0).getSource().setUrl(getLayerURL());
      map.getLayers().item(0).getSource().updateDimensions({'CX': mapCX, 'CY': mapCY});
    } else {
    // WMS
      map.getLayers().item(0).getSource().updateParams({'CX': mapCX, 'CY': mapCY});
    }
    pushURL();
  });

/*
  wmtsLayer.on("prerender", function(event) {
      event.context.imageSmoothingEnabled = false;
      event.context.webkitImageSmoothingEnabled = false;
      event.context.mozImageSmoothingEnabled = false;
      event.context.msImageSmoothingEnabled = false;
  });
*/

  map.on("moveend", function(event) {
    pushURL();
  });
}

function handleLayerRowClicked(event, layerId) {
  mapLayer = layerId;
  if(map.getLayers().item(0) == wmtsLayer) {
  /* WMTS */
    // dirty hack to change WMTS layer, update source and refresh tiles
    map.getLayers().item(0).getSource().layer_ = layerId;
    map.getLayers().item(0).getSource().setUrls(map.getLayers().item(0).getSource().getUrls());
    map.getLayers().item(0).getSource().refresh();
  } else {
  /* WMS */
    map.getLayers().item(0).getSource().updateParams({'LAYERS': layerId});
  }
  pushURL();
}

function handleStyleRowClicked(event, styleId) {
  mapStyle = styleId;
  if(map.getLayers().item(0) == wmtsLayer) {
  /* WMTS */
    // dirty hack to change WMTS style, update source and refresh tiles
    map.getLayers().item(0).getSource().style_ = styleId;
    map.getLayers().item(0).getSource().setUrls(map.getLayers().item(0).getSource().getUrls());
    map.getLayers().item(0).getSource().refresh();
  } else {
  /* WMS */
    map.getLayers().item(0).getSource().updateParams({'STYLES': styleId});
  }
  pushURL();
}


function handleLayersTitleClick() {
  const layersBody = document.getElementById("layers-body");
  const caret = document.getElementById("layers-caret");

  layersBody.classList.toggle("hidden");
  caret.classList.toggle("caret-up");
  caret.classList.toggle("caret-down");
}


function handleStylesTitleClick() {
  const stylesBody = document.getElementById("styles-body");
  const caret = document.getElementById("styles-caret");

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
  const searchParams = new URLSearchParams(location.search);

  if (searchParams.has("x")) {
    const x = parseFloat(searchParams.get("x"));
    if (!Number.isNaN(x)) {
      mapX = x;
    }
  }

  if (searchParams.has("y")) {
    const y = parseFloat(searchParams.get("y"));
    if (!Number.isNaN(y)) {
      mapY = y;
    }
  }

  if (searchParams.has("zoom")) {
    const zoom = parseFloat(searchParams.get("zoom"));
    if (!Number.isNaN(zoom)) {
      mapZoom = zoom;
    }
  }

  if (searchParams.has("cx")) {
    const cx = parseFloat(searchParams.get("cx"));
    if (!Number.isNaN(cx)) {
      mapCX = cx;
    }
  }

  if (searchParams.has("cy")) {
    const cy = parseFloat(searchParams.get("cy"));
    if (!Number.isNaN(cy)) {
      mapCY = cy;
    }
  }

  if (searchParams.has("formula")) {
    const formula = searchParams.get("formula").toLowerCase();
    mapLayer = formula;
  }

  if (searchParams.has("style")) {
    const style = searchParams.get("style").toLowerCase();
    mapStyle = style;
  }

  if (map && map.getView()) {
    const view = map.getView();
    view.setCenter([mapX, mapY]);
    view.setZoom(mapZoom);
  }
}

/**
 * Generate the URL search params for the current view and push it to the window history
 */
function pushURL() {
  const baseUrl = location.protocol + "//" + location.host + location.pathname;

  const searchParams = new URLSearchParams();

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

  const url = baseUrl + "?" + searchParams.toString();

  window.history.pushState({}, window.title, url);
}

initialize();

