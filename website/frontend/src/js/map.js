// TODO: Port to webpack
import * as THREE from 'three';
import {getMapZ, getData} from './mapUtils.js';
import {getScene, getRenderer, getCamera, getLoadingManager, getMapControls, initLights} from './worldInit.js';
import {Stats} from './Stats.js';

import {FontLoader} from 'three/addons/loaders/FontLoader.js';
import {TextGeometry} from 'three/addons/geometries/TextGeometry.js';
import {GUI} from "three/addons/libs/lil-gui.module.min";


const mouse = new THREE.Vector2(1, 1);
let mouseDown = false;
window.onmousedown = (event) => {
    // Check if it's a left click
    if (event.button !== 0) {
        return;
    }
    mouseDown = true;
}
window.onmouseup = (event) => {
    if (event.button !== 0) {
        return;
    }
    mouseDown = false;
}

const guiInterface = {
    waypoint: '',
    maxLabelDistance: 1500
};

let peakValue = 900;
let spread = 4000;

const data = getData();

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
};
for (const system of Object.keys(data)) {
    meshInt[data[system].type]++;
    defaultInt--;
}

function setProgress(amount) {
    $("#progressBar").html(amount);
}

function initGui() { // TODO: Create own gui with autocomplete etc.
    const gui = new GUI();
    gui.domElement.id = 'gui-container';
    gui.add(controls, 'zoomToCursor').name('Zoom to cursor');
    gui.add(controls, 'screenSpacePanning').name('Screen space panning');
    gui.add(controls, 'enableDamping').name('Enable damping');
    gui.add(guiInterface, 'waypoint').name('Waypoint').onChange(function (value) {
        if (Object.keys(systemCoords).includes(value)) {  // TODO: Make case-insensitive
            const waypoint = systemCoords[value];
            controls.target.set(waypoint.x, waypoint.y, waypoint.z);
            camera.position.set(waypoint.x, waypoint.y, waypoint.z + 400);
            controls.autoRotate = true;
            controls.addEventListener('start', function () {
                controls.autoRotate = false;
            });
            controls.update();
        }
    });
    gui.add(guiInterface, 'maxLabelDistance', 500, 5000).name('Max label distance');
}



console.log(meshInt);
console.log("Defaulted on: " + defaultInt);
console.log("Total Systems: " + Object.keys(data).length);
const textMaterial = new THREE.MeshBasicMaterial({color: 0xffffff});
let labels = []

let camera, controls, scene, renderer;
const stats = new Stats();
init().then(() => {
    document.body.appendChild(stats.dom);
    animate();
});
stats.showPanel(0); // 0: fps, 1: ms, 2: mb, 3+: custom

function initMap(scene, data, textures) {
    const geometry = new THREE.SphereGeometry();
    const material = new THREE.MeshPhongMaterial({color: 0x65F550, emissive: 0x317527});
    const redStarMaterial = new THREE.MeshPhongMaterial({
        map: textures["red_star"],
        emissive: 0xffffff,
        emissiveIntensity: 0.5,
        emissiveMap: textures["red_star"]
    });
    const orangeStarMaterial = new THREE.MeshPhongMaterial({
        color: textures["orange_star"],
        emissive: 0xffffff,
        emissiveIntensity: 0.5,
        emissiveMap: textures["orange_star"]
    });
    const white_material = new THREE.MeshPhongMaterial({color: 0xffffff, emissive: 0xffffff});
    const black_material = new THREE.MeshPhongMaterial({color: 0x000000, emissive: 0x1b1b1b});
    const blueStarMaterial = new THREE.MeshPhongMaterial({
        map: textures["blue_star"],
        emissive: 0xffffff,
        emissiveIntensity: 0.5,
        emissiveMap: textures["blue_star"]
    });
    const hyperGiantMaterial = new THREE.MeshPhongMaterial({
        map: textures["hypergiant"],
        roughness: 1,
        emissive: 0xffffff,
        emissiveIntensity: 0.5,
        emissiveMap: textures["hypergiant"] // TODO: Possibly set intensity and color
    });
    const defaultMesh = new THREE.InstancedMesh(geometry, material, defaultInt);
    let redStarInstancedMesh = new THREE.InstancedMesh(geometry, redStarMaterial, meshInt["RED_STAR"]);
    let orangeStarInstancedMesh = new THREE.InstancedMesh(geometry, orangeStarMaterial, meshInt["ORANGE_STAR"]);
    let whiteStarInstancedMesh = new THREE.InstancedMesh(geometry, white_material, meshInt["WHITE_DWARF"]);
    let youngStarInstancedMesh = new THREE.InstancedMesh(geometry, material, meshInt["YOUNG_STAR"]);
    let blackHoleInstancedMesh = new THREE.InstancedMesh(geometry, black_material, meshInt["BLACK_HOLE"]);
    let blueStarInstancedMesh = new THREE.InstancedMesh(geometry, blueStarMaterial, meshInt["BLUE_STAR"]);
    let hyperGiantInstancedMesh = new THREE.InstancedMesh(geometry, hyperGiantMaterial, meshInt["HYPERGIANT"]);
    let neutronStarInstancedMesh = new THREE.InstancedMesh(geometry, white_material, meshInt["NEUTRON_STAR"]);
    let unstableStarInstancedMesh = new THREE.InstancedMesh(geometry, material, meshInt["UNSTABLE"]);
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
        let y = getMapZ(data[system].x, data[system].y, peakValue, spread);
        systemCoords[system] = {x: data[system].x, y: y, z: data[system].y};
        getMatrix(matrix, data[system], y);
        let systemType = data[system].type;
        let mesh;
        if (systemType === "RED_STAR") {
            mesh = redStarInstancedMesh;
        } else if (systemType === "ORANGE_STAR") {
            mesh = orangeStarInstancedMesh;
        } else if (systemType === "WHITE_DWARF") {
            mesh = whiteStarInstancedMesh;
        } else if (systemType === "YOUNG_STAR") {
            mesh = youngStarInstancedMesh;
        } else if (systemType === "BLACK_HOLE") {
            mesh = blackHoleInstancedMesh;
        } else if (systemType === "BLUE_STAR") {
            mesh = blueStarInstancedMesh;
        } else if (systemType === "HYPERGIANT") {
            mesh = hyperGiantInstancedMesh;
        } else if (systemType === "NEUTRON_STAR") {
            mesh = neutronStarInstancedMesh;
        } else if (systemType === "UNSTABLE") {
            mesh = unstableStarInstancedMesh;
        } else {
            mesh = defaultMesh;
        }
        if (!Object.keys(meshInt).includes(data[system].type)) {
            mesh.setMatrixAt(i, matrix);
            i++;
        } else {
            mesh.setMatrixAt(meshInt[data[system].type], matrix);
            meshInt[data[system].type]++;
        }
    }
    scene.add(defaultMesh);
    scene.add(redStarInstancedMesh);
    scene.add(orangeStarInstancedMesh);
    scene.add(whiteStarInstancedMesh);
    scene.add(youngStarInstancedMesh);
    scene.add(blackHoleInstancedMesh);
    scene.add(blueStarInstancedMesh);
    scene.add(hyperGiantInstancedMesh);
    scene.add(neutronStarInstancedMesh);
    scene.add(unstableStarInstancedMesh);
}




