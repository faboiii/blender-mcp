# BlenderMCP Usage Examples

This guide provides practical examples for using BlenderMCP to create 3D scenes with Claude AI.

## Table of Contents

- [Basic Operations](#basic-operations)
- [Scene Creation](#scene-creation)
- [Asset Management](#asset-management)
- [Materials and Textures](#materials-and-textures)
- [Lighting](#lighting)
- [Camera Control](#camera-control)
- [Advanced Workflows](#advanced-workflows)
- [Troubleshooting Common Issues](#troubleshooting-common-issues)

## Basic Operations

### Getting Scene Information

**Prompt:**
```
What's currently in my Blender scene?
```

**What Claude will do:**
- Use `get_scene_info()` to retrieve all objects, materials, and lights
- Provide a summary of the current scene state

### Inspecting a Specific Object

**Prompt:**
```
Tell me about the "Cube" object in my scene
```

**What Claude will do:**
- Use `get_object_info(object_name="Cube")`
- Return position, rotation, scale, materials, and other properties

### Creating Basic Shapes

**Prompt:**
```
Create a red sphere at position (2, 3, 1) with a radius of 1.5
```

**What Claude will do:**
- Use `execute_blender_code()` to create a UV sphere
- Set location, scale, and material properties
- Apply a red material

## Scene Creation

### Low Poly Fantasy Scene

**Prompt:**
```
Create a low poly dungeon scene with a dragon guarding a pot of gold
```

**What Claude will do:**
1. Check available integrations (PolyHaven, Sketchfab, Hyper3D)
2. Search for suitable assets or generate them
3. Position objects appropriately
4. Set up basic lighting
5. Apply materials and colors

**Expected result:**
- Dragon model (from Sketchfab or Hyper3D)
- Gold pot with metallic material
- Stone floor and walls
- Atmospheric lighting

### Beach Environment

**Prompt:**
```
Create a beach scene with sand, rocks, vegetation, and ocean using PolyHaven assets
```

**What Claude will do:**
1. Enable PolyHaven if available
2. Search for beach-related assets:
   - Beach HDRI for lighting
   - Sand texture
   - Rock models
   - Vegetation models
3. Download and import assets
4. Arrange objects naturally
5. Apply textures to ground plane

**Example workflow:**
```
→ get_polyhaven_status()
→ search_polyhaven_assets(asset_type="hdris", categories="outdoor,skies")
→ download_polyhaven_asset(asset_id="beach_hdri", asset_type="hdris", resolution="2k")
→ search_polyhaven_assets(asset_type="models", categories="nature,rocks")
→ download_polyhaven_asset(asset_id="rock_01", asset_type="models")
```

### Architectural Visualization

**Prompt:**
```
Create a modern living room with furniture from Sketchfab
```

**What Claude will do:**
1. Check Sketchfab integration
2. Search for furniture models:
   - Sofa
   - Coffee table
   - Lamp
   - Rug
3. Download and position models
4. Set up studio lighting
5. Adjust camera for best view

## Asset Management

### Using PolyHaven Assets

**For HDRIs (Environment Lighting):**
```
Add a sunset HDRI from PolyHaven to light my scene
```

**What happens:**
```python
search_polyhaven_assets(asset_type="hdris", categories="sunset,outdoor")
download_polyhaven_asset(asset_id="sunset_sky_01", asset_type="hdris", resolution="2k")
```

**For Models:**
```
Add some realistic rocks from PolyHaven
```

**What happens:**
```python
search_polyhaven_assets(asset_type="models", categories="rocks,nature")
download_polyhaven_asset(asset_id="rock_boulder_01", asset_type="models")
```

### Using Sketchfab Models

**Searching for specific models:**
```
Find a realistic car model on Sketchfab
```

**What happens:**
```python
search_sketchfab_models(query="realistic car", count=10, downloadable=True)
# Returns list of models with UIDs
```

**Downloading a model:**
```
Download the model with UID "abc123xyz" from Sketchfab
```

**What happens:**
```python
download_sketchfab_model(uid="abc123xyz")
# Downloads and imports the model
```

### Generating Custom Models with Hyper3D

**Text-based generation:**
```
Generate a 3D model of a garden gnome using Hyper3D
```

**What happens:**
```python
# Step 1: Create generation task
generate_hyper3d_model_via_text(text_prompt="garden gnome statue")
# Returns: {"task_uuid": "...", "subscription_key": "..."}

# Step 2: Poll for completion
poll_rodin_job_status(subscription_key="...")
# Waits until status is "Done"

# Step 3: Import the generated model
import_generated_asset(name="GardenGnome", task_uuid="...")
```

**Image-based generation:**
```
Generate a 3D model based on this image: /path/to/reference.jpg
```

**What happens:**
```python
generate_hyper3d_model_via_images(input_image_paths=["/path/to/reference.jpg"])
poll_rodin_job_status(subscription_key="...")
import_generated_asset(name="CustomModel", task_uuid="...")
```

## Materials and Textures

### Applying PolyHaven Textures

**Prompt:**
```
Apply a wood texture from PolyHaven to the cube
```

**What Claude will do:**
1. Search for wood textures in PolyHaven
2. Download the texture with all maps (diffuse, normal, roughness)
3. Apply to the specified object

**Example:**
```python
search_polyhaven_assets(asset_type="textures", categories="wood")
download_polyhaven_asset(asset_id="wood_planks_02", asset_type="textures", resolution="1k")
set_texture(object_name="Cube", texture_id="wood_planks_02")
```

### Creating Custom Materials

**Prompt:**
```
Make the sphere metallic gold with high reflectivity
```

**What Claude will do:**
```python
execute_blender_code("""
import bpy

# Get the sphere object
sphere = bpy.data.objects.get('Sphere')

# Create a new material
mat = bpy.data.materials.new(name="MetallicGold")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear default nodes
nodes.clear()

# Add Principled BSDF
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)

# Set gold color and metallic properties
bsdf.inputs['Base Color'].default_value = (1.0, 0.766, 0.336, 1.0)  # Gold color
bsdf.inputs['Metallic'].default_value = 1.0
bsdf.inputs['Roughness'].default_value = 0.2

# Add Material Output
output = nodes.new(type='ShaderNodeOutputMaterial')
output.location = (200, 0)

# Link nodes
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Assign material to sphere
if sphere.data.materials:
    sphere.data.materials[0] = mat
else:
    sphere.data.materials.append(mat)
""")
```

## Lighting

### Studio Lighting Setup

**Prompt:**
```
Set up three-point studio lighting for product photography
```

**What Claude will do:**
```python
execute_blender_code("""
import bpy
import math

# Clear existing lights
for obj in bpy.data.objects:
    if obj.type == 'LIGHT':
        bpy.data.objects.remove(obj, do_unlink=True)

# Key light (main light)
bpy.ops.object.light_add(type='AREA', location=(5, -5, 5))
key_light = bpy.context.object
key_light.data.energy = 300
key_light.rotation_euler = (math.radians(45), 0, math.radians(45))

# Fill light (softer, opposite side)
bpy.ops.object.light_add(type='AREA', location=(-3, -3, 3))
fill_light = bpy.context.object
fill_light.data.energy = 100
fill_light.rotation_euler = (math.radians(60), 0, math.radians(-30))

# Back light (rim light)
bpy.ops.object.light_add(type='AREA', location=(0, 5, 4))
back_light = bpy.context.object
back_light.data.energy = 150
back_light.rotation_euler = (math.radians(-45), 0, 0)
""")
```

### Environment Lighting with HDRI

**Prompt:**
```
Use a studio HDRI from PolyHaven for realistic lighting
```

**What Claude will do:**
```python
search_polyhaven_assets(asset_type="hdris", categories="indoor,studio")
download_polyhaven_asset(asset_id="studio_small_03", asset_type="hdris", resolution="2k")
# HDRI is automatically applied to world environment
```

## Camera Control

### Positioning Camera

**Prompt:**
```
Point the camera at the scene center and make it isometric
```

**What Claude will do:**
```python
execute_blender_code("""
import bpy
import math

# Get or create camera
camera = bpy.data.objects.get('Camera')
if not camera:
    bpy.ops.object.camera_add()
    camera = bpy.context.object

# Set camera to isometric (orthographic)
camera.data.type = 'ORTHO'
camera.data.ortho_scale = 10.0

# Position camera for isometric view (45° angles)
camera.location = (10, -10, 10)
camera.rotation_euler = (math.radians(55), 0, math.radians(45))

# Set as active camera
bpy.context.scene.camera = camera
""")
```

### Camera Animation

**Prompt:**
```
Create a 360-degree orbit animation around the object
```

**What Claude will do:**
```python
execute_blender_code("""
import bpy
import math

scene = bpy.context.scene
camera = scene.camera
target = bpy.data.objects.get('Cube')  # Object to orbit

if camera and target:
    # Set animation length
    scene.frame_start = 1
    scene.frame_end = 120

    # Create keyframes for rotation
    radius = 10
    height = 5

    for frame in range(1, 121):
        scene.frame_set(frame)
        angle = (frame / 120.0) * 2 * math.pi

        camera.location.x = target.location.x + radius * math.cos(angle)
        camera.location.y = target.location.y + radius * math.sin(angle)
        camera.location.z = target.location.z + height

        # Point camera at target
        direction = target.location - camera.location
        rot_quat = direction.to_track_quat('-Z', 'Y')
        camera.rotation_euler = rot_quat.to_euler()

        camera.keyframe_insert(data_path="location")
        camera.keyframe_insert(data_path="rotation_euler")
""")
```

## Advanced Workflows

### Taking Screenshots

**Prompt:**
```
Show me what the current viewport looks like
```

**What Claude will do:**
```python
get_viewport_screenshot(max_size=800)
# Returns PNG image of current viewport
```

**Use cases:**
- Reviewing progress
- Debugging positioning issues
- Getting Claude's feedback on composition

### Exporting to Other Formats

**Prompt:**
```
Get the scene information and create a Three.js sketch from it
```

**What Claude will do:**
1. Use `get_scene_info()` to get all objects and their properties
2. Parse object data (positions, rotations, materials)
3. Generate Three.js code that recreates the scene
4. Provide code ready to use in a web page

### Batch Operations

**Prompt:**
```
Create a grid of 5x5 cubes with random colors
```

**What Claude will do:**
```python
execute_blender_code("""
import bpy
import random

# Clear existing cubes
for obj in bpy.data.objects:
    if obj.name.startswith('GridCube'):
        bpy.data.objects.remove(obj, do_unlink=True)

# Create grid
spacing = 2.5
for x in range(5):
    for y in range(5):
        # Create cube
        bpy.ops.mesh.primitive_cube_add(
            location=(x * spacing, y * spacing, 0)
        )
        cube = bpy.context.object
        cube.name = f'GridCube_{x}_{y}'

        # Create random color material
        mat = bpy.data.materials.new(name=f"Material_{x}_{y}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get('Principled BSDF')

        # Random color
        color = (random.random(), random.random(), random.random(), 1.0)
        bsdf.inputs['Base Color'].default_value = color

        # Assign material
        cube.data.materials.append(mat)
""")
```

### Working with Modifiers

**Prompt:**
```
Add a subdivision surface modifier to smooth out the model
```

**What Claude will do:**
```python
execute_blender_code("""
import bpy

obj = bpy.context.active_object
if obj:
    # Add subdivision surface modifier
    modifier = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    modifier.levels = 2
    modifier.render_levels = 2
""")
```

## Troubleshooting Common Issues

### Connection Issues

**Problem:** "Not connected to Blender"

**Solution:**
1. Make sure Blender is running
2. Enable the BlenderMCP addon in Blender
3. Click "Connect to Claude" in the BlenderMCP sidebar panel
4. Restart Claude Desktop if needed

**Prompt to test connection:**
```
Check if you're connected to Blender
```

### Timeout Errors

**Problem:** "Timeout waiting for Blender response"

**Causes:**
- Large asset downloads
- Complex Python operations
- Network issues (for external APIs)

**Solutions:**
1. Break complex operations into smaller steps
2. Use lower resolutions for textures/HDRIs initially
3. Simplify the request

**Example - Instead of:**
```
Download 5 different 4k textures and apply them to different objects
```

**Try:**
```
Download a 1k wood texture from PolyHaven
(wait for completion)
Apply it to the cube
(wait for completion)
Download a 1k metal texture
...
```

### Asset Not Found

**Problem:** Searching for assets returns no results

**For PolyHaven:**
```
Check if PolyHaven is enabled
```

**For Sketchfab:**
```
Check if Sketchfab is enabled and API key is configured
```

**For Hyper3D:**
```
Check if Hyper3D Rodin is enabled
```

### Generation Limits (Hyper3D)

**Problem:** "Insufficient balance" error with free trial key

**Solutions:**
1. Wait for daily limit reset
2. Get your own API key from hyper3d.ai
3. Get your own API key from fal.ai
4. Use PolyHaven or Sketchfab alternatives

**Prompt:**
```
I got an insufficient balance error. What should I do?
```

### Objects Not Visible

**Problem:** Objects created but not visible in viewport

**Checks:**
1. Object is in scene
2. Object is not hidden
3. Camera is positioned correctly
4. Object scale is appropriate

**Prompt:**
```
Show me a screenshot of the viewport and list all objects in the scene
```

### Material Not Showing

**Problem:** Material applied but object looks grey

**Causes:**
- Viewport shading mode
- No lights in scene
- Material not properly configured

**Solutions:**
```
Make sure I'm in Material Preview or Rendered view mode, add some lights if needed
```

## Tips and Best Practices

### 1. Check Status First
Always verify which integrations are available:
```
Check what integrations are enabled (PolyHaven, Sketchfab, Hyper3D)
```

### 2. Use Screenshots for Feedback
Request screenshots to verify progress:
```
Show me what the scene looks like now
```

### 3. Start Simple
Begin with basic shapes, then add complexity:
```
Create a simple scene layout first, then we'll add details
```

### 4. Break Down Complex Tasks
Instead of one large request:
```
Create a complete medieval castle with interior, exterior, furniture, and characters
```

Break it down:
```
1. Create the basic castle structure
2. Add towers and walls
3. Add interior rooms
4. Add furniture
5. Add decorative elements
```

### 5. Use Appropriate Asset Sources
- **PolyHaven**: Best for textures, HDRIs, generic nature items
- **Sketchfab**: Best for specific realistic models
- **Hyper3D**: Best for custom/unique items not in libraries
- **Python code**: Best for primitive shapes and precise control

### 6. Save Your Work
Before major operations:
```
I'm going to try something experimental - make sure to save your Blender file first!
```

### 7. Provide Reference Images
For custom models with Hyper3D:
```
Generate a 3D model based on this image: [provide image path]
```

---

## Example Complete Workflow

**Goal:** Create a product visualization for a coffee mug

**Step-by-step prompts:**

```
1. "Check what integrations are available"
2. "Clear the default scene"
3. "Generate a 3D coffee mug using Hyper3D with text prompt: 'ceramic coffee mug with handle'"
4. "Apply a white ceramic material to the mug with slight roughness"
5. "Download a studio HDRI from PolyHaven for lighting"
6. "Set up the camera for product photography - slightly above and to the side"
7. "Add a reflective plane underneath as a surface"
8. "Show me a screenshot of the result"
9. "Adjust the lighting to be slightly brighter"
10. "Perfect! Now create a 120-frame turntable animation"
```

---

For more examples and community creations, join our [Discord](https://discord.gg/z5apgR8TFU)!
