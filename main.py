import yaml
import duckdb
import requests
import multiprocessing
import os
from tqdm import tqdm
import logging
import argparse

# 定义支持的架构
SUPPORTED_ARCHS = ['linux_amd64', 'linux_amd64_gcc4', 'linux_arm64', 'windows_amd64', 'osx_amd64', 'osx_arm64']

# 配置日志
logging.basicConfig(filename='download.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_config(config_file="config.yaml"):
    """加载配置文件，并用命令行参数覆盖"""
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    parser = argparse.ArgumentParser()
    parser.add_argument("--version", type=str, help="DuckDB version")
    parser.add_argument("--arch", type=str, choices=SUPPORTED_ARCHS, help="Target architecture")
    parser.add_argument("--plugin_name", type=str, help="Plugin name")
    parser.add_argument("--thread_num", type=int, help="Number of threads")
    parser.add_argument("--save_dir", type=str, help="Save directory")
    args = parser.parse_args()

    # 命令行参数覆盖配置文件
    for key, value in vars(args).items():
        if value:
            config[key] = value

    return config


def get_plugin_list(version, arch):
    """获取指定版本和架构的插件列表"""
    query = f"SELECT extension_name FROM duckdb_extensions()"
    result = duckdb.sql(query).fetchall()
    base_url = f"http://extensions.duckdb.org/{version}/{arch}/"
    plugins = [{"name": row[0], "version": version, "arch": arch, "url": f"{base_url}{row[0]}.duckdb_extension.gz"} for
               row in result]
    return plugins


def download_plugin(plugin, save_dir):
    """下载插件，支持断点续传"""
    os.makedirs(os.path.join(save_dir, plugin['version'], plugin['arch']), exist_ok=True)
    file_path = os.path.join(save_dir, plugin['version'], plugin['arch'], plugin['url'].split('/')[-1])
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        headers = {'Range': f'bytes={file_size}-'}
        logging.info(f"Resuming download for {plugin['name']}")
    else:
        file_size = 0
        headers = {}

    response = requests.get(plugin['url'], stream=True, headers=headers)
    total = int(response.headers.get('content-length', 0))
    with open(file_path, 'ab') as f:
        with tqdm(desc=plugin['name'], total=total, initial=file_size, unit='iB',
                  unit_scale=True) as pbar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
    logging.info(f"Downloaded {plugin['name']} successfully.")


def multithread_download(plugins, save_dir, thread_num=None):
    """多线程下载插件"""
    if thread_num is None:
        thread_num = os.cpu_count() // 2
    with multiprocessing.Pool(processes=thread_num) as pool:
        pool.starmap(download_plugin, [(p, save_dir) for p in plugins])


if __name__ == "__main__":
    config = load_config()

    version = config['version']
    arch = config['arch']
    plugin_name = config['plugin_name']
    thread_num = config['thread_num']
    save_dir = config['save_dir']

    # 下载所有架构的插件
    if plugin_name == 'all':
        all_plugins = []
        for arch in SUPPORTED_ARCHS:
            all_plugins.extend(get_plugin_list(version, arch))
        plugins = all_plugins
    else:
        plugins = get_plugin_list(version, arch)
        if plugin_name:
            plugins = [p for p in plugins if p['name'] == plugin_name]

    multithread_download(plugins, save_dir, thread_num)
