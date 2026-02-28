"""
申万行业指数市盈率市净率历史百分位分析脚本 - sw_daily版

使用Tushare sw_daily接口直接获取申万行业指数PE/PB数据
需要5000积分权限

使用方法:
    python industry_pe_pb_sw.py                    # 默认：一级行业，1年历史
    python industry_pe_pb_sw.py --level L2         # 二级行业
    python industry_pe_pb_sw.py --level L3         # 三级行业
    python industry_pe_pb_sw.py --years 3          # 3年历史
    python industry_pe_pb_sw.py --interval 10      # 每10天采样
"""

import tushare as ts
import pandas as pd
from datetime import datetime, timedelta
import time
import argparse
import os


# Tushare Token - 支持环境变量自定义
DEFAULT_TOKEN = '15bb21f848e2844fee6046746341f03079d4911b96fc80f1a48ee8da'
TOKEN = os.environ.get('TUSHARE_TOKEN', DEFAULT_TOKEN)

# API频率限制配置
REQUEST_INTERVAL = 0.3  # sw_daily接口频率限制较宽松
RATE_LIMIT_WAIT = 65


class TushareAPI:
    """Tushare API封装类"""
    
    def __init__(self, pro):
        self.pro = pro
        self.last_request_time = 0
        self.total_requests = 0
    
    def call_with_retry(self, api_func, api_name="未知API", max_retries=5, **kwargs):
        """带重试机制的API调用"""
        for attempt in range(max_retries):
            try:
                elapsed = time.time() - self.last_request_time
                if elapsed < REQUEST_INTERVAL:
                    time.sleep(REQUEST_INTERVAL - elapsed)
                
                result = api_func(**kwargs)
                self.last_request_time = time.time()
                self.total_requests += 1
                
                return result
                
            except Exception as e:
                error_msg = str(e)
                
                if "每分钟最多访问" in error_msg or "访问过于频繁" in error_msg:
                    print(f"⚠️  触发频率限制，等待{RATE_LIMIT_WAIT}秒...")
                    time.sleep(RATE_LIMIT_WAIT)
                    continue
                
                print(f"❌ API调用失败 (尝试 {attempt + 1}/{max_retries}): {error_msg}")
                time.sleep(2)
        
        return None


def get_industry_list(api, level='L1'):
    """
    获取申万行业列表
    
    参数:
        api: TushareAPI实例
        level: L1/L2/L3
    
    返回:
        DataFrame: 行业列表
    """
    # 使用 index_basic 获取申万指数列表
    all_df = api.call_with_retry(
        api.pro.index_basic,
        api_name="index_basic",
        market='SW'
    )
    
    if all_df is None or len(all_df) == 0:
        return None
    
    # 根据级别筛选
    if level == 'L1':
        # 一级行业：代码格式 801xx0.SI
        df = all_df[all_df['ts_code'].str.match(r'801\d{2}0\.SI')]
        df = df[df['name'].str.contains('申万')]
        # 排除特殊指数
        exclude_patterns = ['申万50', '申万中小', '申万A股', '申万创业', '申万300', 
                           '申万制造', '申万消费', '申万投资', '申万服务', '申万宏源']
        for pattern in exclude_patterns:
            df = df[~df['name'].str.contains(pattern)]
    
    elif level == 'L2':
        # 二级行业：代码格式 801xxx.SI (末尾不是0)
        df = all_df[all_df['ts_code'].str.match(r'801\d{3}\.SI')]
        df = df[~df['ts_code'].str.match(r'801\d{2}0\.SI')]  # 排除一级行业
        df = df[df['name'].str.contains('申万')]
        # 排除非行业指数
        exclude_patterns = ['申万50', '申万中小', '申万A股', '申万创业', '申万300', 
                           '申万宏源', '大盘指数', '中盘指数', '小盘指数',
                           '高市盈率', '中市盈率', '低市盈率',
                           '高市净率', '中市净率', '低市净率',
                           '高价股', '中价股', '低价股',
                           '亏损股', '微利股', '绩优股',
                           '配股指数', '活跃指数', '新股指数',
                           '基金重仓', '基金核心', '申万重点']
        for pattern in exclude_patterns:
            df = df[~df['name'].str.contains(pattern)]
        # 排除300系列指数（如300农林牧渔）
        df = df[~df['ts_code'].str.match(r'8013\d{2}\.SI')]
    
    elif level == 'L3':
        # 三级行业：代码格式 850xxx.SI
        df = all_df[all_df['ts_code'].str.match(r'850\d{3}\.SI')]
        df = df[df['name'].str.contains('申万')]
        # 排除非行业指数
        exclude_patterns = ['申万50', '申万中小', '申万A股', '申万创业', '申万300', '申万宏源']
        for pattern in exclude_patterns:
            df = df[~df['name'].str.contains(pattern)]
    
    else:
        df = None
    
    return df.reset_index(drop=True) if df is not None else None


