import time
import json
import os

TIME_INTERVAL = int(os.environ['TIME_INTERVAL'])
REQUEST_COUNT = int(os.environ['REQUEST_COUNT'])


class RedisMiddleWare:

    redis_reference = None

    @staticmethod
    def set_redis(redis_ref):
        RedisMiddleWare.redis_reference = redis_ref

    @staticmethod
    def get_redis():
        return RedisMiddleWare.redis_reference

    @staticmethod
    def check_limit(request_body):
        client_id = request_body.get('clientId')
        url = request_body.get('url')
        redis_con = RedisMiddleWare.get_redis()
        max_time = int(time.time())
        min_time = int(max_time-TIME_INTERVAL)
        existing_count = redis_con.zcount(client_id, min_time, max_time)
        if existing_count < REQUEST_COUNT:
            pickled_data = json.dumps({'url': url, 'time': max_time})
            redis_con.zadd(client_id, {pickled_data: max_time})
            return False
        return True


