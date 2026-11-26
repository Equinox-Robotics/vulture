import math

import bpy
import random


def import_glb_grouped_at_point(filepath, target_location):
    existing_objects = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=filepath)
    imported_objects = [obj for obj in bpy.data.objects if obj not in existing_objects]

    # Create an Empty at the target location
    root_empty = bpy.data.objects.new("GLB_Root", None)
    root_empty.location = target_location
    root_empty.rotation_euler = (0, 0, math.radians(random.randint(0,360)))

    bpy.context.collection.objects.link(root_empty)

    # Parent top-level imported objects to the Empty
    for obj in imported_objects:
        if obj.parent is None:
            obj.parent = root_empty

def main() -> None:
    # clear objects
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # add objects2
    for x in range(-5,5):
        for y in range(-5,5):
            if random.random() > 0.8:
                x_loc = x*10
                y_loc = y*10
                import_glb_grouped_at_point(
                    "../../assets/" + random.choices(
                        population = ["dead_tree.glb", "tree2.glb", "abandoned_house.glb", "house.glb"],
                        weights = [10, 10, 5, 5], k=1
                    )[0],
                    (x_loc, y_loc, 0)
                )
                #bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0))

    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))

    # Add sky light
    bpy.ops.object.light_add(
        type="AREA",
        location=(0, 0, 100)
    )

    light = bpy.context.active_object
    light.data.energy = 80000
    light.data.shape = 'SQUARE'
    light.data.size = 100


    # Add center highlight light
    bpy.ops.object.light_add(
        type="POINT",
        location=(0,0, 20)
    )

    light = bpy.context.active_object
    light.data.energy = 20000

    # Add random light
    bpy.ops.object.light_add(
        type="POINT",
        location=(random.randint(-50,50), random.randint(-50,50), 20)
    )

    light = bpy.context.active_object
    light.data.energy = 20000



    # Add camera
    bpy.ops.object.camera_add(location=(0, 0, 100))
    camera = bpy.context.active_object
    bpy.context.scene.camera = camera

    camera.rotation_euler = (0, 0, 0)
    camera.data.angle = math.radians(100)


    # Configure rendering
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"

    scene.render.filepath = "scene.png"
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100

    # Render
    bpy.ops.render.render(write_still=True)

if __name__ == "__main__": main()