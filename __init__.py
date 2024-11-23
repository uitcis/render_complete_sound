#空行不能删
bl_info = {
    "name": "Render Complete Sound",
    "author": "817985559@139.com",
    "version": (1, 3),
    "blender": (2, 80, 0),
    "location": "Properties > Scene",
    "description": "Plays a custom sound when rendering is complete",
    "category": "Render"
}
import bpy
from bpy.props import PointerProperty, StringProperty
from bpy.types import PropertyGroup, Panel, Operator, AddonPreferences
import os
import aud

# 获取当前插件的目录
def get_addon_dir():
    for path in bpy.utils.script_paths("addons"):
        addon_dir = os.path.join(path, __name__)
        if os.path.isdir(addon_dir):
            return addon_dir
    return None

# 获取默认声音文件路径
def get_default_sound_path():
    addon_dir = get_addon_dir()
    if addon_dir:
        return os.path.join(addon_dir, "render_complete_sound.wav")
    return ""

class RenderCompleteSoundProperties(PropertyGroup):
    sound_file_path: StringProperty(
        name="Sound File",
        description="Path to the sound file to play when rendering is complete",
        subtype='FILE_PATH',
        default=""
    )

class RenderCompleteSoundPreferences(AddonPreferences):
    bl_idname = __name__

    # 设置默认的声音文件路径
    default_sound_file_path: StringProperty(
        name="Default Sound File",
        description="Default path to the sound file to play when rendering is complete",
        subtype='FILE_PATH',
        default=get_default_sound_path(),
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "default_sound_file_path")
class RenderCompleteSoundPreferences(AddonPreferences):  
    bl_idname = __name__  
    default_sound_file_path: StringProperty(  
        name="Default Sound File",  
        description="Default path to the sound file to play when rendering is complete",  
        subtype='FILE_PATH',  
        default="",  
    )  
    def draw(self, context):  
        layout = self.layout  
        row = layout.row()  
        row.prop(self, "default_sound_file_path")    
      
class BrowseSoundFileOperator(Operator):  
    bl_idname = "scene.browse_sound_file"  
    bl_label = "Browse for Sound File"  
  
    def execute(self, context):  
        # 使用Blender的文件选择器来选择一个文件  
        context.window_manager.fileselect_add(self.select_file)  
        return {'RUNNING_MODAL'}  
  
    def select_file(self, context, filepath):  
        # 当用户选择一个文件时调用  
        if filepath:  
            bpy.context.scene.render_complete_sound.sound_file_path = filepath  
        # 退出文件选择器  
        return {'FINISHED'}  
  
    def invoke(self, context, event):  
        # 设置文件选择器的过滤器（可选）  
        bpy.types.WindowManager.fileselect_set_filter(bpy.context, 'SOUND')  
        return super().invoke(context, event)
 
class TestSoundFileOperator(Operator):  
    bl_idname = "scene.test_sound_file"  
    bl_label = "Test Sound File"  
  
    def execute(self, context):  
        scene = context.scene  
        props = scene.render_complete_sound  
        sound_path = props.sound_file_path  
  
      
        if not sound_path or not os.path.isfile(sound_path):  
            
            prefs = bpy.context.preferences.addons[__name__].preferences  
            sound_path = prefs.default_sound_file_path  
  
        if not sound_path or not os.path.isfile(sound_path):  
            self.report({'ERROR'}, "No valid sound file selected or file does not exist.")  
            return {'CANCELLED'}  
  
        global _current_sound_handle  
       
        if _current_sound_handle:  
            _current_sound_handle.stop()  
            _current_sound_handle = None  
  
        try:  
            device = aud.Device()  
            sound = aud.Sound(sound_path)  
            _current_sound_handle = device.play(sound)    
            _current_sound_handle.volume = 1.0  
            _current_sound_handle.loop_count = 0  
            self.report({'INFO'}, "Sound file played successfully.")  
        except Exception as e:  
            _current_sound_handle = None    
            self.report({'ERROR'}, f"Failed to play sound: {sound_path}. Error: {e}")  
  
        return {'FINISHED'}
 
