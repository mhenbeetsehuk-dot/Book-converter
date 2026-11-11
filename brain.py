"""Deterministic book-to-scene planner and Blender script generator (stdlib only)."""
import json
import re
from dataclasses import dataclass, asdict

@dataclass
class Scene:
    id: str
    title: str
    source_excerpt: str
    duration_seconds: int
    setting: str
    status: str = "draft"

def plan(text: str) -> list[dict]:
    text = text.replace("\r\n", "\n").strip()
    if not text:
        raise ValueError("The manuscript is empty.")
    chunks = re.split(r"(?im)^\\s*(?:chapter\\s+\\d+|part\\s+[ivx\\d]+)\\b[^\\n]*$", text)
    chunks = [c.strip() for c in chunks if c.strip()]
    if len(chunks) == 1:
        chunks = [c.strip() for c in re.split(r"\n\s*\n", text) if c.strip()]
    scenes = []
    for i, chunk in enumerate(chunks[:250], 1):
        words = chunk.split()
        scenes.append(asdict(Scene(
            id=f"S{i:03d}", title=f"Scene {i}", source_excerpt=chunk[:1800],
            duration_seconds=max(8, min(90, round(len(words) / 2.4))),
            setting="Unspecified — requires creative review"
        )))
    return scenes

def blender_script(scene: dict) -> str:
    """Return a self-contained Blender Python scene with placeholder geometry."""
    label = str(scene.get("title", "Scene"))[:70]
    seconds = max(2, min(30, int(scene.get("duration_seconds", 8))))
    return f'''import bpy
import math
from mathutils import Vector
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items.keys() else "BLENDER_EEVEE"
scene.render.resolution_x = 640
scene.render.resolution_y = 360
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.frame_end = {seconds} * 24
def material(name, rgba):
    m = bpy.data.materials.new(name)
    m.diffuse_color = rgba
    return m
ground = material("Ground", (0.08, 0.10, 0.16, 1))
actor = material("Actor", (0.2, 0.6, 0.8, 1))
bpy.ops.mesh.primitive_cube_add(size=2, location=(0,0,-0.3))
floor = bpy.context.object
floor.name = "Set floor"
floor.scale = (6,6,0.2)
floor.data.materials.append(ground)
for x in (-1.2, 1.2):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, location=(x,0,1.3))
    obj = bpy.context.object
    obj.name = "Placeholder actor"
    obj.scale = (0.4,0.35,1.2)
    obj.data.materials.append(actor)
    obj.location.z = 1.3
    obj.keyframe_insert(data_path="location", frame=1)
    obj.location.y = -0.35
    obj.keyframe_insert(data_path="location", frame=scene.frame_end)
bpy.ops.object.light_add(type="AREA", location=(0,-2,6))
bpy.context.object.data.energy = 950
bpy.context.object.data.shape = "DISK"
bpy.context.object.data.size = 5
bpy.ops.object.camera_add(location=(7,-10,5))
cam = bpy.context.object
direction = Vector((0,0,1)) - cam.location
cam.rotation_euler = direction.to_track_quat("-Z","Y").to_euler()
scene.camera = cam
cam.keyframe_insert(data_path="location", frame=1)
cam.location.x = 5
cam.keyframe_insert(data_path="location", frame=scene.frame_end)
scene.render.image_settings.file_format = "FFMPEG"
scene.render.ffmpeg.format = "MPEG4"
scene.render.ffmpeg.codec = "H264"
scene.render.filepath = "/content/book_converter_scene.mp4"
bpy.ops.render.render(animation=True)
'''
