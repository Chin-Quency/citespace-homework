import re
import csv
def extract_key_info(abstract, title=""):
    info = {"Method": "N/A", "Data": "N/A", "Application": "N/A", "Performance": "N/A"}
    
    # 结合标题和摘要进行分析
    full_text = (title + " " + (abstract if abstract else "")).lower()

    # 1. 扩充 BCI 专属方法词库
    method_categories = {
        "范式与检测": ['p300', 'ssvep', 'vep', 'motor imagery', 'mi', 'steady state', 'motion-onset'],
        "高级算法": ['independent component analysis', 'ica', 'nonlinear', 'classifier', 'machine learning', 'decoding'],
        "硬件与材料": ['electrode', 'near-infrared spectroscopy', 'fnirs', 'sensor', 'circuit', 'system design'],
        "处理技术": ['reconstruction', 'phase resetting', 'evoked activity', 'signal analysis', 'compression']
    }

    found_methods = []
    for cat, keywords in method_categories.items():
        for kw in keywords:
            if kw in full_text:
                found_methods.append(kw.upper())

    # 2. 针对标题的“基于型”提取 (例如: ...Based on X)
    # 匹配 "Interface Based on [Method]" 或 "Using [Method]"
    title_method = re.search(r'(?:based on|using|via)\s+([^,.]+)', title, re.I)
    if title_method:
        found_methods.append(str(title_method.group(1)).strip().upper())

    # 3. 结果合并与去重
    if found_methods:
        # 去重并过滤掉太短或无效的词
        clean_methods = list(set([m for m in found_methods if len(m) > 2]))
        info["Method"] = " | ".join(clean_methods)
    
    # [Data, Application 提取逻辑...]
    # 针对图片中常见的应用场景 (Robot, Speller, Rehabilitation)
    if 'robot' in full_text: info["Application"] = "Robot Navigation/Control"
    if 'speller' in full_text: info["Application"] = "BCI Speller"
    if 'rehabilitation' in full_text or 'stroke' in full_text: info["Application"] = "Stroke Rehabilitation"

    return info

import csv
import pandas as pd

# [你的 extract_key_info 函数保持不变，此处略]

def generate_evidence_chain_from_csv(input_csv, output_csv):
    """
    直接从筛选后的 CSV 读取数据，仅分析保留的文献
    """
    try:
        # 读取筛选脚本生成的 CSV
        df = pd.read_csv(input_csv)
    except Exception as e:
        print(f"读取文件失败: {e}")
        return

    # 1. 核心过滤：只提取标记为保留 (Include) 的文献
    included_df = df[df['Decision'] == 'Include'].copy()
    
    if included_df.empty:
        print("Sub-optimal: 未发现标记为 'Include' 的文献，请检查筛选逻辑。")
        return

    evidence_data = []

    # 2. 遍历保留的文章
    for _, row in included_df.iterrows():
        # 获取摘要和标题（处理可能的 NaN 情况）
        abstract = str(row.get('AB', '')) if pd.notnull(row.get('AB')) else ""
        title = str(row.get('TI', 'Unknown Title'))
        
        # 3. 调用你原有的提取逻辑
        keys = extract_key_info(abstract)
        keys['Title'] = title
        
        # 如果你之前的 CSV 里有年份 PY，也可以顺便带上
        keys['Year'] = row.get('PY', 'N/A')
        
        evidence_data.append(keys)

    # 4. 写入新的证据链 CSV
    if evidence_data:
        # 在你原有的字段基础上增加了 Year
        fields = ['Title', 'Year', 'Method', 'Data', 'Application', 'Performance']
        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(evidence_data)
        print(f"📊 证据链提取完成！共处理 {len(evidence_data)} 篇保留文献。")
        print(f"💾 已保存至: {output_csv}")

# 修改调用处
generate_evidence_chain_from_csv("../outputs/screening_results.csv", "../outputs/evidence_raw_data.csv")