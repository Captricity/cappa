import platform


IS_MAC = 'Darwin' in platform.platform(terse=1)
IS_UBUNTU = platform.dist()[0] == 'Ubuntu'
ALL_MANAGERS = ('npm', 'npmg', 'yarn', 'yarng', 'bower', 'tsd', 'pip', 'pip3', 'pip_pypy', 'sys', 'Captricity')
