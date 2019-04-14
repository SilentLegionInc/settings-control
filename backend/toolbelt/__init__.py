from toolbelt.main import app


def create_app(env, start_response):
    print(env)
    print(start_response)
    return app
