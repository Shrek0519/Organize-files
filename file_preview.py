import os

class FilePreview:
    def __init__(self):
        self.supported_previews = {
            '.txt': self.preview_text,
            '.doc': self.preview_word,
            '.docx': self.preview_word,
            '.pdf': self.preview_pdf,
            '.jpg': self.preview_image,
            '.png': self.preview_image
        }
    
    def get_preview(self, file_path):
        """获取文件预览"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext in self.supported_previews:
            return self.supported_previews[ext](file_path)
        return "不支持预览此类型文件" 