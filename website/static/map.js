import * as THREE from 'three';
import {Stats} from './Stats.js';
import {GUI} from 'three/addons/libs/lil-gui.module.min.js';

import {FontLoader} from 'three/addons/loaders/FontLoader.js';
import {TextGeometry} from 'three/addons/geometries/TextGeometry.js';

import {MapControls} from 'three/addons/controls/MapControls.js';

let peakValue = 900;
let spread = 4000;
const guiInterface = {
    waypoint: '',
    maxLabelDistance: 1500
};
const data = JSON.parse(jQuery.ajax({
    url: "/static/systems.json",
    async: false
}).responseText)

const systemCoords = {};

let defaultInt = Object.keys(data).length;
let meshInt = {
    "RED_STAR": 0,
    "ORANGE_STAR": 0,
    "WHITE_DWARF": 0,
    "YOUNG_STAR": 0,
    "BLACK_HOLE": 0,
    "BLUE_STAR": 0,
    "HYPERGIANT": 0,
    "NEUTRON_STAR": 0,
    "UNSTABLE": 0
}
for (const system of Object.keys(data)) {
    meshInt[data[system].type]++;
    defaultInt--;
}
console.log(meshInt);
console.log("Defaulted on: " + defaultInt);
console.log("Total Systems: " + Object.keys(data).length)
const textMaterial = new THREE.MeshBasicMaterial({color: 0xffffff});
const geometry = new THREE.SphereGeometry();
const material = new THREE.MeshPhongMaterial({color: 0x65F550, flatShading: true, emissive: 0x317527});
const red_material = new THREE.MeshPhongMaterial({color: 0xF52900, flatShading: true, emissive: 0xB51E00});
const orange_material = new THREE.MeshPhongMaterial({color: 0xF57500, flatShading: true, emissive: 0xDB6A00});
const white_material = new THREE.MeshPhongMaterial({color: 0xffffff, flatShading: true, emissive: 0xffffff});
const black_material = new THREE.MeshPhongMaterial({color: 0x000000, flatShading: true, emissive: 0x1b1b1b});
const blue_material = new THREE.MeshPhongMaterial({color: 0x0074F0, flatShading: true, emissive: 0x005BBD});
const dark_red_material = new THREE.MeshPhongMaterial({color: 0xDB2500, flatShading: true, emissive: 0x751400});
const defaultMesh = new THREE.InstancedMesh(geometry, material, defaultInt);
const colorMap = {
    "RED_STAR": new THREE.InstancedMesh(geometry, red_material, meshInt["RED_STAR"]),
    "ORANGE_STAR": new THREE.InstancedMesh(geometry, orange_material, meshInt["ORANGE_STAR"]),
    "WHITE_DWARF": new THREE.InstancedMesh(geometry, white_material, meshInt["WHITE_DWARF"]),
    "YOUNG_STAR": new THREE.InstancedMesh(geometry, material, meshInt["YOUNG_STAR"]),
    "BLACK_HOLE": new THREE.InstancedMesh(geometry, black_material, meshInt["BLACK_HOLE"]),
    "BLUE_STAR": new THREE.InstancedMesh(geometry, blue_material, meshInt["BLUE_STAR"]),
    "HYPERGIANT": new THREE.InstancedMesh(geometry, dark_red_material, meshInt["HYPERGIANT"]),
    "NEUTRON_STAR": new THREE.InstancedMesh(geometry, white_material, meshInt["NEUTRON_STAR"]),
    "UNSTABLE": new THREE.InstancedMesh(geometry, material, meshInt["UNSTABLE"])
}
let labels = []

let camera, controls, scene, renderer;
const stats = new Stats()
stats.showPanel(0) // 0: fps, 1: ms, 2: mb, 3+: custom
document.body.appendChild(stats.dom)

init();
animate();

function getZ(x, y, peakValue, spread) {
    // Calculate distance from origin
    const d = Math.sqrt(x * x + y * y);

    // Compute Z based on Gaussian function
    let Z = peakValue * Math.exp(-(d * d) / (2 * spread * spread));

    // Add randomness to Z
    Z = Z * Math.random();
    if (Math.random() > 0.5) {
        return Z;
    } else {
        return -Z;
    }
}

