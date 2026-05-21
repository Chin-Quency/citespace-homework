import re
import csv
import pandas as pd

def extract_key_info(abstract, title=""):
    info = {"Method": "N/A", "Data": "N/A", "Application": "N/A", "Performance": "N/A"}
    
    full_text = (title + " " + (abstract if abstract else "")).lower()

    # ================= 1. 核心技术方法 (Method) 提取 =================
    method_categories = {
        "压缩与特征提取": [
            'compressive sensing', 'cs', 'discrete wavelet transform', 'dwt', 
            'principal component analysis', 'pca', 'autoencoder', 'huffman', 
            'spike sorting', 'feature extraction', 'delta encoding', 'lz'
        ],
        "模拟前端(AFE)与ADC": [
            'analog front-end', 'afe', 'low noise amplifier', 'lna', 
            'successive approximation register', 'sar adc', 'sigma-delta', 
            'mixed-signal', 'analog-to-digital converter'
        ],
        "硬件架构": [
            'system-on-chip', 'soc', 'cmos', 'asic', 'fpga', 
            'implantable medical device', 'system level'
        ]
    }

    found_methods = []
    for cat, keywords in method_categories.items():
        for kw in keywords:
            if kw in full_text:
                found_methods.append(kw.upper())

    # 针对标题的“基于型”提取 (例如: A CMOS AFE Based on Compressed Sensing...)
    title_method = re.search(r'(?:based on|using|via)\s+([^,.]+)', title, re.I)
    if title_method:
        found_methods.append(str(title_method.group(1)).strip().upper())

    if found_methods:
        clean_methods = list(set([m for m in found_methods if len(m) > 2]))
        info["Method"] = " | ".join(clean_methods)

    # ================= 2. 信号/数据类型 (Data) 提取 =================
    data_keywords = ['ecog', 'electrocorticogra', 'lfp', 'local field potential', 
                     'action potential', 'spike', 'ieeg', 'intracranial eeg', 'neural recording']
    found_data = [kw.upper() for kw in data_keywords if kw in full_text]
    if found_data:
        info["Data"] = " | ".join(list(set(found_data)))

    # ================= 3. 应用场景 (Application) 提取 =================
    if 'seizure' in full_text or 'epilepsy' in full_text: 
        info["Application"] = "Seizure Detection / Epilepsy"
    elif 'motor' in full_text or 'prosthes' in full_text: 
        info["Application"] = "Motor Decoding / Neuroprosthesis"
    elif 'closed-loop' in full_text or 'stimulation' in full_text: 
        info["Application"] = "Closed-loop Stimulation"
    elif 'implant' in full_text or 'in vivo' in full_text:
        info["Application"] = "Implantable Neural Interface"

    # ================= 4. 核心性能指标 (Performance) 正则提取 =================
    # 这是写硬件/压缩综述最关键的数据，通过正则自动抓取！
    performances = []
    
    # 抓取工艺节点 (例如: 65nm CMOS, 180-nm)
    tech_match = re.search(r'(\d{2,3}\s*[-]?\s*(?:nm|um|µm)\s*(?:cmos)?)', full_text)
    if tech_match: performances.append(f"工艺:{tech_match.group(1)}")
        
    # 抓取功耗 (例如: 1.2 uW, 450nW)
    power_match = re.search(r'([\d\.]+\s*(?:[nµu]w|mw|pw))', full_text)
    if power_match: performances.append(f"功耗:{power_match.group(1)}")
        
    # 抓取压缩率 CR (例如: compression ratio of 16x, 15:1)
    cr_match = re.search(r'(?:compression ratio|cr)[^\d]*?([\d\.]+\s*(?:x|times|:?\s*1|%))', full_text)
    if cr_match: performances.append(f"压缩率(CR):{cr_match.group(1)}")
        
    if performances:
        info["Performance"] = " | ".join(performances)

    return info

# ================= 数据流处理逻辑 =================

def generate_evidence_chain_from_csv(input_csv, output_csv):
    """
    直接从筛选后的 CSV 读取数据，提取写综述所需的证据链特征
    """
    try:
        df = pd.read_csv(input_csv)
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return

    # 核心过滤：只提取标记为保留 (Include) 的文献
    included_df = df[df['Decision'] == 'Include'].copy()
    
    if included_df.empty:
        print("⚠️ 未发现标记为 'Include' 的文献，请检查输入的 CSV 是否有数据。")
        return

    evidence_data = []

    # 遍历保留的文章
    for _, row in included_df.iterrows():
        abstract = str(row.get('AB', '')) if pd.notnull(row.get('AB')) else ""
        title = str(row.get('TI', 'Unknown Title'))
        
        # 【修复点】：在此处把 title 参数传进去了，之前的脚本漏了
        keys = extract_key_info(abstract, title)
        
        # 组装这行数据
        keys['Title'] = title
        keys['Year'] = row.get('PY', 'N/A')
        keys['Journal'] = str(row.get('SO', 'N/A')).title() # 顺便带上期刊名，方便写综述时评估权重
        
        evidence_data.append(keys)

    # 写入新的证据链 CSV
    if evidence_data:
        fields = ['Title', 'Year', 'Journal', 'Method', 'Data', 'Application', 'Performance']
        
        import os
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        
        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(evidence_data)
            
        print(f"📊 证据链特征提取完成！共解析 {len(evidence_data)} 篇核心保留文献。")
        print(f"💾 结构化综述素材库已保存至: {output_csv}")
        print("\n💡 提示：重点检查输出表格中的 'Performance' 列，这能极大加速你对比不同芯片/算法参数的过程。")

if __name__ == "__main__":
    generate_evidence_chain_from_csv("../outputs/screening_results.csv", "../outputs/evidence_raw_data.csv")