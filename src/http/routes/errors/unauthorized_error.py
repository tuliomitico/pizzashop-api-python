class UnauthorizedError(Exception):
    def __init__(self, *args: object) -> None:
        super('Unauthorized.').__init__(*args)