function initLabels(font) {
    setProgress(1);
    let count = 0;
    let total = Object.keys(systemCoords).length;
    for (const system of Object.keys(systemCoords)) {
        console.log(Math.round(count / total * 100));
        let textGeo = new TextGeometry(system, {
            font: font,
            size: 10,
            height: 1,
            curveSegments: 3,
        });
        textGeo.computeBoundingBox();
        textGeo.center();
        let textMesh = new THREE.Mesh(textGeo, textMaterial)
        textMesh.position.set(systemCoords[system].x, systemCoords[system].y + 20, systemCoords[system].z);
        textMesh.hidden = true;
        labels.push(textMesh);
        count++;
    }
    for (const mesh of labels) {
        scene.add(mesh);
    }
}

async function init() {
    scene = getScene();

    const loadingManager = getLoadingManager();
    const loader = new FontLoader(loadingManager);
    const textureLoader = new THREE.TextureLoader();
    let hyperGiantTexture = new Promise((resolve, reject) => {
        textureLoader.load('/static/images/hypergiant.jpg', data => resolve(data), null, reject);
    });
    let redStarTexture = new Promise((resolve, reject) => {
        textureLoader.load('/static/images/red_star.jpg', data => resolve(data), null, reject);
    });
    let blueStarTexture = new Promise((resolve, reject) => {
        textureLoader.load('/static/images/blue_star.jpg', data => resolve(data), null, reject);
    });
    let orangeStarTexture = new Promise((resolve, reject) => {
        textureLoader.load('/static/images/orange_star.jpg', data => resolve(data), null, reject);
    });
    let neutronStarTexture = new Promise((resolve, reject) => {
        textureLoader.load('/static/images/neutron_star.jpg', data => resolve(data), null, reject);
    });
    let font = new Promise((resolve, reject) => {
        loader.load('/static/font.typeface.json', data => resolve(data), null, reject);
    });
    initMap(scene, data, {
        "hypergiant": await hyperGiantTexture,
        "blue_star": await blueStarTexture,
        "red_star": await redStarTexture,
        "orange_star": await orangeStarTexture,
        "neutron_star": await neutronStarTexture
    });
    renderer = getRenderer();
    document.body.appendChild(renderer.domElement);

    camera = getCamera();

    // controls
    controls = getMapControls(camera, renderer);
    // world
    initLights(scene);
    // events
    window.addEventListener('resize', onWindowResize);
    document.addEventListener('mousemove', onMouseMove);
    initLabels(await font);
    // gui
    initGui();
}


function onMouseMove(event) {
    event.preventDefault();
    const rect = renderer.domElement.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    mouse.x = (x / canvas.clientWidth) * 2 - 1;
    mouse.y = (y / canvas.clientHeight) * -2 + 1
}

function onWindowResize() {
    camera.aspect = window.innerWidth / (window.innerHeight - 100);
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, (window.innerHeight - 100));
}

function updateLabels() {
    for (const label of labels) {
        let distance = camera.position.distanceTo(label.position);
        if (distance > guiInterface.maxLabelDistance && label.visible) {
            label.rotation.x = 0
            label.rotation.y = 0
            label.rotation.z = 0
            label.visible = false;
        } else if (distance < guiInterface.maxLabelDistance) {
            label.visible = true;
        }
        if (label.visible) {
            label.quaternion.rotateTowards(camera.quaternion, 0.2);
        }
    }
}

function animate() {
    stats.begin();
    updateLabels();
    controls.update(); // only required if controls.enableDamping = true, or if controls.autoRotate = true
    render(renderer);
    stats.end();
    requestAnimationFrame(animate);
}

function render(renderer) {
    renderer.render(scene, camera);
}
