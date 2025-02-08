import os
from datetime import datetime
from typing import List, Dict
from utils.config import Config
from utils.file_utils import FileUtils

class FileClassifier:
    def __init__(self):
        self.config = Config()
        self.file_utils = FileUtils()

    def classify_files(self, files_info: List[Dict], output_base_dir: str) -> Dict:
        """对文件进行分类并移动到对应目录"""
        classification_results = {
            'success': [],
            'failed': [],
            'skipped': [],  # 添加跳过的文件列表
            'version_archived': []
        }

        # 添加调试信息
        print(f"开始分类，共 {len(files_info)} 个文件")

        for file_info in files_info:
            try:
                # 跳过Excel临时文件
                if '~$' in file_info['name']:
                    classification_results['skipped'].append({
                        'file': file_info['name'],
                        'reason': '临时文件'
                    })
                    continue

                # 获取文件类别
                file_category = self.get_file_category(file_info)
                print(f"文件 {file_info['name']} 被分类为: {file_category}")

                # 获取目标文件夹路径
                category_folder = self.config.SUPPORTED_TYPES[file_category]['folder']
                category_dir = os.path.join(output_base_dir, category_folder)
                
                # 创建目标文件夹
                self.file_utils.create_directory(category_dir)
                print(f"创建目录: {category_dir}")

                # 构建目标文件路径
                new_path = os.path.join(category_dir, file_info['name'])
                
                # 移动文件
                try:
                    self.file_utils.move_file(file_info['path'], new_path)
                    classification_results['success'].append({
                        'file': file_info['name'],
                        'new_location': new_path,
                        'category': file_category
                    })
                    print(f"成功移动文件: {file_info['name']} -> {category_folder}")
                except Exception as move_error:
                    error_msg = f"移动文件失败: {file_info['name']}, 错误: {str(move_error)}"
                    print(error_msg)
                    classification_results['failed'].append({
                        'file': file_info['name'],
                        'error': error_msg
                    })

            except Exception as e:
                error_msg = f"处理文件失败: {file_info['name']}, 错误: {str(e)}"
                print(error_msg)
                classification_results['failed'].append({
                    'file': file_info['name'],
                    'error': error_msg
                })

        # 打印分类结果统计
        print(f"\n分类完成:")
        print(f"成功: {len(classification_results['success'])} 个文件")
        print(f"失败: {len(classification_results['failed'])} 个文件")
        print(f"跳过: {len(classification_results['skipped'])} 个文件")

        return classification_results

    def get_file_category(self, file_info):
        """确定文件所属类别"""
        extension = file_info['extension'].lower()
        file_name = file_info['name'].lower()
        
        # 对Word文档进行特殊处理
        if extension in ['.doc', '.docx']:
            try:
                # 获取文件的创建月份，将datetime转换为时间戳
                file_month = datetime.strftime(file_info['created_time'], '%m')
                category_key = f'word_{file_month}'
                
                # 确保该月份的分类存在
                if category_key in self.config.SUPPORTED_TYPES:
                    return category_key
            except Exception as e:
                print(f"处理文件 {file_name} 的日期时出错: {str(e)}")
            
            # 如果日期处理失败，归类到其他文档
            return 'word_other'
            
        # 对PDF文件进行特殊处理
        elif extension == '.pdf':
            file_path = file_info['path']
            
            # 尝试读取PDF文件的前几页内容进行分类
            try:
                import pdfplumber
                content = ""
                with pdfplumber.open(file_path) as pdf:
                    # 只读取前3页
                    for page in pdf.pages[:3]:
                        content += page.extract_text().lower()
                
                # 按关键词匹配分类
                for category, type_info in self.config.SUPPORTED_TYPES.items():
                    if extension in type_info['extensions'] and 'keywords' in type_info:
                        for keyword in type_info['keywords']:
                            if keyword.lower() in content or keyword.lower() in file_name:
                                return category
                
                # 如果没有匹配到关键词，归类到其他PDF
                return 'pdf_other'
                
            except Exception:
                # 如果无法读取PDF内容，则只根据文件名判断
                for category, type_info in self.config.SUPPORTED_TYPES.items():
                    if extension in type_info['extensions'] and 'keywords' in type_info:
                        for keyword in type_info['keywords']:
                            if keyword.lower() in file_name:
                                return category
                return 'pdf_other'
        
        # 对PPT文件进行特殊处理
        elif extension in ['.ppt', '.pptx', '.potx', '.pot']:
            # 如果是.potx或.pot格式，直接归类为模板
            if extension in ['.potx', '.pot']:
                return 'ppt_template'
                
            # 检查文件名中是否包含模板关键词
            for category, type_info in self.config.SUPPORTED_TYPES.items():
                if extension in type_info['extensions'] and 'keywords' in type_info:
                    for keyword in type_info['keywords']:
                        if keyword.lower() in file_name:
                            return category
            
            # 如果没有匹配到模板关键词，归类为普通PPT
            return 'powerpoint'
        
        # 其他文件类型的处理
        for category, type_info in self.config.SUPPORTED_TYPES.items():
            if extension in type_info['extensions']:
                return category
                
        return 'others'

    def handle_versions(self, file_info: Dict, category_dir: str, results: Dict) -> None:
        """处理文件版本"""
        if file_info['similar_files']:
            # 创建归档目录
            archive_dir = os.path.join(category_dir, 
                self.config.VERSION_CONTROL['archive_folder'])
            self.file_utils.create_directory(archive_dir)

            # 检查是否是最新版本
            is_latest = all(
                file_info['modified_time'] >= os.path.getmtime(f) 
                for f in file_info['similar_files']
            )

            if is_latest:
                # 移动最新版本到主目录
                new_path = os.path.join(category_dir, f"[最新版本]{file_info['name']}")
                self.file_utils.move_file(file_info['path'], new_path)
                results['success'].append({
                    'file': file_info['name'],
                    'new_location': new_path,
                    'status': 'latest_version'
                })
            else:
                # 移动到归档目录
                timestamp = datetime.now().strftime(
                    self.config.VERSION_CONTROL['timestamp_format']
                )
                archived_name = f"{os.path.splitext(file_info['name'])[0]}_{timestamp}{file_info['extension']}"
                new_path = os.path.join(archive_dir, archived_name)
                self.file_utils.move_file(file_info['path'], new_path)
                results['version_archived'].append({
                    'file': file_info['name'],
                    'new_location': new_path
                })
        else:
            # 没有相似文件，直接移动
            new_path = os.path.join(category_dir, file_info['name'])
            self.file_utils.move_file(file_info['path'], new_path)
            results['success'].append({
                'file': file_info['name'],
                'new_location': new_path
            })