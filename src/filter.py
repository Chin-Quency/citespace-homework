import re
import csv
import os

def extract_field(field, text, default=""):
    pattern = rf'\n{field} (.*?)(?=\n[A-Z]{{2}} |\Z)'
    match = re.search(pattern, "\n" + text, re.S)
    if match:
        return match.group(1).replace('\n', ' ').strip()
    return default

def screen_logic(item):
    text = (item['TI'] + " " + item['AB'] + " " + item['DE']).lower()
    
    # ---- 概念 1 和 2 ----
    c1_keywords = ['implant', 'invasive', 'neural interfac', 'neural record', 'ecog', 'lfp', 'eeg']
    c2_keywords = ['compress', 'data reduc', 'compressive sensing', 'feature extract', 'on-chip process', 'edge comput']
    
    has_c1 = any(kw in text for kw in c1_keywords)
    has_c2 = any(kw in text for kw in c2_keywords)
    
    if not (has_c1 and has_c2):
        return "Exclude", "E1 - Topic Irrelevant (Missing BCI or Compression)"
        
    dl_keywords = ['deep learning', 'convolutional neural network', 'transformer model', 'neural network']
    if any(kw in text for kw in dl_keywords):
        return "Exclude", "E4 - Pure Algorithm/DL"

    # ---- 修复核心 1：E3 动物实验排除 ----
    animal_pattern = re.compile(r'\b(rat|rats|mouse|mice|rodent|rodents|macaque|macaques|monkey|monkeys|primate|primates|animal|animals|feline|canine|pig|pigs|porcine)\b')
    has_animal = bool(animal_pattern.search(text))
    
    human_pattern = re.compile(r'\b(human|humans|patient|patients|clinical|subject|subjects)\b')
    has_human = bool(human_pattern.search(text))

    if has_animal and (not has_human):
        return "Exclude", "E3 - Pure Animal Study"

    # ---- 修复核心 2：E5 剔除非神经领域的临床/骨科/外科噪音 ----
    # 针对性屏蔽：骨骼、脊柱、经皮椎体成形术、骨折、固定、牙科、心血管支架等
    med_noise_pattern = re.compile(r'\b(bone|bones|spine|spinal|vertebroplasty|orthopedic|orthopaedic|fracture|fractures|fixation|lumbar|cervical|dental|stent|stents|arthroplasty|osteoporosis|joint|cardiovascular|myocardial)\b')
    if bool(med_noise_pattern.search(text)):
        return "Exclude", "E5 - Non-Neural Medical/Orthopedic Noise"

    return "Include", "Pass"

def run_screening(input_folder, output_csv, citespace_output_txt):
    if not os.path.exists(input_folder):
        print(f"❌ 错误：找不到输入文件夹 {input_folder}")
        return

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    all_records = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            print(f"正在读取：{filename}")

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 以换行符+ER作为分隔，提取每个独立的文献块
            records = content.split('\nER')
            for r in records:
                if r.strip() and "FN Clarivate" not in r:
                    all_records.append(r)
                    
    if not all_records:
        print("❌ 未在输入文件夹中解析到任何有效记录！")
        return

    results = []
    citespace_raw_records = [] 
    
    # 字典新增了 Excluded_E5
    stats = {
        "Total": 0, "Excluded_E1": 0, "Excluded_E3": 0, "Excluded_E4": 0, "Excluded_E5": 0, "Included": 0
    }

    for record in all_records:
        item = {
            'TI': extract_field('TI', record, "N/A"),
            'AB': extract_field('AB', record, ""),
            'DE': extract_field('DE', record, ""),
            'PY': extract_field('PY', record, "N/A"),
            'AU': extract_field('AU', record, "N/A"),
            'SO': extract_field('SO', record, "N/A")
        }

        decision, reason = screen_logic(item)
        item['Decision'] = decision
        item['Reason_Code'] = reason
        results.append(item)

        stats["Total"] += 1
        if decision == "Include": 
            stats["Included"] += 1
            citespace_raw_records.append(record)
        else:
            if "E1" in reason: stats["Excluded_E1"] += 1
            elif "E3" in reason: stats["Excluded_E3"] += 1
            elif "E4" in reason: stats["Excluded_E4"] += 1
            elif "E5" in reason: stats["Excluded_E5"] += 1

    # 1. 保存所有结果
    if results:
        keys = results[0].keys()
        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)

    # 2. 生成专门用于 CiteSpace 画图的 TXT 文件
    if citespace_raw_records:
        with open(citespace_output_txt, 'w', encoding='utf-8') as f:
            f.write("FN Clarivate Analytics Web of Science\nVR 1.0\n")
            for rec in citespace_raw_records:
                f.write(rec.strip() + "\nER\n")

    print(f"\n✅ 修复版筛选完成！")
    print(f"📊 PRISMA 追踪记录已存至 CSV: {output_csv}")
    print(f"🎨 CiteSpace 专用绘图文件已生成: {citespace_output_txt}")
    print("\n" + "="*45)
    print("📊 PRISMA 数据统计 (包含 CiteSpace 导出)")
    print("="*45)
    print(f"1. 初始检索数量: {stats['Total']}")
    print(f"2. 初筛排除数量: {stats['Total'] - stats['Included']}")
    print(f"   - E1 (主题不符): {stats['Excluded_E1']}")
    print(f"   - E3 (纯动物实验): {stats['Excluded_E3']}")
    print(f"   - E4 (纯算法/DL): {stats['Excluded_E4']}")
    print(f"   - E5 (医疗/骨科/外科噪音): {stats['Excluded_E5']}  <-- [本次重点拦截]")
    print(f"3. 拟纳入全文复筛 (用于 CiteSpace): {stats['Included']} 篇")
    print("="*45)
    print("💡 下一步：请用新生成的 txt 文件重新运行 CiteSpace！")

if __name__ == "__main__":
    run_screening("../data", 
                  "../outputs/screening_results.csv", 
                  "../outputs/download_included_for_citespace.txt")