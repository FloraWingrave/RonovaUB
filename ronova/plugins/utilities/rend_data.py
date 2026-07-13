from config import RENDER_API


class GetServices:

    def __init__(self):
        self.service_id: str | None = None

    async def get_services(self, session):
        url = "https://api.render.com/v1/services"
        headers = {"Authorization": f"Bearer {RENDER_API}"}

        async with session.get(url, headers=headers) as res:
            data = await res.json()

        services = []
        for item in data:
            service = item.get("service", {})

            if service.get("suspended") == "not_suspended":
                details = service.get("serviceDetails", {})

                trimmed = {
                    "id": service.get("id"),
                    "name": service.get("name"),
                    "type": service.get("type"),
                    "region": details.get("region"),
                    "url": details.get("url"),
                    "branch": service.get("branch"),
                }
                services.append(trimmed)

                if self.service_id is None:
                    self.service_id = trimmed["id"]

        return services or None

    async def trigger_deploy(self, session, service_id: str):
        url = f"https://api.render.com/v1/services/{service_id}/deploys"
        headers = {"Authorization": f"Bearer {RENDER_API}"}

        async with session.post(url, headers=headers) as res:
            if res.status in (200, 201):
                data = await res.json()
                return data.get("id")
            return None