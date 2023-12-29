# standard imports
import os
import sys

# lib imports
import yaml

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_modules():
    addon_config = os.path.join(root_dir, 'addon.yaml')
    with open(addon_config, 'r') as file:
        data = yaml.safe_load(file)

    modules = []
    for requirement in data['addon']['requires']['import']:
        if requirement['addon'].startswith('script.module.'):
            modules.append(requirement['addon'])

    return modules


def bootstrap_modules():
    lib_dirs = (
        'lib',
        'libs',
    )

    required_modules = get_modules()

    # check if the required modules are installed, only for unit testing
    for m in required_modules:
        module_found = False
        for p in sys.path:
            if not module_found:
                for lib_dir in lib_dirs:
                    if p.endswith(os.path.join(m, lib_dir)):
                        module_found = True
                        break  # break out of lib_dirs loop
            else:
                break  # module already found, break out of sys.path loop
        if not module_found:

            for lib_dir in lib_dirs:
                dev_path = os.path.join(root_dir, 'third-party', 'repo-scripts', m, lib_dir)
                if os.path.isdir(dev_path):
                    print(f"Adding dev path: {dev_path}")
                    sys.path.insert(0, dev_path)
                    module_found = True
                    break

            if not module_found:
                print(f"Module not found: {m}")
                raise ModuleNotFoundError(f"Module not found: {m}")
