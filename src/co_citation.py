import pandas as pd
import numpy as np
from pathlib import Path

def get_included_papers(screening_csv):
    """
    [新增模块] 读取初筛结果，获取所有通过筛选 (Include) 的文献标题
    """
    try:
        df_screen = pd.read_csv(screening_csv, encoding='utf-8-sig')
        # 过滤出通过筛选的文献
        included = df_screen[df_screen['Decision'] == 'Include']
        
        # 提取标题，统一转小写并去除首尾空格，用于后续极其稳健的匹配
        valid_titles = set(included['TI'].astype(str).str.strip().str.lower())
        print(f"✅ 成功加载初筛记录: 共 {len(valid_titles)} 篇被纳入分析的核心文献。")
        return valid_titles
    except Exception as e:
        print(f"❌ 读取筛选结果文件失败: {e}")
        return set()

import os

def load_citation_edges(csv_path, valid_papers=None):
    """
    加载边表，并利用初筛白名单进行过滤
    修复了文件不存在或读取失败时的 UnboundLocalError
    """
    # 1. 增加绝对的安全检查：文件是否存在
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"❌ 找不到引文数据文件: {csv_path}。请确保您已经运行了 extract_citations.py")

    encodings = ["utf-8-sig", "utf-8", "gbk", "latin1"]
    df = None
    
    # 2. 尝试不同的编码读取文件
    for enc in encodings:
        try:
            df = pd.read_csv(csv_path, encoding=enc)
            print(f"✅ 成功以 {enc} 编码读取文件。")
            break
        except Exception as e:
            continue

    # 3. 如果所有编码都失败，或者 df 依然是 None，抛出明确的异常，而不是继续往下走
    if df is None:
        raise ValueError(f"❌ 无法读取文件 {csv_path}。可能是文件损坏或格式不支持。")

    required = ["citing_paper", "cited_paper"]
    if not all(c in df.columns for c in required):
        raise KeyError(f"❌ 数据表必须包含 {required} 列，但当前只有 {df.columns.tolist()}")

    # 开始清理数据
    df = df.dropna(subset=required)
    df["citing_paper"] = df["citing_paper"].astype(str).str.strip()
    df["cited_paper"] = df["cited_paper"].astype(str).str.strip()
    df = df[df["citing_paper"] != ""]
    df = df[df["cited_paper"] != ""]
    
    print(f"📊 原始引用网络边数: {len(df)}")

    # ================= 核心修改：利用筛选数据过滤 =================
    if valid_papers:
        citing_lower = df["citing_paper"].str.lower()
        df = df[citing_lower.isin(valid_papers)]
        print(f"🔍 经过 PRISMA 纳入标准过滤后，保留的有效引用边数: {len(df)}")

    # ================= 性能与图谱优化：去除低频噪音 =================
    cite_counts = df["cited_paper"].value_counts()
    
    print(f"📊 被引文献频率分布 (前 5 名):\n{cite_counts.head(5)}")
    print(f"⚠️ 总计唯一的被引文献数量: {len(cite_counts)}")
    
    # 动态阈值：建议根据您的内存设置 3 或 5
    THRESHOLD = 3 
    
    valid_cited = cite_counts[cite_counts >= THRESHOLD].index 
    print(f"🛡️ 启用内存保护：过滤掉被引频次 < {THRESHOLD} 次的文献...")
    print(f"📉 过滤后用于构建矩阵的核心被引文献数量: {len(valid_cited)}")
    
    df = df[df["cited_paper"].isin(valid_cited)]
    print(f"🧹 最终用于建模的边数: {len(df)}")

    df = df.drop_duplicates()
    return df    # ... (前面的代码保持不变) ...

    # ================= 核心修改：利用筛选数据过滤 =================
    if valid_papers:
        citing_lower = df["citing_paper"].str.lower()
        df = df[citing_lower.isin(valid_papers)]
        print(f"🔍 经过 PRISMA 纳入标准过滤后，保留的有效引用边数: {len(df)}")

    # ================= 性能与图谱优化：去除低频噪音 =================
    # 【修复重点】提高过滤阈值，只保留被引用次数 >= 3 (或 5) 的文献
    # 之前设定的 >= 2 门槛太低，导致了 5万多篇文献涌入矩阵
    cite_counts = df["cited_paper"].value_counts()
    
    # 建议先打印一下统计分布，做到心中有数
    print(f"📊 被引文献频率分布 (前 10 名):\n{cite_counts.head(10)}")
    print(f"⚠️ 总计唯一的被引文献数量: {len(cite_counts)}")
    
    # === 动态阈值调整 ===
    # 如果您的电脑只有 16GB 内存，建议矩阵维度 (len(valid_cited)) 不要超过 15,000。
    # 您可以手动把这里的 3 改成 5 甚至 10，直到 `valid_cited` 的长度小于 15000。
    THRESHOLD = 3 
    
    valid_cited = cite_counts[cite_counts >= THRESHOLD].index 
    print(f"🛡️ 启用内存保护：过滤掉被引频次 < {THRESHOLD} 次的文献...")
    print(f"📉 过滤后用于构建矩阵的核心被引文献数量: {len(valid_cited)}")
    
    df = df[df["cited_paper"].isin(valid_cited)]
    print(f"🧹 最终用于建模的边数: {len(df)}")

    df = df.drop_duplicates()
    return df
