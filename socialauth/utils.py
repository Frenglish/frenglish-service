from importlib import import_module


def _check_adapter_exist(name):
    try:
        import_module("socialauth.providers.{}.adapter".format(name))
        return True
    except ModuleNotFoundError:
        return False
