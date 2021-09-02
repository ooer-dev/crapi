from crapi.blueprints import standalone, auth

blueprint_packages = [
    standalone,
    auth,
]

blueprints = [p.blueprint for p in blueprint_packages]
