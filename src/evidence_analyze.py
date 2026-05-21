import pandas as pd
import re
from collections import Counter

def extract_power(text):
    """安全提取功耗数值，统一换算为 uW (微瓦)"""
    if pd.isna(text): return None
    # 匹配上一步脚本提取生成的 "功耗:1.2 uW" 或 原始文本的功耗描述
    match = re.search(r'(?:功耗:)?([\d\.]+)\s*([µuumnp])w', str(text), re.I)
    if match:
        try:
            val = float(match.group(1))
            unit = match.group(2).lower()
            if unit == 'm': return val * 1000      # mW (毫瓦) -> uW
            if unit in ['u', 'µ']: return val      # uW (微瓦) -> uW
            if unit == 'n': return val / 1000      # nW (纳瓦) -> uW
            if unit == 'p': return val / 1000000   # pW (皮瓦) -> uW
            return val
        except: return None
    return None

def extract_compression_ratio(text):
    """安全提取片上数据压缩比数值 (如 8:1, 10x)，包含防崩溃机制"""
    if pd.isna(text): return None
    text = str(text)
    
    try:
        # 修复点1：将原来粗糙的 ([\d\.]+) 替换为严格要求必须有数字的 (\d+\.?\d*)
        cr_match = re.search(r'压缩率\(CR\):(\d+\.?\d*)', text, re.I)
        if cr_match and cr_match.group(1):
            return float(cr_match.group(1))
            
        # 备用模式 1: 匹配 8:1 或 16.5:1
        ratio_match = re.search(r'(\d+\.?\d*)\s*:\s*1', text)
        if ratio_match and ratio_match.group(1): 
            return float(ratio_match.group(1))
        
        # 备用模式 2: 匹配 10x 或 10-fold
        fold_match = re.search(r'(\d+\.?\d*)\s*(?:x|fold)', text, re.I)
        if fold_match and fold_match.group(1): 
            return float(fold_match.group(1))
            
    except ValueError:
        # 修复点2：捕获由于脏数据引发的转换报错，遇到不能转换的内容直接忽略
        return None
        
    return None

def extract_tech_node(text):
    """提取集成电路制造工艺节点 (统一转换为 nm)"""
    if pd.isna(text): return None
    text = str(text)
    
    # 匹配 "工艺:65nm" 或 "180 nm CMOS"
    match = re.search(r'(?:工艺:)?(\d{2,3})\s*(?:nm)', text, re.I)
    if match:
        return int(match.group(1))
        
    # 自动换算：将 0.18 um 转换为 180 nm
    match_um = re.search(r'(?:工艺:)?(0\.\d+)\s*(?:um|µm)', text, re.I)
    if match_um:
        return int(float(match_um.group(1)) * 1000)
    return None

def analyze_evidence_statistics(csv_path):
    try:
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        return

    if df.empty:
        print("⚠️ 数据集为空！请检查提取脚本是否正确运行。")
        return

    print("\n" + "█" * 65)
    print("     🧠 植入式脑机接口 (芯片/电路/压缩) 深度统计报告")
    print("█" * 65)

    # --- [1. 核心芯片架构与压缩算法统计] ---
    if 'Method' in df.columns:
        all_methods = [i.strip().upper() for m in df['Method'].dropna() 
                       for i in str(m).split('|') if i.strip().upper() != 'N/A']
        counts = Counter(all_methods)
        print("\n🛠️ [1] 核心电路架构与算法热点 (Top 8):")
        for m, c in counts.most_common(8):
            print(f"  > {m:<28} | {c:>3} 篇")

    # --- [2. 侵入式信号模态分布] ---
    if 'Data' in df.columns:
        all_data = [i.strip().upper() for m in df['Data'].dropna() 
                       for i in str(m).split('|') if i.strip().upper() != 'N/A']
        d_counts = Counter(all_data)
        print("\n📡 [2] 侵入式神经信号模态:")
        for d, c in d_counts.most_common():
            print(f"  > {d:<28} | {c/len(df)*100:>5.1f}% ({c}篇)")

    # --- [3. 功耗水平量化统计] ---
    if 'Performance' in df.columns:
        powers = df['Performance'].apply(extract_power).dropna()
        print("\n⚡ [3] 系统功耗水平 (统一换算为 uW 微瓦):")
        if not powers.empty:
            print(f"  > 有效量化样本: {len(powers)} 篇硬核论文")
            print(f"  > 平均功耗: {powers.mean():.2f} uW  |  中位数 (更准): {powers.median():.2f} uW")
            print(f"  > 极低功耗 (<10uW) 占比: {(powers < 10).sum()/len(powers)*100:.1f}%")
            print(f"  > 最低功耗记录: {powers.min():.4f} uW")
        else:
            print("  > 提示: 未成功解析到具体的量化功耗指标。")

    # --- [4. 数据压缩比统计] ---
    if 'Performance' in df.columns:
        crs = df['Performance'].apply(extract_compression_ratio).dropna()
        print("\n📦 [4] 片上数据压缩性能 (Ratio : 1):")
        if not crs.empty:
            print(f"  > 有效量化样本: {len(crs)} 篇论文")
            print(f"  > 平均压缩比: {crs.mean():.1f} : 1  |  最高达: {crs.max():.1f} : 1")
            high_cr = (crs >= 10).sum()
            print(f"  > 超高压缩文献 (≥10倍) 占比: {high_cr/len(crs)*100:.1f}%")
        else:
            print("  > 提示: 未解析到具体的压缩比例 (e.g., 10x, 8:1)。")

    # --- [5. 芯片工艺制程统计 (新增绝杀功能)] ---
    if 'Performance' in df.columns:
        nodes = df['Performance'].apply(extract_tech_node).dropna()
        print("\n🔬 [5] CMOS 制造工艺制程 (Technology Node):")
        if not nodes.empty:
            node_counts = Counter(nodes)
            for n, c in node_counts.most_common(5):
                print(f"  > {int(n):<3} nm 工艺 | {c:>3} 篇 ({c/len(nodes)*100:.1f}%)")
        else:
            print("  > 提示: 未识别到工艺节点参数。")

    # --- [6. 应用场景统计] ---
    if 'Application' in df.columns:
        app_series = df['Application'].astype(str).str.split('|').explode().str.strip()
        app_counts = app_series[app_series != 'N/A'].value_counts()
        print("\n🏥 [6] 终端临床应用场景:")
        for a, c in app_counts.items():
            print(f"  > {a:<28} | {c:>3} 篇 ({c/len(df)*100:.1f}%)")

    print("\n" + "█" * 65)

if __name__ == "__main__":
    analyze_evidence_statistics("../outputs/evidence_raw_data.csv")