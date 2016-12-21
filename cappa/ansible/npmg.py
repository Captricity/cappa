from .npm import requirements_to_playbook_tasks as npm


def requirements_to_playbook_tasks(requirements, **options):
    options['global'] = True
    return npm(requirements, **options)
