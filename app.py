from flask import Flask, render_template, jsonify
import time
from redis import (
    ConnectionPool,
    StrictRedis
)

app = Flask(__name__)

connection_pool = ConnectionPool().from_url(url="redis://localhost:6379")
redis_client = StrictRedis(connection_pool=connection_pool)


def initialize_scoreboard():
    for i in range(1, 10):
        redis_client.zadd(name="scoreboard:1", mapping={f'player:{i}': 0})


@app.route('/')
def home():
    initialize_scoreboard()
    return render_template('home.html')


@app.route('/scores')
def scores():
    z_scores = redis_client.zrange(name="scoreboard:1", start=0, end=-1, desc=True, withscores=True)
    z_scores = [{'player_id': score[0].decode, 'score': score[1]} for score in z_scores]  # can't jsonify bytes
    return jsonify(scores=z_scores, last_updated_at=time.time())


if __name__ == '__main__':
    app.run()
