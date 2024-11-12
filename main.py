from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse

import db_actions
from db import create_db


app = Flask(__name__)
api = Api(app)


def row_to_json(posts: list):
    data = []
    for post in posts:
        data.append({
            "id": post.id,
            "author": post.author,
            "text": post.text
        })

    data_response = jsonify(data)
    data_response.status_code = 200
    return data_response


class PostAPI(Resource):
    def get(self, id=0):
        if id:
            post = db_actions.get_post(id)
            if post:
                return row_to_json([post])

            answer = jsonify("Відсутня така стаття")
            answer.status_code = 404
            return answer

        posts = db_actions.get_posts()
        return row_to_json(posts)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("text")
        params = parser.parse_args()
        id = db_actions.add_post(params.get("author"), params.get("text"))
        answer = jsonify(f"Нову статтю успішно додано під id {id}")
        answer.status_code = 200
        return answer

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("text")
        params = parser.parse_args()
        answer = db_actions.update_post(id, params.get("author"), params.get("text"))
        answer = jsonify(answer)
        answer.status_code = 200
        return answer

    def delete(self, id):
        answer = db_actions.delete_post(id)
        answer = jsonify(answer)
        answer.status_code = 200
        return answer


api.add_resource(PostAPI, "/api/posts/", "/api/posts/<int:id>/")


if __name__ == "__main__":
    create_db()
    app.run(debug=True, port=3000)
