import os

class Config:
    # 基础路径配置
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 支持的文件类型
    SUPPORTED_TYPES = {
        'word_01': {
            'extensions': ['.doc', '.docx'],
            'folder': 'Word文档/01月',
            'month': '01'
        },
        'word_02': {
            'extensions': ['.doc', '.docx'],
            'folder': 'Word文档/02月',
            'month': '02'
        },
        'word_03': {
            'extensions': ['.doc', '.docx'],
            'folder': 'Word文档/03月',
            'month': '03'
        },
        'word_04': {
            'extensions': ['.doc', '.docx'],
            'folder': 'Word文档/04月',
            'month': '04'
        },
        'word_05': {
            'extensions': ['.doc', '.docx'],
            'folder': 'Word文档/05月',
            'month': '05'
        },
        'word_06': {
            'extensions': ['.doc', '.docx'],
            'folder': 'Word文档/06月',
            'month': '06'
        },
        'word_07': {
            'extensions': ['.doc', '.docx'],
            'folder': 'Word文档/07月',
            'month': '07'
        },
        'word_08': {
            'extensions': ['.doc', '.docx'],
            'folder': 'Word文档/08月',
            'month': '08'
        },
        'word_09': {
            'extensions': ['.doc', '.docx'],
            'folder': 'Word文档/09月',
            'month': '09'
        },
        'word_10': {
            'extensions': ['.doc', '.docx'],
            'folder': 'Word文档/10月',
            'month': '10'
        },
        'word_11': {
            'extensions': ['.doc', '.docx'],
            'folder': 'Word文档/11月',
            'month': '11'
        },
        'word_12': {
            'extensions': ['.doc', '.docx'],
            'folder': 'Word文档/12月',
            'month': '12'
        },
        'word_draft': {
            'extensions': ['.doc', '.docx'],
            'folder': 'Word文档/草稿文件',
            'keywords': ['草稿', '草案', 'draft', '未完成']
        },
        'word_final': {
            'extensions': ['.doc', '.docx'],
            'folder': 'Word文档/定稿文件',
            'keywords': ['终稿', '定稿', 'final', '完成版']
        },
        'word_other': {
            'extensions': ['.doc', '.docx'],
            'folder': 'Word文档/其他文档'
        },
        'pdf_thesis': {
            'extensions': ['.pdf'],
            'folder': 'PDF论文',
            'keywords': ['毕业论文', '学位论文', '硕士', '博士']
        },
        'pdf_report': {
            'extensions': ['.pdf'],
            'folder': 'PDF查重报告',
            'keywords': ['查重报告', '检测报告', '相似度']
        },
        'pdf_literature': {
            'extensions': ['.pdf'],
            'folder': 'PDF文献资料',
            'keywords': ['journal', 'research', 'paper', '期刊', '会议']
        },
        'pdf_other': {
            'extensions': ['.pdf'],
            'folder': 'PDF其他文件'
        },
        'ppt_template': {
            'extensions': ['.ppt', '.pptx', '.potx', '.pot'],
            'folder': 'PPT模板',
            'keywords': ['模板', 'template', '模版', '范例']
        },
        'powerpoint': {
            'extensions': ['.ppt', '.pptx'],
            'folder': 'PPT演示文稿'
        },
        'excel': {
            'extensions': ['.xls', '.xlsx'],
            'folder': 'Excel文件'
        },
        'images': {
            'extensions': ['.jpg', '.jpeg', '.png', '.gif'],
            'folder': 'Images'
        },
        'videos': {
            'extensions': ['.mp4', '.mov', '.avi'],
            'folder': 'Videos'
        }
    }
    
    # 版本控制配置
    VERSION_CONTROL = {
        'archive_folder': 'Archived_Versions',
        'mark_latest': True,
        'timestamp_format': '%Y%m%d_%H%M%S'
    }
    
    # 标签配置
    TAG_CONFIG = {
        'use_windows_tags': True,
        'create_excel_index': False,
        'index_file': 'file_index.xlsx'
    }