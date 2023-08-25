#version 330 core
out vec4 fragColor;

// uniform vec3 uColor; // don't necessarily need a color here, gonna be white

void main()
{
    // fragColor = vec4(uColor, 1.0);
    fragColor = vec4(1.0, 1.0, 1.0, 1.0);
}