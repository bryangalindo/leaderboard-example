import time

from flask import Flask, render_template, jsonify
from redis import ConnectionPool, StrictRedis


app = Flask(__name__)

connection_pool = ConnectionPool().from_url(url="redis://localhost:6379")
redis_client = StrictRedis(connection_pool=connection_pool)


def set_scoreboard():
    for i in range(1, 10):
        redis_client.zadd(name="scoreboard:1",
                          mapping={f'player:{i}': 0})


def get_scores():
    z_scores = redis_client.zrange(name="scoreboard:1",
                                   start=0,
                                   end=-1,
                                   desc=True,
                                   withscores=True)
    return [{'player_id': score[0].decode(), 'score': score[1]} for score in z_scores]


@app.route('/')
def home():
    set_scoreboard()
    return render_template('home.html')


@app.route('/scores')
def scores():
    z_scores = get_scores()
    return jsonify(scores=z_scores, last_updated_at=time.time())


if __name__ == '__main__':
    app.run()
