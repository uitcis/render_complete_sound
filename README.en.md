

# Render Complete Sound Plugin

## Introduction
This is a plugin designed for Blender that allows playing a custom sound upon completion of rendering.

## Features
- Play a specified sound file when rendering is complete.
- Allow users to set a default sound file path through preferences.
- Provide operators for testing, stopping, and resetting the sound file.

## Usage
1. Install the plugin.
2. Locate the plugin settings in Blender's user interface.
3. Set the path to the sound file you want to play upon rendering completion.
4. Start rendering, and you will hear the sound when it's done.

## Class and Method Description
- `RenderCompleteSoundProperties`: The plugin's property group, containing the setting for the sound file path.
- `RenderCompleteSoundPreferences`: The plugin's preferences class, allowing users to specify the default sound file path.
- `BrowseSoundFileOperator`: Operator used to browse and select a sound file.
- `TestSoundFileOperator`: Operator used to test the selected sound file.
- `StopSoundFileOperator`: Operator used to stop the currently playing sound.
- `ResetSoundFileOperator`: Operator used to reset the sound file path to its default.
- `RenderCompleteSoundPanel`: The user interface panel of the plugin, displaying the settings.
- `play_sound_on_render_complete`: Function that plays the sound upon rendering completion.
- `load_handler`: Ensures the render complete callback is correctly set when loading a file.

## License
This plugin is released under the MIT License.