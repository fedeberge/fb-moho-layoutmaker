'''
TODO

que lea el tipo de marker, chapter es una nueva escena


que lea la cantidad de escenas y defina el padding necesario para los numeros
idem para los planos

chequear si string_a_time funciona cuando esta solo en frames

dividir consolidarMarcadores en differentes funciones con un solo proposito

que guardarXML suceda cuando no hay audio
evaluar si tiene sentido guardar en xml

errores de buscarExtension():
    error si no hay ningun archivo compatible
    error si hay mas de un archivo compatible

    capaz es mejor que sea una funcion que corre una vez y guarda los archivos en un dictionary, asi no tieen que correr otra vez para los audios
    seria leerCarpeta

'''
import cv2 as cv
import csv, sys, os, ffmpeg, shutil, json
import xml.etree.ElementTree as ET
from pathlib import Path, PurePath
from mutagen.mp4 import MP4
from zipfile import ZipFile
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

mohoBase = """
{
    "mime_type": "application/x-vnd.lm_mohodoc",
    "version": 1041,
    "major_version": 1,
    "rev_version": 0,
    "comment": "",
    "doc_uuid": "acbc3243-417a-4198-ae9d-694d51da45ba",
    "created_date": "Mon Jun 24 03:31:39 2024",
    "modified_date": "Mon Jun 24 16:21:29 2024",
    "project_data": {
      "width": 1920,
      "height": 1080,
      "start_frame": 1,
      "end_frame": 240,
      "fps": 24.0,
      "back_color": { "r": 234, "g": 234, "b": 234, "a": 255 },
      "display_quality": 28670,
      "noise_grain": 0,
      "pixelation": 0,
      "antialiasing": true,
      "depth_sort": false,
      "distance_sort": false,
      "depth_of_field": false,
      "focus_distance": 2.0,
      "focus_range": 1.0,
      "focus_blur": 0.016481,
      "global_render_style_fill_style": 0,
      "global_render_style_line_style": 0,
      "global_render_style_layer_style": 0,
      "global_render_style_minimize_randomness": true,
      "stereo_mode": 0,
      "stereo_separation": -1.0,
      "extra_swf_frame": false,
      "color_palette": "",
      "soundtrack": ""
    },
    "thumbnail": "",
    "styles": [
      {
        "type": "Style",
        "name": "Wet Ink",
        "uuid": "2df8624e-ac67-4de2-b214-f42977cd8626",
        "define_fill_color": false,
        "fill_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "define_line_width": false,
        "line_width": 0.022222,
        "define_line_col": false,
        "line_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "line_caps": 1,
        "brush_name": "Brush503.png",
        "brush_align": true,
        "brush_jitter": 6.195919,
        "brush_spacing": 0.43,
        "brush_angle_drift": 0.0,
        "brush_randomize": false,
        "brush_merged_alpha": false,
        "brush_tint": true,
        "brush_rand_order": false,
        "brush_size_amp": 0.14,
        "brush_size_scale": 0.03,
        "brush_random_interval": 1
      },
      {
        "type": "Style",
        "name": "Light Charcoal",
        "uuid": "59128913-5055-4425-988a-bcc14524ed53",
        "define_fill_color": false,
        "fill_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "define_line_width": false,
        "line_width": 0.013889,
        "define_line_col": false,
        "line_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "line_caps": 1,
        "brush_name": "Brush002",
        "brush_align": true,
        "brush_jitter": 6.283185,
        "brush_spacing": 0.34,
        "brush_angle_drift": 0.0,
        "brush_randomize": false,
        "brush_merged_alpha": false,
        "brush_tint": true,
        "brush_rand_order": true,
        "brush_size_amp": 0.23,
        "brush_size_scale": 0.2,
        "brush_random_interval": 1
      },
      {
        "type": "Style",
        "name": "Chisel Tip Marker",
        "uuid": "68c90036-44fb-4c28-9991-01b1259aee37",
        "define_fill_color": false,
        "fill_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "define_line_width": false,
        "line_width": 0.017223,
        "define_line_col": false,
        "line_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "line_caps": 1,
        "brush_name": "Brush509_0_0_0.png",
        "brush_align": false,
        "brush_jitter": 0.0,
        "brush_spacing": 0.0,
        "brush_angle_drift": 0.261799,
        "brush_randomize": false,
        "brush_merged_alpha": true,
        "brush_tint": true,
        "brush_rand_order": false,
        "brush_size_amp": 0.0,
        "brush_size_scale": 0.3,
        "brush_random_interval": 1
      },
      {
        "type": "Style",
        "name": "Strong Charcoal",
        "uuid": "e9a62b2e-4c98-4958-9d9b-e83362417fd6",
        "define_fill_color": false,
        "fill_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "define_line_width": false,
        "line_width": 0.005556,
        "define_line_col": false,
        "line_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "line_caps": 1,
        "brush_name": "CK Ink DIFF SMASHER.png",
        "brush_align": true,
        "brush_jitter": 6.283185,
        "brush_spacing": 0.36,
        "brush_angle_drift": 0.0,
        "brush_randomize": false,
        "brush_merged_alpha": false,
        "brush_tint": true,
        "brush_rand_order": false,
        "brush_size_amp": 0.64,
        "brush_size_scale": 0.07,
        "brush_random_interval": 1
      },
      {
        "type": "Style",
        "name": "Dry Pencil",
        "uuid": "edaf34f9-4c8e-42ad-85a4-aa213ba000f8",
        "define_fill_color": false,
        "fill_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "define_line_width": false,
        "line_width": 0.005556,
        "define_line_col": false,
        "line_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "line_caps": 1,
        "brush_name": "CK Sketch Sponge m.png",
        "brush_align": true,
        "brush_jitter": 6.283185,
        "brush_spacing": 0.69,
        "brush_angle_drift": 0.0,
        "brush_randomize": false,
        "brush_merged_alpha": false,
        "brush_tint": true,
        "brush_rand_order": true,
        "brush_size_amp": 0.27,
        "brush_size_scale": 0.17,
        "brush_random_interval": 1
      },
      {
        "type": "Style",
        "name": "Light Pastel",
        "uuid": "fba7636e-7585-4301-b7be-9b18255faf50",
        "define_fill_color": false,
        "fill_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "define_line_width": false,
        "line_width": 0.022222,
        "define_line_col": false,
        "line_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "line_caps": 1,
        "brush_name": "Brush571_0_0_35.png",
        "brush_align": false,
        "brush_jitter": 2.530727,
        "brush_spacing": 0.5,
        "brush_angle_drift": 0.0,
        "brush_randomize": false,
        "brush_merged_alpha": false,
        "brush_tint": true,
        "brush_rand_order": false,
        "brush_size_amp": 0.11,
        "brush_size_scale": 0.05,
        "brush_random_interval": 1
      },
      {
        "type": "Style",
        "name": "Pastel",
        "uuid": "f6885f39-301f-4236-b8cc-4069f1db0a7b",
        "define_fill_color": false,
        "fill_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "define_line_width": false,
        "line_width": 0.022222,
        "define_line_col": false,
        "line_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "line_caps": 1,
        "brush_name": "Brush560_0_270_55.png",
        "brush_align": true,
        "brush_jitter": 3.839724,
        "brush_spacing": 0.46,
        "brush_angle_drift": 0.0,
        "brush_randomize": false,
        "brush_merged_alpha": false,
        "brush_tint": true,
        "brush_rand_order": true,
        "brush_size_amp": 0.27,
        "brush_size_scale": 0.14,
        "brush_random_interval": 1
      },
      {
        "type": "Style",
        "name": "Gouache",
        "uuid": "a617b58c-eb8a-451a-bbf5-ec3c5b1d702e",
        "define_fill_color": false,
        "fill_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "define_line_width": false,
        "line_width": 0.010556,
        "define_line_col": false,
        "line_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "line_caps": 1,
        "brush_name": "MC-Chunky.mohobrush",
        "brush_align": true,
        "brush_jitter": 0.0,
        "brush_spacing": 0.5,
        "brush_angle_drift": 0.0,
        "brush_randomize": false,
        "brush_merged_alpha": false,
        "brush_tint": true,
        "brush_rand_order": true,
        "brush_size_amp": 0.7,
        "brush_size_scale": 0.1,
        "brush_random_interval": 1
      },
      {
        "type": "Style",
        "name": "Rough Ink",
        "uuid": "992fbed9-0e7a-4783-b8a4-d40622fd1019",
        "define_fill_color": false,
        "fill_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "define_line_width": false,
        "line_width": 0.008889,
        "define_line_col": false,
        "line_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "line_caps": 1,
        "brush_name": "CK Ink Scratch_1_0_0_1_1_0_0_1",
        "brush_align": true,
        "brush_jitter": 0.0,
        "brush_spacing": 0.0,
        "brush_angle_drift": 0.0,
        "brush_randomize": false,
        "brush_merged_alpha": false,
        "brush_tint": true,
        "brush_rand_order": true,
        "brush_size_amp": 0.26,
        "brush_size_scale": 0.0,
        "brush_random_interval": 1
      },
      {
        "type": "Style",
        "name": "Watercolor",
        "uuid": "1ad12149-b514-4f0f-b2d1-4d0f796d30b8",
        "define_fill_color": false,
        "fill_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "define_line_width": false,
        "line_width": 0.012222,
        "define_line_col": false,
        "line_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 0.105882, "g": 0.235294, "b": 0.717647, "a": 0.180392 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "line_caps": 1,
        "brush_name": "CK Ink Waterstroke_1_0_0_0_0_0_0_0.png",
        "brush_align": true,
        "brush_jitter": 0.0,
        "brush_spacing": 0.0,
        "brush_angle_drift": 0.0,
        "brush_randomize": true,
        "brush_merged_alpha": false,
        "brush_tint": true,
        "brush_rand_order": false,
        "brush_size_amp": 0.28,
        "brush_size_scale": 0.05,
        "brush_random_interval": 1
      },
      {
        "type": "Style",
        "name": "Dark Core",
        "uuid": "263df108-e0a6-4acd-9acf-fa5167348812",
        "define_fill_color": false,
        "fill_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "define_line_width": false,
        "line_width": 0.005556,
        "define_line_col": false,
        "line_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "line_caps": 1,
        "brush_name": "Spray.mohobrush",
        "brush_align": false,
        "brush_jitter": 6.283185,
        "brush_spacing": 0.19,
        "brush_angle_drift": 0.0,
        "brush_randomize": false,
        "brush_merged_alpha": false,
        "brush_tint": true,
        "brush_rand_order": false,
        "brush_size_amp": 0.25,
        "brush_size_scale": 0.12,
        "brush_random_interval": 1
      },
      {
        "type": "Style",
        "name": "Dark Core Soft",
        "uuid": "89a6b32d-49f6-4888-acad-6fb5ea057151",
        "define_fill_color": false,
        "fill_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "define_line_width": false,
        "line_width": 0.092223,
        "define_line_col": false,
        "line_color": {
          "type": "Color",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0 }],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 0, "h": 0, "s": false, "t": 0 }
          ]
        },
        "line_caps": 1,
        "brush_name": "Dots.mohobrush",
        "brush_align": false,
        "brush_jitter": 6.195919,
        "brush_spacing": 0.17,
        "brush_angle_drift": 0.0,
        "brush_randomize": false,
        "brush_merged_alpha": false,
        "brush_tint": true,
        "brush_rand_order": false,
        "brush_size_amp": 0.38,
        "brush_size_scale": 0.03,
        "brush_random_interval": 1
      }
    ],
    "layercomps": [],
    "onions_enabled": false,
    "onions_sellayer": true,
    "onions_filled": false,
    "onions_colored": false,
    "onions_relative": true,
    "onions_behind": false,
    "onions_frame0": -100000,
    "onions_frame1": -100000,
    "onions_frame2": -100000,
    "onions_frame3": -100000,
    "onions_frame4": -100000,
    "onions_frame5": -100000,
    "onions_frame6": -100000,
    "onions_frame7": -100000,
    "metadata": { "what": 0, "layerwnd_searchcontext": 5078, "save_time": 0 },
    "action_refs": [],
    "animated_values": {
      "camera_track": {
        "type": "Vec3",
        "ref": false,
        "mute": false,
        "when": [0],
        "val": [{ "x": 0.0, "y": 0.0, "z": 3.732051 }],
        "interp": [
          { "im": 1, "v1": 0.1, "v2": 0.5, "in": 1, "h": 0, "s": false, "t": 0 }
        ]
      },
      "camera_zoom": {
        "type": "Val",
        "ref": false,
        "mute": false,
        "when": [0],
        "val": [2.0],
        "interp": [
          { "im": 1, "v1": 0.1, "v2": 0.5, "in": 1, "h": 0, "s": false, "t": 0 }
        ]
      },
      "camera_roll": {
        "type": "Val",
        "ref": false,
        "mute": false,
        "when": [0],
        "val": [0.0],
        "interp": [
          { "im": 1, "v1": 0.1, "v2": 0.5, "in": 1, "h": 0, "s": false, "t": 0 }
        ]
      },
      "camera_pan_tilt": {
        "type": "Vec2",
        "ref": false,
        "mute": false,
        "when": [0],
        "val": [{ "x": 0.0, "y": 0.0 }],
        "interp": [
          { "im": 1, "v1": 0.1, "v2": 0.5, "in": 1, "h": 0, "s": false, "t": 0 }
        ]
      },
      "timeline_markers": {
        "type": "String",
        "ref": false,
        "mute": false,
        "when": [-1000000],
        "val": [""],
        "interp": [
          { "im": 1, "v1": 0.1, "v2": 0.5, "in": 1, "h": 0, "s": false, "t": 0 }
        ]
      }
    },
    "layers": [
      {
        "type": "SwitchLayer",
        "expanded": true,
        "frame_by_frame": false,
        "previewAlignment": 0,
        "switch_data": "",
        "switch_interpolation": false,
        "switch_keys": {
          "type": "String",
          "ref": false,
          "mute": false,
          "when": [0],
          "val": ["05-040.mp4"],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 1, "h": 0, "s": false, "t": 0 }
          ]
        },
        "skeleton": {
          "type": "Skeleton",
          "binding_mode": 1,
          "bones": [],
          "bones_groups": []
        },
        "layers": [
          {
            "type": "ImageLayer",
            "image_fileref": {
              "relativeTo": "Project",
              "path": "202-animation/05/assets/05-040.mp4"
            },
            "image_path": "202-animation/05/assets/05-040.mp4",
            "psd_layerid": -2,
            "psd_layer_identifier": "",
            "psd_trim_alpha": true,
            "modification_date": 1719212723,
            "quality_level": 1,
            "interpreted_fps": 24.0,
            "avi_alpha": false,
            "movie_looping": false,
            "reverse_movie": false,
            "persist_first_frame": false,
            "persist_last_frame": false,
            "toon_effect": false,
            "toon_min_edge_threshold": 216,
            "toon_max_edge_threshold": 220,
            "toon_gray_threshold": 96,
            "toon_black_threshold": 32,
            "toon_saturation": 60,
            "toon_lightness": 0,
            "toon_quantize": 6,
            "sampling_mode": 1,
            "premultiplied_movie": false,
            "psd_layer_bounds": { "top": 0, "left": 0, "right": 0, "bottom": 0 },
            "psd_layer_translation": { "x": 1000000.0, "y": 1000000.0 },
            "width": 3.555556,
            "height": 2.0,
            "image_cropped": false,
            "audio_fileref": {
              "relativeTo": "Project",
              "path": "202-animation/05/assets/05-040.mp4"
            },
            "audio_path": "202-animation/05/assets/05-040.mp4",
            "spatial_positioning": false,
            "audio_level": {
              "type": "Val",
              "ref": false,
              "mute": false,
              "when": [0],
              "val": [1.0],
              "interp": [
                {
                  "im": 1,
                  "v1": 0.1,
                  "v2": 0.5,
                  "in": 1,
                  "h": 0,
                  "s": false,
                  "t": 0
                }
              ]
            },
            "audio_jump": {
              "type": "Val",
              "ref": false,
              "mute": false,
              "when": [0],
              "val": [0.0],
              "interp": [
                {
                  "im": 1,
                  "v1": 0.1,
                  "v2": 0.5,
                  "in": 1,
                  "h": 0,
                  "s": false,
                  "t": 0
                }
              ]
            },
            "name": "05-040.mp4",
            "uuid": "f55b12f9-f762-4322-821f-c56050c1519c",
            "label_col": 0,
            "quality_flags": 12286,
            "animated_layer_effects": false,
            "origin": { "x": 0.0, "y": 0.0 },
            "parent_bone": -3,
            "visible": true,
            "shown_in_timeline": false,
            "consolidated_channels": false,
            "render_only": false,
            "edit_only": false,
            "ignored_by_layer_picker": false,
            "scale_compensation": true,
            "scale_normalization": 1.0,
            "rotate_to_follow": false,
            "face_camera": false,
            "face_camera_mode": 2,
            "masking": 0,
            "mask_expansion": false,
            "blend_mode": 0,
            "camera_immune": false,
            "dof_immune": false,
            "layer_ref_uuid": "",
            "layer_ref_fileref": { "relativeTo": "Absolute", "path": "" },
            "layer_ref_path": "",
            "layer_ref_same_doc": false,
            "layer_ref_mod_date": 0,
            "flexi_bone_subset": "",
            "flexi_bone_elbow": false,
            "timing_offset": 0,
            "follow_layer_uuid": "",
            "follow_curve": -1,
            "follow_bending": false,
            "distortion_layer_uuid": "",
            "random_num": 29838,
            "transforms": {
              "translation": {
                "type": "Vec3",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "x": 0.0, "y": 0.0, "z": 0.0 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "scale": {
                "type": "Vec3",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "x": 1.0, "y": 1.0, "z": 1.0 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "rotation_x": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "rotation_y": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "rotation_z": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "flip_h": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "flip_v": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "shear": {
                "type": "Vec3",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "x": 0.0, "y": 0.0, "z": 0.0 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "following": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "physics_nudge": {
                "type": "Vec2",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "x": 0.0, "y": 0.0 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              }
            },
            "layer_effects": {
              "visibility": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [true],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "blur": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "alpha": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [1.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "ambient_occlusion": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "threshold": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "noise": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "pixelation": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              }
            },
            "layer_shadow": {
              "on": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "angle": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [5.497787],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "offset": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.033333],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "blur": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.016667],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "expansion": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "color": {
                "type": "Color",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 0.501961 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "noise_amp": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "noise_scale": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [64.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "threshold": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "clip_to_group": false
            },
            "layer_shading": {
              "on": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "angle": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [5.497787],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "offset": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.033333],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "blur": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.066667],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "contraction": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "color": {
                "type": "Color",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 0.501961 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "noise_amp": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "noise_scale": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [64.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "threshold": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              }
            },
            "perspective_shadow": {
              "on": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "blur": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.012346],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "scale": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [1.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "shear": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "color": {
                "type": "Color",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 0.501961 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "threshold": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              }
            },
            "motion_blur": {
              "on": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "sub_frames": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [true],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "frames": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [20.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "skip": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [1.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "alpha_start": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.3],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "alpha_end": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.1],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "radius": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.008333],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "frame_percentage": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [1.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "extended_frames": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              }
            },
            "layer_outline": {
              "on": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "width": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.004115],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "color": {
                "type": "Color",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              }
            },
            "layer_color": {
              "on": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "color": {
                "type": "Color",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              }
            },
            "timeline_markers": {
              "type": "String",
              "ref": false,
              "mute": false,
              "when": [-1000000],
              "val": [""],
              "interp": [
                {
                  "im": 1,
                  "v1": 0.1,
                  "v2": 0.5,
                  "in": 1,
                  "h": 0,
                  "s": false,
                  "t": 0
                }
              ]
            },
            "physics": {
              "enabled": true,
              "static": false,
              "sleeping": false,
              "respawn": 0,
              "velocity": { "x": 0.0, "y": 0.0 },
              "density": 1.0,
              "friction": 0.3,
              "restitution": 0.5,
              "pivot": false,
              "enable_motor": false,
              "motor_speed": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [3.141593],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "motor_torque": 10000.0,
              "force_field": false,
              "force_field_vector": {
                "type": "Vec2",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "x": 0.0, "y": 1.0 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              }
            },
            "layer_user_comments": "",
            "layer_user_tags": ""
          },
          {
            "type": "AudioLayer",
            "audio_fileref": {
              "relativeTo": "Project",
              "path": "202-animation/02/assets/05-040.wav"
            },
            "audio_path": "202-animation/02/assets/05-040.wav",
            "spatial_positioning": false,
            "audio_level": {
              "type": "Val",
              "ref": false,
              "mute": false,
              "when": [0],
              "val": [1.0],
              "interp": [
                {
                  "im": 1,
                  "v1": 0.1,
                  "v2": 0.5,
                  "in": 1,
                  "h": 0,
                  "s": false,
                  "t": 0
                }
              ]
            },
            "audio_jump": {
              "type": "Val",
              "ref": false,
              "mute": false,
              "when": [0],
              "val": [0.0],
              "interp": [
                {
                  "im": 1,
                  "v1": 0.1,
                  "v2": 0.5,
                  "in": 1,
                  "h": 0,
                  "s": false,
                  "t": 0
                }
              ]
            },
            "audio_text": "",
            "name": "05-040.wav",
            "uuid": "7e1f7b97-891b-4f2a-a3c4-1d115fa786c3",
            "label_col": 0,
            "quality_flags": 12286,
            "animated_layer_effects": false,
            "origin": { "x": 0.0, "y": 0.0 },
            "parent_bone": -1,
            "visible": true,
            "shown_in_timeline": false,
            "consolidated_channels": false,
            "render_only": false,
            "edit_only": false,
            "ignored_by_layer_picker": false,
            "scale_compensation": true,
            "scale_normalization": 1.0,
            "rotate_to_follow": false,
            "face_camera": false,
            "face_camera_mode": 2,
            "masking": 0,
            "mask_expansion": false,
            "blend_mode": 0,
            "camera_immune": false,
            "dof_immune": false,
            "layer_ref_uuid": "",
            "layer_ref_fileref": { "relativeTo": "Absolute", "path": "" },
            "layer_ref_path": "",
            "layer_ref_same_doc": false,
            "layer_ref_mod_date": 0,
            "flexi_bone_subset": "",
            "flexi_bone_elbow": false,
            "timing_offset": 0,
            "follow_layer_uuid": "",
            "follow_curve": -1,
            "follow_bending": false,
            "distortion_layer_uuid": "",
            "random_num": 12201,
            "transforms": {
              "translation": {
                "type": "Vec3",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "x": 0.0, "y": 0.0, "z": 0.0 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "scale": {
                "type": "Vec3",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "x": 1.0, "y": 1.0, "z": 1.0 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "rotation_x": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "rotation_y": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "rotation_z": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "flip_h": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "flip_v": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "shear": {
                "type": "Vec3",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "x": 0.0, "y": 0.0, "z": 0.0 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "following": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "physics_nudge": {
                "type": "Vec2",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "x": 0.0, "y": 0.0 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              }
            },
            "layer_effects": {
              "visibility": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [true],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "blur": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "alpha": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [1.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "ambient_occlusion": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "threshold": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "noise": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "pixelation": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              }
            },
            "layer_shadow": {
              "on": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "angle": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [5.497787],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "offset": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.033333],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "blur": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.016667],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "expansion": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "color": {
                "type": "Color",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 0.501961 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "noise_amp": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "noise_scale": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [64.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "threshold": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "clip_to_group": false
            },
            "layer_shading": {
              "on": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "angle": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [5.497787],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "offset": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.033333],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "blur": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.066667],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "contraction": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "color": {
                "type": "Color",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 0.501961 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "noise_amp": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "noise_scale": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [64.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "threshold": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              }
            },
            "perspective_shadow": {
              "on": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "blur": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.012346],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "scale": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [1.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "shear": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "color": {
                "type": "Color",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 0.501961 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "threshold": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              }
            },
            "motion_blur": {
              "on": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "sub_frames": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [true],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "frames": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [20.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "skip": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [1.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "alpha_start": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.3],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "alpha_end": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.1],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "radius": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.008333],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "frame_percentage": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [1.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "extended_frames": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.0],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              }
            },
            "layer_outline": {
              "on": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "width": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [0.004115],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "color": {
                "type": "Color",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              }
            },
            "layer_color": {
              "on": {
                "type": "Bool",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [false],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "color": {
                "type": "Color",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              }
            },
            "timeline_markers": {
              "type": "String",
              "ref": false,
              "mute": false,
              "when": [-1000000],
              "val": [""],
              "interp": [
                {
                  "im": 1,
                  "v1": 0.1,
                  "v2": 0.5,
                  "in": 1,
                  "h": 0,
                  "s": false,
                  "t": 0
                }
              ]
            },
            "physics": {
              "enabled": true,
              "static": false,
              "sleeping": false,
              "respawn": 0,
              "velocity": { "x": 0.0, "y": 0.0 },
              "density": 1.0,
              "friction": 0.3,
              "restitution": 0.5,
              "pivot": false,
              "enable_motor": false,
              "motor_speed": {
                "type": "Val",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [3.141593],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              },
              "motor_torque": 10000.0,
              "force_field": false,
              "force_field_vector": {
                "type": "Vec2",
                "ref": false,
                "mute": false,
                "when": [0],
                "val": [{ "x": 0.0, "y": 1.0 }],
                "interp": [
                  {
                    "im": 1,
                    "v1": 0.1,
                    "v2": 0.5,
                    "in": 1,
                    "h": 0,
                    "s": false,
                    "t": 0
                  }
                ]
              }
            },
            "layer_user_comments": "",
            "layer_user_tags": ""
          }
        ],
        "name": "animatic",
        "uuid": "34000130-6335-487f-a14c-6d14181046f8",
        "label_col": 0,
        "quality_flags": 12286,
        "animated_layer_effects": false,
        "origin": { "x": 0.0, "y": 0.0 },
        "parent_bone": -1,
        "visible": true,
        "shown_in_timeline": false,
        "consolidated_channels": false,
        "render_only": false,
        "edit_only": false,
        "ignored_by_layer_picker": false,
        "scale_compensation": true,
        "scale_normalization": 1.0,
        "rotate_to_follow": false,
        "face_camera": false,
        "face_camera_mode": 2,
        "masking": 0,
        "mask_expansion": false,
        "blend_mode": 0,
        "camera_immune": false,
        "dof_immune": false,
        "layer_ref_uuid": "",
        "layer_ref_fileref": { "relativeTo": "Absolute", "path": "" },
        "layer_ref_path": "",
        "layer_ref_same_doc": false,
        "layer_ref_mod_date": 0,
        "flexi_bone_subset": "",
        "flexi_bone_elbow": false,
        "timing_offset": 0,
        "follow_layer_uuid": "",
        "follow_curve": -1,
        "follow_bending": false,
        "distortion_layer_uuid": "",
        "random_num": 4251,
        "transforms": {
          "translation": {
            "type": "Vec3",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [{ "x": 0.0, "y": 0.0, "z": 0.0 }],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "scale": {
            "type": "Vec3",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [{ "x": 1.0, "y": 1.0, "z": 1.0 }],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "rotation_x": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "rotation_y": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "rotation_z": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "flip_h": {
            "type": "Bool",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [false],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "flip_v": {
            "type": "Bool",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [false],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "shear": {
            "type": "Vec3",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [{ "x": 0.0, "y": 0.0, "z": 0.0 }],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "following": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "physics_nudge": {
            "type": "Vec2",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [{ "x": 0.0, "y": 0.0 }],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          }
        },
        "layer_effects": {
          "visibility": {
            "type": "Bool",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [true],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "blur": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "alpha": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [1.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "ambient_occlusion": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "threshold": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "noise": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "pixelation": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          }
        },
        "layer_shadow": {
          "on": {
            "type": "Bool",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [false],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "angle": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [5.497787],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "offset": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.033333],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "blur": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.016667],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "expansion": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "color": {
            "type": "Color",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 0.501961 }],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "noise_amp": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "noise_scale": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [64.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "threshold": {
            "type": "Bool",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [false],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "clip_to_group": false
        },
        "layer_shading": {
          "on": {
            "type": "Bool",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [false],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "angle": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [5.497787],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "offset": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.033333],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "blur": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.066667],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "contraction": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "color": {
            "type": "Color",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 0.501961 }],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "noise_amp": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "noise_scale": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [64.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "threshold": {
            "type": "Bool",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [false],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          }
        },
        "perspective_shadow": {
          "on": {
            "type": "Bool",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [false],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "blur": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.012346],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "scale": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [1.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "shear": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "color": {
            "type": "Color",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 0.501961 }],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "threshold": {
            "type": "Bool",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [false],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          }
        },
        "motion_blur": {
          "on": {
            "type": "Bool",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [false],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "sub_frames": {
            "type": "Bool",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [true],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "frames": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [20.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "skip": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [1.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "alpha_start": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.3],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "alpha_end": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.1],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "radius": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.008333],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "frame_percentage": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [1.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "extended_frames": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.0],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          }
        },
        "layer_outline": {
          "on": {
            "type": "Bool",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [false],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "width": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [0.004115],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "color": {
            "type": "Color",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0 }],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          }
        },
        "layer_color": {
          "on": {
            "type": "Bool",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [false],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "color": {
            "type": "Color",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [{ "r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0 }],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          }
        },
        "timeline_markers": {
          "type": "String",
          "ref": false,
          "mute": false,
          "when": [-1000000],
          "val": [""],
          "interp": [
            { "im": 1, "v1": 0.1, "v2": 0.5, "in": 1, "h": 0, "s": false, "t": 0 }
          ]
        },
        "physics": {
          "enabled": true,
          "static": false,
          "sleeping": false,
          "respawn": 0,
          "velocity": { "x": 0.0, "y": 0.0 },
          "density": 1.0,
          "friction": 0.3,
          "restitution": 0.5,
          "pivot": false,
          "enable_motor": false,
          "motor_speed": {
            "type": "Val",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [3.141593],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          },
          "motor_torque": 10000.0,
          "force_field": false,
          "force_field_vector": {
            "type": "Vec2",
            "ref": false,
            "mute": false,
            "when": [0],
            "val": [{ "x": 0.0, "y": 1.0 }],
            "interp": [
              {
                "im": 1,
                "v1": 0.1,
                "v2": 0.5,
                "in": 1,
                "h": 0,
                "s": false,
                "t": 0
              }
            ]
          }
        },
        "layer_user_comments": "",
        "layer_user_tags": ""
      }
    ],
    "documentviewstate": {
      "DocState_viewportSetting": 1,
      "DocState_gridOn": false,
      "DocState_gridStyle": 0,
      "DocState_gridSize": 20,
      "DocState_gridSnappingOn": true,
      "DocState_showOutputOnly": false,
      "DocState_showVideoSafeZones": false,
      "DocState_showRuleOfThirds": false,
      "DocState_viewPortLeftWidthPct": 1.0,
      "DocState_viewPortTopWidthPct": 1.0,
      "DocState_zoom0": 0.63701,
      "DocState_viewOffset0": { "x": 0.048904, "y": -0.067194 },
      "DocState_rotation0": 0.0,
      "DocState_stereo0": false,
      "DocState_enableOutsideView0": false,
      "DocState_outsideViewPitch0": 0.0,
      "DocState_outsideViewYaw0": 0.0,
      "DocState_outsideViewRadius0": 0.0,
      "DocState_outsideViewAttn0": { "x": 0.0, "y": 0.0, "z": 0.0 },
      "DocState_zoom1": 0.0,
      "DocState_viewOffset1": { "x": 0.0, "y": 0.0 },
      "DocState_rotation1": 0.0,
      "DocState_stereo1": false,
      "DocState_enableOutsideView1": false,
      "DocState_outsideViewPitch1": 0.0,
      "DocState_outsideViewYaw1": 0.0,
      "DocState_outsideViewRadius1": 0.0,
      "DocState_outsideViewAttn1": { "x": 0.0, "y": 0.0, "z": 0.0 },
      "DocState_zoom2": 0.0,
      "DocState_viewOffset2": { "x": 0.0, "y": 0.0 },
      "DocState_rotation2": 0.0,
      "DocState_stereo2": false,
      "DocState_enableOutsideView2": false,
      "DocState_outsideViewPitch2": 0.0,
      "DocState_outsideViewYaw2": 0.0,
      "DocState_outsideViewRadius2": 0.0,
      "DocState_outsideViewAttn2": { "x": 0.0, "y": 0.0, "z": 0.0 },
      "DocState_zoom3": 0.0,
      "DocState_viewOffset3": { "x": 0.0, "y": 0.0 },
      "DocState_rotation3": 0.0,
      "DocState_stereo3": false,
      "DocState_enableOutsideView3": false,
      "DocState_outsideViewPitch3": 0.0,
      "DocState_outsideViewYaw3": 0.0,
      "DocState_outsideViewRadius3": 0.0,
      "DocState_outsideViewAttn3": { "x": 0.0, "y": 0.0, "z": 0.0 },
      "DocState_playStart": -1,
      "DocState_playEnd": -1
    }
  }
  
"""

