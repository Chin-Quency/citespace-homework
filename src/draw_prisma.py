import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import os


def draw_prisma_chart(output_path="../outputs/prisma_flowchart.png"):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # ================= 颜色与样式 =================
    C_BG = "#F7F9FC"
    C_IDENT = "#D6EAF8"
    C_SCREEN = "#D5F5E3"
    C_EXCLUDE = "#FADBD8"
    C_INCLUDE = "#ABEBC6"
    C_BORDER = "#2C3E50"
    C_ARROW = "#34495E"
    C_LABEL = "#7F8C8D"

    fig.patch.set_facecolor('white')

    # ================= 辅助函数 =================
    def draw_box(x, y, w, h, facecolor, text, fontsize=9, bold=False, text_color="#2C3E50"):
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.15",
            facecolor=facecolor, edgecolor=C_BORDER,
            linewidth=1.2, zorder=2
        )
        ax.add_patch(box)
        weight = 'bold' if bold else 'normal'
        ax.text(x + w / 2, y + h / 2, text,
                ha='center', va='center', fontsize=fontsize,
                fontweight=weight, color=text_color, zorder=3,
                linespacing=1.4)

    def draw_arrow(x1, y1, x2, y2):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=C_ARROW,
                                    lw=1.5, shrinkA=0, shrinkB=0),
                    zorder=1)

    # ================= 节点定义 =================
    # 中心列 x=1.5, w=4.5; 排除列 x=6.5, w=3
    cx, cw = 1.5, 4.5
    ex, ew = 6.5, 3.0
    bh = 1.2  # 基础框高
    gap = 0.5  # 框间距

    # --- Identification ---
    y_id = 6.2
    draw_box(cx, y_id, cw, bh, C_IDENT,
             "Identification\nRecords from Web of Science\n(n = 16,000)",
             fontsize=9.5, bold=True)

    # --- Screening ---
    y_sc = y_id - bh - gap
    draw_box(cx, y_sc, cw, bh, C_SCREEN,
             "Screening\nAutomated script screening\n(n = 16,000)",
             fontsize=9.5, bold=True)

    # --- Excluded ---
    y_ex = y_sc
    draw_box(ex, y_ex, ew, bh + 0.5, C_EXCLUDE,
             "Excluded (n = 10,310)\n"
             "E1 Topic irrelevant: 2,294\n"
             "E3 Pure animal study: 14\n"
             "E4 Pure DL/algorithm: 2,489\n"
             "E5 Non-neural medical: 5,513",
             fontsize=8, text_color="#922B21")

    # --- Included ---
    y_in = y_sc - bh - gap
    draw_box(cx, y_in, cw, bh, C_INCLUDE,
             "Included\nCiteSpace / VOSviewer analysis\n(n = 5,690)",
             fontsize=9.5, bold=True, text_color="#1E8449")

    # ================= 箭头 =================
    mid_cx = cx + cw / 2
    mid_ex = ex + ew / 2

    # Identification -> Screening
    draw_arrow(mid_cx, y_id, mid_cx, y_sc + bh)
    # Screening -> Included
    draw_arrow(mid_cx, y_sc, mid_cx, y_in + bh)
    # Screening -> Excluded
    draw_arrow(cx + cw, y_sc + bh / 2, ex, y_ex + (bh + 0.5) / 2)

    # ================= 侧边区域标签 =================
    label_x = 0.4
    ax.text(label_x, y_id + bh / 2, "Identification",
            fontsize=9, fontweight='bold', rotation=90,
            va='center', ha='center', color=C_LABEL)
    ax.text(label_x, y_sc + bh / 2, "Screening",
            fontsize=9, fontweight='bold', rotation=90,
            va='center', ha='center', color=C_LABEL)
    ax.text(label_x, y_in + bh / 2, "Included",
            fontsize=9, fontweight='bold', rotation=90,
            va='center', ha='center', color=C_LABEL)

    # ================= 分隔线 =================
    line_y1 = y_sc + bh + gap * 0.45
    line_y2 = y_in + bh + gap * 0.45
    ax.plot([1.0, 9.5], [line_y1, line_y1], linestyle='--', color='#D5D8DC', lw=0.8, zorder=0)
    ax.plot([1.0, 9.5], [line_y2, line_y2], linestyle='--', color='#D5D8DC', lw=0.8, zorder=0)

    # ================= 保存 =================
    plt.tight_layout(pad=0.3)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"PRISMA flowchart saved to: {output_path}")
    plt.close()


if __name__ == "__main__":
    draw_prisma_chart()
