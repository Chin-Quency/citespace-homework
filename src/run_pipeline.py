"""
自动化流水线脚本
按顺序执行：citespace -> filter -> evidence_chain -> evidence_analyze
可选执行：extract_citations -> co_citation
"""
import os
import sys
import argparse

# 计算项目根目录和关键路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")

# 确保 outputs 目录存在
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# 将 src 目录加入模块搜索路径
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)


def step_citespace():
    """Step 1: 加载 WoS 数据并统计字段缺失率"""
    import citespace
    print("\n" + "=" * 60)
    print("Step 1/4: 加载 WoS 数据 & 字段统计 (citespace.py)")
    print("=" * 60)

    df = citespace.load_wos_data_folder(DATA_DIR)
    stats = citespace.get_data_stats(df)
    print("数据规模:", len(df))
    print("\n字段统计：")
    print(stats)

    stats.to_csv(os.path.join(OUTPUTS_DIR, "field_stats.csv"), encoding="utf-8-sig")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    missing_rate = df.isnull().sum() / len(df)
    missing_rate.plot(kind="bar", title="Missing Rate per Field")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUTS_DIR, "field_missing_rate.png"), dpi=150)
    plt.close()
    print("图表已保存至 outputs/field_missing_rate.png")


def step_filter():
    """Step 2: PRISMA 筛选"""
    import filter
    print("\n" + "=" * 60)
    print("Step 2/4: PRISMA 筛选 (filter.py)")
    print("=" * 60)

    filter.run_screening(
        DATA_DIR,
        os.path.join(OUTPUTS_DIR, "screening_results.csv"),
        os.path.join(OUTPUTS_DIR, "download_included_for_citespace.txt"),
    )


def step_evidence_chain():
    """Step 3: 证据链特征提取"""
    import evidence_chain
    print("\n" + "=" * 60)
    print("Step 3/4: 证据链特征提取 (evidence_chain.py)")
    print("=" * 60)

    evidence_chain.generate_evidence_chain_from_csv(
        os.path.join(OUTPUTS_DIR, "screening_results.csv"),
        os.path.join(OUTPUTS_DIR, "evidence_raw_data.csv"),
    )


def step_evidence_analyze():
    """Step 4: 证据链统计分析"""
    import evidence_analyze
    print("\n" + "=" * 60)
    print("Step 4/4: 证据链统计分析 (evidence_analyze.py)")
    print("=" * 60)

    evidence_analyze.analyze_evidence_statistics(
        os.path.join(OUTPUTS_DIR, "evidence_raw_data.csv"),
    )


def step_extract_citations():
    """Step 5 (可选): 提取引文边表"""
    import extract_citations
    print("\n" + "=" * 60)
    print("Step 5/6 [可选]: 提取引文边表 (extract_citations.py)")
    print("=" * 60)

    extract_citations.parse_wos_citations(
        os.path.join(OUTPUTS_DIR, "download_included_for_citespace.txt"),
        os.path.join(DATA_DIR, "merged_with_citations.csv"),
    )


def step_co_citation():
    """Step 6 (可选): 共被引矩阵分析"""
    import co_citation
    print("\n" + "=" * 60)
    print("Step 6/6 [可选]: 共被引矩阵分析 (co_citation.py)")
    print("=" * 60)

    co_citation.run_co_citation_model(
        os.path.join(OUTPUTS_DIR, "screening_results.csv"),
        os.path.join(DATA_DIR, "merged_with_citations.csv"),
        os.path.join(OUTPUTS_DIR, "co_citation_network"),
    )


def main():
    parser = argparse.ArgumentParser(description="文献计量分析自动化流水线")
    parser.add_argument(
        "--with-co-citation",
        action="store_true",
        help="运行可选的共被引矩阵分析（耗时较长）",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  文献计量分析流水线")
    print(f"  项目根目录: {PROJECT_ROOT}")
    print(f"  数据目录:   {DATA_DIR}")
    print(f"  输出目录:   {OUTPUTS_DIR}")
    print("=" * 60)

    # 主流水线
    step_citespace()
    step_filter()
    step_evidence_chain()
    step_evidence_analyze()

    # 可选步骤
    if args.with_co_citation:
        step_extract_citations()
        step_co_citation()
    else:
        print("\n" + "-" * 60)
        print("提示: 添加 --with-co-citation 参数可运行共被引矩阵分析")
        print("  例: python run_pipeline.py --with-co-citation")
        print("-" * 60)

    print("\n" + "=" * 60)
    print("  流水线执行完毕！所有结果已保存至 outputs/ 目录")
    print("=" * 60)


if __name__ == "__main__":
    main()
