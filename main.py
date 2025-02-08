import os
from file_scanner import FileScanner
from file_classifier import FileClassifier
from tag_generator import TagGenerator
from utils.file_utils import FileUtils
from utils.config import Config

class FileOrganizer:
    def __init__(self):
        self.scanner = FileScanner()
        self.classifier = FileClassifier()
        self.tag_generator = TagGenerator()
        self.file_utils = FileUtils()
        self.config = Config()

    def organize_directory(self, input_dir: str, output_dir: str, progress_callback=None) -> dict:
        """
        整理指定目录的文件
        progress_callback: 进度回调函数，接收参数(current, total, status_message)
        """
        results = {
            'scanned': 0,
            'classified': 0,
            'tagged': 0,
            'errors': []
        }

        try:
            print(f"\n开始扫描目录: {input_dir}")
            files_info = self.scanner.scan_directory(input_dir, progress_callback)
            results['scanned'] = len(files_info)
            
            if progress_callback:
                progress_callback(0, len(files_info), "开始分类文件...")

            print("\n开始分类文件...")
            for i, file_info in enumerate(files_info, 1):
                try:
                    # 分类单个文件
                    category = self.classifier.classify_file(file_info, output_dir)
                    if category:
                        results['classified'] += 1
                    
                    # 更新进度
                    if progress_callback:
                        progress_callback(i, len(files_info), f"正在处理: {file_info['name']}")
                        
                except Exception as e:
                    results['errors'].append(f"处理文件失败: {file_info['name']}, 错误: {str(e)}")

            print(f"\n分类完成，成功分类 {results['classified']} 个文件")

            # 创建索引文件
            if self.config.TAG_CONFIG['create_excel_index']:
                try:
                    index_path = os.path.join(output_dir, 'file_index.xlsx')
                    self.file_utils.create_excel_index(files_info, index_path)
                except Exception as e:
                    results['errors'].append(f"创建索引文件失败: {str(e)}")

        except Exception as e:
            results['errors'].append(str(e))

        return results

def main():
    organizer = FileOrganizer()
    
    # 这里可以添加命令行参数处理
    # 现在先使用硬编码的路径进行测试
    input_dir = input("请输入要整理的文件夹路径: ")
    output_dir = input("请输入整理后的文件夹路径: ")

    if os.path.exists(input_dir):
        results = organizer.organize_directory(input_dir, output_dir)
        
        print("\n整理完成！")
        print(f"扫描文件数: {results['scanned']}")
        print(f"成功分类文件数: {results['classified']}")
        print(f"成功添加标签文件数: {results['tagged']}")
        
        if results['errors']:
            print("\n发生的错误:")
            for error in results['errors']:
                print(f"- {error}")
    else:
        print("输入的文件夹路径不存在！")

if __name__ == "__main__":
    main()