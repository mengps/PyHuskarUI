import QtQuick

ShaderEffect {
    id: shaderEffect
    vertexShader: 'qrc:/Gallery/shaders/effect2.vert.qsb'
    fragmentShader: 'qrc:/Gallery/shaders/effect2.frag.qsb'

    property vector3d iResolution: Qt.vector3d(width, height, 0)
    property real iTime: 0

    FrameAnimation {
        running: true
        onTriggered: {
            shaderEffect.iTime += frameTime;
        }
    }
}
