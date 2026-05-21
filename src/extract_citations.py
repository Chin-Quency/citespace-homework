import re
import pandas as pd
import os

def parse_wos_citations(txt_file_path, output_csv_path):
    if not os.path.exists(txt_file_path):
        print(f"❌ 错误：找不到文件 {txt_file_path}")
        print("请确认您已经运行了上一步的筛选脚本，并生成了 CiteSpace 专用的 txt 文件。")
        return

    print(f"正在读取并解析全字段文献库: {txt_file_path}...")
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 以 \nER 分割每篇文献
    records = content.split('\nER')
    
    citation_edges = []
    papers_with_refs = 0
    total_refs = 0

    for record in records:
        if not record.strip() or "FN Clarivate" in record:
            continue

        # 1. 提取施引文献标题 (Citing Paper) -> 作为 TI
        # 使用 [A-Z0-9]{2} 是因为 WoS 标签包含 C1, U1 等带数字的标签
        ti_match = re.search(r'\nTI (.*?)(?=\n[A-Z0-9]{2} |\Z)', "\n" + record, re.S)
        if not ti_match:
            continue
        citing_paper = ti_match.group(1).replace('\n', ' ').strip().lower() # 转小写方便后续匹配

        # 2. 提取该文章的参考文献列表 (Cited Papers) -> 作为 CR
        cr_match = re.search(r'\nCR (.*?)(?=\n[A-Z0-9]{2} |\Z)', "\n" + record, re.S)
        if not cr_match:
            continue
            
        cr_text = cr_match.group(1).strip()
        
        # 3. 将连续的参考文献文本打散为单条记录
        # WoS 的 CR 字段中，每一条参考文献通常以换行符分隔
        refs = cr_text.split('\n')
        
        valid_refs_in_paper = 0
        for ref in refs:
            ref_clean = ref.strip()
            # 过滤掉无效空行或极其简短的乱码
            if len(ref_clean) > 5: 
                citation_edges.append({
                    "citing_paper": citing_paper,
                    "cited_paper": ref_clean
                })
                valid_refs_in_paper += 1
                total_refs += 1
                
        if valid_refs_in_paper > 0:
            papers_with_refs += 1

    # 4. 转换为 DataFrame 并去重、保存
    if not citation_edges:
        print("⚠️ 提取失败：未在文件中找到任何有效的引文 (CR) 记录。")
        return

    df = pd.DataFrame(citation_edges)
    df = df.drop_duplicates()
    
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    
    print("\n✅ 引文边表 (Citation Edges) 提取完成！")
    print("-" * 40)
    print(f"包含参考文献的文章数: {papers_with_refs} 篇")
    print(f"总计提取出的引用连边: {len(df)} 条")
    print(f"边表数据已保存至: {output_csv_path}")
    print("-" * 40)
if __name__ == "__main__":
    # 输入：我们上一步用 PRISMA 筛选并保存了全字段的 TXT 文件
    input_txt = "../outputs/download_included_for_citespace.txt"
    
    # 输出：生成给共被引脚本吃的 CSV
    output_csv = "../data/merged_with_citations.csv"
    
    parse_wos_citations(input_txt, output_csv)