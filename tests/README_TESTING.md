# 测试说明

本文件描述如何运行 MultiModelLocalization 项目的测试套件。

## 测试环境配置

### 1. 安装依赖

首先确保安装了所有必要的依赖：

```bash
pip install -r requirements.txt
```

### 2. 运行测试

有几种方式运行测试：

#### 方式一：使用测试脚本（推荐）
```bash
python run_tests.py
```

#### 方式二：直接使用pytest
```bash
python -m pytest tests/test_translators.py -v
```

#### 方式三：运行特定测试
```bash
python -m pytest tests/test_translators.py::TestTranslators::test_config_default_values -v
```

### 3. 测试覆盖率

如果想查看测试覆盖率：

```bash
python -m pytest tests/test_translators.py --cov=src --cov-report=html
```

## 测试说明

### 测试文件结构
- `tests/test_translators.py` - 主测试文件，包含翻译器相关的单元测试
- `tests/test_config.yaml` - 测试用的配置文件
- `run_tests.py` - 测试运行脚本

### 测试内容

当前的测试套件包括：

1. **LocalizationConfig 测试**
   - 配置文件加载
   - 默认值处理
   - 配置项访问

2. **TranslatorFactory 测试**
   - 支持的翻译器类型创建
   - 不支持类型的错误处理
   - 配置参数传递

3. **集成测试**
   - 使用项目配置文件的测试
   - 依赖处理（处理可选依赖缺失的情况）

### 依赖处理

由于项目使用了多个可选的翻译服务依赖（如 volcenginesdkarkruntime），测试代码经过特殊处理：

- 当某些依赖缺失时，测试不会失败
- 只测试核心逻辑，不强制要求所有翻译器都能初始化
- 使用模拟和存根来避免网络依赖

## 故障排除

### 常见问题

1. **ModuleNotFoundError: No module named 'xxx'**
   - 解决方案：运行 `pip install -r requirements.txt` 安装依赖

2. **测试超时或挂起**
   - 可能是网络连接问题
   - 某些测试会尝试初始化翻译器客户端，如果网络不佳可能会超时

3. **导入错误**
   - 确保项目路径设置正确
   - 检查 Python 环境是否正确激活

### 开发测试

在开发过程中，建议：
- 每次修改代码后运行测试
- 添加新功能时同步添加测试用例
- 使用 `--tb=short` 参数获取简洁的错误信息

## 测试配置文件修改

如果需要修改测试配置，编辑 `tests/test_config.yaml` 文件。注意：
- 测试使用的是模拟配置，不会进行真实的API调用
- API密钥等敏感信息使用测试用的虚拟值

## 贡献指南

添加新测试时：
1. 在 `tests/test_translators.py` 中添加新的测试方法
2. 遵循现有的命名约定（`test_` 前缀）
3. 使用有意义的测试描述字符串
4. 确保测试是独立的，不依赖其他测试的状态
