class ReportGenerator:
    def generate_report(self, results):
        """生成整理报告"""
        report = {
            'summary': self.generate_summary(results),
            'details': self.generate_details(results),
            'charts': self.generate_charts(results)
        }
        return report 