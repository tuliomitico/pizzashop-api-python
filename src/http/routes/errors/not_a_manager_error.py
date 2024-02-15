class NotAManagerError(Exception):
    def __init__(self, *args: object) -> None:
        super("User is not a restaurant manager.").__init__(*args)
