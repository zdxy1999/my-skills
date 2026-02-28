---
name: china-industry-valuation
description: 执行申万行业PE PB估值分析脚本，生成行业估值报告和趋势分析。使用时当用户需要获取A股行业估值数据、分析PE/PB历史百分位、生成行业估值报告时触发。
---

# China Industry Valuation

执行申万行业指数市盈率(PE)和市净率(PB)估值分析，生成完整的历史百分位分析报告和趋势汇总。

## When to use

当用户以下情况时使用此 skill：
- 需要获取申万行业指数的PE/PB估值数据
- 需要分析A股行业的估值水平（高估/低估判断）
- 需要生成行业估值历史百分位报告
- 需要跟踪行业估值趋势变化
- 用户提到"行业估值"、"申万行业"、"PE PB分析"

## Prerequisites

### 1. 安装 Python 依赖

```bash
pip install tushare pandas
```

### 2. 配置 Tushare Token

可以通过环境变量设置（推荐）：

```bash
export TUSHARE_TOKEN="your_token_here"
```

或者直接在执行时作为参数传入。

获取 Token：注册 [Tushare](https://tushare.pro/) 账号后，在个人中心获取。

**注意**：需要 5000+ 积分权限才能使用 `sw_daily` 接口。

## Instructions

### 工作流程

执行以下步骤生成完整的行业估值报告：

1. **获取当前日期**
   - 获取今天的日期作为分析基准日

2. **执行三级行业分析**
   - 对 L1（一级）、L2（二级）、L3（三级）行业分别执行分析
   - 时间跨度设置为 30 年历史数据
   - 输出 CSV 文件到 `assets/output/` 目录

3. **清理过期文件**
   - 删除 7 天前的分析文件
   - 保留最近 7 天的历史数据用于趋势分析

4. **生成汇总报告**
   - 创建 `assets/output/valuation_report_YYYYMMDD.md` 汇总报告

### 执行命令

#### 方式 1：使用环境变量（推荐）

```bash
export TUSHARE_TOKEN="your_token_here"
python assets/run_valuation.py
```

#### 方式 2：命令行参数

```bash
python assets/run_valuation.py --token "your_token_here"
```

#### 方式 3：指定输出目录

```bash
python assets/run_valuation.py --output ./output
python assets/run_valuation.py --output /path/to/custom/output
```

#### 方式 4：使用内置默认 token

```bash
python assets/run_valuation.py
```

### 可用参数

| 参数 | 短参数 | 说明 | 默认值 |
|------|--------|------|--------|
| `--token` | `-t` | Tushare Token（不指定则使用环境变量或默认值） | - |
| `--output` | `-o` | 输出目录路径 | `./output` |
| `--cleanup-days` | `-c` | 清理多少天前的旧文件 | `7` |

### 汇总报告结构

生成的 `valuation_report_YYYYMMDD.md` 包含以下部分：

#### 第一部分：本日估值概览

完整的表格数据，包含所有行业的：
- 行业代码、名称
- 当前 PE 值、PE 历史百分位
- 当前 PB 值、PB 历史百分位
- 最新数据日期

**估值判断标准**：
- PE 百分位 ≤ 20%：低估（绿色）
- PE 百分位 ≥ 80%：高估（橙色）
- 20% < PE 百分位 < 80%：中间估值（灰色）
- PB 百分位 ≤ 20%：低估（绿色）
- PB 百分位 ≥ 80%：高估（橙色）
- 20% < PB 百分位 < 80%：中间估值（灰色）

根据行业特性，某些高成长的行业可能长期维持较高估值，需结合行业分析。

#### 第二部分：行业估值汇总分析

对 L1、L2、L3 三个级别的结果进行汇总分析：
- 低估行业列表（PE 或 PB 百分位 ≤ 20%）
- 高估行业列表（PE 或 PB 百分位 ≥ 80%）
- 中位数估值水平统计

#### 第三部分：七日趋势变化

分析最近 7 天的估值变化：
- PE 百分位变化超过 10% 的行业（标注上升/下降）
- PB 百分位变化超过 10% 的行业（标注上升/下降）
- 重点提示变化异常大的行业（列出具体数据和变化值）

## File Structure

```
china_industry_valuation/
├── SKILL.md                     # Skill 主文件
├── assets/
│   ├── industry_pe_pb_sw.py     # 原始分析脚本
│   ├── run_valuation.py         # 执行脚本（主入口）
│   ├── generate_report.py      # 报告生成脚本
│   ├── README.md                # 脚本说明文档
│   └── output/                  # 输出目录
│       ├── industry_pe_pb_sw_L1_*.csv
│       ├── industry_pe_pb_sw_L2_*.csv
│       ├── industry_pe_pb_sw_L3_*.csv
│       └── valuation_report_*.md
```

## Troubleshooting

### 权限不足

如果提示"抱歉，您没有访问该接口的权限"：
- 确认 Tushare 账号积分是否达到 5000+
- 确认 Token 是否正确配置

### 频率限制与网络连接

- 脚本内置了频率限制处理机制，会自动等待后重试
- 首次运行过程中可能出现偶发的网络连接错误（如 "Max retries exceeded"），脚本会自动重试并继续执行
- 如频繁触发频率限制，可适当增加 `REQUEST_INTERVAL` 参数值

### 部分行业无数据

某些退市或新成立的行业指数可能无 30 年历史数据，脚本会自动跳过并记录警告：
- 退市行业可能只有部分历史数据，最新数据日期较早
- 新成立行业可能数据点较少

### 输出目录位置

- 默认输出目录为脚本运行目录下的 `./output/`（通常是项目根目录）
- 如果需要在特定目录输出，使用 `--output` 参数：
  ```bash
  python assets/run_valuation.py --output /path/to/output
  ```

### 七日趋势变化无数据

- **首次运行**：由于没有历史数据，七日趋势变化部分会显示"无显著变化"，这是正常现象
- 需要至少运行两次（间隔超过7天）才能看到趋势对比数据
- 只有变化超过 10% 的行业才会被列出

### 行业数量说明

- L1（一级行业）：约 30-40 个
- L2（二级行业）：约 180-200 个
- L3（三级行业）：约 150-160 个
- 部分行业标记为"(退市)"，但仍包含在分析中供参考

## References

- [Tushare 接口文档](https://tushare.pro/document/2?doc_id=131)
- [申万宏源指数](http://www.swsindex.com/)
- 脚本详细说明：`assets/README.md`
