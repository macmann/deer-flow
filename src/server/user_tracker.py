signed_in_users: set[str] = set()

def add_user(email: str) -> None:
    signed_in_users.add(email)

def list_users() -> list[str]:
    return sorted(signed_in_users)
