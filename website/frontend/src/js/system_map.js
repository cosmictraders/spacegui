import {getCamera, getMapControls, getRenderer, getScene, initLights} from './worldInit.js';
import {Stats} from './Stats.js';
import * as THREE from "three";
import {GUI} from "three/addons/libs/lil-gui.module.min";

let d = JSON.parse(jQuery.ajax({
    url: "/system-map-api/X1-QQ41",
    async: false
}).responseText);

let camera, controls, scene, renderer;
const stats = new Stats();
init().then(() => {
    document.body.appendChild(stats.dom);
    animate();
});

// Ray casting
const raycaster = new THREE.Raycaster();

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

function onPointerMove(event) {

    // calculate pointer position in normalized device coordinates
    // (-1 to +1) for both components

    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

}

function initGui() { // TODO: Create own gui with autocomplete etc.
    const gui = new GUI();
    gui.domElement.id = 'gui-container';
    gui.add(controls, 'zoomToCursor');
    gui.add(controls, 'screenSpacePanning');
    gui.add(controls, 'enableDamping');
}


async function init() {
    scene = getScene();
    renderer = getRenderer();
    document.body.appendChild(renderer.domElement);
    camera = getCamera();
    // controls
    controls = getMapControls(camera, renderer);
    // world
    let light = new THREE.PointLight(0xffffff, 2);
    light.position.set(0, 500, 0);
    light.updateMatrix();
    scene.add(light);
    let sphereGeometry = new THREE.SphereGeometry(1, 64, 64);
    let starMaterial = new THREE.MeshBasicMaterial({color: 0x65F550, emissive: 0x317527});
    let star = new THREE.Mesh(sphereGeometry, starMaterial);
    star.position.set(0, 0, 0);
    star.scale.set(100, 100, 100);
    star.updateMatrix();
    star.matrixAutoUpdate = false;
    scene.add(star);
    for (let waypoint of d["waypoints"]) {
        let waypoint = new THREE.Mesh(sphereGeometry, starMaterial);
        waypoint.position.set(waypoint.x * 10, 0, waypoint.y * 10);
        waypoint.scale.set(20, 20, 20);
        waypoint.updateMatrix();
        star.matrixAutoUpdate = false;
        scene.add(waypoint);
    }
    initGui();
    // events
    window.addEventListener('resize', onWindowResize);
}

function animate() { // TODO: Raycaster
    stats.begin();
    // update the picking ray with the camera and pointer position
    raycaster.setFromCamera(mouse, camera);

    // calculate objects intersecting the picking ray
    const intersects = raycaster.intersectObjects(scene.children);
    if (intersects.length > 0) {
        console.log(intersects[0].instanceId);
    }
    controls.update(); // only required if controls.enableDamping = true, or if controls.autoRotate = true
    render(renderer);
    stats.end();
    requestAnimationFrame(animate);
}

function render(renderer) {
    renderer.render(scene, camera);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / (window.innerHeight - 100);
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, (window.innerHeight - 100));
}