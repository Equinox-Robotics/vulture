import bpy

def main() -> None:
    # 1. Clear existing objects in the scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # 2. Add a cube and get a reference to it
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    cube = bpy.context.active_object

    # 3. Create a green material (use_nodes is True by default in Blender 5.0+)
    mat = bpy.data.materials.new(name="GreenMaterial")
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.0, 0.8, 0.0, 1.0)
    cube.data.materials.append(mat)


    # 4. Add a light source so the cube isn't pitch black
    bpy.ops.object.light_add(type="POINT", location=(4, -4, 5))
    light = bpy.context.active_object
    light.data.energy = 1000

    # 5. Add a camera and point it at the cube
    bpy.ops.object.camera_add(location=(5, -5, 4))
    camera = bpy.context.active_object
    bpy.context.scene.camera = camera

    # Point camera toward the origin (0, 0, 0)
    direction = cube.location - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    # 6. Configure render settings
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"

    scene.render.filepath = "green_cube.png"  # Update path as needed
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080

    bpy.ops.render.render(write_still=True)

main()