def build_citation_matrix(edges):
    # 构建 施引文献 × 被引文献 的二值化矩阵 R
    R = edges.pivot_table(
        index="citing_paper",
        columns="cited_paper",
        values="cited_paper",
        aggfunc=lambda x: 1,
        fill_value=0
    )
    return R
def build_co_citation_matrix(R):
    # 构建 共被引矩阵 C = R^T * R
    R_array = R.values.astype(np.float32) 
    C_array = np.dot(R_array.T, R_array)
    
    # 【修复点】：直接修改纯 NumPy 数组，而不是修改 DataFrame.values
    np.fill_diagonal(C_array, 0)  # 去掉自环
    
    # 修改完毕后，再将其转化为 DataFrame
    C = pd.DataFrame(C_array, index=R.columns, columns=R.columns)
    return C

def cosine_similarity_matrix(C):
    # 计算余弦相似度进行归一化
    X = C.values.astype(np.float32)
    norm = np.linalg.norm(X, axis=1, keepdims=True)
    norm[norm == 0] = 1
    sim = np.dot(X, X.T) / (norm * norm.T)
    sim = np.nan_to_num(sim)
    
    # 【修复点】：同样在这里提前对 NumPy 数组进行对角线清零
    np.fill_diagonal(sim, 0)
    
    # 最后再组装成 DataFrame
    sim_df = pd.DataFrame(sim, index=C.index, columns=C.columns)
    return sim_df
def matrix_to_edges(matrix, min_weight=0.01):
    # 抽取上三角矩阵，防止生成重复的双向边 (A-B 和 B-A)
    nodes = matrix.columns.tolist()
    arr = np.triu(matrix.values, k=1) # 仅取上三角
    
    # 快速找到满足权重的索引，比双重 for 循环快几百倍
    row_idx, col_idx = np.where(arr >= min_weight)
    
    edges = [
        [nodes[r], nodes[c], arr[r, c]] 
        for r, c in zip(row_idx, col_idx)
    ]
    
    return pd.DataFrame(edges, columns=["source", "target", "weight"])

def run_co_citation_model(screening_csv_path, citation_csv_path, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    print("\n[1/5] 读取初筛纳入文献名单...")
    valid_papers = get_included_papers(screening_csv_path)

    print("\n[2/5] 读取并过滤引用数据...")
    edges = load_citation_edges(citation_csv_path, valid_papers)
    
    if edges.empty:
        print("❌ 错误：过滤后没有留下任何引用数据，请检查 citing_paper 是否与筛选表中的 TI (标题) 一致。")
        return

    print("\n[3/5] 构建引用矩阵 R (Citing x Cited)...")
    R = build_citation_matrix(edges)

    print("\n[4/5] 构建共被引矩阵 C 及计算余弦相似度...")
    C = build_co_citation_matrix(R)
    sim = cosine_similarity_matrix(C)

    print("\n[5/5] 生成共被引网络边表...")
    edge_list = matrix_to_edges(sim, min_weight=0.1) # 相似度 >= 0.1 才建边

    # 保存全部结果
    R.to_csv(output_dir / "citation_matrix_R.csv", encoding="utf-8-sig")
    C.to_csv(output_dir / "co_citation_matrix_C.csv", encoding="utf-8-sig")
    sim.to_csv(output_dir / "similarity_matrix.csv", encoding="utf-8-sig")
    edge_list.to_csv(output_dir / "co_citation_edges.csv", index=False, encoding="utf-8-sig")

    print("\n✅ 共被引网络建模完成！")
    print("-" * 40)
    print(f"引用矩阵 R (施引 x 被引): {R.shape}")
    print(f"共被引矩阵 C (被引 x 被引): {C.shape}")
    print(f"满足阈值的网络边数: {len(edge_list)}")
    print(f"输出文件已保存到: {output_dir}")
    print("-" * 40)

if __name__ == "__main__":
    # 我们之前清洗生成的筛选结果表
    screening_csv = "../outputs/screening_results.csv" 
    # 您的原始引用边数据
    citation_csv = "../data/merged_with_citations.csv"  
    # 建模结果输出目录
    output_directory = "../outputs/co_citation_network" 
    
    run_co_citation_model(screening_csv, citation_csv, output_directory)