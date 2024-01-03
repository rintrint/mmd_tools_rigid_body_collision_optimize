bl_info = {
    "name": "mmd_tools_rigid_body_collision_optimize", 
    "description": "Put rigid bodys into appropriate collision collection in order to avoid collision between selected rigid bodys.",
    "author": "rint",
    "version": (0, 0, 3),
    "blender": (2, 93, 18),
    "location": "View3D > Sidebar > MMD Tools Panel",
    "category": "Object",
}

import bpy
import mmd_tools.core.model as mmd_model
import mmd_tools
from mmd_tools_rigid_body_collision_optimize.utils import *

# Define a property group to store the custom toggles
class mmd_tools_rigid_body_collision_optimize_PG(bpy.types.PropertyGroup):
    #for i in range(20):
    #    exec(f"custom_toggle_{i}: bpy.props.BoolProperty(name='{i}', default=True)")
    
    #element_list = [0, 10, 1, 11, 2, 12, 3, 13, 4, 14]
    #for i in element_list:
    #    exec(f"custom_toggle_{i}: bpy.props.BoolProperty(name='{i}', default=True)")
    #element_list = [5, 15, 6, 16, 7, 17, 8, 18, 9, 19]
    #for i in element_list:
    #    exec(f"custom_toggle_{i}: bpy.props.BoolProperty(name='{i}', default=False)")
    
    custom_toggles: bpy.props.BoolVectorProperty(
        name = "Available Collections",
        description = "",
        size = 20
    )
    def __init__(self):
        element_list = [0, 10, 1, 11, 2, 12, 3, 13, 4, 14]
        for i in element_list:
            self.custom_toggles[i] = True
    
class PANEL1_PT_mmd_tools_rigid_body_collision_optimize(bpy.types.Panel):
    bl_label = "Collision Collection Interleave"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MMD"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        test5_property_group = context.scene.test5_property_group # Get the property group
        
        col = self.layout.column(align=True)
        col.label(text='Rigid Body')
        
        grid = col.grid_flow(row_major=True, align=True)
        
        row = grid.row(align=True)
        row.operator_context = 'EXEC_DEFAULT'
        op = row.operator('mmd_tools.rigid_body_select', text='Select', icon='RESTRICT_SELECT_OFF')
        row.separator()
        op = row.operator('mmd_tools_rigid_body_collision_optimize.clear', text='Clear')
        op = row.operator('mmd_tools_rigid_body_collision_optimize.interleave', text='Interleave')
        op = row.operator('mmd_tools_rigid_body_collision_optimize.put_into_all', text='Put into All')
        
        # Use the property group to draw the toggles
        col = self.layout.column(align=True)
        col.label(text='Available Collections')
        
        grid = layout.grid_flow(columns=11, align=True)
        
        element_list = [0, 10, 1, 11, 2, 12, 3, 13, 4, 14]
        for i in element_list:
            grid.prop(test5_property_group, 'custom_toggles', index=i, text='', toggle=True)
        
        grid.separator()
        grid.separator()
        
        element_list = [5, 15, 6, 16, 7, 17, 8, 18, 9, 19]
        for i in element_list:
            grid.prop(test5_property_group, 'custom_toggles', index=i, text='', toggle=True)

class mmd_tools_rigid_body_collision_optimize_Button0(bpy.types.Operator):
    bl_idname = 'mmd_tools_rigid_body_collision_optimize.clear'
    bl_label = 'Collision Collection Clear'
    bl_description = 'Unassign rigid body to all collection.'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return mmd_model.isRigidBodyObject(context.active_object)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context: bpy.types.Context):
        try:
            rigid_body_collection_clear(context)
            
            message = 'OK'
            self.report({'INFO'}, f"{message}")
            
        except Exception as ex:
            self.report(type={'ERROR'}, message=str(ex))
            return {'CANCELLED'}

        return {'FINISHED'}

class mmd_tools_rigid_body_collision_optimize_Button1(bpy.types.Operator):
    bl_idname = 'mmd_tools_rigid_body_collision_optimize.interleave'
    bl_label = 'Collision Collection Interleave'
    bl_description = 'Put rigid bodys into appropriate collision collection in order to avoid collision between selected rigid bodys.'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return mmd_model.isRigidBodyObject(context.active_object)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context: bpy.types.Context):
        try:
            test5_property_group = context.scene.test5_property_group
            
            rigid_body_collection_coloring(context, available_collections=test5_property_group.custom_toggles)
            
            message = 'OK'
            self.report({'INFO'}, f"{message}")
            
        except Exception as ex:
            self.report(type={'ERROR'}, message=str(ex))
            return {'CANCELLED'}

        return {'FINISHED'}

class mmd_tools_rigid_body_collision_optimize_Button2(bpy.types.Operator):
    bl_idname = 'mmd_tools_rigid_body_collision_optimize.put_into_all'
    bl_label = 'Collision Collection Put into All'
    bl_description = 'Put rigid bodys into all available collections(selected).'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return mmd_model.isRigidBodyObject(context.active_object)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context: bpy.types.Context):
        try:
            test5_property_group = context.scene.test5_property_group
            
            rigid_body_collection_put_into_all(context, available_collections=test5_property_group.custom_toggles)
            
            message = 'OK'
            self.report({'INFO'}, f"{message}")
            
        except Exception as ex:
            self.report(type={'ERROR'}, message=str(ex))
            return {'CANCELLED'}

        return {'FINISHED'}

classes = (
    mmd_tools_rigid_body_collision_optimize_PG,
	PANEL1_PT_mmd_tools_rigid_body_collision_optimize,
    mmd_tools_rigid_body_collision_optimize_Button0,
    mmd_tools_rigid_body_collision_optimize_Button1,
    mmd_tools_rigid_body_collision_optimize_Button2
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.test5_property_group = bpy.props.PointerProperty(type=mmd_tools_rigid_body_collision_optimize_PG)
    # 翻譯
    from mmd_tools_rigid_body_collision_optimize.m17n import translation_dict
    bpy.app.translations.register(bl_info['name'], translation_dict)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.test5_property_group
    # 翻譯
    bpy.app.translations.unregister(bl_info['name'])

# 插件名可以改一下，容易辨識，也可以不改，不會導致衝突
# bl_idname不能和其他插件一樣，插件同時啟用會導致衝突
# classes名不能和其他插件一樣，插件同時啟用會導致衝突
# Test_Panel3.bl_category和其他插件一樣就會放在一起
