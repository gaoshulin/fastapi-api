# /Applications/project/python/echosell-api/app/config/log.py
import logging
import os
import json
from logging.handlers import RotatingFileHandler


class JSONFormatter(logging.Formatter):
    """
    自定义 JSON 日志格式化器
    """
    def format(self, record):
        payload = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        data = record.__dict__.get("data")
        if data is not None:
            if isinstance(data, dict):
                payload.update(data)
            else:
                payload["data"] = data
        return json.dumps(payload, ensure_ascii=False)


def _log_dir():
    """
    获取日志目录路径
    """
    root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    path = os.path.join(root, "logs")
    os.makedirs(path, exist_ok=True)
    return path


def get_json_logger(filename: str, level: int = logging.INFO) -> logging.Logger:
    """
    获取 JSON 格式的日志记录器
    """
    logger = logging.getLogger(filename)
    if not any(
        isinstance(h, logging.FileHandler) and getattr(h, "baseFilename", "").endswith(filename)
        for h in logger.handlers
    ):
        # fh = logging.FileHandler(os.path.join(_log_dir(), filename))
        # 配置文件滚动日志
        fh = RotatingFileHandler(
            os.path.join(_log_dir(), filename), # 日志文件名
            maxBytes=5*1024*1024, # 单个文件最大5MB
            backupCount=7, # 备份文件数量
            encoding='utf-8'  # 确保中文正常写入
        )
        fh.setFormatter(JSONFormatter())
        logger.setLevel(level)
        logger.addHandler(fh)
        logger.propagate = False
    return logger


def log_json(filename: str, message: str, data=None, level: int = logging.INFO) -> None:
    """
    记录 JSON 格式的日志
    """
    logger = get_json_logger(filename, level=level)
    logger.log(level, message, extra={"data": data or {}})