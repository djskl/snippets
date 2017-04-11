var MOUSE_EVENT_LEFT_CLICK = 1;
var MOUSE_EVENT_LEFT_CLICK_HANDLERS = new Map();

cmap.getProvid = function (lng, lat) {
    if (this.provjson == null) {
        $.ajax({
            url: "{{STATIC_URL}}data/provs.geojson",
            dataType: "JSON",
            async: false,
            success: function (data) {
                cmap.provjson = data;
            },
            error: function () {
            }
        });
    }

    if(this.provjson == null){
        return null;
    }

    var pt = turf.point([lng, lat]);
    var features = cmap.provjson["features"];
    for (var idx in features) {
        var ft = features[idx];
        var mply = turf.multiPolygon(ft["geometry"]["coordinates"]);
        if (turf.inside(pt, mply)) {
            return ft["properties"]["provid"];//title
        }
    }
    return null;
};

cmap.addPositionEvent = function (cb, prov) {
    var _viwer = this.viewer;
    var _scene = _viwer.scene;
    var ellipsoid = _scene.globe.ellipsoid;
    var cartographic;
    var longitudeString;
    var latitudeString;
    var handler = new Cesium.ScreenSpaceEventHandler(_scene.canvas);
    handler.setInputAction(function (movement) {
        var cartesian = cmap.viewer.camera.pickEllipsoid(movement.endPosition, ellipsoid);
        if (cartesian) {
            cartographic = ellipsoid.cartesianToCartographic(cartesian);
            longitudeString = Cesium.Math.toDegrees(cartographic.longitude).toFixed(6);
            latitudeString = Cesium.Math.toDegrees(cartographic.latitude).toFixed(6);
        }
    }, Cesium.ScreenSpaceEventType.MOUSE_MOVE);

    MOUSE_EVENT_LEFT_CLICK_HANDLERS.set("getLngLat", function (e) {
        if (e.which == MOUSE_EVENT_LEFT_CLICK) {
            if (!!cb && cb instanceof Function) {
                var lng = parseFloat(longitudeString);
                var lat = parseFloat(latitudeString);
                if(!!prov){
                    var provid = cmap.getProvid(lng, lat);
                    cb(provid);
                }else{
                    cb(lng, lat)
                }
            }
        }
    });
};

cmap.delPositionEvent = function () {
    MOUSE_EVENT_LEFT_CLICK_HANDLERS.delete("getLngLat");
};
