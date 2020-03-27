var height = 600;
var width = 400;
var canvas = ctx = false;
var frameRate = 1 / 2;
var frameDelay = frameRate * 1000;
var loopTimer = false;
var lastTime = false;

window.requestAnimFrame = (function () {
    return window.requestAnimationFrame ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame ||
        window.oRequestAnimationFrame ||
        window.msRequestAnimationFrame ||
        function (callback) {
            window.setTimeout(callback, 1000 / 2);
        };
})();

var pendulum = {mass: 100, length: 100, theta: Math.PI / 2 - 0.4, omega: 0, alpha: 0, J: 0};
var setup = function () {
    pendulum.J = pendulum.mass * pendulum.length * pendulum.length / 500;
    canvas = document.getElementById("canvas");
    ctx = canvas.getContext("2d");

    ctx.strokeStyle = "black";
    ctx.fillStyle = "gold";

    // loopTimer = setInterval(loop, frameDelay);
    lastTime = new Date();
    requestAnimFrame(loop);
}

let previousStates = [];

var loop = function () {
    var timeMs = (new Date()).getTime();
    var deltaT = (timeMs - lastTime.getTime()) / 1000;

    /* 
    When switching away from the window, 
    requestAnimationFrame is paused. Switching back
    will give us a giant deltaT and cause an explosion.
    We make sure that the biggest possible deltaT is 50 ms
    */

    if (deltaT > 0.050) {
        deltaT = 0.050;
    }
    deltaT = 0.01;

    time = new Date(timeMs);

    /* Velocity Verlet */
    /* Calculate current position from last frame's position, velocity, and acceleration */
    pendulum.theta += pendulum.omega * deltaT + (0.5 * pendulum.alpha * deltaT * deltaT);

    /* Calculate forces from current position. */
    var T = pendulum.mass * 9.81 * Math.cos(pendulum.theta) * pendulum.length;

    /* Current acceleration */
    var alpha = T / pendulum.J;

    /* Calculate current velocity from last frame's velocity and 
        average of last frame's acceleration with this frame's acceleration. */
    pendulum.omega += 0.5 * (alpha + pendulum.alpha) * deltaT;

    /* Update acceleration */
    pendulum.alpha = alpha;

    var px = width / 2 + pendulum.length * Math.cos(pendulum.theta);
    var py = 50 + pendulum.length * Math.sin(pendulum.theta);

    // console.log("hi");

    // Start drawing
    ctx.clearRect(0, 0, width, height);
    // Draw bar for Pendulum
    ctx.strokeStyle = 'black';
    ctx.beginPath();
    ctx.moveTo(width / 2, 50);
    ctx.lineTo(px, py);
    ctx.stroke();
    ctx.closePath();
    ctx.fillStyle = 'red';


    // Draw pendulum
    ctx.beginPath();
    ctx.arc(px, py, 15, 0, Math.PI * 2, false);
    ctx.fill();
    ctx.closePath();

    ctx.beginPath();
    ctx.rect(0, 200, 400, 400);
    ctx.stroke();
    ctx.moveTo(0, 400);
    ctx.lineTo(400, 400);
    ctx.stroke();
    ctx.moveTo(200, 200);
    ctx.lineTo(200, 600);
    ctx.stroke();
    ctx.closePath();

    const statesToSave = 80;
    previousStates.unshift({theta: pendulum.theta, omega: pendulum.omega});
    if (previousStates.length > statesToSave) {
        for (let i = statesToSave; i < previousStates.length; i++) {
            previousStates.pop()
        }
    }
    ctx.fillStyle = 'black';
    let prevState = previousStates[0];
    let prevRed = statesToSave;
    for (let i = 0; i < previousStates.length; i++) {
        const value = previousStates[i];
        ctx.beginPath();


        // ctx.moveTo(thetaToPos(prevState.theta), omegaToPos(prevState.omega));
        // ctx.lineTo(thetaToPos(value.theta), omegaToPos(value.omega));
        ctx.fillStyle = "rgb(" + prevRed * 3 + ", 0, 0)";
        ctx.arc(thetaToPos(value.theta), omegaToPos(value.omega), (statesToSave - i + statesToSave * 0.1) / 12, 0, 2 * Math.PI, false);

        prevState = value;

        prevRed--;
        ctx.fill();
        ctx.closePath();
    }


    lastTime = new Date();
    requestAnimFrame(loop);

}

function thetaToPos(theta) {
    return 200 - (theta - Math.PI / 2) * 100
}

function omegaToPos(omega) {
    return 400 + omega * 30
}

setup();


// ctx.beginPath();

// ctx.moveTo(width/2, 100);
// ctx.lineTo(
//     width/2 + 40*Math.cos(ang+0.06),
//     100 + 40*Math.sin(ang+0.06)
//     );
// ctx.lineTo(
//     width/2 + 50*Math.cos(ang-0.06),
//     100 + 50*Math.sin(ang-0.06)
//     );
// ctx.closePath();
// ctx.fill();

// // Draw minute hand
// var ang = time.getMinutes() + (time.getSeconds()/60);
// ang *= 6*Math.PI/180;
// ang -= Math.PI/2;
// ctx.fillStyle = '#999';
// ctx.beginPath();

// ctx.moveTo(width/2, 100);
// ctx.lineTo(
//     width/2 + 60*Math.cos(ang+0.03),
//     100 + 60*Math.sin(ang+0.03)
//     );
// ctx.lineTo(
//     width/2 + 70*Math.cos(ang-0.03),
//     100 + 70*Math.sin(ang-0.03)
//     );
// ctx.closePath();
// ctx.fill();
//
// // Draw second hand
// var ms = Math.round(time.getMilliseconds() / 250) / 4;
// var ang = time.getSeconds() + ms;
// ang *= 6*Math.PI/180;
// ang -= Math.PI/2;
// ctx.strokeStyle = '#CCC';
// ctx.beginPath();
// ctx.moveTo(width/2, 100);
// ctx.lineTo(
//     width/2 + 70*Math.cos(ang),
//     100 + 70*Math.sin(ang)
//     );
// ctx.stroke();
// ctx.closePath();