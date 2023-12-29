# standard imports
import os
import shutil
import subprocess
import sys

# local imports
from src.themerr import constants

# list of directory to copy contents of
source_dirs = [
    'src',
]

# list of files to copy
source_files = [
    'LICENSE.txt',
]

# clean directories
clean_dirs = [
    os.path.join('resources', 'lib', 'bin'),
]

script_directory: str = os.path.dirname(os.path.abspath(__file__))
root_directory: str = os.path.dirname(script_directory)
build_root_directory: str = os.path.join(root_directory, 'build')
build_directory: str = os.path.join(build_root_directory, constants.addon_id)
pip_install_directory: str = os.path.join(build_directory, 'resources', 'lib')


def build():
    # create the build directory
    try:
        os.makedirs(build_directory, exist_ok=False)
    except FileExistsError:
        # remove the build directory
        shutil.rmtree(build_directory)

        # create the build directory
        os.makedirs(build_directory, exist_ok=False)

    # copy the source directories, recursively
    for directory in source_dirs:
        source_directory: str = os.path.join(root_directory, directory)
        shutil.copytree(
            src=source_directory,
            dst=build_directory,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns('*.pyc', '__pycache__'),
        )

    # copy the source files
    for file in source_files:
        source_file: str = os.path.join(root_directory, file)
        destination_file: str = os.path.join(build_directory, file)

        shutil.copy2(source_file, destination_file)


def generate_xml():
    """
    Generate addon.xml from addon.yaml.
    """
    # yaml file
    yaml_file: str = os.path.join(root_directory, 'addon.yaml')

    # xml file
    xml_file: str = os.path.join(build_directory, 'addon.xml')

    # convert yaml to xml
    subprocess.run(
        args=[
            sys.executable, '-m', 'scripts.addon_yaml_to_xml',
            '--input', yaml_file,
            '--output', xml_file,
        ],
        check=True,  # raise called process error if return code is non-zero
    )


def compile_localizations():
    """
    Compile localizations in subprocess.
    """
    # kodi using po files for localization, no need to compile to mo
    subprocess.run(
        args=[sys.executable, '-m', 'scripts.locale', '--update'],
    )

    # locale directories
    locale_source_directory: str = os.path.join(root_directory, 'locale')
    locale_dest_directory: str = os.path.join(build_directory, 'resources', 'language')

    # for each directory in locale source directory
    for item in os.listdir(locale_source_directory):
        if os.path.isdir(os.path.join(locale_source_directory, item)):
            # copy the po file
            po_source_file: str = os.path.join(locale_source_directory, item, 'LC_MESSAGES', 'themerr-kodi.po')
            language = item
            po_dest_directory: str = os.path.join(locale_dest_directory, f'resource.language.{language}')
            po_dest_file: str = os.path.join(po_dest_directory, 'strings.po')

            # create the destination directory
            os.makedirs(po_dest_directory, exist_ok=True)
            shutil.copy2(po_source_file, po_dest_file)


def check_addon():
    """
    Run kodi-addon-checker --branch nexus service.themerr in subprocess.
    """
    kodi_branch = os.getenv('KODI_BRANCH', 'Nexus').lower()
    subprocess.run(
        args=['kodi-addon-checker', '--branch', kodi_branch, build_directory],
        check=True,  # raise called process error if return code is non-zero
    )


def install_dependencies():
    """
    Install dependencies in subprocess, using this script's python executable.
    """
    # get python executable path
    python = sys.executable

    # install dependencies to specified directory
    subprocess.run(
        args=[python, '-m', 'pip', 'install', '-r', 'requirements.txt', '-t', pip_install_directory],
        check=True,  # raise called process error if return code is non-zero
    )


def clean():
    """
    Clean the build directory.
    """
    for directory in clean_dirs:
        directory_path: str = os.path.join(build_directory, directory)
        if os.path.isdir(directory_path):
            print(f"Removing {directory_path}")
            shutil.rmtree(directory_path)

    # recursively remove any __pycache__ directories
    for root, dirs, files in os.walk(build_directory):
        for directory in dirs:
            if directory == '__pycache__':
                directory_path: str = os.path.join(root, directory)
                print(f"Removing {directory_path}")
                shutil.rmtree(directory_path)


def package():
    """
    Package the addon into a zip file.
    """
    # remove the archive if it exists
    archive_name: str = constants.addon_id
    archive_path: str = os.path.join(root_directory, f"{archive_name}.zip")
    final_archive_path: str = os.path.join(build_root_directory, f"{archive_name}.zip")
    if os.path.exists(final_archive_path):
        os.remove(final_archive_path)

    shutil.make_archive(
        base_name=archive_name,
        format='zip',
        root_dir=build_root_directory,
    )

    # move to build root directory
    shutil.move(
        src=archive_path,
        dst=build_root_directory,
    )


if __name__ == '__main__':
    build()
    generate_xml()
    compile_localizations()

    check_addon()

    # ideally this would be before the check, but kodi-addon-checker tries refactoring everything
    install_dependencies()
    clean()

    package()
