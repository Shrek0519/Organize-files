class SmartClassifier:
    def __init__(self):
        self.rules = []
        self.load_rules()
    
    def learn_from_user(self, file_info, user_category):
        """从用户的分类决定中学习"""
        new_rule = self.generate_rule(file_info, user_category)
        self.rules.append(new_rule)
        self.save_rules() 