import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const scene = new THREE.Scene();
const camera = new THREE.OrthographicCamera();
scene.add(camera);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);


const loader = new GLTFLoader();
loader.load('exports/result.glb', function (gltf) {
    scene.add(gltf.scene);
    renderer.render(scene, camera);
}, undefined, function (error) {
    console.error(error);
});
