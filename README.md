

# 渲染完成声音插件

## 简介
这是一个为Blender设计的插件，可以在渲染完成后播放自定义的声音。

## 功能
- 当渲染完成时播放指定的声音文件。
- 允许用户通过偏好设置指定默认的声音文件路径。
- 提供了用于测试、停止和重置声音文件的操作符。

## 使用方法
1. 安装插件。
2. 在Blender的用户界面中找到插件设置。
3. 设置渲染完成后想要播放的声音文件路径。
4. 开始渲染，完成后即可听到声音。

## 类和方法说明
- `RenderCompleteSoundProperties`：插件的属性组，包含声音文件路径的设置。
- `RenderCompleteSoundPreferences`：插件的偏好设置，允许指定默认声音文件路径。
- `BrowseSoundFileOperator`：操作符，用于浏览并选择声音文件。
- `TestSoundFileOperator`：操作符，用于测试选择的声音文件。
- `StopSoundFileOperator`：操作符，用于停止正在播放的声音。
- `ResetSoundFileOperator`：操作符，用于重置声音文件路径为默认值。
- `RenderCompleteSoundPanel`：插件的用户界面面板，用于展示设置。
- `play_sound_on_render_complete`：渲染完成后播放声音的函数。
- `load_handler`：确保在加载文件时正确设置渲染完成回调。

## 许可证
该插件遵循MIT许可证。