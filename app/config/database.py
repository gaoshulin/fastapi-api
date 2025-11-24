from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings
from app.config.logs import get_json_logger
import time

# 创建数据库引擎
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=1800,
        connect_args={"connect_timeout": 5}
    )


# 创建查询日志记录器
query_logger = get_json_logger("query.log")

@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()
    # 记录查询开始日志
    query_logger.info("start", extra={"data": {"statement": statement, "params": parameters}})

@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    duration = None
    try:
        duration = time.time() - context._query_start_time
    except Exception:
        pass
    # 记录查询结束日志
    query_logger.info("end", extra={"data": {"rowcount": cursor.rowcount, "duration": f"{duration:.6f}s" if duration is not None else None}})


# 创建数据库模型基类
Base = declarative_base()

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
