# DuckDB 插件下载器

一个用于下载指定版本和架构的 DuckDB 插件的 Python 工具。该工具支持多线程下载，并能恢复中断的下载。

## 特性

- 从 YAML 文件加载配置。
- 通过命令行参数覆盖配置。
- 获取指定 DuckDB 版本和架构的插件列表。
- 支持恢复中断下载。
- 多线程下载功能。

## 支持的架构

- `linux_amd64`
- `linux_amd64_gcc4`
- `linux_arm64`
- `windows_amd64`
- `osx_amd64`
- `osx_arm64`

## 先决条件

- Python 3.6 或更高版本
- 所需库：
  - `requests`
  - `duckdb`
  - `yaml`
  - `tqdm`

您可以使用 pip 安装所需的库：

```bash
pip install -r requirements.txt
```

## 配置

创建一个 `config.yaml` 文件，结构如下：

```yaml
version: "your_duckdb_version"
arch: "linux_amd64"  # 或其他支持的架构
plugin_name: "all"   # 或指定一个插件名称
thread_num: 4        # 可选，默认是 CPU 数量的一半
save_dir: "./plugins"  # 下载插件的保存目录
```

## 使用方法

通过命令行运行脚本：

```bash
python download_plugins.py --version <version> --arch <architecture> --plugin_name <plugin_name> --thread_num <number_of_threads> --save_dir <save_directory>
```

您也可以不带任何参数运行它，以使用 `config.yaml` 中指定的配置。

## 日志记录

下载进度和任何问题将记录到 `download.log` 文件中。

## 许可证

该项目遵循 MIT 许可证。

## 贡献

欢迎提交问题或拉取请求！