def get_sw_daily_data(api, ts_code, start_date, end_date):
    """
    获取申万行业指数日行情数据（包含PE/PB）
    
    参数:
        api: TushareAPI实例
        ts_code: 指数代码
        start_date: 开始日期 (YYYYMMDD)
        end_date: 结束日期 (YYYYMMDD)
    
    返回:
        DataFrame: 日行情数据
    """
    df = api.call_with_retry(
        api.pro.sw_daily,
        api_name="sw_daily",
        ts_code=ts_code,
        start_date=start_date,
        end_date=end_date
    )
    
    return df


def calculate_percentile_rank(series, value):
    """计算数值在序列中的历史百分位"""
    if pd.isna(value) or len(series) == 0:
        return None
    
    clean_series = series.dropna()
    if len(clean_series) == 0:
        return None
    
    count_below = (clean_series < value).sum()
    count_equal = (clean_series == value).sum()
    percentile = (count_below + 0.5 * count_equal) / len(clean_series) * 100
    
    return round(percentile, 2)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='申万行业指数估值百分位分析 - sw_daily版')
    parser.add_argument('--years', type=int, default=1, help='回看历史年数 (默认1年)')
    parser.add_argument('--interval', type=int, default=0, 
                        help='采样间隔天数 (默认0表示使用全部数据)')
    parser.add_argument('--level', type=str, default='L1', choices=['L1', 'L2', 'L3'],
                        help='行业分类级别: L1-一级行业, L2-二级行业, L3-三级行业')
    parser.add_argument('--output', '-o', type=str, default='.',
                        help='输出目录路径 (默认当前目录)')
    args = parser.parse_args()
    
    # 初始化
    pro = ts.pro_api(TOKEN)
    api = TushareAPI(pro)
    
    level_names = {'L1': '一级行业', 'L2': '二级行业', 'L3': '三级行业'}
    
    print("=" * 70)
    print("申万行业指数市盈率市净率历史百分位分析 - sw_daily版")
    print("=" * 70)
    print()
    print("📊 使用接口: sw_daily (直接获取官方PE/PB数据)")
    print()
    print(f"📅 分析时间范围: 最近 {args.years} 年")
    print(f"📊 行业级别: {level_names[args.level]}")
    if args.interval > 0:
        print(f"📊 采样间隔: 每{args.interval}天")
    else:
        print(f"📊 采样间隔: 使用全部交易日数据")
    print()
    
    # 计算日期范围
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=args.years*365)).strftime('%Y%m%d')
    
    # 步骤1：获取行业列表
    print(f"【步骤1】获取申万{level_names[args.level]}列表...")
    industry_df = get_industry_list(api, args.level)
    
    if industry_df is None or len(industry_df) == 0:
        print(f"❌ 无法获取申万{level_names[args.level]}列表")
        return
    
    print(f"✅ 获取到 {len(industry_df)} 个{level_names[args.level]}")
    print(f"\n{level_names[args.level]}列表:")
    for _, row in industry_df.iterrows():
        print(f"  - {row['ts_code']}: {row['name']}")
    
    # 步骤2：获取各行业PE/PB历史数据
    print(f"\n【步骤2】获取各行业PE/PB历史数据...")
    
    results = []
    
    for i, row in industry_df.iterrows():
        ts_code = row['ts_code']
        name = row['name']
        
        print(f"  处理: {name} ({ts_code})")
        
        # 获取历史数据
        df = get_sw_daily_data(api, ts_code, start_date, end_date)
        
        if df is None or len(df) == 0:
            print(f"    ⚠️ 无数据")
            continue
        
        # 按日期排序
        df = df.sort_values('trade_date', ascending=False)
        
        # 采样（如果指定了间隔）
        if args.interval > 0:
            df = df.iloc[::args.interval].reset_index(drop=True)
        
        # 获取最新值
        latest = df.iloc[0]
        current_pe = latest['pe']
        current_pb = latest['pb']
        
        # 计算百分位
        pe_percentile = calculate_percentile_rank(df['pe'], current_pe)
        pb_percentile = calculate_percentile_rank(df['pb'], current_pb)
        
        results.append({
            'index_code': ts_code,
            'index_name': name,
            'pe': round(current_pe, 2) if pd.notna(current_pe) else None,
            'pe_percentile': pe_percentile,
            'pb': round(current_pb, 2) if pd.notna(current_pb) else None,
            'pb_percentile': pb_percentile,
            'sample_count': len(df),
            'latest_date': latest['trade_date']
        })
        
        pe_str = f"{current_pe:.2f}" if pd.notna(current_pe) else "N/A"
        pb_str = f"{current_pb:.2f}" if pd.notna(current_pb) else "N/A"
        print(f"    ✅ PE={pe_str} ({pe_percentile}%), PB={pb_str} ({pb_percentile}%)")
    
    # 步骤3：输出结果
    print("\n" + "=" * 70)
    print(f"申万{level_names[args.level]}估值百分位排名（按PE百分位从低到高）")
    print("=" * 70)
    
    if not results:
        print("❌ 无有效数据")
        return
    
    results_df = pd.DataFrame(results)
    # 按PE百分位升序排列，NaN值排在最后
    results_df = results_df.sort_values('pe_percentile', ascending=True, na_position='last')
    
    # 格式化输出
    print(f"{'排名':<4} {'行业代码':<12} {'行业名称':<20} {'PE':<10} {'PE百分位':<10} {'PB':<10} {'PB百分位':<10} {'数据点':<8}")
    print("-" * 90)
    
    for i, (_, row) in enumerate(results_df.iterrows(), 1):
        pe_str = f"{row['pe']:.2f}" if row['pe'] else "N/A"
        pb_str = f"{row['pb']:.2f}" if row['pb'] else "N/A"
        pe_pct_str = f"{row['pe_percentile']:.1f}%" if row['pe_percentile'] is not None else "N/A"
        pb_pct_str = f"{row['pb_percentile']:.1f}%" if row['pb_percentile'] is not None else "N/A"
        
        print(f"{i:<4} {row['index_code']:<12} {row['index_name']:<20} {pe_str:<10} {pe_pct_str:<10} {pb_str:<10} {pb_pct_str:<10} {row['sample_count']:<8}")
    
    # 保存结果
    output_dir = args.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 创建输出目录: {output_dir}")
    
    output_file = os.path.join(output_dir, f"industry_pe_pb_sw_{args.level}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    results_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✅ 结果已保存至: {output_file}")
    
    # 统计信息
    print(f"\n📊 统计信息:")
    print(f"   - API总调用次数: {api.total_requests}")
    print(f"   - 行业数量: {len(results_df)}")
    print(f"   - 分析起始日期: {start_date}")
    print(f"   - 分析结束日期: {end_date}")


if __name__ == '__main__':
    main()
