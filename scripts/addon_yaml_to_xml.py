# standard imports
import argparse
import os

# lib imports
from kodi_addon_checker.check_dependencies import VERSION_ATTRB as xbmc_versions
from lxml import etree
import requests
import yaml

# global vars
kodi_branch = os.getenv('KODI_BRANCH', 'Nexus').lower()


def handle_asset_elements(
        parent: etree.ElementBase,
        asset_data: dict
):
    """Create asset elements, handling both single items and lists."""
    for key, value in asset_data.items():
        if isinstance(value, list):
            for item in value:
                etree.SubElement(parent, key).text = item
        else:
            etree.SubElement(parent, key).text = value


def get_branch_plugins():
    url = f'http://mirrors.kodi.tv/addons/{kodi_branch}/addons.xml'
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f'Failed to get {url}')

    return etree.fromstring(response.content)


def yaml_to_xml_lxml(yaml_file: str) -> str:
    # Load YAML file
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    # Update dynamic values
    build_version = os.getenv('BUILD_VERSION')
    if build_version:  # update version if building from CI
        data['addon']['version'] = build_version

    branch_addons_xml = None

    for requirement in data['addon']['requires']['import']:
        if requirement.get('version'):
            # if the version is specified in yaml, don't look it up
            # this allows pinning a requirement to a specific version
            continue

        requirement_xml = None

        if requirement['addon'].startswith('xbmc.'):
            requirement['version'] = xbmc_versions[requirement['addon']][kodi_branch]['advised']
        elif requirement['addon'].startswith('script.module.'):
            requirement_xml = os.path.join(
                os.getcwd(), 'third-party', 'repo-scripts', requirement['addon'], 'addon.xml')
        else:
            if not branch_addons_xml:
                branch_addons_xml = get_branch_plugins()  # only get the branch addons.xml if we need it

            # get the requirement version from the branch addons.xml
            addon = branch_addons_xml.xpath(f'//addon[@id="{requirement["addon"]}"]')
            version = addon[0].attrib['version']
            requirement['version'] = version

        if requirement_xml:
            # get the version property out of the addon tag
            with open(requirement_xml, 'r', encoding='utf-8') as file:
                requirement_data = etree.parse(file)
                requirement['version'] = requirement_data.getroot().attrib['version']

    # Create XML root
    addon = etree.Element('addon', {
        'id': data['addon']['id'],
        'name': data['addon']['name'],
        'version': data['addon']['version'],
        'provider-name': data['addon']['provider-name']
    })

    # Add extensions
    for ext in data['addon']['extension']:
        extension = etree.SubElement(addon, 'extension', {'point': ext['point']})
        if 'library' in ext:
            extension.set('library', ext['library'])
        if 'assets' in ext:
            assets = etree.SubElement(extension, 'assets')
            handle_asset_elements(assets, ext['assets'])

        if 'description' in ext:
            description = etree.SubElement(extension, 'description', {'lang': ext['description']['lang']})
            description.text = ext['description']['text']

        for key in ['license', 'platform', 'source', 'website']:
            if key in ext:
                etree.SubElement(extension, key).text = ext[key]

        if 'summary' in ext:
            summary = etree.SubElement(extension, 'summary', {'lang': ext['summary']['lang']})
            summary.text = ext['summary']['text']

    # Add requirements
    requires = etree.SubElement(addon, 'requires')
    for imp in data['addon']['requires']['import']:
        etree.SubElement(requires, 'import', {
            'addon': imp['addon'],
            'version': imp['version']
        })

    # Return pretty-printed XML string
    return etree.tostring(
        addon,
        pretty_print=True,
        xml_declaration=True,
        encoding="UTF-8",
        standalone=True,
    ).decode('utf-8')


def write_xml(xml_output: str, output_file: str):
    with open(output_file, 'w') as file:
        file.write(xml_output)


def main():
    # setup argparse
    parser = argparse.ArgumentParser(description='Convert addon.yaml to XML.')
    parser.add_argument('-i', '--input', help='addon.yaml file to convert')
    parser.add_argument('-o', '--output', help='output file')
    args = parser.parse_args()

    xml_output = yaml_to_xml_lxml(yaml_file=args.input)
    if args.output:
        write_xml(xml_output=xml_output, output_file=args.output)
    else:
        print(xml_output)


if __name__ == '__main__':
    main()
