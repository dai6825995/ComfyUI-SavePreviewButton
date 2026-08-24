# -*- coding: utf-8 -*-
"""Queue 出预览后，点按钮保存到 output，不再重新跑工作流。"""

from aiohttp import web

from nodes import PreviewImage, SaveImage

try:
    from server import PromptServer
except Exception:
    PromptServer = None

# node_id -> 上次 Queue 得到的图和文件名前缀
CACHE = {}


def _key(node_id):
    return str(node_id)


class SavePreviewButton:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "preview"
    OUTPUT_NODE = True
    CATEGORY = "image"
    DESCRIPTION = "先 Queue 出预览，再点节点上的按钮保存到 output，不弹另存为、也不用再跑一遍。"

    def preview(self, images, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None, unique_id=None):
        CACHE[_key(unique_id)] = {
            "images": images,
            "filename_prefix": filename_prefix,
            "prompt": prompt,
            "extra_pnginfo": extra_pnginfo,
        }
        return PreviewImage().save_images(images, filename_prefix, prompt, extra_pnginfo)


async def _handle_save(request):
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False, "error": "请求无效"}, status=400)

    item = CACHE.get(_key(data.get("node_id")))
    if not item:
        return web.json_response(
            {"ok": False, "error": "还没有预览图。请先 Queue 一次，出图后再点保存。"},
            status=400,
        )

    try:
        result = SaveImage().save_images(
            item["images"],
            item["filename_prefix"],
            item.get("prompt"),
            item.get("extra_pnginfo"),
        )
    except Exception as e:
        return web.json_response({"ok": False, "error": str(e)}, status=500)

    files = (result or {}).get("ui", {}).get("images") or []
    first = files[0] if files else {}
    sub = first.get("subfolder") or ""
    name = first.get("filename") or ""
    shown = f"{sub}/{name}" if sub else name
    return web.json_response({"ok": True, "path": shown, "filename": name, "subfolder": sub})


def setup_routes():
    if PromptServer is None or getattr(PromptServer, "instance", None) is None:
        return False
    if getattr(PromptServer.instance, "_save_preview_button_routes", False):
        return True
    PromptServer.instance._save_preview_button_routes = True
    PromptServer.instance.routes.post("/save_preview_button/save")(_handle_save)
    return True


setup_routes()

if not setup_routes():
    import threading
    import time

    def _retry():
        for _ in range(30):
            time.sleep(0.5)
            try:
                if setup_routes():
                    return
            except Exception:
                pass

    threading.Thread(target=_retry, daemon=True).start()
