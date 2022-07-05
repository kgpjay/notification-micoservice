from datetime import datetime
from typing import Tuple

import connexion
from flask import jsonify
from sqlalchemy.orm import joinedload

from project.models.init_db import db
from project.models.models import Film, FilmCast
from project.serializers.serializers import FilmCastSchema

def get() -> Tuple[dict, int]:
    query = FilmCast.query.options(
        joinedload(FilmCast.film),
        joinedload(FilmCast.actor),
    ).paginate(
        connexion.request.args.get("paginationKey", 1),
        connexion.request.args.get("pageSize", 5)
    )
    schema = FilmCastSchema()
    result = schema.dump(query.items, many=True)
    return jsonify(result), 200


def search() -> Tuple[dict, int]:
    return get()


def post()-> dict:
    if connexion.request.is_json:
        data = connexion.request.get_json()
        film_cast = FilmCast(film_id=data["filmId"], actor_id=data["actorId"])
        db.session.add(film_cast)
        db.session.commit()

        return jsonify(FilmCastSchema().dump(film_cast))
    return jsonify({})

