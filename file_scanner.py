import os
from typing import List, Dict
from utils.config import Config
from utils.file_utils import FileUtils

class FileScanner:
    def __init__(self):
        self.config = Config()
        self.file_utils = FileUtils()
        self.supported_extensions = []
        for type_info in self.config.SUPPORTED_TYPES.values():
            self.supported_extensions.extend(type_info['extensions'])

    def scan_directory(self, directory_path: str, progress_callback=None) -> List[Dict]:
        """扫描指定目录，返回文件信息列表"""
        files_info = []
        
        try:
            # 首先计算总文件数
            total_files = sum([len(files) for _, _, files in os.walk(directory_path)])
            current_file = 0
            
            # 遍历目录下的所有文件
            for root, _, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_ext = os.path.splitext(file)[1].lower()
                    
                    # 更新进度
                    current_file += 1
                    if progress_callback:
                        progress_callback(current_file, total_files, f"正在扫描: {file}")
                    
                    # 只处理支持的文件类型
                    if file_ext in self.supported_extensions:
                        # 获取文件信息
                        file_info = self.file_utils.get_file_info(file_path)
                        
                        # 查找相似文件
                        similar_files = self.file_utils.find_similar_files(
                            file, 
                            [f for f in files if f != file]
                        )
                        file_info['similar_files'] = [os.path.join(root, f) for f in similar_files]
                        
                        files_info.append(file_info)
                        print(f"已扫描文件: {file_path}")  # 添加日志
        except Exception as e:
            print(f"扫描出错: {str(e)}")  # 添加错误日志
            
        return files_info

    def get_file_type_category(self, file_extension: str) -> str:
        """根据文件扩展名返回文件类别"""
        for category, type_info in self.config.SUPPORTED_TYPES.items():
            if file_extension in type_info['extensions']:
                return category
        return 'others'