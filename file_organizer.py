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

    def organize_directory(self, input_dir: str, output_dir: str) -> dict:
        """
        整理指定目录的文件
        """
        results = {
            'scanned': 0,
            'classified': 0,
            'tagged': 0,
            'errors': []
        }

        try:
            # 扫描文件
            files_info = self.scanner.scan_directory(input_dir)
            results['scanned'] = len(files_info)

            # 分类文件
            classification_results = self.classifier.classify_files(files_info, output_dir)
            results['classified'] = len(classification_results['success'])

            # 生成和应用标签
            for file_info in files_info:
                tags = self.tag_generator.generate_tags(file_info)
                if self.tag_generator.apply_tags(file_info['path'], tags):
                    results['tagged'] += 1

            # 创建索引文件
            if self.config.TAG_CONFIG['create_excel_index']:
                index_path = os.path.join(output_dir, self.config.TAG_CONFIG['index_file'])
                self.file_utils.create_excel_index(files_info, index_path)

        except Exception as e:
            results['errors'].append(str(e))

        return results 