function initMap(font) {
    meshInt = {
        "RED_STAR": 0,
        "ORANGE_STAR": 0,
        "WHITE_DWARF": 0,
        "YOUNG_STAR": 0,
        "BLACK_HOLE": 0,
        "BLUE_STAR": 0,
        "HYPERGIANT": 0,
        "NEUTRON_STAR": 0,
        "UNSTABLE": 0
    }
    const position = new THREE.Vector3();
    const rotation = new THREE.Euler();
    const quaternion = new THREE.Quaternion();
    const scale = new THREE.Vector3();

    const getMatrix = function (matrix, system, y) {

        position.x = system.x;
        position.y = y;
        position.z = system.y;

        rotation.x = 0;
        rotation.y = 0;
        rotation.z = 0;

        quaternion.setFromEuler(rotation);

        scale.x = scale.y = scale.z = 15;

        matrix.compose(position, quaternion, scale);
    }
    const matrix = new THREE.Matrix4();
    let i = 0;
    for (const system of Object.keys(data)) {
        let y = getZ(data[system].x, data[system].y, peakValue, spread);
        systemCoords[system] = {x: data[system].x, y: y, z: data[system].y};
        getMatrix(matrix, data[system], y);
        const mesh = colorMap[data[system].type] || defaultMesh;
        if (!Object.keys(meshInt).includes(data[system].type)) {
            mesh.setMatrixAt(i, matrix);
            i++;
        } else {
            mesh.setMatrixAt(meshInt[data[system].type], matrix);
            meshInt[data[system].type]++;
        }
        let textGeo = new TextGeometry(system, {
            font: font,
            size: 10,
            height: 1,
            curveSegments: 3,
        });
        var center = new THREE.Vector3();
        textGeo.computeBoundingBox();
        textGeo.boundingBox.getCenter(center);
        textGeo.center();
        position.copy(center);
        let textMesh = new THREE.Mesh(textGeo, textMaterial)
        textMesh.position.set(data[system].x, y + 20, data[system].y);
        labels.push(textMesh);
    }
    for (const mesh of labels) {
        scene.add(mesh);
    }
    scene.add(defaultMesh);
    scene.add(colorMap["RED_STAR"]);
    scene.add(colorMap["ORANGE_STAR"]);
    scene.add(colorMap["WHITE_DWARF"]);
    scene.add(colorMap["YOUNG_STAR"]);
    scene.add(colorMap["BLACK_HOLE"]);
    scene.add(colorMap["BLUE_STAR"]);
    scene.add(colorMap["HYPERGIANT"]);
    scene.add(colorMap["NEUTRON_STAR"]);
    scene.add(colorMap["UNSTABLE"]);
}

function initLights() {
    // lights
    const dirLight1 = new THREE.DirectionalLight(0xffffff, 3);
    dirLight1.position.set(1, 1, 1);
    scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0x002288, 3);
    dirLight2.position.set(-1, -1, -1);
    scene.add(dirLight2);

    const ambientLight = new THREE.AmbientLight(0x000000);
    scene.add(ambientLight);
}

function init() {
    scene = new THREE.Scene();
    // font
    const loader = new FontLoader();
    scene.background = new THREE.Color(0x000000);

    renderer = new THREE.WebGLRenderer({antialias: true});
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, (window.innerHeight - 100));
    document.body.appendChild(renderer.domElement);

    camera = new THREE.PerspectiveCamera(60, window.innerWidth / (window.innerHeight - 100), 1, 100000);
    camera.position.set(0, 500, -400);

    // controls
    controls = new MapControls(camera, renderer.domElement);
    controls.enableDamping = true; // an animation loop is required when either damping or autorotation are enabled
    controls.dampingFactor = 0.05;

    controls.screenSpacePanning = false;

    controls.minDistance = 50;

    controls.maxPolarAngle = Math.PI / 2;
    loader.load('/static/font.typeface.json', function (font) {
        initMap(font)
    });
    // world
    initLights()
    // resize event
    window.addEventListener('resize', onWindowResize);

    // gui
    const gui = new GUI();
    gui.domElement.id = 'gui-container';
    gui.add(controls, 'zoomToCursor').name('Zoom to cursor');
    gui.add(controls, 'screenSpacePanning').name('Screen space panning');
    gui.add(controls, 'enableDamping').name('Enable damping');
    gui.add(guiInterface, 'waypoint').name('Waypoint').onChange(function (value) {
        if (Object.keys(systemCoords).includes(value)) {
            const waypoint = systemCoords[value];
            controls.target.set(waypoint.x, waypoint.y, waypoint.z);
            camera.position.set(waypoint.x, waypoint.y, waypoint.z + 400);
            controls.autoRotate = true;
            controls.addEventListener('start', function(){
                controls.autoRotate = false;
            });
            controls.update();
        }
    });
    gui.add(guiInterface, 'maxLabelDistance', 500, 5000).name('Max label distance');
}

function onWindowResize() {
    camera.aspect = window.innerWidth / (window.innerHeight - 100);
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, (window.innerHeight - 100));
}

function animate() {
    stats.begin();
    for (const label of labels) {
        let distance = camera.position.distanceTo(label.position);
        label.visible = distance < guiInterface.maxLabelDistance;
        if (label.visible) {
            label.quaternion.rotateTowards(camera.quaternion, 0.25);
        }
    }
    controls.update(); // only required if controls.enableDamping = true, or if controls.autoRotate = true
    render();
    stats.end();
    requestAnimationFrame(animate);
}

function render() {
    renderer.render(scene, camera);
}
