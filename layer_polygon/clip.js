var _clip = function (geom) {
    if (!!geom == false) {
        return;
    }

    this.on('precompose', function (e) {
        if (!geom) return;
        var ctx = e.context;
        ctx.save();

        var ratio = e.frameState.pixelRatio;
        var m = e.frameState.coordinateToPixelTransform;

        function tr(pt) {
            return [
                (pt[0] * m[0] + pt[1] * m[1] + m[4]) * ratio,
                (pt[0] * m[2] + pt[1] * m[3] + m[5]) * ratio
            ];
        }

        //兼容老版本的ol3
        if (!m) {
            m = e.frameState.coordinateToPixelMatrix;
            tr = function (pt) {
                return [
                    (pt[0] * m[0] + pt[1] * m[1] + m[12]) * ratio,
                    (pt[0] * m[4] + pt[1] * m[5] + m[13]) * ratio
                ];
            }
        }

        // Geometry
        var ll = geom.getCoordinates();
        if (geom.getType() == "Polygon") ll = [ll];

        ctx.beginPath();
        for (var l = 0; l < ll.length; l++) {
            var c = ll[l];
            for (var i = 0; i < c.length; i++) {
                var pt = tr(c[i][0]);
                ctx.moveTo(pt[0], pt[1]);
                for (var j = 1; j < c[i].length; j++) {
                    pt = tr(c[i][j]);
                    ctx.lineTo(pt[0], pt[1]);
                }
            }
        }
        ctx.clip("evenodd");
    });

    this.on('postcompose', function (e) {
        e.context.restore();
    });

    if (this.renderSync) {
        this.renderSync();
    } else {
        this.changed();
    }

};

ol.layer.Base.prototype.clip = function (geom) {
    _clip.call(this, geom);
};

var BaseLayer = new ol.layer.Tile({
    source: new ol.source.XYZ({
        url: 'http://webst0{1-4}.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}'
    })
});

BaseLayer.clip(new ol.geom.Polygon([[[105, 24], [105, 34], [114, 34], [110, 30], [114, 24], [105, 24]]]));
