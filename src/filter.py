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

    # ---- 修复核心：E3 逻辑全面升级 ----
    animal_pattern = re.compile(r'\b(rat|rats|mouse|mice|rodent|rodents|macaque|macaques|monkey|monkeys|primate|primates|animal|animals|feline|canine|pig|pigs|porcine)\b')
    has_animal = bool(animal_pattern.search(text))
    
    human_pattern = re.compile(r'\b(human|humans|patient|patients|clinical|subject|subjects)\b')
    has_human = bool(human_pattern.search(text))

    if has_animal and (not has_human):
        return "Exclude", "E3 - Pure Animal Study"

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
    citespace_raw_records = [] # 新增：用于存放准备喂给 CiteSpace 的原始文献块
    
    stats = {
        "Total": 0, "Excluded_E1": 0, "Excluded_E3": 0, "Excluded_E4": 0, "Included": 0
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
            # 新增：如果判定保留，则将完整的带有 WoS 标签的原文存起来
            citespace_raw_records.append(record)
        else:
            if "E1" in reason: stats["Excluded_E1"] += 1
            if "E3" in reason: stats["Excluded_E3"] += 1
            if "E4" in reason: stats["Excluded_E4"] += 1

    # 1. 保存所有结果（包含筛选原因）为 CSV 文件，用于 PRISMA 流程图
    if results:
        keys = results[0].keys()
        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)

    # 2. [新增核心功能] 生成专门用于 CiteSpace 画图的 TXT 文件
    if citespace_raw_records:
        with open(citespace_output_txt, 'w', encoding='utf-8') as f:
            # 必须添加 WoS 标准文件头，否则 CiteSpace 可能会报错识别不出
            f.write("FN Clarivate Analytics Web of Science\nVR 1.0\n")
            for rec in citespace_raw_records:
                # 把之前 split 截掉的 ER 尾部补回来，保证格式绝对合法
                f.write(rec.strip() + "\nER\n")

    print(f"\n✅ 修复版筛选完成！")
    print(f"📊 PRISMA 追踪记录已存至 CSV: {output_csv}")
    print(f"🎨 CiteSpace 专用绘图文件已生成: {citespace_output_txt}")
    print("\n" + "="*40)
    print("📊 PRISMA 数据统计 (包含 CiteSpace 导出)")
    print("="*40)
    print(f"1. 初始检索数量: {stats['Total']}")
    print(f"2. 初筛排除数量: {stats['Total'] - stats['Included']}")
    print(f"   - E1 (主题不符): {stats['Excluded_E1']}")
    print(f"   - E3 (纯动物实验): {stats['Excluded_E3']}")
    print(f"   - E4 (纯算法/DL): {stats['Excluded_E4']}")
    print(f"3. 拟纳入全文复筛 (用于 CiteSpace): {stats['Included']} 篇")
    print("="*40)
    print("💡 下一步操作提示: 直接将生成的 txt 文件放入您的 CiteSpace Data 文件夹中即可运行！")

if __name__ == "__main__":
    # 我们将生成的供 CiteSpace 使用的 txt 命名为 download_ 开头，符合其软件读取习惯
    run_screening("../data", 
                  "../outputs/screening_results.csv", 
                  "../outputs/download_included_for_citespace.txt")