import distro


IS_MAC = distro.id() == 'darwin'
IS_UBUNTU = distro.id() == 'ubuntu' or distro.id() == 'debian'
ALL_MANAGERS = ('npm', 'npmg', 'yarn', 'yarng', 'bower', 'tsd', 'pip', 'pip3', 'pip_pypy', 'sys', 'Captricity')