#todo definir clases proyecto (duracion, escenas, marcadores, video)
class Marker:
    #todo ver como usar el comment para entender que tipo de Marker es
    def __init__(self,id, scene, shot, letter = "a", startCsv=0,fps=24):
        self.id = id
        self.scene = scene
        self.shot = shot
        self.letter = letter
        self.start = self.setStart(startCsv, fps)
        self.duration = 0
        self.partialDuration = 0
        self.complete = True

    def __str__(self):
        global videoIn
        numScenes = videoIn.numScenes
        numShots = videoIn.numShots
        padScenes = len(str(numScenes))
        padShots = len(str(numShots))
        shot= str(self.scene).zfill(padScenes)+"-"+str(self.shot).zfill(padShots)
        return shot
    
    def appendLetter(self):
        shotName = str(self)
        if self.complete:
            return shotName
        else:
            return shotName + self.letter

    #todo chequear si anda con frames
    def setStart(self,startCsv, fps):
        if ";" in startCsv:
            startCsv = startCsv.split(";")
        elif ":" in startCsv:
            startCsv = startCsv.split(":")
        
        if len(startCsv) == 4:
            _,minutos,segundos,frames = startCsv
            frames=int(frames)
            segundos=int(segundos)
            minutos=int(minutos)
            segundos+=minutos*60
            frames+=segundos*24
        else:
            frames = int(startCsv[0])
        return (frames)/fps

