class TagGenerator:
    def __init__(self):
        pass

    def generate_tags(self, file_info):
        tags = []
        file_ext = file_info['extension'].lower()
        
        # 根据文件类型添加更详细的标签
        if file_ext in ['.doc', '.docx']:
            tags.extend(['文档', 'Word文档'])
        elif file_ext == '.pdf':
            tags.extend(['文档', 'PDF文件'])
        elif file_ext in ['.ppt', '.pptx']:
            tags.extend(['文档', 'PPT文件'])
        elif file_ext in ['.xls', '.xlsx']:
            tags.extend(['文档', 'Excel文件'])
        elif file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
            tags.append('图片')
        elif file_ext in ['.mp4', '.mov', '.avi']:
            tags.append('视频')
            
        # 添加文件大小标签
        size_mb = file_info.get('size', 0) / (1024 * 1024)  # 转换为MB
        if size_mb > 100:
            tags.append('大文件')
        elif size_mb < 1:
            tags.append('小文件')
            
        return tags

    def apply_tags(self, file_path, tags):
        # 由于Windows文件标签需要特殊API，这里先返回True
        return True
