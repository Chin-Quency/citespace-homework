import re
import csv
import os

def extract_field(field, text, default=""):
    # 优化的正则：匹配字段开头到下一个大写字母字段开头或文件结束
    pattern = rf'\n{field} (.*?)(?=\n[A-Z]{{2}} |\Z)'
    match = re.search(pattern, "\n" + text, re.S) # 开头加换行符方便统一匹配
    if match:
        return match.group(1).replace('\n', ' ').strip()
    return default

def screen_logic(item):
    include_keywords = [
        'low power', 'energy efficient', 'data compression', 
        'signal acquisition', 'on-chip', 'asic', 'fpga',
        'eeg', 'brain-computer interface', 'bci',
        'integrated circuit', 'analog frontend', 'afe'
    ]
    
    
    exclude_keywords = [
        'animal', 'rat', 'monkey', 'canine',
        'deep learning', 'convolutional neural network', 'transformer model'
    ]
    
    title_abs = (item['TI'] + " " + item['AB']).lower()
    
    # E1: 主题不相关
    if not any(kw in title_abs for kw in include_keywords):
        return "Exclude", "E1"
    text = (item['TI'] + " " + item['AB']).lower()
    # E4: 时间不符 (示例：只要 2010 年以后的)
    # 逻辑判断
    if not any(kw in text for kw in include_keywords):
        return "Exclude", "E1 - Topic Irrelevant"
    
    if any(kw in text for kw in exclude_keywords):
        if 'deep learning' in text or 'neural network' in text:
            return "Exclude", "E4 - Pure Algorithm/DL"
        return "Exclude", "E3 - Non-human study"

    return "Include", "Pass"

def run_screening(input_path, output_csv):
    if not os.path.exists(input_path):
        print(f"错误：找不到输入文件 {input_path}")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    records = content.split('\nER')
    results = []
    
    # PRISMA 计数器
    stats = {
        "Total": 0,
        "Excluded_E1": 0,
        "Excluded_E3": 0,
        "Excluded_E4": 0,
        "Included": 0
    }

    for record in records:
        if not record.strip() or "FN Clarivate" in record: continue
        
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

        # 更新统计
        stats["Total"] += 1
        if decision == "Include":
            stats["Included"] += 1
        else:
            if "E1" in reason: stats["Excluded_E1"] += 1
            if "E3" in reason: stats["Excluded_E3"] += 1
            if "E4" in reason: stats["Excluded_E4"] += 1

    # 保存为 CSV
    keys = results[0].keys()
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

    print(f"✅ 筛选完成！结果已存至: {output_csv}")
    print("\n" + "="*30)
    print("📊 PRISMA 流程图数据统计")
    print("="*30)
    print(f"1. 初始检索数量 (Identification): {stats['Total']}")
    print(f"2. 初筛排除数量 (Screening Excluded): {stats['Total'] - stats['Included']}")
    print(f"   - 其中 E1 (主题不符): {stats['Excluded_E1']}")
    print(f"   - 其中 E3 (Non-human study): {stats['Excluded_E3']}")
    print(f"   - 其中 E4 (Pure Algorithm/DL): {stats['Excluded_E4']}")
    print(f"3. 拟纳入全文复筛数量 (Eligibility): {stats['Included']}")
    print("="*30)

# 执行
run_screening("../data/spacetext.txt", "../outputs/screening_results.csv")