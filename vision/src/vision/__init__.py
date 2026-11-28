import math

import bpy
import random
import mathutils

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

    #skybox
    world = bpy.context.scene.world
    if world is None:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world

    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links

    nodes.clear()

    # Create nodes
    node_output = nodes.new(type="ShaderNodeOutputWorld")
    node_output.location = (400, 0)

    node_bg = nodes.new(type="ShaderNodeBackground")
    node_bg.location = (200, 0)
    node_bg.inputs["Strength"].default_value = 1.0

    node_sky = nodes.new(type="ShaderNodeTexSky")
    node_sky.location = (0, 0)

    node_sky.sky_type = "MULTIPLE_SCATTERING"


    node_sky.sun_disc = True
    node_sky.sun_size = 0.00951
    node_sky.sun_intensity = 1.0
    node_sky.sun_elevation = math.radians(20)
    node_sky.sun_rotation = 0.3

    node_sky.altitude = 0.0
    node_sky.air_density = 1.0
    node_sky.aerosol_density = 1.0
    node_sky.ozone_density = 1.0

    links.new(node_sky.outputs["Color"], node_bg.inputs["Color"])
    links.new(node_bg.outputs["Background"], node_output.inputs["Surface"])

    bpy.ops.mesh.primitive_plane_add(size=200.0, location=(0.0, 0.0, 0.0))
    plane = bpy.context.active_object
    plane.name = "RectPlane"

    mat = bpy.data.materials.new(name="RepeatingMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new(type="ShaderNodeOutputMaterial")
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    tex_image = nodes.new(type="ShaderNodeTexImage")
    mapping = nodes.new(type="ShaderNodeMapping")
    tex_coord = nodes.new(type="ShaderNodeTexCoord")

    bsdf.inputs["Roughness"].default_value = 0.95
    bsdf.inputs["Specular IOR Level"].default_value = 0.05
    bsdf.inputs["Diffuse Roughness"].default_value = 0.8

    tex_image.image = bpy.data.images.load(
        "../../assets/grass.jpg", check_existing=True
    )
    tex_image.extension = "REPEAT"

    tiles_per_meter = 0.1
    mapping.inputs["Scale"].default_value = (
        200 * tiles_per_meter,
        200 * tiles_per_meter,
        1.0,
    )

    links.new(tex_coord.outputs["UV"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], tex_image.inputs["Vector"])
    links.new(tex_image.outputs["Color"], bsdf.inputs["Base Color"])
    links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

    plane.data.materials.append(mat)

    # add objects2
    for x in range(-5,5):
        for y in range(-5,5):
            if random.random() > 0.0 and not (x == 0 and y == 0):
                x_loc = x*10
                y_loc = y*10
                import_glb_grouped_at_point(
                    "../../assets/" + random.choices(
                        population = ["grass.glb","dead_tree.glb", "tree2.glb", "abandoned_house.glb", "house.glb"],
                        weights = [40, 10, 10, 3, 3], k=1
                    )[0],
                    (x_loc, y_loc, 0)
                )
                #bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0))




    # Add camera
    bpy.ops.object.camera_add(location=(0, 0, 100))
    camera = bpy.context.active_object
    bpy.context.scene.camera = camera

    camera.rotation_euler = (0, 0, 0)
    camera.data.angle = math.radians(100)

    bpy.ops.object.camera_add(location=(0, 0, 1))
    camera = bpy.context.active_object
    bpy.context.scene.camera = camera

    camera.rotation_euler = (math.radians(95), 0, 0)
    camera.data.angle = math.radians(100)
    #camera.data.clip_end = 40


    # Configure rendering
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'

    # 5. Lower Output Resolution Percentage
    scene.render.resolution_percentage = 50
    bpy.context.scene.cycles.transparent_max_bounces = 64

    scene.render.filepath = "scene.png"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True
    scene.view_settings.exposure = -3.5
    glass_mat = bpy.data.materials.get("GlassMaterial")
    if glass_mat:
        glass_mat.use_raytrace_refraction = True

    # Render
    bpy.ops.render.render(write_still=True)

if __name__ == "__main__": main()