from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings
import logging
import os
import json
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


# 创建数据库模型基类
class JSONFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "data"):
            data = record.__dict__.get("data")
            if isinstance(data, dict):
                payload.update(data)
            else:
                payload["data"] = data
        return json.dumps(payload, ensure_ascii=False)


LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 配置查询日志记录
query_logger = logging.getLogger("query")
if not any(isinstance(h, logging.FileHandler) and getattr(h, "baseFilename", "").endswith("query.log") for h in query_logger.handlers):
    qh = logging.FileHandler(os.path.join(LOG_DIR, "query.log"))
    qh.setFormatter(JSONFormatter())
    query_logger.setLevel(logging.INFO)
    query_logger.addHandler(qh)

@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()
    query_logger.info("start", extra={"data": {"statement": statement, "params": parameters}})

@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    duration = None
    try:
        duration = time.time() - context._query_start_time
    except Exception:
        pass
    query_logger.info("end", extra={"data": {"rowcount": cursor.rowcount, "duration": f"{duration:.6f}s" if duration is not None else None}})

Base = declarative_base()

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
