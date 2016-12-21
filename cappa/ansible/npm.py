import os
import json
from ..enums import IS_MAC


def requirements_to_playbook_tasks(requirements, **options):
    """
    "npm": package_json

    should become

    - name: install npm packages
      npm:
        path: app location

    ----------
    "npm": {
        'foo': '2.5.4'
    }

    should become

    - name: install npm packages
      npm:
        name: foo
        version: 2.5.4
        path: current
    """
    # HACK: detect whether or not package.json by looking for name keyword
    if 'name' in requirements:
        return __package_json_to_playbook_tasks(requirements, **options)
    else:
        return __standard_to_playbook_tasks(requirements, **options)


def __package_json_to_playbook_tasks(requirements, **options):
    if 'target_dir' in requirements:
        # set application path
        application_path = os.path.abspath(requirements['target_dir'])
    else:
        application_path = os.path.abspath(os.getcwd())

    with open(os.path.join(application_path, 'package.json'), 'w') as json_file:
        json.dump(requirements, json_file)

    task = {
        'name': 'install npm packages',
        'npm': {
            'path': application_path
        }
    }
    if options.get('global', False):
        task['npm']['global'] = 'yes'
        if not IS_MAC:
            task['become'] = 'yes'

    if options.get('save_js', False):
        return [task]
    else:
        rm_js_task = {
            'name': 'remove npm package.json',
            'file': {
                'path': json_file.name,
                'state': 'absent'
            }
        }
        return [task, rm_js_task]


def __standard_to_playbook_tasks(requirements, **options):
    if 'target_dir' in requirements:
        # set application path
        application_path = os.path.abspath(requirements['target_dir'])
    else:
        application_path = os.path.abspath(os.getcwd())

    item_list = [{'name': key, 'version': value} for key, value in requirements.iteritems()]
    task = {
        'name': 'install npm packages',
        'npm': {
            'path': application_path,
            'name': '{{ item.name }}',
            'version': '{{ item.version }}'
        },
        'with_items': item_list
    }
    if options.get('global', False):
        task['npm']['global'] = 'yes'
        if not IS_MAC:
            task['become'] = 'yes'
    return [task]