class Video:
    def __init__(self, csvIn, animaticIn):
        self.name = csvIn.split("-")[0]
        self.csvIn = csvIn
        self.animaticIn = animaticIn
        self.duration = LayoutMarker.calculateSupportedDuration(animaticIn)
        self.fps = 24 #todo, con mutagen?
        self.markers = []
        self.scenes = {}
        self.numScenes = 1
        self.numShots = 1

    def countScenes (self):
        self.numScenes = len(self.scenes.keys())
    
    #todo testear
    def consolidateScenes (self): 
        abc="abcdefghijklmnopqrstuvwxyz"
        rep = "b"
        tempScenes = [self.scenes[0][0]]
        for i in range(1,len(self.scenes.keys())):
            if self.scenes[i][0] not in tempScenes and int(self.scenes[i][0]) > int(tempScenes[i-1]):
                tempScenes.append(self.scenes[i][0])    
                rep="b"
            else:
                prevScene = tempScenes[-1]
                if prevScene[-1].isdigit():
                    self.scenes[i][0] = prevScene + rep
                else:
                    self.scenes[i][0] = prevScene[-1] + abc[abc.find(rep)+1]
                    rep = self.scenes[i][0][-1]
                tempScenes.append(self.scenes[i][0])
        
        for i in range(len(self.scenes.keys())):
            currentScene = self.scenes[i][0]
            currentSceneMarkersIds = self.scenes[i][1]
            for currentSceneMarkerId in currentSceneMarkersIds:
                for marker in self.markers:
                    if marker.id == currentSceneMarkerId:
                        marker.scene = currentScene
        self.countScenes()

    def countShots (self):
        self.numShots = len([marker for marker in self.markers if marker.letter == "a"])

    def getPadScenes(self):
        return len(str(self.numScenes))
    
    def getPadShots(self):
        return len(str(self.numShots))

    def calculateDurations(self):
        for i, marker in enumerate(self.markers[:-1]):
            marker.partialDuration = self.markers[i+1].start - marker.start
        self.markers[-1].partialDuration = self.duration - self.markers[-1].start

    def consolidateMarkers(self):
        for i, marker in enumerate(self.markers):
            if marker.letter == "a":
                marker.duration = marker.partialDuration
                j = i+1
                if j <len(self.markers)-1:
                    while self.markers[j].letter != "a":
                        marker.duration+=self.markers[j].partialDuration
                        j+=1
        
        for i, marker in enumerate(self.markers):
            abc = "abcdefghijklmnopqrstuvwxyz"
            if marker.letter != "a":
                currentLetter = abc[abc.find(self.markers[i-1].letter)+1]
                marker.letter = currentLetter
                marker.complete = False
                self.markers[i-1].complete = False
        self.countShots()

    def readCSV(self):
        lastMarker = 0
        latestScene = 1
        shotId=0
        sceneId=0
        with open(self.csvIn, encoding="utf-16") as csvFile:
            csvReader = csv.DictReader(csvFile, delimiter="\t")
            for row in csvReader:
                currentName = row["Marker Name"]
                currentIn = row["In"]
                
                if currentName.isdigit():
                    if latestScene != int(currentName):
                        latestScene = int(currentName)
                        sceneId+=1
                    self.scenes[sceneId] = (latestScene,[])
                if currentName != "m":
                    lastMarker +=1
                    currentMarker = Marker(shotId,latestScene, lastMarker, startCsv = currentIn)
                elif currentName =="m":
                    currentMarker = Marker(shotId,latestScene,lastMarker,"m",currentIn)
                self.markers.append(currentMarker)
                self.scenes[sceneId][1].append(shotId)
                shotId+=1

    def writeXML(self):
        root = ET.Element("xml")
        general = ET.SubElement(root, "general")
        ET.SubElement(general, "version").text ="1"

        layers= ET.SubElement(root,"layers")
        layer=ET.SubElement(layers,"layer")

        for marker in self.markers:
            xmlMarker= ET.SubElement(layer,"marker")
            ET.SubElement(xmlMarker, "comment", value=str(marker))
            ET.SubElement(xmlMarker, "time", value=str(marker.start))
            ET.SubElement(xmlMarker, "duration", value="0")
            ET.SubElement(xmlMarker, "cuePointName", value="")
            ET.SubElement(xmlMarker, "eventCuePoint", value="true")
            ET.SubElement(xmlMarker, "chapter", value="")
            ET.SubElement(xmlMarker, "frameTarget", value="")
            ET.SubElement(xmlMarker, "url", value="")
            ET.SubElement(xmlMarker, "params")

        tree = ET.ElementTree(root)
        tree.write(f"{self.name}-Markers.xml")  
        return tree

