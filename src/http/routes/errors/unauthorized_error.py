class UnauthorizedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('Unauthorized.',*args)
