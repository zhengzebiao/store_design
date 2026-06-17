from app.core.database import SessionLocal
from app.seed.store_design_seed import DEFAULT_COMPANY_ID, seed_store_design


def main() -> None:
    db = SessionLocal()
    try:
        seed_store_design(db, company_id=DEFAULT_COMPANY_ID)
    finally:
        db.close()


if __name__ == "__main__":
    main()