class LayoutMarker:
    supportedFormats = {"mp4": MP4}
    baseFolder = os.path.dirname(os.path.abspath(__file__))
    neededFolders = {"storyFolder": "story","layoutFolder": "202-animation"}
    csvOut = "export-duraciones.csv"

    def __init__(self, thisVideo):
        self.thisVideo = thisVideo
        self.animaticOut = thisVideo.name + "-out"

    @staticmethod
    def getExtension(file):
        if file is not None:
            _, extension = os.path.splitext(file)
            return extension[1:]

    @staticmethod
    def searchExtension(ext):
        return [file for file in os.listdir() if file.endswith(ext)]    
    
    @classmethod
    def searchFiles(cls, ext):
        result = cls.searchExtension(ext)

        if not result:
            return None
        
        if len(result) == 1:
            return result[0]
        
        print(f"Multiple .{ext} files found:")
        for idx, file in enumerate(result, 1):
            print(f"{idx}: {file}")
        print(f"0: None")
        selected_index = int(input("Select the file to use (enter the number): ")) - 1
        if selected_index == -1: return None
        return result[selected_index]
    
    @classmethod
    def calculateSupportedDuration(cls, animaticIn):
        ext = cls.getExtension(animaticIn)
        return cls.supportedFormats[ext](animaticIn).info.length

    @classmethod
    def deleteFolder(cls, folder):
        if os.path.isdir(folder):
            shutil.rmtree(folder)

    @classmethod
    def createFolder(cls, folder):
        if not os.path.exists(folder):
            os.mkdir(folder)

    @classmethod
    def deleteFile(cls, file):
        if os.path.exists(file):
            os.remove(file)

    @classmethod
    def cleanBase(cls):
        file = cls.csvOut
        cls.deleteFile(file)
        for folder in cls.neededFolders.keys():
            cls.deleteFolder(cls.neededFolders[folder])

    @classmethod
    def printClose(cls, msj):
        print(msj)
        input("Press any key to close")
        sys.exit(1)

    def createSceneFolders(self):
        self.createFolder(self.neededFolders["layoutFolder"])
        lastestScene = self.thisVideo.scenes[0][0]
        for marker in self.thisVideo.markers:
            shotName = str(marker) #01-001
            currentScene, _ = shotName.split("-")
            if currentScene != lastestScene:
                lastestScene = currentScene
                sceneFolder = os.path.join(self.baseFolder,self.neededFolders["layoutFolder"],lastestScene)
                self.createFolder(sceneFolder)
                os.mkdir(os.path.join(sceneFolder,f"{lastestScene}_render"))
                os.mkdir(os.path.join(sceneFolder,"assets")) 

    def draw_label(self, frame, text):
        font_face = cv.FONT_HERSHEY_SIMPLEX
        pos = (1600, 62)
        bg_color = (255, 255, 255)
        scale = 1.2
        color = (0, 0, 0)
        thickness = cv.FILLED
        margin = 10

        txt_size = cv.getTextSize(text, font_face, scale, thickness)

        end_x = pos[0] + txt_size[0][0] + margin
        end_y = pos[1] - txt_size[0][1] - margin

        cv.rectangle(frame, pos, (end_x, end_y), bg_color, thickness)
        cv.putText(frame, text, pos, font_face, scale, color, 1, cv.LINE_AA)

    def overlayLabels(self):
        currentFrame = 0
        cvAnimatic = cv.VideoCapture(self.thisVideo.animaticIn) 
        frame_width = int(cvAnimatic.get(3)) 
        frame_height = int(cvAnimatic.get(4)) 
        currentMarkerIndex = 0
        size = (frame_width, frame_height) 

        animaticOut = cv.VideoWriter( f'temp-{self.animaticOut}.mp4',  cv.VideoWriter_fourcc(*'H264'), 24, size)

        while(True): 
            # Capture frames in the video 
            ret, frame = cvAnimatic.read() 
            markersList = self.thisVideo.markers
            currentMarker = markersList[currentMarkerIndex]
            currentFrame +=1/self.thisVideo.fps    

            if currentFrame >= currentMarker.start and currentFrame < currentMarker.start + currentMarker.partialDuration:
                currentText = currentMarker.appendLetter()
            elif currentFrame >= currentMarker.start + currentMarker.partialDuration and currentMarkerIndex < len(markersList)-1:
                currentMarkerIndex+=1
                currentMarker = markersList[currentMarkerIndex]
                currentText = currentMarker.appendLetter()

            self.draw_label(frame, currentText)
            animaticOut.write(frame) 

            print(currentFrame * 100 / self.thisVideo.duration)
            if currentFrame > self.thisVideo.duration: 
                break
    
        # release the cap object 
        cvAnimatic.release() 
        animaticOut.release()
        # close all windows 
        cv.destroyAllWindows() 

    def splitVideo(self):
        layoutFolder = self.neededFolders["layoutFolder"]
        for marker in self.thisVideo.markers:
            scene = str(marker).split("-")[0]
            if marker.letter == "a":
                shotName = str(marker)
                print(shotName + " split start")
                os.path.join(self.baseFolder,layoutFolder,scene ,shotName,"Assets")
                start = marker.start
                if marker.start == 1: start = 0
                duration = marker.duration
                salidaMp4 = str(os.path.join(self.baseFolder, layoutFolder, scene, "Assets", shotName+".mp4"))
                salidaWav = str(os.path.join(self.baseFolder, layoutFolder, scene, "Assets", shotName+".wav"))
                inVideo = ffmpeg.input(f'temp-{self.animaticOut}.mp4', ss=start)
                inAudio = ffmpeg.input(self.thisVideo.animaticIn, ss=start)
                #fede
                streamMp4 = ffmpeg.output(inVideo, inAudio.audio, salidaMp4, t=duration)
                streamWav = ffmpeg.output(inAudio, salidaWav, t=duration)
                try: 
                    ffmpeg.run(streamMp4,capture_stdout=True, capture_stderr=True)
                    ffmpeg.run(streamWav,capture_stdout=True, capture_stderr=True)
                except ffmpeg.Error as e:
                    print('stdout:', e.stdout.decode('utf8'))
                    print('stderr:', e.stderr.decode('utf8'))
                    raise e
                print(shotName + " split end")

    def muxAnimaticOut(self):
        #layoutFolder = self.neededFolders["layoutFolder"]
        baseFolder = self.baseFolder
        outName = f'{self.animaticOut}.mp4'
        start = 0
        duration = self.thisVideo.duration
        inVideo = ffmpeg.input(f'temp-{self.animaticOut}.mp4', ss=start)
        inAudio = ffmpeg.input(self.thisVideo.animaticIn, ss=start)
        streamMp4 = ffmpeg.output(inVideo, inAudio.audio, outName, t=duration)
        try: 
            ffmpeg.run(streamMp4,capture_stdout=True, capture_stderr=True)
        except ffmpeg.Error as e:
            print('stdout:', e.stdout.decode('utf8'))
            print('stderr:', e.stderr.decode('utf8'))
            raise e
    
    def storyFromVideo(self):
        storyFolder = self.neededFolders["storyFolder"]
        self.createFolder(storyFolder)
        for marker in self.thisVideo.markers:
            shotName = marker.appendLetter()
            print(shotName + " story start")
            start = marker.start
            image = shotName+".png"
            salida = os.path.join(self.baseFolder,storyFolder, image)
            stream = ffmpeg.input(f'temp-{self.animaticOut}.mp4', ss=start)
            stream = ffmpeg.output(stream, salida, t=1/self.thisVideo.fps)
            try: 
                ffmpeg.run(stream,capture_stdout=True, capture_stderr=True)
            except ffmpeg.Error as e:
                print('stdout:', e.stdout.decode('utf8'))
                print('stderr:', e.stderr.decode('utf8'))
                raise e
            print(shotName + " story end")
    
    def writeCSV(self):
        rows =[]
        for marker in self.thisVideo.markers:
            if marker.letter =="a":
                shotName = str(marker)
                emptyField = ""
                duration = round(marker.duration * self.thisVideo.fps)
                row = [shotName, duration]
                rows.append(row)

        with open(self.csvOut, "w") as csvFile:
            csvWriter = csv.writer(csvFile, lineterminator = '\n')
            csvWriter.writerows(rows)

    def mohoFromMarkers(self):
        layoutFolder = self.neededFolders["layoutFolder"]
        for marker in self.thisVideo.markers:
            if marker.letter == "a":

                scene = str(marker).split("-")[0]
                temp = "Project.mohoproj"
                self.deleteFile(temp)
                temp = json.loads(mohoBase)
                shotName = str(marker)
                
                moviePath = str("assets/"+ shotName+ ".mp4")
                wavPath = str("assets/"+ shotName+ ".wav")

                temp["project_data"]["end_frame"] = round(marker.duration * self.thisVideo.fps)
                temp["layers"][0]["switch_keys"]["val"][0] = f'{shotName}.mp4' 
                temp["layers"][0]["layers"][0]["image_fileref"]["path"] = moviePath 
                temp["layers"][0]["layers"][0]["image_path"] = moviePath
                temp["layers"][0]["layers"][0]["audio_fileref"]["path"] = moviePath
                temp["layers"][0]["layers"][0]["audio_path"] = moviePath
                temp["layers"][0]["layers"][0]["name"] = shotName+".mp4"
                
                temp["layers"][0]["layers"][1]["audio_fileref"]["path"] = wavPath 
                temp["layers"][0]["layers"][1]["audio_path"] = wavPath
                temp["layers"][0]["layers"][1]["name"] = shotName+".wav"
                temp["layers"][0]["name"] = "animatic"

                temp2 = json.dumps(temp)
                with open("Project.mohoproj", "w") as tempFile:
                    tempFile.write(temp2)
                temp = "Project.mohoproj"
                with ZipFile(PurePath.joinpath(Path.cwd(), layoutFolder,scene, shotName+".moho"), mode="w") as archivo:
                    archivo.write(temp)

        self.deleteFile("Project.mohoproj")
        

#main
def main():
    LayoutMarker.cleanBase()
    global videoIn
    csvIn = LayoutMarker.searchFiles("csv")
    if (csvIn == None): 
        LayoutMarker.printClose("No CSV found")
    
    animaticIn = LayoutMarker.searchFiles("mp4")
    if (animaticIn == None): 
        LayoutMarker.printClose("No MP4 found")
    
    videoIn = Video(csvIn, animaticIn)
    
    thisLayoutMaker = LayoutMarker(videoIn)

    #todo limpiar anterioir

    videoIn.readCSV()
    videoIn.calculateDurations()
    videoIn.consolidateMarkers()
    videoIn.consolidateScenes()

    thisLayoutMaker.createSceneFolders()
    thisLayoutMaker.overlayLabels()

    thisLayoutMaker.splitVideo()
    thisLayoutMaker.storyFromVideo()
    thisLayoutMaker.writeCSV()
    thisLayoutMaker.mohoFromMarkers()
    thisLayoutMaker.muxAnimaticOut()

if __name__ == "__main__":
    main()


#ffmpeg -i test.avi -vcodec png -ss 10 -vframes 1 -an -f rawvideo test.png
#mohoFromMarkers