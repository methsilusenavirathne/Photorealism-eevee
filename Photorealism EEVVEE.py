bl_info = {
    "name": "Photorealism EEVVEE",
    "author": "Lithika Senavirathne",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Render > Real EEVVEE",
    "description": "Photorealism for Eevee render engine",
    "warning": "",
    "doc_url": "https://github.com/methsilusenavirathne",
    "category": "Render",
}

import bpy

def QuickEffects(context):
    bpy.context.scene.eevee.use_gtao = True
    bpy.context.scene.eevee.gtao_distance = 1
    bpy.context.scene.eevee.use_ssr = True
    bpy.context.scene.eevee.use_bloom = True
    bpy.context.scene.view_settings.look = 'High Contrast'
    bpy.context.scene.eevee.use_motion_blur = True
    bpy.context.scene.eevee.volumetric_tile_size = '2'
    bpy.context.scene.eevee.use_ssr_halfres = False
    bpy.context.scene.eevee.use_volumetric_shadows = True
    bpy.context.scene.eevee.shadow_cube_size = '256'

def DisableEffects(context):
    bpy.context.scene.eevee.use_gtao = False
    bpy.context.scene.eevee.use_bloom = False
    bpy.context.scene.eevee.use_ssr = False
    bpy.context.scene.eevee.use_motion_blur = False
    bpy.context.scene.eevee.shadow_cube_size = '512'

def Quickdop(context):
    cam_ob = bpy.context.scene.camera
    if cam_ob is None:
        return {'CANCELLED'}
    elif cam_ob.type == 'CAMERA':
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        activeobj = bpy.context.active_object
        activeobj.name = "DOP_Control"
        bpy.ops.object.select_camera()
        cam_ob.data.dof.use_dof = True
        cam_ob.data.dof.focus_object = bpy.data.objects["DOP_Control"]
        cam_ob.data.dof.aperture_fstop = 0.5

    else:
        print("%s object as camera" % cam_ob.type)

class Quick_Effects(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Quick Optimize"

    def execute(self, context):
        QuickEffects(context)
        return {'FINISHED'}
    
class Disable_Effects(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator1"
    bl_label = "Disable for laggy viewport" 

    def execute(self, context):
        DisableEffects(context)
        return {'FINISHED'}    
   
class Quick_DOP(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator2"
    bl_label = "Quick DOP"

    def execute(self, context):
        Quickdop(context)
        return {'FINISHED'}     
    
class RealEEVVEEPanel(bpy.types.Panel):
    
    bl_label = "Real EEVVEE"
    bl_idname = "RENDER_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        
        layout = self.layout

        scene = context.scene
        
        if (bpy.context.scene.render.engine == 'CYCLES') :
            layout.label(text="Not supported for Cycles",icon = "ERROR")    
        
        box = layout.box()
        box.label(text="Quick Effects:")
        row = box.row()
        row.scale_y = 2.0
        row.operator("object.simple_operator")
        
        row = box.row()
        row = box.row()
        row.scale_y = 1.0
        row.operator("object.simple_operator1")
        
        row = box.row()
        
class TweakSettings(bpy.types.Panel):

    bl_label = "Tweak settings"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_parent_id = "RENDER_PT_layout"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout

        scene = context.scene
        
        #layout.label(text="Tweak settings")
        
        row = layout.row()
        row.prop(context.scene.eevee, "taa_render_samples",text = "Render Samples")
        
        row = layout.row()
        row.prop(context.scene.eevee, "gtao_distance",text = "AO distance")
        row.prop(context.scene.eevee, "gtao_factor",text = "AO factor")

        row = layout.row()
        row.prop(context.scene.eevee, "bloom_intensity",text = "Bloom Effect")
        
        row = layout.row()
        row.prop(context.scene.eevee, "use_ssr_refraction",text = "Optimize for glass (ony if using glass)")
        
        row = layout.row()
        row.prop(context.scene.eevee, "motion_blur_shutter",text = "Motion Blur Effect")
        
        row = layout.row()
        row.prop(context.scene.eevee, "volumetric_tile_size",text = "Volume Res")
        
        row = layout.row()
        row.label(text="if using sss: ")
        row.scale_x = 2.0
        row.prop(context.scene.eevee, "sss_samples",text = "Subsurf Samples")
        
        row = layout.row()
        row.prop(scene.render, "use_freestyle",text = "Cartoonish Outlines")   
        
class QuickDOP(bpy.types.Panel):

    bl_label = "Quick DOP"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_parent_id = "RENDER_PT_layout"

    def draw(self, context):

        layout = self.layout

        scene = context.scene
        
        box = layout.box()
        box.label(text="Quick Depth Of Field Setup")
        row = box.row()
        row.scale_y = 2.0
        row.operator("object.simple_operator2")
        row = box.row()
        box.label(text="not working without a camera",icon = "INFO")
        
class AboutPanel(bpy.types.Panel):

    bl_label = "About"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_parent_id = "RENDER_PT_layout"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout

        scene = context.scene
        box = layout.box()
        row = box.row
        box.label(text="Developed by:",icon = "INFO")
        row = box.row
        box.label(text="Author : Lithika Senavirathne", icon = "GREASEPENCIL")
        row = box.row
        box.label(text="Company : methsilusenavirathne (individual)",icon = "GROUP")
        row = box.row
        box.label(text="Country : Sri Lanka",icon = "KEYFRAME_HLT")
        

def register():
    bpy.utils.register_class(Quick_Effects)
    bpy.utils.register_class(RealEEVVEEPanel)
    bpy.utils.register_class(Disable_Effects)
    bpy.utils.register_class(Quick_DOP)
    bpy.utils.register_class(TweakSettings)
    bpy.utils.register_class(QuickDOP)
    bpy.utils.register_class(AboutPanel)


def unregister():
    bpy.utils.unregister_class(Quick_Effects) 
    bpy.utils.unregister_class(RealEEVVEEPanel)
    bpy.utils.unregister_class(Disable_Effects)
    bpy.utils.unregister_class(Quick_DOP)
    bpy.utils.unregister_class(TweakSettings)
    bpy.utils.unregister_class(QuickDOP)
    bpy.utils.unregister_class(AboutPanel)
    
    
if __name__ == "__main__":
    register()
    

    
    
