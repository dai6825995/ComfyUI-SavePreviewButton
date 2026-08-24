from .save_preview_button import SavePreviewButton, setup_routes

setup_routes()

NODE_CLASS_MAPPINGS = {
    "SavePreviewButton": SavePreviewButton,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SavePreviewButton": "预览 · 点按钮保存",
}

WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
