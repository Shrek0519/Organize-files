import os
import shutil
from datetime import datetime
import pandas as pd
from typing import List, Dict

class FileUtils:
    @staticmethod
    def get_file_info(file_path: str) -> Dict:
        """获取文件基本信息"""
        try:
            stats = os.stat(file_path)
            return {
                'name': os.path.basename(file_path),
                'extension': os.path.splitext(file_path)[1].lower(),
                'size': stats.st_size,
                'created_time': datetime.fromtimestamp(stats.st_ctime),
                'modified_time': datetime.fromtimestamp(stats.st_mtime),
                'path': file_path
            }
        except Exception as e:
            print(f"获取文件信息失败: {file_path}, 错误: {str(e)}")
            # 返回基本信息
            return {
                'name': os.path.basename(file_path),
                'extension': os.path.splitext(file_path)[1].lower(),
                'size': 0,
                'created_time': datetime.now(),  # 使用当前时间作为默认值
                'modified_time': datetime.now(),
                'path': file_path
            }

    @staticmethod
    def find_similar_files(filename: str, file_list: List[str]) -> List[str]:
        """查找相似文件名的文件"""
        base_name = os.path.splitext(filename)[0]
        return [f for f in file_list if base_name in os.path.splitext(f)[0]]

    @staticmethod
    def create_directory(path: str) -> None:
        """创建目录（如果不存在）"""
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def move_file(source: str, destination: str) -> None:
        """移动文件到目标位置"""
        try:
            # 确保目标目录存在
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            
            # 如果是Excel文件且被占用，跳过处理
            if source.endswith('.xlsx') or '~$' in os.path.basename(source):
                if os.path.exists(destination):
                    print(f"跳过被占用的Excel文件: {source}")
                    return

            # 如果目标文件已存在，添加序号
            base, ext = os.path.splitext(destination)
            counter = 1
            while os.path.exists(destination):
                destination = f"{base}_{counter}{ext}"
                counter += 1
            
            # 移动文件
            shutil.move(source, destination)
            print(f"已移动文件: {source} -> {destination}")  # 添加日志
            
        except Exception as e:
            error_msg = f"移动文件失败: {source} -> {destination}, 错误: {str(e)}"
            print(error_msg)
            # 如果是Excel文件的错误，不抛出异常
            if not (source.endswith('.xlsx') or '~$' in os.path.basename(source)):
                raise Exception(error_msg)

    @staticmethod
    def create_excel_index(files_info: List[Dict], output_path: str) -> None:
        """创建文件索引Excel"""
        try:
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            os.makedirs(output_dir, exist_ok=True)
            
            # 如果文件被占用，尝试使用新的文件名
            base, ext = os.path.splitext(output_path)
            counter = 1
            while True:
                try:
                    df = pd.DataFrame(files_info)
                    df.to_excel(output_path, index=False)
                    print(f"已创建索引文件: {output_path}")
                    break
                except PermissionError:
                    output_path = f"{base}_{counter}{ext}"
                    counter += 1
                    if counter > 10:  # 最多尝试10次
                        raise
        except Exception as e:
            print(f"创建索引文件失败: {output_path}, 错误: {str(e)}")
            # 这里不抛出异常，让程序继续运行