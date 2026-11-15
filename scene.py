# RUN THIS:
# blender --background --python scene.py

import math
from pathlib import Path

import bpy
from mathutils import Vector

render_dir = Path.cwd() / "renders"

# blank scene
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

# ground
bpy.ops.mesh.primitive_plane_add(size=16, location=(0, 0, 0))
ground = bpy.context.object
ground.name = "ground"

ground_material = bpy.data.materials.new("ground mat")
ground_material.diffuse_color = (0.52, 0.56, 0.62, 1.0)
ground.data.materials.append(ground_material)

# cube rests on ground
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
cube = bpy.context.object
cube.name = "test cube"

cube_material = bpy.data.materials.new("cube mat")
cube_material.diffuse_color = (0.86, 0.88, 0.90, 1.0)
cube.data.materials.append(cube_material)

# TEMP fixed sunlight
bpy.ops.object.light_add(type="SUN", location=(0, 0, 5))
sun = bpy.context.object
sun.name = "sun"
sun.rotation_euler = (math.radians(40), math.radians(-25), math.radians(25))
sun.data.energy = 2.0
sun.data.angle = math.radians(2.0)  # Slightly softened shadows.

# sky light
world = bpy.context.scene.world
background = world.node_tree.nodes.get("Background")
background.inputs["Color"].default_value = (0.65, 0.76, 0.95, 1.0)
background.inputs["Strength"].default_value = 0.5

# camera points at center of cube
bpy.ops.object.camera_add(location=(7, -9, 6))
camera = bpy.context.object
camera.name = "camera"
target = Vector((0, 0, 0.9))
camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
bpy.context.scene.camera = camera

# render png
# in terminal: blender --background --python scene.py
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 32
scene.render.resolution_x = 800
scene.render.resolution_y = 500
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(render_dir / "render.png")

bpy.ops.render.render(write_still=True)
print(f"saved {scene.render.filepath}")