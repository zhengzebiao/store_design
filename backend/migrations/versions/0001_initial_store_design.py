"""initial store design tables

Revision ID: 0001_initial_store_design
Revises:
Create Date: 2026-06-17
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial_store_design"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

jsonb = postgresql.JSONB(astext_type=sa.Text())


def upgrade() -> None:
    op.create_table(
        "store_design_template",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("company_id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False, server_default="diy"),
        sa.Column("is_sel", sa.SmallInteger(), nullable=False, server_default="0"),
        sa.Column("is_open_tabbar", sa.SmallInteger(), nullable=False, server_default="0"),
        sa.Column("other_company_show", sa.SmallInteger(), nullable=False, server_default="0"),
        sa.Column("pid", sa.BigInteger(), nullable=False, server_default="0"),
        sa.Column("head_img", sa.Text(), nullable=True),
        sa.Column("price", sa.Numeric(10, 2), nullable=False, server_default="0.00"),
        sa.Column("theme_id", sa.BigInteger(), nullable=True),
        sa.Column("system_recommend_template", sa.SmallInteger(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("idx_template_company_updated", "store_design_template", ["company_id", "updated_at"])
    op.create_index("idx_template_company_type", "store_design_template", ["company_id", "type"])
    op.create_index("idx_template_company_is_sel", "store_design_template", ["company_id", "is_sel"])
    op.create_index("idx_template_pid", "store_design_template", ["pid"])

    op.create_table(
        "store_design_page",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("diy_id", sa.BigInteger(), nullable=False),
        sa.Column("company_id", sa.BigInteger(), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False, server_default="home_page"),
        sa.Column("page_name", sa.String(length=255), nullable=False),
        sa.Column("datas", jsonb, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("other_company_show", sa.SmallInteger(), nullable=False, server_default="0"),
        sa.Column("page_info", jsonb, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("member_level", jsonb, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("level", jsonb, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("status", sa.SmallInteger(), nullable=False, server_default="1"),
        sa.Column("page_sort", sa.SmallInteger(), nullable=False, server_default="2"),
        sa.Column("page_scene", sa.SmallInteger(), nullable=False, server_default="2"),
        sa.Column("top_id", jsonb, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("foot_type", sa.SmallInteger(), nullable=False, server_default="1"),
        sa.Column("foot_id", jsonb, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("page_type", sa.String(length=32), nullable=False, server_default="2"),
        sa.Column("schema_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("company_id", "diy_id", name="uk_page_company_diy"),
    )
    op.create_index("idx_page_company_scene", "store_design_page", ["company_id", "page_scene"])
    op.create_index("idx_page_company_updated", "store_design_page", ["company_id", "updated_at"])
    op.create_index("idx_page_diy_id", "store_design_page", ["diy_id"])
    op.create_index("idx_page_datas_gin", "store_design_page", ["datas"], postgresql_using="gin")
    op.create_index("idx_page_info_gin", "store_design_page", ["page_info"], postgresql_using="gin")

    op.create_table(
        "store_design_component_meta",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("component_key", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("icon", sa.String(length=255), nullable=True),
        sa.Column("tpl_id", sa.BigInteger(), nullable=True),
        sa.Column("templates", jsonb, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("schema_json", jsonb, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("default_data_json", jsonb, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("enabled", sa.SmallInteger(), nullable=False, server_default="1"),
        sa.Column("sort", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("component_key", name="uk_component_key"),
    )
    op.create_index("idx_component_category_sort", "store_design_component_meta", ["category_id", "sort"])
    op.create_index("idx_component_enabled", "store_design_component_meta", ["enabled"])
    op.create_index("idx_component_schema_json_gin", "store_design_component_meta", ["schema_json"], postgresql_using="gin")

    op.create_table(
        "store_design_asset",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("company_id", sa.BigInteger(), nullable=False),
        sa.Column("asset_type", sa.String(length=32), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=True),
        sa.Column("mime_type", sa.String(length=100), nullable=True),
        sa.Column("size", sa.BigInteger(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_asset_company_created", "store_design_asset", ["company_id", "created_at"])

    op.create_table(
        "store_design_operation_log",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("company_id", sa.BigInteger(), nullable=False),
        sa.Column("diy_id", sa.BigInteger(), nullable=True),
        sa.Column("page_id", sa.BigInteger(), nullable=True),
        sa.Column("operator_id", sa.BigInteger(), nullable=True),
        sa.Column("operation", sa.String(length=64), nullable=False),
        sa.Column("before_snapshot", jsonb, nullable=True),
        sa.Column("after_snapshot", jsonb, nullable=True),
        sa.Column("ip", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_operation_company_diy_created", "store_design_operation_log", ["company_id", "diy_id", "created_at"])


def downgrade() -> None:
    op.drop_index("idx_operation_company_diy_created", table_name="store_design_operation_log")
    op.drop_table("store_design_operation_log")
    op.drop_index("idx_asset_company_created", table_name="store_design_asset")
    op.drop_table("store_design_asset")
    op.drop_index("idx_component_schema_json_gin", table_name="store_design_component_meta")
    op.drop_index("idx_component_enabled", table_name="store_design_component_meta")
    op.drop_index("idx_component_category_sort", table_name="store_design_component_meta")
    op.drop_table("store_design_component_meta")
    op.drop_index("idx_page_info_gin", table_name="store_design_page")
    op.drop_index("idx_page_datas_gin", table_name="store_design_page")
    op.drop_index("idx_page_diy_id", table_name="store_design_page")
    op.drop_index("idx_page_company_updated", table_name="store_design_page")
    op.drop_index("idx_page_company_scene", table_name="store_design_page")
    op.drop_table("store_design_page")
    op.drop_index("idx_template_pid", table_name="store_design_template")
    op.drop_index("idx_template_company_is_sel", table_name="store_design_template")
    op.drop_index("idx_template_company_type", table_name="store_design_template")
    op.drop_index("idx_template_company_updated", table_name="store_design_template")
    op.drop_table("store_design_template")
