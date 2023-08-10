import requests

from app.internal.settings import env
from app.core.logger import log


class Session:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = env.base_url

    def set_token(self):
        self.session.headers.update(env.auth_header)
        response = self.session.post(
            url=env.base_url + "/v1/auth/token",
            data=f"grant_type=&username={env.username}&password={env.password}&scope=&client_id=&client_secret=",
        )
        # print(response.json())
        match response.status_code:
            case 200:
                auth = response.json()
                token = {"Authorization": f"Bearer {auth['access_token']}"}
                self.session.headers.update(env.app_header, **token)
            case _:
                raise ValueError("failed to authenticate")

    def update(self):
        installation_response = self.session.get(
            self.base_url + "/v1/installation/all")
        match installation_response.status_code:
            case 200:
                installations = installation_response.json()
                for installation in installations:
                    task_response = self.session.get(
                        self.base_url + f"/task/update/installation/{installation['id']}")
                    match task_response.status_code:
                        case 200:
                            task_response.json()
                            print(
                                f"updating instalaltion {installation['name']}")
                        case _:
                            print(task_response.content)
                            log.info("Unhandled error: %s",
                                     task_response.status_code)
            case _:
                log.info("Unhandled error: %s", installation_response.content)


www = Session()
