import {GUI} from 'three/addons/libs/lil-gui.module.min.js';

export function getMapZ(x, y, peakValue, spread) {
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

export function getData() {
    return JSON.parse(jQuery.ajax({
        url: "/static/systems.json",
        async: false
    }).responseText);
}

export function getSystemData(systemName) {
    return JSON.parse(jQuery.ajax({
        url: "/system/" + systemName + "/api-json",
        async: false
    }).responseText);
}

export function getShipData() {
    return JSON.parse(jQuery.ajax({
        url: "/ships/api-json",
        async: false
    }).responseText);
}