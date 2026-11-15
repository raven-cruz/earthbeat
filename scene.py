import math
from pathlib import Path

import bpy
from mathutils import Vector

render_dir = Path.cwd() / "renders"

# blank scene
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

# camera points at center of cube
bpy.ops.object.camera_add(location=(7, -9, 6))
camera = bpy.context.object
bpy.context.scene.camera = camera

# render png
# in terminal: blender --background --python scene.py
scene = bpy.context.scene
scene.render.resolution_x = 800
scene.render.resolution_y = 500
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(render_dir / "render.png") # overwrites every time

bpy.ops.render.render(write_still=True)
print(f"saved {scene.render.filepath}")
