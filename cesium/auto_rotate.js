//https://groups.google.com/forum/#!topic/cesium-dev/XoUwDWE3YZU
var lastNow = Date.now();
viewer.clock.onTick.addEventListener(function(clock) {
                var now = Date.now();
                var spinRate = 0.08;
                var delta = (now - lastNow) / 1000;
                lastNow = now;
                viewer.scene.camera.rotate(Cesium.Cartesian3.UNIT_Z, -spinRate * delta);
});
