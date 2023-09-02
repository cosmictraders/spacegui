import * as THREE from "three";
import {MapControls} from 'three/addons/controls/MapControls.js';

function onTransitionEnd(event) {
    event.target.remove();
}

export function getScene() {
    let scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);
    return scene;
}

export function getRenderer() {
    let renderer = new THREE.WebGLRenderer({antialias: true, powerPreference: "high-performance"});
    renderer.domElement.id = 'canvas';
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, (window.innerHeight - 100));
    return renderer
}

export function getCamera() {
    let camera = new THREE.PerspectiveCamera(60, window.innerWidth / (window.innerHeight - 100), 1, 100000);
    camera.position.set(0, 500, -400);
    return camera
}

export function getLoadingManager() {
    return new THREE.LoadingManager(() => {

        const loadingScreen = document.getElementById('loading-screen');
        loadingScreen.classList.add('fade-out');

        // optional: remove loader from DOM via event listener
        loadingScreen.addEventListener('transitionend', onTransitionEnd);

    });
}

export function getMapControls(camera, renderer) {
    let mapControls = new MapControls(camera, renderer.domElement);
    mapControls.enableDamping = true; // an animation loop is required when either damping or autorotation are enabled
    mapControls.dampingFactor = 0.05;
    mapControls.screenSpacePanning = false;
    mapControls.minDistance = 50;
    mapControls.maxPolarAngle = Math.PI / 2;
    return mapControls;
}

export function initLights(s) {
    const ambientLight = new THREE.AmbientLight(0x000000);
    s.add(ambientLight);
}
