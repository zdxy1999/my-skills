#!/usr/bin/env python3
"""
申万行业估值分析执行脚本

功能：
1. 执行 L1、L2、L3 三个级别的行业估值分析（30年历史数据）
2. 清理7天前的分析文件
3. 生成汇总报告
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime, timedelta
import pandas as pd
import glob


def run_analysis(level, years=30, output_dir="./output"):
    """
    执行指定级别的行业估值分析

    参数:
        level: L1/L2/L3
        years: 历史年数
        output_dir: 输出目录

    返回:
        str: 生成的CSV文件路径，如果失败返回None
    """
    script_path = os.path.join(os.path.dirname(__file__), "industry_pe_pb_sw.py")

    if not os.path.exists(script_path):
        print(f"❌ 脚本文件不存在: {script_path}")
        return None

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 执行脚本
    cmd = [sys.executable, script_path, "--level", level, "--years", str(years), "--output", output_dir]

    print(f"\n{'='*70}")
    print(f"执行 {level} 行业分析")
    print(f"{'='*70}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
    except subprocess.CalledProcessError as e:
        print(f"❌ {level} 行业分析执行失败")
        return None

    # 查找最新生成的文件
    pattern = os.path.join(output_dir, f"industry_pe_pb_sw_{level}_*.csv")
    files = glob.glob(pattern)

    if not files:
        print(f"⚠️  未找到 {level} 分析结果文件")
        return None

    # 返回最新文件
    latest_file = max(files, key=os.path.getmtime)
    print(f"✅ {level} 分析完成: {latest_file}")
    return latest_file


def cleanup_old_files(output_dir="./output", days=7):
    """
    清理指定天数前的旧文件

    参数:
        output_dir: 输出目录
        days: 保留天数
    """
    cutoff_time = datetime.now() - timedelta(days=days)

    pattern = os.path.join(output_dir, "industry_pe_pb_sw_*.csv")
    files = glob.glob(pattern)

    cleaned_count = 0
    for file_path in files:
        file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        if file_time < cutoff_time:
            os.remove(file_path)
            cleaned_count += 1
            print(f"🗑️  删除旧文件: {os.path.basename(file_path)}")

    if cleaned_count > 0:
        print(f"\n✅ 已清理 {cleaned_count} 个超过 {days} 天的旧文件")
    else:
        print(f"\nℹ️  没有超过 {days} 天的旧文件需要清理")


def generate_summary_report(l1_file, l2_file, l3_file, output_dir="./output"):
    """
    生成汇总报告

    参数:
        l1_file: L1分析结果文件路径
        l2_file: L2分析结果文件路径
        l3_file: L3分析结果文件路径
        output_dir: 输出目录

    返回:
        str: 生成的报告文件路径
    """
    report_date = datetime.now().strftime('%Y%m%d')
    report_file = os.path.join(output_dir, f"valuation_report_{report_date}.md")

    with open(report_file, 'w', encoding='utf-8') as f:
        # 标题
        f.write(f"# 申万行业估值分析报告\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**数据来源**: Tushare sw_daily 接口\n\n")
        f.write(f"**历史跨度**: 30年\n\n")
        f.write("---\n\n")

        # 第一部分：本日估值概览
        f.write("## 第一部分：本日估值概览\n\n")

        for level, file_path, level_name in [
            ('L1', l1_file, '一级行业'),
            ('L2', l2_file, '二级行业'),
            ('L3', l3_file, '三级行业')
        ]:
            if file_path is None or not os.path.exists(file_path):
                f.write(f"### {level_name} - 无数据\n\n")
                continue

            df = pd.read_csv(file_path)
            df = df.sort_values('pe_percentile', ascending=True, na_position='last')

            f.write(f"### {level_name}\n\n")

            # Markdown 表格
            f.write("| 排名 | 行业代码 | 行业名称 | PE | PE百分位 | PB | PB百分位 | 数据点 | 最新日期 |\n")
            f.write("|------|----------|----------|----|---------|----|---------|-------|---------|\n")

            for idx, row in df.iterrows():
                pe_str = f"{row['pe']:.2f}" if pd.notna(row['pe']) else "N/A"
                pb_str = f"{row['pb']:.2f}" if pd.notna(row['pb']) else "N/A"
                pe_pct_str = f"{row['pe_percentile']:.1f}%" if pd.notna(row['pe_percentile']) else "N/A"
                pb_pct_str = f"{row['pb_percentile']:.1f}%" if pd.notna(row['pb_percentile']) else "N/A"
                latest_date_str = str(row['latest_date']) if pd.notna(row['latest_date']) else "N/A"

                # 标记高估/低估
                pe_valuation = ""
                if pd.notna(row['pe_percentile']):
                    if row['pe_percentile'] <= 20:
                        pe_valuation = " 🟢"
                    elif row['pe_percentile'] >= 80:
                        pe_valuation = " 🔴"

                pb_valuation = ""
                if pd.notna(row['pb_percentile']):
                    if row['pb_percentile'] <= 20:
                        pb_valuation = " 🟢"
                    elif row['pb_percentile'] >= 80:
                        pb_valuation = " 🔴"

                f.write(f"| {int(idx)+1} | {row['index_code']} | {row['index_name']} | {pe_str} | {pe_pct_str}{pe_valuation} | {pb_str} | {pb_pct_str}{pb_valuation} | {row['sample_count']} | {latest_date_str} |\n")

            # 汇总统计
            f.write(f"\n**{level_name}汇总**：\n\n")
            pe_low = df[df['pe_percentile'] <= 20].shape[0]
            pe_high = df[df['pe_percentile'] >= 80].shape[0]
            pb_low = df[df['pb_percentile'] <= 20].shape[0]
            pb_high = df[df['pb_percentile'] >= 80].shape[0]
            pe_median = df['pe_percentile'].median()
            pb_median = df['pb_percentile'].median()

            f.write(f"- 低估行业（PE ≤ 20%）：{pe_low} 个\n")
            f.write(f"- 高估行业（PE ≥ 80%）：{pe_high} 个\n")
            f.write(f"- 低估行业（PB ≤ 20%）：{pb_low} 个\n")
            f.write(f"- 高估行业（PB ≥ 80%）：{pb_high} 个\n")
            f.write(f"- PE 百分位中位数：{pe_median:.1f}%\n")
            f.write(f"- PB 百分位中位数：{pb_median:.1f}%\n\n")

        # 第二部分：七日趋势变化
        f.write("---\n\n")
        f.write("## 第三部分：七日趋势变化\n\n")

        f.write("### PE 百分位变化（超过 10%）\n\n")
        f.write("| 行业级别 | 行业名称 | 当前百分位 | 7日前百分位 | 变化 |\n")
        f.write("|----------|----------|-----------|------------|------|\n")

        has_pe_change = False
        for level, file_path, level_name in [
            ('L1', l1_file, '一级行业'),
            ('L2', l2_file, '二级行业'),
            ('L3', l3_file, '三级行业')
        ]:
            if file_path is None or not os.path.exists(file_path):
                continue

            # 获取当前数据
            df_current = pd.read_csv(file_path)

            # 查找7天前的数据
            cutoff_time = datetime.now() - timedelta(days=7)
            pattern = os.path.join(output_dir, f"industry_pe_pb_sw_{level}_*.csv")
            old_files = [f for f in glob.glob(pattern)
                        if datetime.fromtimestamp(os.path.getmtime(f)) < cutoff_time]

            if old_files:
                df_old_file = max(old_files, key=os.path.getmtime)
                df_old = pd.read_csv(df_old_file)

                # 比较变化
                merged = pd.merge(df_current[['index_name', 'pe_percentile']],
                                 df_old[['index_name', 'pe_percentile']],
                                 on='index_name', suffixes=('_current', '_old'))

                # 找出变化超过10%的
                merged['pe_change'] = merged['pe_percentile_current'] - merged['pe_percentile_old']
                large_changes = merged[abs(merged['pe_change']) >= 10]

                for _, row in large_changes.iterrows():
                    change_arrow = "📈" if row['pe_change'] > 0 else "📉"
                    f.write(f"| {level_name} | {row['index_name']} | {row['pe_percentile_current']:.1f}% | {row['pe_percentile_old']:.1f}% | {change_arrow} {row['pe_change']:+.1f}% |\n")
                    has_pe_change = True

        if not has_pe_change:
            f.write("| - | 无显著变化 | - | - | - |\n")

        f.write("\n### PB 百分位变化（超过 10%）\n\n")
        f.write("| 行业级别 | 行业名称 | 当前百分位 | 7日前百分位 | 变化 |\n")
        f.write("|----------|----------|-----------|------------|------|\n")

        has_pb_change = False
        for level, file_path, level_name in [
            ('L1', l1_file, '一级行业'),
            ('L2', l2_file, '二级行业'),
            ('L3', l3_file, '三级行业')
        ]:
            if file_path is None or not os.path.exists(file_path):
                continue

            # 获取当前数据
            df_current = pd.read_csv(file_path)

            # 查找7天前的数据
            cutoff_time = datetime.now() - timedelta(days=7)
            pattern = os.path.join(output_dir, f"industry_pe_pb_sw_{level}_*.csv")
            old_files = [f for f in glob.glob(pattern)
                        if datetime.fromtimestamp(os.path.getmtime(f)) < cutoff_time]

            if old_files:
                df_old_file = max(old_files, key=os.path.getmtime)
                df_old = pd.read_csv(df_old_file)

                # 比较变化
                merged = pd.merge(df_current[['index_name', 'pb_percentile']],
                                 df_old[['index_name', 'pb_percentile']],
                                 on='index_name', suffixes=('_current', '_old'))

                # 找出变化超过10%的
                merged['pb_change'] = merged['pb_percentile_current'] - merged['pb_percentile_old']
                large_changes = merged[abs(merged['pb_change']) >= 10]

                for _, row in large_changes.iterrows():
                    change_arrow = "📈" if row['pb_change'] > 0 else "📉"
                    f.write(f"| {level_name} | {row['index_name']} | {row['pb_percentile_current']:.1f}% | {row['pb_percentile_old']:.1f}% | {change_arrow} {row['pb_change']:+.1f}% |\n")
                    has_pb_change = True

        if not has_pb_change:
            f.write("| - | 无显著变化 | - | - | - |\n")

        # 特别提醒
        f.write("\n### ⚠️ 特别提醒\n\n")
        f.write("- 🟢 表示低估（百分位 ≤ 20%），可能存在投资机会\n")
        f.write("- 🔴 表示高估（百分位 ≥ 80%），需要注意风险\n")
        f.write("- 估值判断需结合行业特性，成长性行业可能长期维持较高估值\n")
        f.write("- 百分位变化超过 10% 需要特别关注\n\n")

        f.write("---\n\n")
        f.write(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

    print(f"\n{'='*70}")
    print(f"✅ 汇总报告已生成: {report_file}")
    print(f"{'='*70}")

    return report_file


def main():
    parser = argparse.ArgumentParser(description='申万行业估值分析执行脚本')
    parser.add_argument('--token', '-t', type=str, help='Tushare Token (不指定则使用环境变量或默认值)')
    parser.add_argument('--output', '-o', type=str, default='./output', help='输出目录路径 (默认 ./output)')
    parser.add_argument('--cleanup-days', '-c', type=int, default=365, help='清理多少天前的旧文件 (默认 365)')
    args = parser.parse_args()

    # 设置 token
    if args.token:
        os.environ['TUSHARE_TOKEN'] = args.token
        print(f"✅ 使用命令行指定的 Token")

    # 输出目录
    output_dir = args.output

    # 步骤1：清理旧文件
    print("\n" + "="*70)
    print("步骤1：清理旧文件")
    print("="*70)
    cleanup_old_files(output_dir, args.cleanup_days)

    # 步骤2：执行三级分析
    print("\n" + "="*70)
    print("步骤2：执行行业估值分析")
    print("="*70)

    l1_file = run_analysis('L1', years=30, output_dir=output_dir)
    l2_file = run_analysis('L2', years=30, output_dir=output_dir)
    l3_file = run_analysis('L3', years=30, output_dir=output_dir)

    # 步骤3：生成汇总报告
    print("\n" + "="*70)
    print("步骤3：生成汇总报告")
    print("="*70)

    generate_summary_report(l1_file, l2_file, l3_file, output_dir)

    print("\n" + "="*70)
    print("✅ 所有任务完成！")
    print("="*70)


if __name__ == '__main__':
    main()
