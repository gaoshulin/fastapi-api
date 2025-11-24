import redis
import json
from typing import Any, Optional
from app.config.settings import settings


class RedisCache:
    """
    Redis 缓存工具类，支持字符串/JSON 存储
    """
    def __init__(self, host: str = settings.REDIS_HOST,port: int = settings.REDIS_PORT,db: int = settings.REDIS_DB,password: str = settings.REDIS_PASS,expire_seconds: int = 3600):
        # 初始化连接池
        self.pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )
        self.redis = redis.Redis(connection_pool=self.pool)
        self.default_expire = expire_seconds

    def set(self, key: str, value: Any, expire_seconds: Optional[int] = None):
        """
        写入缓存（自动适配字符串/JSON）
        :param key: 缓存键
        :param value: 缓存值（字符串/字典/列表）
        :param expire_seconds: 过期时间，默认使用类的默认值
        """
        expire = expire_seconds or self.default_expire
        # 若为非字符串，序列化为 JSON
        if not isinstance(value, str):
            value = json.dumps(value, ensure_ascii=False)
        self.redis.set(key, value, ex=expire)

    def get(self, key: str, is_json: bool = False) -> Optional[Any]:
        """
        读取缓存
        :param key: 缓存键
        :param is_json: 是否反序列化为 JSON
        :return: 缓存值（None=不存在/过期）
        """
        value = self.redis.get(key)
        if not value:
            return None
        # 若需 JSON，反序列化
        if is_json:
            return json.loads(value)
        return value

    def delete(self, key: str) -> bool:
        """删除缓存，返回是否删除成功"""
        return self.redis.delete(key) > 0

    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        return self.redis.exists(key) > 0

    def clear_prefix(self, prefix: str) -> int:
        """按前缀删除缓存（如：prefix='api:' 删除所有 api: 开头的键）"""
        keys = self.redis.keys(f"{prefix}*")
        if not keys:
            return 0
        return self.redis.delete(*keys)
