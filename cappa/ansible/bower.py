import os
import json


def requirements_to_playbook_tasks(requirements, **options):
    """
    "bower": package_json

    should become

    - name: install bower packages
      bower:
        path: app location

    ----------
    "bower": {
        'foo': '2.5.4'
    }

    should become

    - name: install bower packages
      bower:
        name: foo
        version: 2.5.4
        path: current
    """
    # HACK: detect whether or not package.json by looking for name keyword
    if 'name' in requirements:
        return __bower_json_to_playbook_tasks(requirements, **options)
    else:
        return __standard_to_playbook_tasks(requirements, **options)


def __bower_json_to_playbook_tasks(requirements, **options):
    if 'target_dir' in requirements:
        # set application path
        application_path = os.path.abspath(requirements['target_dir'])
    else:
        application_path = os.path.abspath(os.getcwd())

    with open(os.path.join(application_path, 'bower.json'), 'w') as json_file:
        json.dump(requirements, json_file)

    task = {
        'name': 'install bower packages',
        'bower': {
            'path': application_path
        }
    }

    if options.get('save_js', False):
        return [task]
    else:
        rm_js_task = {
            'name': 'remove bower bower.json',
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
        'name': 'install bower packages',
        'bower': {
            'path': application_path,
            'name': '{{ item.name }}',
            'version': '{{ item.version }}'
        },
        'with_items': item_list
    }
    return [task]
