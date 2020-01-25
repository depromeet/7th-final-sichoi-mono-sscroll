import json
import traceback
from contextlib import contextmanager
from functools import wraps

from app import db, models
from app.context import ApiContext
from flask import abort, request


@contextmanager
def create_session():
    session = db.create_session()
    try:
        yield session
        session.commit()
    except Exception as e:
        print(traceback.format_exc())
        session.rollback()
        raise
    finally:
        session.close()


def router(application, **kwargs):
    def route(uri, **kwargs):
        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):

                with create_session() as session:
                    res = {}
                    context = create_context(session)
                    kwargs['context'] = context
                    res: str = json.dumps(fn(*args, **kwargs))

                    packet = models.Packet(
                        request_header=dict(context.request.headers),
                        request_body=context.data,
                        response_header={},
                        response_body=res,
                    )

                    context.session.add(packet)
                    context.session.commit()
                return res

            application.add_url_rule(uri, fn.__name__, decorator, **kwargs)
            return decorator

        return wrapper

    return route


def create_context(session=None):
    if session is None:
        session = db.create_session()
    return ApiContext(session=session, request=request)
