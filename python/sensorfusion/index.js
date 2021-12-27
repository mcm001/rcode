
var scene;
var camera;
var renderer;

var cube; var rocket;


function render() {
    requestAnimationFrame(render);
    renderer.render(scene, camera);
}

function CubeBegin() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    renderer = new THREE.WebGLRenderer();

    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);
    var geometry = new THREE.BoxGeometry(5, 5, 5);
    var cubeMaterials = [
        new THREE.MeshBasicMaterial({ color: 0xfe4365 }),
        new THREE.MeshBasicMaterial({ color: 0xfc9d9a }),
        new THREE.MeshBasicMaterial({ color: 0xf9cdad }),
        new THREE.MeshBasicMaterial({ color: 0xc8cba9 }),
        new THREE.MeshBasicMaterial({ color: 0x83af98 }),
        new THREE.MeshBasicMaterial({ color: 0xe5fcc2 })
    ];

    var material = new THREE.MeshFaceMaterial(cubeMaterials);
    // var material = cubeMaterials
    // cube = new THREE.Mesh(geometry, material);
    scene.add(cube);
    scene.add(new THREE.ArrowHelper(new THREE.Vector3(1, 0, 0).normalize(), new THREE.Vector3(0, 0, 0),
        10, // length
        0xff0000
    ))
    scene.add(new THREE.ArrowHelper(new THREE.Vector3(0, 1, 0).normalize(), new THREE.Vector3(0, 0, 0),
        10, // length
        0x00ff00
    ))
    scene.add(new THREE.ArrowHelper(new THREE.Vector3(0, 0, 1).normalize(), new THREE.Vector3(0, 0, 0),
        10, // length
        0x0000ff
    ))

    camera.position.x = 10;
    camera.position.y = 10;
    camera.position.z = 10;
    camera.up = new THREE.Vector3(0, 0, 1);
    camera.lookAt(new THREE.Vector3(0, 0, 0));

    var light = new THREE.PointLight(0xFFFFFF);
    light.position.set(10, 10, 10);
    scene.add(light);

    const loader = new THREE.STLLoader()
    const rocketMat = new THREE.MeshPhongMaterial({ color: 0xaa5533, specular: 0x111111, shininess: 200 });
    loader.load(
        'rocket2.stl',
        function (geometry) {
            rocket = new THREE.Mesh(geometry, rocketMat)
            const scale = 0.1
            rocket.scale.set(scale, scale, scale);
            scene.add(rocket)
        },
        (xhr) => {
            console.log((xhr.loaded / xhr.total) * 100 + '% loaded')
        },
        (error) => {
            console.log(error)
        }
    )

    render();
}
function WebSocketBegin() {
    CubeBegin();

    fetch('../../orient.json')
        .then(response => response.json())
        .then(jsonResponse => {

            i = 150
            if (true)
                setInterval(() => {
                    row = jsonResponse[i]
                    // console.log(row)

                    // we get wxyz, but need xyzw
                    rocket.quaternion.set(row[1], row[2], row[3], row[0])
                    rocket.quaternion = rocket.quaternion.multiply(new THREE.Quaternion(0,0,1,0).normalize())
                    rocket.quaternion.normalize()
                    i += 1
                }, 30);
        })

}