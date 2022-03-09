from redis import ConnectionPool, StrictRedis
import random
import time

connection_pool = ConnectionPool().from_url(url="redis://localhost:6379")
redis_client = StrictRedis(connection_pool=connection_pool)


if __name__ == '__main__':
    while True:
        for i in range(1, 10):
            score_amount = random.randint(-5, 15)
            redis_client.zincrby("scoreboard:1", value=f'player:{i}', amount=score_amount)
        time.sleep(0.5)
