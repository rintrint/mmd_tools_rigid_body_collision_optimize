import bpy
import mmd_tools.core.model as mmd_model
import mmd_tools

def rigid_body_collection_clear(context = bpy.context):
    root = mmd_model.Model.findRoot(context.active_object)
    rig = mmd_model.Model(root)
    
    rigid_objects = [i for i in list(rig.rigidBodies()) if i.select == True]
    
    for rigid_object in rigid_objects:
        for i in range(0, 20):
            rigid_object.rigid_body.collision_collections[i] = False

def rigid_body_collection_coloring(context = bpy.context, available_collections=[]):
    # 如果沒有任何顏色可選
    if True not in available_collections:
        return
    
    root = mmd_model.Model.findRoot(context.active_object)
    rig = mmd_model.Model(root)
    
    rigid_objects = [i for i in list(rig.rigidBodies()) if i.select]
    
    colors = []
    
    def get_best_color(obj_a):
        min_colors_distance = [float('inf') - i for i in range(20)]
        
        for i in range(0, 20):
            if available_collections[i] == False:
                min_colors_distance[i] = -i
        
        print(available_collections)
        print(min_colors_distance)
        
        for i in range(len(colors)):
            color = colors[i]
            obj_b = rigid_objects[i]
            distance = (obj_a.location - obj_b.location).length
            min_colors_distance[color] = min(min_colors_distance[color], distance)

        max_value = max(min_colors_distance)
        best_color = min_colors_distance.index(max_value)
        return best_color
    
    def paint_color():
        for obj_a in rigid_objects:
            best_color = get_best_color(obj_a)
            colors.append(best_color)
    
    paint_color()
    
    print("Colors:", colors)
    
    # 上色
    total = len(rigid_objects)
    for i in range(total):
        rigid_objects[i].rigid_body.collision_collections[colors[i]] = True

def rigid_body_collection_put_into_all(context = bpy.context, available_collections=[]):
    # 如果沒有任何顏色可選
    if True not in available_collections:
        return
    
    root = mmd_model.Model.findRoot(context.active_object)
    rig = mmd_model.Model(root)
    
    rigid_objects = [i for i in list(rig.rigidBodies()) if i.select == True]
    
    for rigid_object in rigid_objects:
        for i in range(0, 20):
            rigid_object.rigid_body.collision_collections[i] |= available_collections[i]
