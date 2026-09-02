"""Get package version to display in documentation"""

from importlib.metadata import version

def define_env(env):
    env.variables['package_version'] = version("lgbfscotland")
