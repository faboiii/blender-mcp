# Blender MCP Examples

This directory contains example scripts that demonstrate how to use the Blender MCP to create and manipulate 3D objects in Blender.

## Available Examples

### rotating_cube.py

Creates a cube with a continuous rotation animation around the Z-axis.

**How to use with Blender MCP:**

1. Make sure Blender is running with the BlenderMCP addon enabled
2. Make sure the MCP server is connected to Blender
3. In Claude (or any MCP client), ask:
   ```
   "Execute the rotating cube example from examples/rotating_cube.py"
   ```

**Or execute the code directly:**

You can also copy the content of `rotating_cube.py` and ask Claude to execute it via the `execute_blender_code` tool.

**What it does:**

- Clears the current scene
- Creates a 2x2x2 cube at the origin
- Sets up a 120-frame animation (5 seconds at 24fps)
- Animates a full 360° rotation around the Z-axis
- Uses linear interpolation for smooth rotation
- Sets up cyclic modifiers so the animation loops

**Customization ideas:**

- Change the rotation axis by modifying the euler angles
- Add rotation on multiple axes simultaneously
- Adjust animation duration by changing `scene.frame_end`
- Add multiple cubes with different rotation speeds
- Combine rotation with position or scale animations

### rotating_cube_advanced.py

Creates multiple cubes with different rotation patterns, demonstrating advanced animation techniques.

**What it does:**

- Creates 5 cubes with different colors and rotation patterns:
  - **Red cube**: Rotates around X-axis
  - **Green cube**: Rotates around Y-axis
  - **Blue cube**: Rotates around Z-axis
  - **Yellow cube**: Tumbles on all three axes simultaneously
  - **Magenta cube**: Fast rotation on Z-axis (2x speed)
- Applies metallic materials with different colors
- Sets up a camera and lighting for the scene
- All animations loop seamlessly

**Use cases:**

- Learning about rotation on different axes
- Understanding multi-axis rotation (tumbling)
- Creating comparison scenes with multiple animated objects
- Learning about materials and scene setup

## Running Examples Manually in Blender

You can also run these scripts directly in Blender:

1. Open Blender
2. Switch to the "Scripting" workspace
3. Click "Open" and select the example script
4. Click "Run Script"

## Contributing

Feel free to add more examples! Each example should:

- Be well-documented with comments
- Include a docstring explaining what it does
- Print a success message when complete
- Be self-contained (not depend on external files)
