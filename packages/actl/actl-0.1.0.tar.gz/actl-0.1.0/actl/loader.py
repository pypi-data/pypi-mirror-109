import importlib.util
import inspect


def get_objects(module, match_class):
    objects = []
    for name, obj in inspect.getmembers(module):
        if isinstance(obj, match_class):
            objects.append(obj)
    return objects


def load_modules(prefix, path, match_class):
    all_objects = []
    module_list = path.glob("*.py")
    for module_fname in module_list:
        mod_name = f"{prefix}{module_fname.stem}"
        spec = importlib.util.spec_from_file_location(mod_name, module_fname)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        all_objects.extend(get_objects(module, match_class))
    return all_objects
