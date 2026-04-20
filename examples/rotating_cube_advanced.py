"""
Example: Advanced Rotating Cubes

This script demonstrates more advanced rotation techniques:
- Multiple cubes with different rotation axes
- Multi-axis rotation (tumbling effect)
- Different rotation speeds
- Color-coded materials

This code can be executed in Blender via the BlenderMCP's execute_blender_code tool.
"""

import bpy
import math

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Remove default materials
for material in bpy.data.materials:
    bpy.data.materials.remove(material)

# Set up the animation timeline
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 120

def create_rotating_cube(name, location, color, rotation_axis='Z', speed=1.0):
    """
    Create a cube with rotation animation

    Args:
        name: Name of the cube
        location: (x, y, z) tuple for cube position
        color: (r, g, b, a) tuple for cube color
        rotation_axis: 'X', 'Y', 'Z', or 'ALL' for tumbling
        speed: Rotation speed multiplier (1.0 = full rotation in 120 frames)
    """
    # Create cube
    bpy.ops.mesh.primitive_cube_add(size=1.5, location=location)
    cube = bpy.context.active_object
    cube.name = name

    # Create and assign material
    material = bpy.data.materials.new(name=f"{name}_Material")
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Metallic'].default_value = 0.8
        bsdf.inputs['Roughness'].default_value = 0.2

    cube.data.materials.append(material)

    # Create animation
    action = bpy.data.actions.new(f"{name}_RotationAction")
    cube.animation_data_create()
    cube.animation_data.action = action

    # Set keyframes based on rotation axis
    cube.rotation_euler = (0, 0, 0)
    cube.keyframe_insert(data_path="rotation_euler", frame=1)

    if rotation_axis == 'X':
        cube.rotation_euler = (math.pi * 2 * speed, 0, 0)
    elif rotation_axis == 'Y':
        cube.rotation_euler = (0, math.pi * 2 * speed, 0)
    elif rotation_axis == 'Z':
        cube.rotation_euler = (0, 0, math.pi * 2 * speed)
    elif rotation_axis == 'ALL':
        # Tumbling rotation on all axes
        cube.rotation_euler = (
            math.pi * 2 * speed,
            math.pi * 2 * speed * 0.7,
            math.pi * 2 * speed * 0.5
        )

    cube.keyframe_insert(data_path="rotation_euler", frame=120)

    # Set linear interpolation
    for fcurve in action.fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'LINEAR'
        # Add cyclic modifier for looping
        modifier = fcurve.modifiers.new(type='CYCLES')

    return cube

# Create multiple cubes with different rotation patterns
cubes = []

# Red cube - rotates around X axis
cubes.append(create_rotating_cube(
    "RedCube_X",
    location=(-4, 0, 0),
    color=(1.0, 0.1, 0.1, 1.0),  # Red
    rotation_axis='X',
    speed=1.0
))

# Green cube - rotates around Y axis
cubes.append(create_rotating_cube(
    "GreenCube_Y",
    location=(0, 0, 0),
    color=(0.1, 1.0, 0.1, 1.0),  # Green
    rotation_axis='Y',
    speed=1.0
))

# Blue cube - rotates around Z axis
cubes.append(create_rotating_cube(
    "BlueCube_Z",
    location=(4, 0, 0),
    color=(0.1, 0.1, 1.0, 1.0),  # Blue
    rotation_axis='Z',
    speed=1.0
))

# Yellow cube - tumbles on all axes
cubes.append(create_rotating_cube(
    "YellowCube_Tumble",
    location=(0, 3, 0),
    color=(1.0, 1.0, 0.1, 1.0),  # Yellow
    rotation_axis='ALL',
    speed=1.0
))

# Magenta cube - fast rotation on Z axis
cubes.append(create_rotating_cube(
    "MagentaCube_Fast",
    location=(0, -3, 0),
    color=(1.0, 0.1, 1.0, 1.0),  # Magenta
    rotation_axis='Z',
    speed=2.0  # Twice as fast
))

# Add a camera
bpy.ops.object.camera_add(location=(0, -15, 5))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(70), 0, 0)
scene.camera = camera

# Add lighting
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
sun = bpy.context.active_object
sun.data.energy = 2.0

print("✓ Advanced rotating cubes created successfully!")
print(f"  - Created {len(cubes)} cubes with different rotation patterns")
print("  - Red: X-axis rotation")
print("  - Green: Y-axis rotation")
print("  - Blue: Z-axis rotation")
print("  - Yellow: Tumbling (all axes)")
print("  - Magenta: Fast Z-axis rotation (2x speed)")
print("  - Press spacebar in Blender to play the animation")
