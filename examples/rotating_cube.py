"""
Example: Creating a Rotating Cube in Blender

This script demonstrates how to create a cube with a continuous rotation animation
using the Blender Python API (bpy).

This code can be executed in Blender via the BlenderMCP's execute_blender_code tool.
"""

import bpy
import math

# Clear the scene (optional - removes default objects)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create a cube
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "RotatingCube"

# Set up the animation timeline
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 120  # 120 frames = 5 seconds at 24 fps

# Create an animation action for the cube
action = bpy.data.actions.new("CubeRotationAction")
cube.animation_data_create()
cube.animation_data.action = action

# Set initial rotation (frame 1)
cube.rotation_euler = (0, 0, 0)
cube.keyframe_insert(data_path="rotation_euler", frame=1)

# Set final rotation (frame 120) - full 360 degree rotation around Z-axis
cube.rotation_euler = (0, 0, math.pi * 2)  # 2π radians = 360 degrees
cube.keyframe_insert(data_path="rotation_euler", frame=120)

# Optional: Set interpolation to LINEAR for smooth, constant rotation
for fcurve in action.fcurves:
    for keyframe in fcurve.keyframe_points:
        keyframe.interpolation = 'LINEAR'

# Optional: Make the animation loop by setting cyclic modifiers
for fcurve in action.fcurves:
    modifier = fcurve.modifiers.new(type='CYCLES')

print("✓ Rotating cube created successfully!")
print(f"  - Object name: {cube.name}")
print(f"  - Animation: {scene.frame_start} to {scene.frame_end} frames")
print(f"  - Rotation: 360° around Z-axis")
print("  - Press spacebar in Blender to play the animation")
