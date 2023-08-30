import * as THREE from 'three';
import {Stats} from './Stats.js';
import { GUI } from 'three/addons/libs/lil-gui.module.min.js';

import { FontLoader } from 'three/addons/loaders/FontLoader.js';
import { TextGeometry } from 'three/addons/geometries/TextGeometry.js';

import {MapControls} from 'three/addons/controls/MapControls.js';

const data = JSON.parse(jQuery.ajax({
    url: "/static/systems.json",
    async: false
}).responseText)

let camera, controls, scene, renderer;
const stats = new Stats()
stats.showPanel(0) // 0: fps, 1: ms, 2: mb, 3+: custom
document.body.appendChild(stats.dom)
init();
//render(); // remove when using next line for animation loop (requestAnimationFrame)
animate();

function initStats() {
}

function init() {
    initStats();
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);

    renderer = new THREE.WebGLRenderer({antialias: true, logarithmicDepthBuffer: true }) ;
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize( window.innerWidth, (window.innerHeight-100) );
    document.body.appendChild( renderer.domElement );

    camera = new THREE.PerspectiveCamera(60, window.innerWidth / (window.innerHeight-100), 1, 100000);
    camera.position.set(0, 200, -400);

    // controls

    controls = new MapControls(camera, renderer.domElement);

    //controls.addEventListener( 'change', render ); // call this only in static scenes (i.e., if there is no animation loop)

    controls.enableDamping = true; // an animation loop is required when either damping or auto-rotation are enabled
    controls.dampingFactor = 0.05;

    controls.screenSpacePanning = false;

    controls.minDistance = 50;

    controls.maxPolarAngle = Math.PI / 2;

    // world

    const geometry = new THREE.SphereGeometry();
    const material = new THREE.MeshPhongMaterial({color: 0x65F550, flatShading: true, emissive: 0x317527});
    const red_material = new THREE.MeshPhongMaterial({color: 0xF52900, flatShading: true, emissive: 0xB51E00});
    const orange_material = new THREE.MeshPhongMaterial({color: 0xF57500, flatShading: true, emissive: 0xDB6A00});
    const white_material = new THREE.MeshPhongMaterial({color: 0xffffff, flatShading: true, emissive: 0xffffff});
    const black_material = new THREE.MeshPhongMaterial({color: 0x000000, flatShading: true, emissive: 0xa1a1a1});
    const blue_material = new THREE.MeshPhongMaterial({color: 0x0074F0, flatShading: true, emissive: 0x005BBD});
    const dark_red_material = new THREE.MeshPhongMaterial({color: 0xDB2500, flatShading: true, emissive: 0x751400});

    const colorMap = {
        "RED_STAR": red_material,
        "ORANGE_STAR": orange_material,
        "WHITE_DWARF": white_material,
        "YOUNG_STAR": material,
        "BLACK_HOLE": black_material,
        "BLUE_STAR": blue_material,
        "HYPERGIANT": dark_red_material,
        "NEUTRON_STAR": white_material,
        "UNSTABLE": material
    }
    for (const system of Object.keys(data)) {
        const mesh = new THREE.Mesh(geometry, colorMap[data[system].type] || material);
        mesh.position.x = data[system].x;
        mesh.position.y = Math.random() * 200;
        mesh.position.z = data[system].y;
        mesh.scale.x = 10;
        mesh.scale.y = 10;
        mesh.scale.z = 10;
        mesh.updateMatrix();
        mesh.matrixAutoUpdate = false;
        scene.add(mesh);
    }
    var real_font;
    const loader = new FontLoader();
    loader.load('/static/font.typeface.json', function (font) {
        real_font = font;
    });
    // lights
    const dirLight1 = new THREE.DirectionalLight(0xffffff, 3);
    dirLight1.position.set(1, 1, 1);
    scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0x002288, 3);
    dirLight2.position.set(-1, -1, -1);
    scene.add(dirLight2);

    const ambientLight = new THREE.AmbientLight(0x000000);
    scene.add(ambientLight);

    // resize event

    window.addEventListener('resize', onWindowResize);


    const gui = new GUI();
    gui.domElement.id = 'gui-container';
    gui.add(controls, 'zoomToCursor').name('Zoom to cursor');
    gui.add(controls, 'screenSpacePanning').name('Screen space panning');
}

function onWindowResize() {

    camera.aspect = window.innerWidth / (window.innerHeight-100);
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, (window.innerHeight - 100));

}

function animate() {
    requestAnimationFrame(animate);
    stats.begin();
    controls.update(); // only required if controls.enableDamping = true, or if controls.autoRotate = true
    render();
    stats.end();
}

function render() {
    renderer.render( scene, camera );
}
