# main.py
import argparse
from fraud_research_agent.agent.orchestrator import orchestrator


def main():
    parser = argparse.ArgumentParser(description="Fraud Research Agent 主程序入口")
    parser.add_argument(
        "--topic",
        type=str,
        required=True,
        help="用户研究主题，例如 'fraud detection behavior sequence'"
    )

    args = parser.parse_args()

    # 执行 orchestrator
    result = orchestrator(args.topic)

    # 输出结果概要
    print("\n=== 最终执行结果 ===")
    print(f"分类映射: {result['field_mapping']}")
    print(f"清洗后论文数量: {len(result['clean_papers'])}")
    print(f"研究报告:\n{result['report']}")


if __name__ == "__main__":
    main()
