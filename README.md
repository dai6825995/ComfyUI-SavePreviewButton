# ComfyUI-SavePreviewButton

先 Queue 出预览，再点节点上的 **保存到 output**。不弹另存为，也不用再跑一遍工作流。

## 安装

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/dai6825995/ComfyUI-SavePreviewButton.git
```

重启 ComfyUI。节点名：**预览 · 点按钮保存**（`SavePreviewButton`）。

## 用法

1. 把图像接到 `images`，文件名前缀接到 `filename_prefix`（可含 `%date:yyyy-MM-dd%`）。
2. Queue 一次，节点上出现预览。
3. 看中了点 **保存到 output**，文件进 ComfyUI 的 `output` 目录。
