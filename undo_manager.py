class UndoManager:
    def __init__(self):
        self.operations = []
    
    def record_operation(self, source, destination):
        self.operations.append({
            'source': destination,
            'destination': source
        })
    
    def undo_last(self):
        if self.operations:
            operation = self.operations.pop()
            shutil.move(operation['source'], operation['destination']) 