class StopSoundFileOperator(Operator):  
    bl_idname = "scene.stop_sound_file"  
    bl_label = "Stop Sound File"  
    def execute(self, context):  
        global _current_sound_handle  
        if _current_sound_handle:  
            _current_sound_handle.stop()    
            _current_sound_handle = None    
        self.report({'INFO'}, "Sound file stopped.")  
        return {'FINISHED'}
  
class RenderCompleteSoundPanel(Panel):  
    bl_label = "Render Complete Sound"  
    bl_idname = "RENDER_PT_render_complete_sound"  
    bl_space_type = 'PROPERTIES'  
    bl_region_type = 'WINDOW'  
    bl_context = "output"  
    def draw(self, context):  
        layout = self.layout  
        props = context.scene.render_complete_sound  
  
        row = layout.row(align=True)  
        row.prop(props, "sound_file_path", text="")  
          
        if not props.sound_file_path:  
            layout.label(text="No sound file selected!", icon='ERROR')  
        elif not os.path.isfile(props.sound_file_path):  
            layout.label(text="File not found!", icon='ERROR')  
            props.sound_file_path = ""  
        layout.operator("scene.browse_sound_file", text="Browse")  
        layout.operator("scene.test_sound_file", text="Test Sound")  
        layout.label(text="To change the default sound file, go to Edit > Preferences > Add-ons > Render Complete Sound.", icon='PREFERENCES')
          
        if _current_sound_handle is not None:  
            layout.operator("scene.stop_sound_file", text="Stop Sound")  
        else:  
            layout.label(text="No sound playing.")                   
  
def play_sound_on_render_complete(scene):  
    global _current_sound_handle  
    sound_path = scene.render_complete_sound.sound_file_path  
    
    if _current_sound_handle:  
        _current_sound_handle.stop()  
        _current_sound_handle = None  
     
    if not sound_path or not os.path.isfile(sound_path):  
        prefs = bpy.context.preferences.addons[__name__].preferences  
        sound_path = prefs.default_sound_file_path  
    if not sound_path or not os.path.isfile(sound_path):  
        print("No valid sound file selected or file does not exist.")  
        return  
    try:  
        device = aud.Device()  
        sound = aud.Sound(sound_path)  
        _current_sound_handle = device.play(sound)  
        _current_sound_handle.volume = 1.0  
        _current_sound_handle.loop_count = 0  
    except Exception as e:  
        print(f"An error occurred while playing sound: {e}")  
        _current_sound_handle = None
def register():  
    bpy.utils.register_class(RenderCompleteSoundProperties)  
    bpy.types.Scene.render_complete_sound = PointerProperty(type=RenderCompleteSoundProperties)  
    bpy.utils.register_class(RenderCompleteSoundPreferences)  
    bpy.utils.register_class(RenderCompleteSoundPanel)  
    bpy.utils.register_class(BrowseSoundFileOperator)  
    bpy.utils.register_class(TestSoundFileOperator)  
    bpy.utils.register_class(StopSoundFileOperator)  
    bpy.app.handlers.render_complete.append(play_sound_on_render_complete)  
def unregister():  
      
    global _current_sound_handle  
    if _current_sound_handle:  
        try:  
            _current_sound_handle.stop()  
        except Exception as e:  
            print(f"Failed to stop sound on unregister: {e}")  
        _current_sound_handle = None  
    bpy.app.handlers.render_complete.remove(play_sound_on_render_complete)  
    bpy.utils.unregister_class(StopSoundFileOperator)  
    bpy.utils.unregister_class(TestSoundFileOperator)  
    bpy.utils.unregister_class(BrowseSoundFileOperator)  
    bpy.utils.unregister_class(RenderCompleteSoundPanel)  
    del bpy.types.Scene.render_complete_sound  
    bpy.utils.unregister_class(RenderCompleteSoundPreferences)  
    bpy.utils.unregister_class(RenderCompleteSoundProperties)  
if __name__ == "__main__":  
    register()