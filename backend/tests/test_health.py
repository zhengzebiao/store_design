import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.seed.store_design_seed import seed_store_design


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        seed_store_design(db)
    finally:
        db.close()

    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)


def test_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_templates_list(client: TestClient):
    response = client.get("/api/store-design/templates?company_id=3")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["total"] >= 1
    assert body["data"][0]["name"] == "默认首页模板"


def test_components_list(client: TestClient):
    response = client.get("/api/store-design/components")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"][0]["component_key"] == "U_search"


def test_save_page_create(client: TestClient):
    response = client.post(
        "/api/store-design/pages/save",
        json={
            "mode": "create",
            "id": "",
            "diy_id": "",
            "company_id": 3,
            "type": "home_page",
            "page_name": "接口保存冒烟",
            "datas": [],
            "page_info": {},
            "member_level": [],
            "level": [],
            "status": 1,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["diy_id"]


def test_use_template(client: TestClient):
    create_response = client.post(
        "/api/store-design/pages/save",
        json={
            "mode": "create",
            "id": "",
            "diy_id": "",
            "company_id": 3,
            "type": "home_page",
            "page_name": "待使用模板",
            "datas": [],
            "page_info": {},
            "member_level": [],
            "level": [],
            "status": 1,
        },
    )
    diy_id = create_response.json()["data"]["diy_id"]

    response = client.post(f"/api/store-design/templates/{diy_id}/use", json={"company_id": 3})
    assert response.status_code == 200
    list_response = client.get("/api/store-design/templates?company_id=3&is_sel=1")
    selected = list_response.json()["data"]
    assert len(selected) == 1
    assert str(selected[0]["id"]) == str(diy_id)


def test_delete_template(client: TestClient):
    create_response = client.post(
        "/api/store-design/pages/save",
        json={
            "mode": "create",
            "id": "",
            "diy_id": "",
            "company_id": 3,
            "type": "home_page",
            "page_name": "待删除模板",
            "datas": [],
            "page_info": {},
            "member_level": [],
            "level": [],
            "status": 1,
        },
    )
    diy_id = create_response.json()["data"]["diy_id"]

    response = client.delete(f"/api/store-design/templates/{diy_id}?company_id=3")
    assert response.status_code == 200
    detail_response = client.get(f"/api/store-design/templates/{diy_id}?company_id=3")
    assert detail_response.status_code == 404
