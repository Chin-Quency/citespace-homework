import pandas as pd
import numpy as np
from pathlib import Path


def load_citation_edges(csv_path):
    encodings = ["utf-8-sig", "utf-8", "gbk", "latin1"]
    df = None
    for enc in encodings:
        try:
            df = pd.read_csv(csv_path, encoding=enc)
            break
        except:
            continue

    required = ["citing_paper", "cited_paper"]
    if not all(c in df.columns for c in required):
        raise Exception("必须包含 citing_paper 和 cited_paper 列")

    df = df.dropna(subset=required)
    df["citing_paper"] = df["citing_paper"].astype(str).str.strip()
    df["cited_paper"] = df["cited_paper"].astype(str).str.strip()
    df = df[df["citing_paper"] != ""]
    df = df[df["cited_paper"] != ""]
    df = df.drop_duplicates()
    return df


def build_citation_matrix(edges):
    R = edges.pivot_table(
        index="citing_paper",
        columns="cited_paper",
        values="cited_paper",
        aggfunc=lambda x: 1,
        fill_value=0
    )
    return R


def build_co_citation_matrix(R):
    C = np.dot(R.T, R)
    C = pd.DataFrame(C, index=R.columns, columns=R.columns)
    np.fill_diagonal(C.values, 0)  # 去掉自环
    return C


def cosine_similarity_matrix(C):
    X = C.values
    norm = np.linalg.norm(X, axis=1, keepdims=True)
    norm[norm == 0] = 1
    sim = np.dot(X, X.T) / (norm * norm.T)
    sim = np.nan_to_num(sim)
    sim_df = pd.DataFrame(sim, index=C.index, columns=C.columns)
    np.fill_diagonal(sim_df.values, 0)
    return sim_df


def matrix_to_edges(matrix, min_weight=0.01):
    nodes = list(matrix.index)
    arr = matrix.values
    edges = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            w = arr[i, j]
            if w >= min_weight:
                edges.append([nodes[i], nodes[j], w])
    return pd.DataFrame(edges, columns=["source", "target", "weight"])


def run_co_citation_model(csv_path, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    print("读取引用数据...")
    edges = load_citation_edges(csv_path)

    print("构建引用矩阵 R...")
    R = build_citation_matrix(edges)

    print("构建共被引矩阵 C...")
    C = build_co_citation_matrix(R)

    print("计算余弦相似度...")
    sim = cosine_similarity_matrix(C)

    print("生成共被引网络边表...")
    edge_list = matrix_to_edges(sim, min_weight=0.1)

    # 保存全部结果
    R.to_csv(output_dir / "citation_matrix_R.csv", encoding="utf-8-sig")
    C.to_csv(output_dir / "co_citation_matrix_C.csv", encoding="utf-8-sig")
    sim.to_csv(output_dir / "similarity_matrix.csv", encoding="utf-8-sig")
    edge_list.to_csv(output_dir / "co_citation_edges.csv", index=False, encoding="utf-8-sig")

    print("\n 共被引网络建模完成")
    print(f"引用矩阵 R: {R.shape}")
    print(f"共被引矩阵 C: {C.shape}")
    print(f"网络边数: {len(edge_list)}")
    print(f"输出文件已保存到: {output_dir}")


if __name__ == "__main__":
    csv_path = "data/merged_with_citations.csv"
    output_dir = "data/co_citation_network"
    run_co_citation_model(csv_path, output_dir)
