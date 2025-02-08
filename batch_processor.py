class BatchProcessor:
    def process_multiple_folders(self, input_folders, output_base):
        """处理多个文件夹"""
        results = []
        for folder in input_folders:
            result = self.process_single_folder(folder, output_base)
            results.append(result)
        return results 