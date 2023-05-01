import redis
import os


# create connection to redis
redis = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    db=0)
# create connection to postgres