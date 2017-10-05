from setuptools import setup, find_packages

console_scripts = [
        'git2nd=git2nd.git2nd:main',
        'gi=git2nd.git2nd:main',
        'gis=git2nd.git2nd:status_func',
        'gia=git2nd.git2nd:add_routine',
        'gic=git2nd.git2nd:commit_routine',
        'gip=git2nd.git2nd:push_routine',
        'gib=git2nd.git2nd:branch_routine',
        'gim=git2nd.git2nd:merge_routine',
        'gil=git2nd.git2nd:log_routine',
        'giff=git2nd.git2nd:diff_routine',
        'gif=git2nd.git2nd:diff_routine',
        'gir=git2nd.git2nd:return_routine',
        'giv=git2nd.git2nd:vim_routine',
        'giac=git2nd.git2nd:ac_routine',
        'giacp=git2nd.git2nd:acp_routine',
        'gicp=git2nd.git2nd:cp_routine',
        'gimp=git2nd.git2nd:mp_routine'
        ]

setup(
    name='git2nd',
    version='0.0.1',
    packages=find_packages(),
    description='git2nd',
    author='Taisei Miyagawa @miyagaw61',
    author_email='miyagaw61@gmail.com',
    install_requires=['enert==0.0.2', 'better_exceptions'],
    dependency_links=['git+https://github.com/miyagaw61/enert.git#egg=enert-0.0.2'],
    entry_points = {'console_scripts': console_scripts},
    url='https://github.com/miyagaw61/git2nd',
    license='MIT'
)
