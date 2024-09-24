# DuckDB Plugin Downloader

A Python utility for downloading DuckDB plugins based on specified versions and architectures. This tool supports multi-threaded downloads and can resume interrupted downloads.

## Features

- Load configurations from a YAML file.
- Override configurations with command-line arguments.
- Fetch plugins for specified DuckDB versions and architectures.
- Support for resuming downloads if interrupted.
- Multi-threaded download capability.

## Supported Architectures

- `linux_amd64`
- `linux_amd64_gcc4`
- `linux_arm64`
- `windows_amd64`
- `osx_amd64`
- `osx_arm64`

## Prerequisites

- Python 3.6 or later
- Required libraries:
  - `requests`
  - `duckdb`
  - `yaml`
  - `tqdm`

You can install the necessary libraries using pip:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `config.yaml` file with the following structure:

```yaml
version: "your_duckdb_version"
arch: "linux_amd64"  # or another supported architecture
plugin_name: "all"   # or specify a plugin name
thread_num: 4        # optional, default is half the CPU count
save_dir: "./plugins"  # directory to save downloaded plugins
```

## Usage

Run the script with the command line:

```bash
python download_plugins.py --version <version> --arch <architecture> --plugin_name <plugin_name> --thread_num <number_of_threads> --save_dir <save_directory>
```

You can also run it without any arguments to use the configurations specified in `config.yaml`.

## Logging

Download progress and any issues will be logged to `download.log`.

## License

This project is licensed under the MIT License.

## Contribution

Feel free to submit issues or pull requests!

## Chinese README

For a Chinese version of this README, [click here](readme_cn.md).
