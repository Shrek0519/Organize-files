class FileOrganizerScheduler:
    def schedule_task(self, input_dir, output_dir, schedule_type='daily'):
        """设置定时整理任务"""
        schedule.every().day.at("02:00").do(self.run_task, input_dir, output_dir) 