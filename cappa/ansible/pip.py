import sys


def requirements_to_playbook_tasks(requirements, **options):
    """
    "pip": {
        "psycopg2": "2.5.4"
    }

    should become

    - name: install pip packages
      pip:
        name: "{{ item.name }}"
        version: "{{ item.version }}"
      with_items:
        - {name: psycopg2, version: 2.5.4}
    """
    item_list = [{'name': key, 'version': value} for key, value in requirements.iteritems()]
    _PIP_STRING = """name={{ item.name }}
        {% if item.version %}
            version={{ item.version }}
        {% else %}
            state=latest
        {% endif %}"""
    task = {
        'name': 'install pip packages',
        'pip': _PIP_STRING,
        'with_items': item_list
    }
    if options.get('use_venv', True):
        # Make sure we are in a virtualenv
        # TODO: create a sensible error message
        assert hasattr(sys, 'real_prefix')
    else:
        __modify_with_global(task)
    return [task]


def __modify_with_global(task_dict):
    # Make sure we are NOT in a virtualenv
    # TODO: create a sensible error message
    assert not hasattr(sys, 'real_prefix')
    task_dict['become'] = 'yes'
