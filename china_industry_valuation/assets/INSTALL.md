# 依赖安装说明

## Python 依赖

运行申万行业估值分析脚本需要以下 Python 包：

```bash
pip install tushare pandas
```

## 详细说明

### tushare

用于获取申万行业指数的 PE/PB 数据。

```bash
pip install tushare
```

**注意**：需要 5000+ 积分权限才能使用 `sw_daily` 接口。

### pandas

用于数据处理和 CSV 文件的读写。

```bash
pip install pandas
```

## 一次性安装

可以直接执行以下命令一次性安装所有依赖：

```bash
pip install tushare pandas
```

## 验证安装

安装完成后，可以运行以下命令验证：

```bash
python -c "import tushare; import pandas; print('依赖安装成功！')"
```

如果输出 `依赖安装成功！`，说明安装成功。

## 常见问题

### 权限不足

如果提示安装权限不足，可以尝试：

```bash
pip install --user tushare pandas
```

### 虚拟环境

建议使用虚拟环境：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install tushare pandas
```

### Tushare Token 配置

安装完成后，还需要配置 Tushare Token：

1. 注册 [Tushare](https://tushare.pro/) 账号
2. 在个人中心获取 Token
3. 设置环境变量：

```bash
export TUSHARE_TOKEN="your_token_here"
```

或者在运行时通过命令行参数传入：

```bash
python assets/run_valuation.py --token "your_token_here"
```
