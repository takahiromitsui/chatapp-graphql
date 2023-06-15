from flask import Flask, request, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.controllers.user import resolve_create_user, resolve_login, resolve_users
from src.controllers.room import resolve_create_room, resolve_rooms
from src.controllers.message import resolve_create_message, resolve_messages
from src.models import room, user, user_room, message
from src.extensions import db, migrate
from ariadne import graphql_sync, make_executable_schema, ObjectType, snake_case_fallback_resolvers, gql, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate.init_app(app, db)

query = ObjectType('Query')
query.set_field('users', resolve_users)
query.set_field('rooms', resolve_rooms)
query.set_field('messages', resolve_messages)
query.set_field('login', resolve_login)

mutation = ObjectType('Mutation')
mutation.set_field('createUser', resolve_create_user)
mutation.set_field('createRoom', resolve_create_room)
mutation.set_field('createMessage', resolve_create_message)

explorer_html = ExplorerGraphiQL().html(None)

type_defs = gql(load_schema_from_path("schema.graphql"))
schema = make_executable_schema(type_defs, query, mutation, snake_case_fallback_resolvers)

@app.route("/")
def index():
    return "Hello World!"


@app.route("/graphql", methods=["GET"])
def graphql_explorer():
    return explorer_html, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value={"request": request},
        debug=app.debug
    )

    status_code = 200 if success else 400
    try:
        token = result['data']['login']['token']
        if token:
            response = jsonify(result)
            response.headers["Authorization"] = f"Bearer {token}"
        
    except:
        status_code = 200 if success else 400
        
    return jsonify(result), status_code



if __name__ == "__main__":
    app.run()