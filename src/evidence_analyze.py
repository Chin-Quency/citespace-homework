import pandas as pd
import re
from collections import Counter

def extract_power(text):
    """安全提取功耗数值，统一换算为 uW"""
    if not isinstance(text, str) or pd.isna(text) or str(text).lower() == 'nan':
        return None
    match = re.search(r'(\d+\.?\d*)\s*([uumn])w', text, re.I)
    if match:
        try:
            val = float(match.group(1))
            unit = match.group(2).lower()
            if unit == 'm': return val * 1000  # mW -> uW
            if unit == 'n': return val / 1000  # nW -> uW
            return val
        except: return None
    return None

def extract_compression_ratio(text):
    """安全提取压缩比数值 (如 8:1, 10x, 90%)"""
    if not isinstance(text, str) or pd.isna(text) or str(text).lower() == 'nan':
        return None
    
    # 模式 1: 匹配 8:1 或 16:1
    ratio_match = re.search(r'(\d+\.?\d*)\s*:\s*1', text)
    if ratio_match:
        return float(ratio_match.group(1))
    
    # 模式 2: 匹配 10x 或 10-fold
    fold_match = re.search(r'(\d+\.?\d*)\s*(?:x|fold)', text, re.I)
    if fold_match:
        return float(fold_match.group(1))
        
    # 模式 3: 匹配百分比压缩 (如 90% data reduction -> 10:1)
    percent_match = re.search(r'(\d+\.?\d*)\s*%\s*(?:data )?reduction', text, re.I)
    if percent_match:
        percent = float(percent_match.group(1))
        if percent < 100:
            return 100 / (100 - percent) # 换算为比例
            
    return None

def analyze_evidence_statistics(csv_path):
    try:
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
    except Exception as e:
        print(f"读取失败: {e}"); return

    print("\n" + "█" * 60)
    print("      BCI 全植入系统证据链深度统计报告")
    print("█" * 60)

    # --- [1. 技术路径统计] ---
    method_col = 'Method_Category' if 'Method_Category' in df.columns else 'Method'
    if method_col in df.columns:
        all_methods = [i.strip().upper() for m in df[method_col].dropna() 
                       for i in str(m).split('|') if i.strip().upper() != 'N/A']
        counts = Counter(all_methods)
        print("\n📊 [1] 核心技术热点 (Top 8):")
        for m, c in counts.most_common(8):
            print(f"  > {m:<25} | {c:>3} 篇")

    # --- [2. 功耗水平统计] ---
    perf_col = 'Hardware_Specs' if 'Hardware_Specs' in df.columns else 'Performance'
    powers = df[perf_col].apply(extract_power).dropna()
    print("\n⚡ [2] 功耗量化指标 (uW):")
    if not powers.empty:
        print(f"  > 平均功耗: {powers.mean():.2f} uW  |  中位数: {powers.median():.2f} uW")
        print(f"  > 功耗区间: {powers.min():.2f} ~ {powers.max():.2f} uW")
    else:
        print("  > 提示: 缺失具体数值描述。")

    # --- [3. 压缩比统计 (新增强项)] ---
    # 检查所有可能包含性能描述的列
    comp_col = 'Compression_Stats' if 'Compression_Stats' in df.columns else perf_col
    crs = df[comp_col].apply(extract_compression_ratio).dropna()
    print("\n📦 [3] 数据压缩性能 (Ratio : 1):")
    if not crs.empty:
        print(f"  > 样本数量: {len(crs)} 篇")
        print(f"  > 平均压缩比: {crs.mean():.1f} : 1")
        print(f"  > 最高压缩比: {crs.max():.1f} : 1")
        # 统计高压缩比 (>10x) 的文章比例
        high_cr = (crs >= 10).sum()
        print(f"  > 高压缩比文献 (>10x) 占比: {high_cr/len(crs)*100:.1f}%")
    else:
        print("  > 提示: 未识别到具体的压缩比数值 (e.g., 8:1, 10x)。")

    # --- [4. 范式统计] ---
    paradigm_col = 'BCI_Paradigm' if 'BCI_Paradigm' in df.columns else 'Application'
    p_series = df[paradigm_col].astype(str).str.split('|').explode().str.strip().str.upper()
    p_counts = p_series.value_counts()
    print("\n🧠 [4] BCI 范式分布:")
    for p, c in p_counts.items():
        if p not in ['N/A', 'NAN', 'GENERAL EEG', '']:
            print(f"  > {p:<25} | {c/len(df)*100:>5.1f}% ({c}篇)")

    print("\n" + "█" * 60)

if __name__ == "__main__":
    analyze_evidence_statistics("outputs/evidence_raw_data.csv")