from dataclasses import dataclass

@dataclass
class env:
    logLevel: str = "INFO"

    username: str = "admin@kieback-peter.nl"
    password: str = "Nuklid_8001"

    base_url: str = "https://portal.kieback-peter.net/api"

    auth_header = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    app_header = {
        "Content-Type": "application/json"
    }
