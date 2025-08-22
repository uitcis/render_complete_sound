bl_info = {
    "name": "Render Complete Sound",
    "author": "817985559@139.com",
    "version": (1, 6),
    "blender": (2, 80, 0),
    "location": "Properties > Scene",
    "description": "Plays a custom sound when rendering is complete",
    "category": "Render"
}
import bpy
from bpy.props import PointerProperty, StringProperty
from bpy.types import PropertyGroup, Panel, Operator, AddonPreferences
from bpy.app.handlers import persistent
import os
import aud

# 全局变量
_current_sound_handle = None

# 获取当前插件的目录
def get_addon_dir():
    for path in bpy.utils.script_paths():
        addons_path = os.path.join(path, "addons")
        addon_dir = os.path.join(addons_path, __name__)
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

class BrowseSoundFileOperator(Operator):
    bl_idname = "scene.browse_sound_file"
    bl_label = "Browse for Sound File"

    filepath: StringProperty(subtype='FILE_PATH')
    filter_glob: StringProperty(default='*.wav;*.mp3;*.ogg', options={'HIDDEN'})

    def execute(self, context):
        if self.filepath:
            bpy.context.scene.render_complete_sound.sound_file_path = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class TestSoundFileOperator(Operator):
    bl_idname = "scene.test_sound_file"
    bl_label = "Test Sound File"

    def execute(self, context):
        global _current_sound_handle
        scene = context.scene
        props = scene.render_complete_sound
        sound_path = props.sound_file_path

        if not sound_path or not os.path.isfile(sound_path):
            prefs = bpy.context.preferences.addons[__name__].preferences
            sound_path = prefs.default_sound_file_path

        if not sound_path or not os.path.isfile(sound_path):
            self.report({'ERROR'}, "No valid sound file selected or file does not exist.")
            return {'CANCELLED'}

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

class ResetSoundFileOperator(Operator):
    bl_idname = "scene.reset_sound_file"
    bl_label = "Reset to Default Sound File"

    def execute(self, context):
        prefs = bpy.context.preferences.addons[__name__].preferences
        default_sound_path = prefs.default_sound_file_path
        if default_sound_path and os.path.isfile(default_sound_path):
            bpy.context.scene.render_complete_sound.sound_file_path = default_sound_path
        else:
            self.report({'ERROR'}, "Default sound file not found.")
        return {'FINISHED'}

class RenderCompleteSoundPanel(Panel):
    bl_label = "Render Complete Sound"
    bl_idname = "RENDER_PT_render_complete_sound"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    def draw(self, context):
        global _current_sound_handle
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
        layout.operator("scene.reset_sound_file", text="Reset to Default")

        if _current_sound_handle is not None:
            layout.operator("scene.stop_sound_file", text="Stop Sound")
        else:
            layout.label(text="No sound playing.")

@persistent
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

@persistent
def load_handler(dummy):
    # 确保在加载文件时正确设置渲染完成回调
    if play_sound_on_render_complete not in bpy.app.handlers.render_complete:
        bpy.app.handlers.render_complete.append(play_sound_on_render_complete)

# 定义所有需要注册的类
classes = (
    RenderCompleteSoundProperties,
    RenderCompleteSoundPreferences,
    RenderCompleteSoundPanel,
    BrowseSoundFileOperator,
    TestSoundFileOperator,
    StopSoundFileOperator,
    ResetSoundFileOperator,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # 动态设置Scene属性
    bpy.types.Scene.render_complete_sound = PointerProperty(type=RenderCompleteSoundProperties)
    bpy.app.handlers.render_complete.append(play_sound_on_render_complete)
    # 添加文件加载处理程序以确保回调在重新打开文件后仍然有效
    bpy.app.handlers.load_post.append(load_handler)

def unregister():
    global _current_sound_handle
    if _current_sound_handle:
        try:
            _current_sound_handle.stop()
        except Exception as e:
            print(f"Failed to stop sound on unregister: {e}")
        _current_sound_handle = None

    if play_sound_on_render_complete in bpy.app.handlers.render_complete:
        bpy.app.handlers.render_complete.remove(play_sound_on_render_complete)
    if load_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_handler)
    del bpy.types.Scene.render_complete_sound
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()