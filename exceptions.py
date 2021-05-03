class SBLanguageExceptions(Exception):
    def __init__(self, message="Error in code"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'ERROR: {self.message}'
        