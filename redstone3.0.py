#by hshml123
#bilibili： https://space.bilibili.com/3546671824767138

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import os
import json
import subprocess
from PIL import Image, ImageTk
from io import BytesIO
import threading
import sys
import ttkbootstrap as ttk  # 替换原来的ttk
from ttkbootstrap.constants import *  # 导入常量
from ttkbootstrap.style import Style
import logging
from datetime import datetime

class MinecraftLauncher:
    def __init__(self, root):
        # 在__init__开头添加日志配置
        self.setup_logging()
        # 使用ttkbootstrap主题
        self.style = Style(theme='darkly')  # 可选主题: cosmo, flatly, litera, minty, lumen, sandstone, yeti, pulse等
        self.root = root
        self.root.title("Minecraft Redstone Launcher")
        self.root.geometry("900x700")
        
        # 设置背景色
        self.root.configure(bg='#2b2b2b')
        
        # 检查并加载配置
        self.config = self.load_config()
        if not self.config:  # 如果没有配置文件，则生成默认配置
            self.create_default_config()

        # 状态栏
        self.status_bar = ttk.Label(root, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 进度条
        self.progress = ttk.Progressbar(root, length=300, mode='determinate')
        self.progress.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # 创建主框架和标签页
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # 启动页面
        self.launch_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.launch_frame, text="启动游戏")
        
        # 设置页面
        self.settings_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.settings_frame, text="设置")

        # 添加默认路径
        self.default_minecraft_paths = self.get_default_minecraft_paths()
        self.default_java_paths = self.get_default_java_paths()

        # 创建界面
        self.setup_launch_page()
        self.setup_settings_page()  # 确保在这里调用

        # 在加载配置后立即自动检测游戏目录
        if not self.config.get('game_dir'):
            self.auto_detect_minecraft()  # 确保在这里调用

        # 设置在线图标
        try:
            icon_url = "https://www.helloimg.com/i/2024/11/27/674728eec2b72.ico"
            response = requests.get(icon_url)
            icon_data = BytesIO(response.content)
            icon_image = Image.open(icon_data)
            icon_photo = ImageTk.PhotoImage(icon_image)
            
            # 设置窗口和任务栏图标
            self.root.iconphoto(True, icon_photo)  # 设置窗口图标
            self.root.iconbitmap(icon_url)
        except Exception as e:
            print(f"无法加载在线图标: {e}")

        # 在创建界面后刷新版本列表
        self.refresh_versions()

    def setup_logging(self):
        """配置日志系统"""
        # 创建logs文件夹
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # 设置日志文件名（使用当前时间）
        log_file = f'logs/minecraft_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        
        # 配置日志
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("启动器初始化开始")

    def setup_launch_page(self):
        # 用户信息框架
        user_frame = ttk.LabelFrame(self.launch_frame, text="用户信息", padding="10")
        user_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10, padx=10)
        
        ttk.Label(user_frame, text="用户名:", font=('Arial', 10)).grid(row=0, column=0, pady=10, padx=5)
        self.username = ttk.Entry(user_frame, width=30, style='primary')
        self.username.grid(row=0, column=1, pady=10, padx=5)
        self.username.insert(0, self.config.get('username', ''))
        
        # 游戏设置框架
        game_frame = ttk.LabelFrame(self.launch_frame, text="游戏设置", padding="10")
        game_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10, padx=10)
        
        ttk.Label(game_frame, text="游戏版本:", font=('Arial', 10)).grid(row=0, column=0, pady=10, padx=5)
        self.version = ttk.Combobox(game_frame, values=[], style='primary')
        self.version.grid(row=0, column=1, pady=10, padx=5)
        self.version.set(self.config.get('version', ''))
        
        # 添加刷新版本按钮
        refresh_btn = ttk.Button(
            game_frame, 
            text="刷新版本", 
            style='info.TButton',
            command=self.refresh_versions
        )
        refresh_btn.grid(row=0, column=2, pady=10, padx=5)
        
        ttk.Label(game_frame, text="内存分配:", font=('Arial', 10)).grid(row=1, column=0, pady=10, padx=5)
        self.memory = ttk.Combobox(game_frame, values=["自动选择", "2G", "4G", "8G", "16G"], style='primary')
        self.memory.grid(row=1, column=1, pady=10, padx=5)
        self.memory.set(self.config.get('memory', '自动选择'))
        
        # 启动按钮 - 使用大号按钮并添加图标
        self.launch_button = ttk.Button(
            self.launch_frame, 
            text="启动游戏", 
            style='success.TButton',
            width=20,
            command=self.launch_game
        )
        self.launch_button.grid(row=2, column=0, columnspan=2, pady=20)

    def setup_settings_page(self):
        # Java设置
        java_frame = ttk.LabelFrame(self.settings_frame, text="Java设置", padding="10")
        java_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10, padx=10)
        
        ttk.Label(java_frame, text="Java路径:", font=('Arial', 10)).grid(row=0, column=0, pady=10, padx=5)
        self.java_path = ttk.Entry(java_frame, width=50, style='primary')
        self.java_path.grid(row=0, column=1, pady=10, padx=5)
        self.java_path.insert(0, self.config.get('java_path', ''))
        
        browse_btn = ttk.Button(java_frame, text="浏览", style='info.TButton', command=self.select_java_path)
        browse_btn.grid(row=0, column=2, padx=5)
        
        auto_java_btn = ttk.Button(java_frame, text="自动搜索Java", style='info.Outline.TButton', command=self.auto_detect_java)
        auto_java_btn.grid(row=1, column=0, columnspan=3, pady=10)
        
        # 游戏目录设置
        dir_frame = ttk.LabelFrame(self.settings_frame, text="游戏目录设置", padding="10")
        dir_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10, padx=10)
        
        ttk.Label(dir_frame, text="游戏目录:", font=('Arial', 10)).grid(row=0, column=0, pady=10, padx=5)
        self.game_dir = ttk.Entry(dir_frame, width=50, style='primary')  # 确保这里初始化
        self.game_dir.grid(row=0, column=1, pady=10, padx=5)
        self.game_dir.insert(0, self.config.get('game_dir', ''))
        
        browse_dir_btn = ttk.Button(dir_frame, text="浏览", style='info.TButton', command=self.select_game_dir)
        browse_dir_btn.grid(row=0, column=2, padx=5)
        
        auto_dir_btn = ttk.Button(dir_frame, text="自动搜索游戏目录", style='info.Outline.TButton', command=self.auto_detect_minecraft)
        auto_dir_btn.grid(row=1, column=0, columnspan=3, pady=10)
        
        # 保存按钮
        save_btn = ttk.Button(
            self.settings_frame, 
            text="保存设置", 
            style='success.TButton',
            width=20,
            command=self.save_config
        )
        save_btn.grid(row=2, column=0, columnspan=2, pady=20)

    def create_default_config(self):
        """生成默认配置文件"""
        default_config = {
            'username': '',
            'version': '1.20.4',  # 默认游戏版本
            'memory': '自动选择',  # 默认内存分配
            'java_path': '',  # 默认Java路径
            'game_dir': ''  # 默认游戏目录
        }
        
        with open('launcher_config.json', 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("信息", "未找到配置文件，已生成默认配置文件。")

    def load_config(self):
        try:
            if os.path.exists('launcher_config.json'):
                with open('launcher_config.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载配置文件时出错: {e}")
        return {}

    def save_config(self):
        config = {
            'username': self.username.get(),
            'version': self.version.get(),
            'memory': self.memory.get(),
            'java_path': self.java_path.get(),
            'game_dir': self.game_dir.get()
        }
        
        with open('launcher_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("成功", "设置已保存")

    def select_java_path(self):
        if sys.platform == 'win32':
            file_types = [('Java可执行文件', 'javaw.exe')]
        else:
            file_types = [('Java可执行文件', 'java')]
            
        path = filedialog.askopenfilename(filetypes=file_types)
        if path:
            self.java_path.delete(0, tk.END)
            self.java_path.insert(0, path)

    def select_game_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.game_dir.delete(0, tk.END)
            self.game_dir.insert(0, path)

    def update_status(self, message):
        """更新状态栏显示"""
        self.status_bar.config(
            text=message,
            font=('Arial', 9),
            padding=5
        )
        self.root.update()

    def launch_game(self):
        # 在启动游戏前设置语言为中文
        language_option = '--lang=zh_cn'  # 设置语言为中文

        # 启动游戏的线程
        threading.Thread(target=self.launch_game_thread, args=(language_option,), daemon=True).start()

    def launch_game_thread(self, language_option):
        try:
            self.launch_button.config(state='disabled')
            self.logger.info("开始启动游戏")
            self.update_status("正在准备启动...")

            # 记录启动参数
            self.logger.info(f"用户名: {self.username.get()}")
            self.logger.info(f"Java路径: {self.java_path.get()}")
            self.logger.info(f"游戏目录: {self.game_dir.get()}")
            self.logger.info(f"游戏版本: {self.version.get()}")
            self.logger.info(f"内存分配: {self.memory.get()}")

            self.progress['value'] = 20

            # 构建启动命令
            java_path = self.java_path.get()
            game_dir = self.game_dir.get()
            memory = self.memory.get()
            version = self.version.get()

            # 构建类路径
            classpath = []
            libraries_dir = os.path.join(game_dir, 'libraries')
            version_dir = os.path.join(game_dir, 'versions', version)
            version_jar = os.path.join(version_dir, f'{version}.jar')

            # 读取版本JSON文件获取启动信息
            version_json_path = os.path.join(version_dir, f'{version}.json')
            with open(version_json_path, 'r', encoding='utf-8') as f:
                version_data = json.load(f)

            # 获取主类名
            main_class = version_data.get('mainClass', 'net.minecraft.client.main.Main')

            # 添加libraries
            if 'libraries' in version_data:
                for lib in version_data['libraries']:
                    # 尝试不同的路径获取方式
                    lib_path = None

                    # 方式1: 直接从downloads中获取
                    if 'downloads' in lib and 'artifact' in lib['downloads']:
                        if 'path' in lib['downloads']['artifact']:
                            lib_path = lib['downloads']['artifact']['path']

                    # 方式2: 从name构建路径
                    if not lib_path and 'name' in lib:
                        # name格式: groupId:artifactId:version
                        parts = lib['name'].split(':')
                        if len(parts) >= 3:
                            group_id, artifact_id, version = parts[0], parts[1], parts[2]
                            lib_path = f"{group_id.replace('.', '/')}/{artifact_id}/{version}/{artifact_id}-{version}.jar"

                    if lib_path:
                        full_lib_path = os.path.join(libraries_dir, lib_path.replace('/', os.sep))
                        if os.path.exists(full_lib_path):
                            self.logger.debug(f"添加库: {full_lib_path}")
                            classpath.append(full_lib_path)
                        else:
                            self.logger.warning(f"找不到库文件: {full_lib_path}")

            # 添加主jar
            classpath.append(version_jar)

            # 使用系统分隔符连接类路径
            classpath_separator = ';' if os.name == 'nt' else ':'
            full_classpath = classpath_separator.join(classpath)

            self.logger.debug(f"主类: {main_class}")
            self.logger.debug(f"完整类路径: {full_classpath}")

            # 创建临时类路径文件
            classpath_file = os.path.join(game_dir, 'classpath.txt')
            with open(classpath_file, 'w', encoding='utf-8') as f:
                f.write(full_classpath)

            # 构建启动命令
            launch_cmd = [
                java_path,
                f'-Xmx{memory}',
                '-XX:+UseG1GC',
                '-Xmn128m',
                '-XX:+UnlockExperimentalVMOptions',
                '-XX:G1NewSizePercent=20',
                '-XX:G1ReservePercent=20',
                '-XX:MaxGCPauseMillis=50',
                '-XX:G1HeapRegionSize=16M',
                f'-Djava.library.path={os.path.join(version_dir, "natives")}',
                f'-cp', f'@{classpath_file}',
                main_class,  # 使用从JSON中读取的主类
                '--username', self.username.get(),
                '--version', version,
                '--gameDir', game_dir,
                '--assetsDir', os.path.join(game_dir, 'assets'),
                '--assetIndex', version,
                '--uuid', '0123456789abcdef0123456789abcdef',
                '--accessToken', '0123456789abcdef0123456789abcdef',
                '--userType', 'legacy',
                language_option  # 添加语言选项
            ]

            self.logger.debug(f"启动命令: {' '.join(launch_cmd)}")

            self.progress['value'] = 80

            # 添加错误日志输出
            process = subprocess.Popen(
                launch_cmd,
                cwd=game_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            stdout, stderr = process.communicate()
            if stdout:
                self.logger.debug(f"游戏输出:\n{stdout}")
            if stderr:
                self.logger.error(f"错误输出:\n{stderr}")
                raise Exception(f"Java错误:\n{stderr}")

            self.progress['value'] = 100
            self.update_status("游戏已启动")

        except Exception as e:
            self.logger.error(f"启动失败: {str(e)}", exc_info=True)
            messagebox.showerror("错误", f"启动失败：{str(e)}\n详细信息请查看日志文件")
        finally:
            # 清理临时文件
            try:
                if os.path.exists(classpath_file):
                    os.remove(classpath_file)
            except:
                pass
            self.launch_button.config(state='normal')
            self.progress['value'] = 0

    def get_default_minecraft_paths(self):
        """获取默认的Minecraft安装路径"""
        paths = []
        if sys.platform == 'win32':
            # Windows默认路径
            appdata = os.getenv('APPDATA')
            if appdata:
                paths.append(os.path.join(appdata, '.minecraft'))
        elif sys.platform == 'darwin':
            # macOS默认路径
            home = os.path.expanduser('~')
            paths.append(os.path.join(home, 'Library', 'Application Support', 'minecraft'))
        else:
            # Linux默认路径
            home = os.path.expanduser('~')
            paths.append(os.path.join(home, '.minecraft'))
        
        return [p for p in paths if os.path.exists(p)]

    def get_default_java_paths(self):
        """搜索系统中的Java安装路径"""
        java_paths = []
        
        if sys.platform == 'win32':
            # Windows系统搜索路径
            program_files = [
                os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'),
                os.environ.get('ProgramFiles', 'C:\\Program Files'),
                os.environ.get('ProgramW6432', 'C:\\Program Files')
            ]
            
            for prog_dir in program_files:
                java_dir = os.path.join(prog_dir, 'Java')
                if os.path.exists(java_dir):
                    for folder in os.listdir(java_dir):
                        if folder.startswith('jdk') or folder.startswith('jre'):
                            java_path = os.path.join(java_dir, folder, 'bin', 'javaw.exe')
                            if os.path.exists(java_path):
                                java_paths.append(java_path)
        else:
            # Linux/macOS系统搜索路径
            possible_paths = [
                '/usr/bin/java',
                '/usr/local/bin/java',
                '/opt/java/bin/java',
                '/usr/lib/jvm'
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    if os.path.isfile(path):
                        java_paths.append(path)
                    elif os.path.isdir(path):
                        # 搜索JVM目录下的所有Java安装
                        for root, dirs, files in os.walk(path):
                            if 'java' in files:
                                java_paths.append(os.path.join(root, 'java'))
        
        return java_paths

    def auto_detect_java(self):
        """自动检测Java安装路径"""
        java_paths = self.get_default_java_paths()
        
        if not java_paths:
            messagebox.showwarning("警告", "未找到Java安装，请手动选择Java路径")
            return
            
        if len(java_paths) == 1:
            self.java_path.delete(0, tk.END)
            self.java_path.insert(0, java_paths[0])
        else:
            # 创建选择窗口
            select_window = tk.Toplevel(self.root)
            select_window.title("选择Java路径")
            select_window.geometry("500x300")
            
            # 创建列表框
            listbox = tk.Listbox(select_window, width=70)
            listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            
            # 添加所有找到的路径
            for path in java_paths:
                listbox.insert(tk.END, path)
            
            def confirm_selection():
                selection = listbox.curselection()
                if selection:
                    selected_path = java_paths[selection[0]]
                    self.java_path.delete(0, tk.END)
                    self.java_path.insert(0, selected_path)
                    select_window.destroy()
            
            ttk.Button(select_window, text="确定", 
                      command=confirm_selection).pack(pady=10)

    def auto_detect_minecraft(self):
        """自动检测Minecraft安装路径"""
        minecraft_paths = self.get_default_minecraft_paths()
        
        if not minecraft_paths:
            messagebox.showwarning("警告", "未找到Minecraft安装，请手动选择游戏目录")
            return
            
        if len(minecraft_paths) == 1:
            self.game_dir.delete(0, tk.END)
            self.game_dir.insert(0, minecraft_paths[0])
        else:
            # 创建选择窗口
            select_window = tk.Toplevel(self.root)
            select_window.title("选择游戏目录")
            select_window.geometry("500x300")
            
            # 创建列表框
            listbox = tk.Listbox(select_window, width=70)
            listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            
            # 添加所有找到的路径
            for path in minecraft_paths:
                listbox.insert(tk.END, path)
            
            def confirm_selection():
                selection = listbox.curselection()
                if selection:
                    selected_path = minecraft_paths[selection[0]]
                    self.game_dir.delete(0, tk.END)
                    self.game_dir.insert(0, selected_path)
                    select_window.destroy()
            
            ttk.Button(select_window, text="确定", 
                      command=confirm_selection).pack(pady=10)

    def get_installed_versions(self):
        """扫描已安装的游戏版本"""
        versions = []
        game_dir = self.game_dir.get() if hasattr(self, 'game_dir') else ''
        
        if game_dir and os.path.exists(game_dir):
            versions_dir = os.path.join(game_dir, 'versions')
            if os.path.exists(versions_dir):
                for version_folder in os.listdir(versions_dir):
                    jar_path = os.path.join(versions_dir, version_folder, f'{version_folder}.jar')
                    json_path = os.path.join(versions_dir, version_folder, f'{version_folder}.json')
                    if os.path.exists(jar_path) and os.path.exists(json_path):
                        versions.append(version_folder)
        
        return sorted(versions, reverse=True) if versions else ["1.20.4", "1.19.4", "1.18.2", "1.16.5"]

    def refresh_versions(self):
        """刷新游戏版本列表"""
        versions = self.get_installed_versions()
        if hasattr(self, 'version'):  # 检查version组件是否已创建
            self.version['values'] = versions
            # 如果当前选择的版本不在列表中，设置为第一个可用版本
            if self.version.get() not in versions and versions:
                self.version.set(versions[0])
        self.update_status("已刷新游戏版本列表")
        self.logger.info(f"已刷新版本列表: {versions}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftLauncher(root)
    root.mainloop()
