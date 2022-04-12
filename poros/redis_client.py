# -*- coding: utf-8 -*-
import redis

from conf.settings import REDIS_SETTINGS

# redis初始化
rds = redis.Redis(
    **REDIS_SETTINGS,
    decode_responses=True,
    max_connections=30)

rds_bytes = redis.Redis(
    **REDIS_SETTINGS,
    decode_responses=False,
    max_connections=20)

redis_local = redis.Redis(
    host='127.0.0.1',
    port=6379,
    db=6,
    password='',
    decode_responses=True,
    max_connections=20)
