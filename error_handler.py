class ErrorHandler:
    def handle_error(self, error, context):
        """智能错误处理"""
        if isinstance(error, PermissionError):
            return self.handle_permission_error(error, context)
        elif isinstance(error, FileNotFoundError):
            return self.handle_missing_file(error, context) 