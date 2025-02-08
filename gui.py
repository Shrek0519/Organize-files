import tkinter as tk
from tkinter import ttk, filedialog
import sv_ttk
import customtkinter as ctk
from main import FileOrganizer
import threading
import queue

class FileOrganizerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("文件整理助手")
        self.root.geometry("800x600")
        
        # 使用现代主题
        sv_ttk.set_theme("dark")
        self.setup_styles()
        
        self.organizer = FileOrganizer()
        self.setup_gui()
        
    def setup_styles(self):
        """设置自定义样式"""
        style = ttk.Style()
        
        # 主框架样式
        style.configure("Main.TFrame", background="#202020")
        
        # 标签样式
        style.configure("Title.TLabel", 
                       font=("Microsoft YaHei UI", 16, "bold"),
                       foreground="#ffffff",
                       background="#202020")
        
        # 按钮样式
        style.configure("Action.TButton",
                       font=("Microsoft YaHei UI", 10),
                       padding=10)
        
    def setup_gui(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20", style="Main.TFrame")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title = ttk.Label(main_frame, 
                         text="文件整理助手", 
                         style="Title.TLabel")
        title.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 文件选择区域
        select_frame = ttk.LabelFrame(main_frame, 
                                    text="选择文件夹",
                                    padding="10")
        select_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 输入文件夹
        ttk.Label(select_frame, text="输入文件夹:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_path = tk.StringVar()
        ttk.Entry(select_frame, textvariable=self.input_path, width=50).grid(row=0, column=1, pady=5, padx=5)
        ttk.Button(select_frame, 
                  text="浏览",
                  style="Action.TButton",
                  command=self.browse_input).grid(row=0, column=2, padx=5, pady=5)
        
        # 输出文件夹
        ttk.Label(select_frame, text="输出文件夹:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_path = tk.StringVar()
        ttk.Entry(select_frame, textvariable=self.output_path, width=50).grid(row=1, column=1, pady=5, padx=5)
        ttk.Button(select_frame,
                  text="浏览",
                  style="Action.TButton",
                  command=self.browse_output).grid(row=1, column=2, padx=5, pady=5)
        
        # 配置选项
        config_frame = ttk.LabelFrame(main_frame,
                                    text="配置选项",
                                    padding="10")
        config_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 复选框选项
        self.create_index = tk.BooleanVar(value=False)
        ttk.Checkbutton(config_frame,
                       text="创建索引文件",
                       variable=self.create_index).grid(row=0, column=0, padx=10)
        
        self.keep_structure = tk.BooleanVar(value=False)
        ttk.Checkbutton(config_frame,
                       text="保持原有目录结构",
                       variable=self.keep_structure).grid(row=0, column=1, padx=10)
        
        # 进度显示区域
        progress_frame = ttk.LabelFrame(main_frame,
                                      text="处理进度",
                                      padding="10")
        progress_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 进度条
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # 状态信息
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(progress_frame,
                               textvariable=self.status_var)
        status_label.grid(row=1, column=0, columnspan=3, pady=5)
        
        # 开始按钮
        ttk.Button(main_frame,
                  text="开始整理",
                  style="Action.TButton",
                  command=self.start_organizing).grid(row=4, column=0, columnspan=3, pady=10)
        
        # 日志显示
        log_frame = ttk.LabelFrame(main_frame,
                                 text="处理日志",
                                 padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.log_text = tk.Text(log_frame, height=10, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 滚动条
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # 设置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        log_frame.columnconfigure(0, weight=1)
        
        # 添加主题切换按钮
        theme_button = ttk.Button(main_frame,
                                text="切换主题",
                                style="Action.TButton",
                                command=self.toggle_theme)
        theme_button.grid(row=6, column=0, columnspan=3, pady=10)
        
    def toggle_theme(self):
        """切换深色/浅色主题"""
        current_theme = sv_ttk.get_theme()
        if current_theme == "dark":
            sv_ttk.set_theme("light")
        else:
            sv_ttk.set_theme("dark")
        
    def browse_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_path.set(folder)
            
    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)
            
    def start_organizing(self):
        input_dir = self.input_path.get()
        output_dir = self.output_path.get()
        
        if not input_dir or not output_dir:
            self.log_message("请选择输入和输出文件夹！")
            return
            
        self.progress_var.set("正在处理...")
        self.log_text.delete(1.0, tk.END)
        
        # 在新线程中运行整理任务
        thread = threading.Thread(target=self.organize_files, args=(input_dir, output_dir))
        thread.start()
        
    def organize_files(self, input_dir, output_dir):
        try:
            self.log_message("开始扫描文件...")
            self.progress.set(0)  # 重置进度条
            self.status_var.set("正在扫描文件...")
            
            # 更新配置
            self.organizer.config.TAG_CONFIG['create_excel_index'] = self.create_index.get()
            
            results = self.organizer.organize_directory(
                input_dir, 
                output_dir,
                progress_callback=self.update_progress  # 添加进度回调
            )
            
            self.progress.set(100)  # 完成时设置为100%
            self.log_message(f"\n整理完成！")
            self.log_message(f"扫描文件数: {results['scanned']}")
            self.log_message(f"成功分类文件数: {results['classified']}")
            self.log_message(f"成功添加标签文件数: {results['tagged']}")
            
            if results['errors']:
                self.log_message("\n发生的错误:")
                for error in results['errors']:
                    self.log_message(f"- {error}")
                    
            self.progress_var.set("处理完成")
            self.status_var.set("就绪")
            
        except Exception as e:
            self.log_message(f"发生错误: {str(e)}")
            self.progress_var.set("处理出错")
            self.status_var.set("出错")
            
    def update_progress(self, current, total, status_message=""):
        """更新进度条和状态信息"""
        if total > 0:
            progress = (current / total) * 100
            self.progress['value'] = progress
            self.status_var.set(f"{status_message} - {current}/{total} ({progress:.1f}%)")
        self.root.update()
        
    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()  # 确保界面及时更新
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FileOrganizerGUI()
    app.run()