
import bpy
import os
import math
from mathutils import Vector

# Project paths
BASE = os.getcwd()
BOBBY = os.path.join(BASE, "Bobby.fbx")
SUNNY = os.path.join(BASE, "Sunny.fbx")
OUTPUT_DIR = os.path.join(BASE, "video")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Clear the default scene
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

def import_character(filepath, x_position):
    if not os.path.exists(filepath):
        raise FileNotFoundError("Missing character file: " + filepath)

    old_actions = set(bpy.data.actions)

    bpy.ops.import_scene.fbx(filepath=filepath)

    new_objects = list(bpy.context.selected_objects)
    armatures = [obj for obj in new_objects if obj.type == "ARMATURE"]
    meshes = [obj for obj in new_objects if obj.type == "MESH"]

    if not armatures:
        raise RuntimeError("No armature found in " + filepath)

    rig = armatures[0]

    # Find the imported animation
    if rig.animation_data is None:
        rig.animation_data_create()

    if rig.animation_data.action is None:
        new_actions = [a for a in bpy.data.actions if a not in old_actions]
        if new_actions:
            rig.animation_data.action = new_actions[0]

    # Scale character using its mesh height
    bpy.context.view_layer.update()

    if meshes:
        heights = []
        for mesh in meshes:
            points = [
                mesh.matrix_world @ Vector(corner)
                for corner in mesh.bound_box
            ]
            heights.extend([p.z for p in points])

        height = max(heights) - min(heights)

        if height > 0:
            factor = 2.5 / height
            rig.scale = rig.scale * factor

    rig.location.x = x_position
    bpy.context.view_layer.update()

    # Put character's feet on the floor
    if meshes:
        lowest = min(
            (mesh.matrix_world @ Vector(corner)).z
            for mesh in meshes
            for corner in mesh.bound_box
        )
        rig.location.z -= lowest

    print("Imported:", filepath)
    if rig.animation_data.action:
        print("Animation:", rig.animation_data.action.name)
    else:
        print("WARNING: No animation action detected")

    return rig


# Import both characters
bobby = import_character(BOBBY, -1.4)
sunny = import_character(SUNNY, 1.4)

# Scene setup
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 720
scene.render.resolution_y = 1280
scene.render.resolution_percentage = 50
scene.render.fps = 24

# Background
world = bpy.data.worlds.new("Cartoon World") if not bpy.data.worlds else bpy.data.worlds[0]
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.55, 0.65, 0.8, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.8

# Floor
bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, 0))
floor = bpy.context.object
floor.name = "Cartoon Floor"
mat = bpy.data.materials.new("Warm Floor")
mat.diffuse_color = (0.65, 0.8, 0.55, 1)
floor.data.materials.append(mat)

# Camera
bpy.ops.object.camera_add(location=(0, -9, 2.4))
camera = bpy.context.object
camera.name = "Cartoon Camera"
target = Vector((0, 0, 1.3))
direction = target - camera.location
camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
camera.data.type = "ORTHO"
camera.data.ortho_scale = 6.5
scene.camera = camera

# Lighting
def add_light(name, location, power, size):
    bpy.ops.object.light_add(type="AREA", location=location)
    light = bpy.context.object
    light.name = name
    light.data.energy = power
    light.data.shape = "DISK"
    light.data.size = size
    light.rotation_euler = (
        Vector((0, 0, 1.3)) - light.location
    ).to_track_quat("-Z", "Y").to_euler()

add_light("Main Light", (0, -4, 7), 1500, 5)
add_light("Fill Light", (4, 2, 5), 900, 4)

# Use the imported animations to set video duration
end_frame = 48

scene.frame_start = 1
scene.frame_end = end_frame
scene.frame_set(1)

# Video output
scene.render.image_settings.file_format = "FFMPEG"
scene.render.ffmpeg.format = "MPEG4"
scene.render.ffmpeg.codec = "H264"
scene.render.filepath = os.path.join(OUTPUT_DIR, "3d_test.mp4")

# Render
bpy.ops.render.render(animation=True)

print("3D TEST VIDEO CREATED!")
