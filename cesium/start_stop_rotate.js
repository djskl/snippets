var lastNow = Date.now();
var rotate_over = false;
var rotate_angle = 0;

var _roate_func = function (clock) {
    var spinRate = 0.2; //0.08
    var now = Date.now();
    var delta = (now - lastNow) / 1000;
    lastNow = now;
    if (rotate_over) {
        spinRate = 1;
    }
    var rotate_delta = spinRate * delta;
    viewer.scene.camera.rotate(Cesium.Cartesian3.UNIT_Z, rotate_delta);
    if (rotate_over) {
        rotate_angle = rotate_angle - Math.abs(rotate_delta);
        if (rotate_angle < 0) {
            viewer.clock.onTick.removeEventListener(_roate_func);
            rotate_over = false;
        }
    }
};

var startRotate = function () {
    viewer.clock.onTick.addEventListener(_roate_func);
};

var stopRotate = function () {
    rotate_over = true;
    var ct = getCenter();

    if (ct.longitude > rotate_lng) {
        rotate_angle = ct.longitude - rotate_lng;
    } else {
        rotate_angle = 360 + ct.longitude - rotate_lng;
    }

    rotate_angle = Cesium.Math.toRadians(rotate_angle);
};

$(window).keyup(function (e) {
    if (e.keyCode == 27) {//此处代表按的是键盘的Esc键
        stopRotate();
    }
});
