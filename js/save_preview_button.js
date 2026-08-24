import { app } from "/scripts/app.js";
import { api } from "/scripts/api.js";

app.registerExtension({
  name: "SavePreviewButton",
  async beforeRegisterNodeDef(nodeType, nodeData) {
    if (nodeData.name !== "SavePreviewButton") {
      return;
    }

    const onNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function () {
      const r = onNodeCreated?.apply(this, arguments);

      const wrap = document.createElement("div");
      wrap.style.cssText = "padding:6px 2px 2px;";

      const btn = document.createElement("button");
      btn.type = "button";
      btn.textContent = "保存到 output";
      btn.style.cssText = [
        "width:100%",
        "height:40px",
        "border:0",
        "border-radius:8px",
        "background:#5c2d91",
        "color:#fff",
        "font-size:16px",
        "font-weight:600",
        "cursor:pointer",
      ].join(";");

      const setBusy = (busy, text) => {
        btn.disabled = busy;
        btn.style.opacity = busy ? "0.7" : "1";
        btn.textContent = text;
      };

      btn.addEventListener("click", async (ev) => {
        ev.preventDefault();
        ev.stopPropagation();
        setBusy(true, "正在保存…");
        try {
          const res = await api.fetchApi("/save_preview_button/save", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ node_id: this.id }),
          });
          const data = await res.json();
          if (!data.ok) {
            setBusy(false, "保存到 output");
            alert(data.error || "保存失败");
            return;
          }
          setBusy(false, "已保存 ✓");
          setTimeout(() => {
            if (btn.textContent === "已保存 ✓") {
              btn.textContent = "保存到 output";
            }
          }, 2000);
        } catch (err) {
          setBusy(false, "保存到 output");
          alert("保存失败：" + (err?.message || err));
        }
      });

      wrap.appendChild(btn);
      if (typeof this.addDOMWidget === "function") {
        const w = this.addDOMWidget("save_to_output", "save_to_output", wrap, {
          serialize: false,
        });
        w.computeSize = () => [this.size?.[0] || 400, 52];
      } else {
        this.addWidget("button", "保存到 output", null, () => btn.click());
      }

      return r;
    };
  },
});
