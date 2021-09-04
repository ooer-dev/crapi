from crapi.blueprints import api, auth, standalone

blueprint_packages = [
    api,
    auth,
    standalone,
]

blueprints = [p.blueprint for p in blueprint_packages]
