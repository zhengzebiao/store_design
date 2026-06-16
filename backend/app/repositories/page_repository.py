from app.repositories.memory_store import PAGES, TEMPLATES, clone, next_page_id, next_template_id, now_text
from app.schemas.page import SavePagePayload


class PageRepository:
    def save(self, payload: SavePagePayload) -> dict:
        now = now_text()
        if payload.mode in {"create", "copy"}:
            diy_id = str(next_template_id())
            page_id = str(next_page_id())
            TEMPLATES.append(
                {
                    "id": diy_id,
                    "name": payload.page_name,
                    "type": "diy",
                    "is_sel": 0,
                    "created_at": now,
                    "updated_at": now,
                    "is_open_tabbar": 0,
                    "other_company_show": payload.other_company_show,
                    "pid": payload.route_id or payload.diy_id or 0,
                    "head_img": payload.head_img or "",
                    "price": "0.00",
                    "theme_id": None,
                    "system_recommend_template": 0,
                }
            )
        else:
            diy_id = str(payload.diy_id or payload.route_id)
            page_id = str(payload.id)
            for item in TEMPLATES:
                if str(item["id"]) == diy_id:
                    item["name"] = payload.page_name
                    item["updated_at"] = now
                    break

        page = payload.model_dump()
        page.update({"id": page_id, "diy_id": diy_id, "updated_at": now})
        page.pop("mode", None)
        page.pop("route_id", None)
        page.pop("head_img", None)
        PAGES[diy_id] = page
        return clone(page)
