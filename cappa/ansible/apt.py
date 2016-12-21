def requirements_to_playbook_tasks(requirements, **options):
    """
    "sys": {
        "build-essentials": null
    }

    should become

    - name: install apt packages
      apt:
        name: "{{ item }}"
        update_cache: yes
      become: true
      with_items:
        - build-essentials
    """
    task = {
        'name': 'install apt packages',
        'apt': {
            'name': '{{ item }}',
            'update_cache': 'yes'
        },
        'become': 'true',
        'with_items': list(requirements.keys())
    }
    return [task]
