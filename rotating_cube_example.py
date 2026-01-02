#!/usr/bin/env python3
"""
Rotating Cube Example for Blender MCP
Creates a 3D cube that rotates in space

Usage:
1. Start Blender and enable the BlenderMCP addon
2. Click "Connect to Claude" in the BlenderMCP panel (N key to show sidebar)
3. Run this script: python3 rotating_cube_example.py
"""

import socket
import json
import sys


def send_blender_command(command_type: str, params: dict = None) -> dict:
    """Send a command to the Blender addon"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(('localhost', 9876))

        command = {
            "type": command_type,
            "params": params or {}
        }

        sock.sendall(json.dumps(command).encode('utf-8'))
        sock.settimeout(15.0)

        # Receive response
        chunks = []
        while True:
            try:
                chunk = sock.recv(8192)
                if not chunk:
                    break
                chunks.append(chunk)
                # Try to parse as complete JSON
                try:
                    data = b''.join(chunks)
                    response = json.loads(data.decode('utf-8'))
                    return response
                except json.JSONDecodeError:
                    continue
            except socket.timeout:
                break

        data = b''.join(chunks)
        response = json.loads(data.decode('utf-8'))
        return response

    finally:
        sock.close()


def create_rotating_cube():
    """Create a rotating cube in Blender"""

    blender_code = """
import bpy
import math

# Clear existing mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Create a cube at the origin
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "RotatingCube"

# Set up animation timeline
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 250
scene.frame_current = 1

# Keyframe 1: Initial rotation (frame 1)
cube.rotation_euler = (0, 0, 0)
cube.keyframe_insert(data_path="rotation_euler", frame=1)

# Keyframe 2: Rotate around X and Z (frame 125)
cube.rotation_euler = (math.pi, 0, math.pi)
cube.keyframe_insert(data_path="rotation_euler", frame=125)

# Keyframe 3: Complete rotation (frame 250)
cube.rotation_euler = (2 * math.pi, 0, 2 * math.pi)
cube.keyframe_insert(data_path="rotation_euler", frame=250)

# Set linear interpolation for smooth continuous rotation
if cube.animation_data and cube.animation_data.action:
    for fcurve in cube.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'LINEAR'

# Position camera to view the cube
bpy.ops.object.select_all(action='DESELECT')
if scene.camera:
    scene.camera.location = (7, -7, 5)
    scene.camera.rotation_euler = (1.1, 0, 0.785)
else:
    bpy.ops.object.camera_add(location=(7, -7, 5))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.785)
    scene.camera = camera

# Add or update lighting
lights = [obj for obj in scene.objects if obj.type == 'LIGHT']
if lights:
    light = lights[0]
    light.location = (5, 5, 10)
    light.data.type = 'SUN'
    light.data.energy = 2
else:
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    light = bpy.context.active_object
    light.data.energy = 2

# Create a nice material for the cube
mat = bpy.data.materials.new(name="RotatingCubeMaterial")
mat.use_nodes = True
nodes = mat.node_tree.nodes
bsdf = nodes.get("Principled BSDF")

if bsdf:
    # Set material properties
    bsdf.inputs['Base Color'].default_value = (0.1, 0.5, 0.9, 1.0)  # Blue
    bsdf.inputs['Metallic'].default_value = 0.7
    bsdf.inputs['Roughness'].default_value = 0.3

# Assign material to cube
if cube.data.materials:
    cube.data.materials[0] = mat
else:
    cube.data.materials.append(mat)

# Set viewport shading to solid or material preview
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'SOLID'

# Return success message
result = {
    'cube_name': cube.name,
    'frame_range': f"{scene.frame_start}-{scene.frame_end}",
    'location': list(cube.location),
    'material': mat.name
}
result
"""

    print("Creating rotating cube in Blender...")
    try:
        response = send_blender_command("execute_code", {"code": blender_code})

        if response.get("status") == "success":
            print("✓ Rotating cube created successfully!")
            print(f"  Result: {response.get('result')}")
            print("\nThe cube will rotate continuously in Blender.")
            print("Press SPACEBAR in Blender to play the animation!")
        else:
            print(f"✗ Error: {response.get('message', 'Unknown error')}")
            return False

    except ConnectionRefusedError:
        print("✗ Error: Could not connect to Blender.")
        print("  Make sure:")
        print("  1. Blender is running")
        print("  2. BlenderMCP addon is installed and enabled")
        print("  3. You clicked 'Connect to Claude' in the BlenderMCP panel")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Rotating Cube Example - BlenderMCP")
    print("=" * 60)

    if create_rotating_cube():
        print("\n" + "=" * 60)
        print("Success! Your rotating cube is ready.")
        print("In Blender: Press SPACEBAR to play the animation!")
        print("=" * 60)
        sys.exit(0)
    else:
        sys.exit(1)
