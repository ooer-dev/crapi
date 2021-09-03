from crapi.blueprints import standalone, auth, api

blueprint_packages = [
    standalone,
    auth,
    api,
]

blueprints = [p.blueprint for p in blueprint_packages]
