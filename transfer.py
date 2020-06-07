import redis


local_r = redis.Redis()

na_redis = redis.Redis('', db=1)


def migrate_redis(src, dst):
    for key in src.keys('*'):
        ttl = src.ttl(key)
        if ttl < 0:
            ttl = 0
        print("Dumping key: %s" % key)
        value = src.dump(key)
        print("Restoring key: %s" % key)
        try:
            dst.restore(key, ttl * 1000, value, replace=True)
        except redis.exceptions.ResponseError:
            print("Failed to restore key: %s" % key)
            pass
    return

migrate_redis(local_r, na_redis)
