function init() {
    var geometry = new THREE.SphereBufferGeometry(0.5);
    var material = new THREE.MeshPhongMaterial({flatShading: true});
    var colorParsChunk = [
        'attribute vec3 instanceColor;',
        'varying vec3 vInstanceColor;',
        '#include <common>'
    ].join('\n');

    var instanceColorChunk = [
        '#include <begin_vertex>',
        '\tvInstanceColor = instanceColor;'
    ].join('\n');

    var fragmentParsChunk = [
        'varying vec3 vInstanceColor;',
        '#include <common>'
    ].join('\n');

    var colorChunk = [
        'vec4 diffuseColor = vec4( diffuse * vInstanceColor, opacity );'
    ].join('\n');

    material.onBeforeCompile = function (shader) {

        shader.vertexShader = shader.vertexShader
            .replace('#include <common>', colorParsChunk)
            .replace('#include <begin_vertex>', instanceColorChunk);

        shader.fragmentShader = shader.fragmentShader
            .replace('#include <common>', fragmentParsChunk)
            .replace('vec4 diffuseColor = vec4( diffuse, opacity );', colorChunk);

    };

    mesh = new THREE.InstancedMesh(geometry, material, count);

    var i = 0;
    var offset = (amount - 1) / 2;

    var transform = new THREE.Object3D();

    var instanceColors = [];

    for (var x = 0; x < amount; x++) {
        for (var y = 0; y < amount; y++) {
            for (var z = 0; z < amount; z++) {
                transform.position.set(offset - x, offset - y, offset - z).multiplyScalar(1.5);
                transform.updateMatrix();

                mesh.setMatrixAt(i++, transform.matrix);

                instanceColors.push(Math.random());
                instanceColors.push(Math.random());
                instanceColors.push(Math.random());
            }
        }
    }
    var instanceColorsBase = new Float32Array(instanceColors.length);
    instanceColorsBase.set(instanceColors);
    geometry.setAttribute('instanceColor', new THREE.InstancedBufferAttribute(new Float32Array(instanceColors), 3));
    geometry.setAttribute('instanceColorBase', new THREE.BufferAttribute(new Float32Array(instanceColorsBase), 3));

}

function animate() {
    requestAnimationFrame(animate);

    render();
}

function setInstanceColor(instanceId, isHighlighting) {
    if (instanceId == -1) return;
    mesh.geometry.attributes.instanceColor.setXYZ(
        instanceId,
        isHighlighting ? highlightColor.r : mesh.geometry.attributes.instanceColorBase.getX(instanceId),
        isHighlighting ? highlightColor.g : mesh.geometry.attributes.instanceColorBase.getY(instanceId),
        isHighlighting ? highlightColor.b : mesh.geometry.attributes.instanceColorBase.getZ(instanceId)
    );
    mesh.geometry.attributes.instanceColor.needsUpdate = true;
}

function render() {
    raycaster.setFromCamera(mouse, camera);

    var intersection = raycaster.intersectObject(mesh);

    if (intersection.length > 0) {
        var instanceId = intersection[0].instanceId;
        if (instanceId != prevInstanceId) {
            setInstanceColor(instanceId, true);
            setInstanceColor(prevInstanceId, false);
            prevInstanceId = instanceId;
        }

        mesh.getMatrixAt(instanceId, instanceMatrix);
        matrix.multiplyMatrices(instanceMatrix, rotationMatrix);

        mesh.setMatrixAt(instanceId, matrix);
        mesh.instanceMatrix.needsUpdate = true;
    } else {
        setInstanceColor(prevInstanceId, false);
        prevInstanceId = -1;
    }

    renderer.render(scene, camera);

    stats.update();
}
