import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def draw_prisma_chart(output_path="../outputs/prisma_flowchart.png"):
    # 创建画布 (宽 10, 高 8)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axis('off')  # 关闭坐标轴

    # 定义文本框的统一样式
    box_style = dict(boxstyle="round,pad=0.5", facecolor="#F5F5F5", edgecolor="#333333", linewidth=1.5)
    exclude_box_style = dict(boxstyle="round,pad=0.5", facecolor="#FFF0F0", edgecolor="#D62728", linewidth=1.5)
    include_box_style = dict(boxstyle="round,pad=0.5", facecolor="#F0FFF0", edgecolor="#2CA02C", linewidth=1.5)

    # ================= 1. 定义节点文本内容 =================
    text_identification = "Identification:\nRecords identified through\nWeb of Science database\n(n = 16,000)"
    text_screening = "Screening:\nRecords screened by\nautomated scripts\n(n = 16,000)"
    text_excluded = "Excluded (n = 4,797):\n- E1 (Topic Irrelevant): 2,294\n- E3 (Pure Animal Study): 14\n- E4 (Pure Algorithm/DL): 2,489"
    text_included = "Included:\nRecords included for\nCiteSpace / VOSviewer analysis\n(n = 11,203)"

    # ================= 2. 定义节点位置 (X, Y) =================
    pos_id = (0.35, 0.85)
    pos_screen = (0.35, 0.55)
    pos_exclude = (0.80, 0.55)
    pos_include = (0.35, 0.25)

    # ================= 3. 绘制文本框 =================
    # Identification Box
    ax.text(pos_id[0], pos_id[1], text_identification, size=11, ha="center", va="center", bbox=box_style, wrap=True)
    
    # Screening Box
    ax.text(pos_screen[0], pos_screen[1], text_screening, size=11, ha="center", va="center", bbox=box_style, wrap=True)
    
    # Excluded Box
    ax.text(pos_exclude[0], pos_exclude[1], text_excluded, size=11, ha="center", va="center", bbox=exclude_box_style)
    
    # Included Box
    ax.text(pos_include[0], pos_include[1], text_included, size=12, ha="center", va="center", fontweight='bold', bbox=include_box_style)

    # ================= 4. 绘制连接箭头 =================
    arrow_props = dict(facecolor='black', edgecolor='black', width=2, headwidth=8, headlength=10, shrink=0.05)

    # Identification -> Screening (向下)
    ax.annotate('', xy=(pos_screen[0], pos_screen[1] + 0.12), 
                xytext=(pos_id[0], pos_id[1] - 0.12),
                arrowprops=arrow_props)

    # Screening -> Included (向下)
    ax.annotate('', xy=(pos_include[0], pos_include[1] + 0.12), 
                xytext=(pos_screen[0], pos_screen[1] - 0.12),
                arrowprops=arrow_props)

    # Screening -> Excluded (向右)
    ax.annotate('', xy=(pos_exclude[0] - 0.18, pos_exclude[1]), 
                xytext=(pos_screen[0] + 0.15, pos_screen[1]),
                arrowprops=arrow_props)

    # ================= 5. 添加区域侧边标签 (可选，增加学术感) =================
    ax.text(0.05, pos_id[1], "Identification", size=14, fontweight='bold', rotation=90, va='center', color='gray')
    ax.text(0.05, pos_screen[1], "Screening", size=14, fontweight='bold', rotation=90, va='center', color='gray')
    ax.text(0.05, pos_include[1], "Included", size=14, fontweight='bold', rotation=90, va='center', color='gray')

    # 添加分割虚线
    ax.plot([0.1, 0.95], [0.72, 0.72], linestyle='--', color='lightgray', zorder=0)
    ax.plot([0.1, 0.95], [0.40, 0.40], linestyle='--', color='lightgray', zorder=0)

    # ================= 6. 保存与显示 =================
    plt.tight_layout()
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ PRISMA 流程图绘制成功！已保存至: {output_path}")
    plt.show()

if __name__ == "__main__":
    draw_prisma_chart()