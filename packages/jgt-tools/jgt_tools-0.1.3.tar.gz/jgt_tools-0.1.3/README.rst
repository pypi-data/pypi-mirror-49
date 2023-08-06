JGT Tools
=========

JGT Tools is a collection of package helpers for common CLI functions within a properly-formatted repository.


Quickstart
----------

Just include ``jgt_tools`` in your package VirtualEnv, and you'll have access to these CLI calls:

- ``env-setup`` - set up the development environment with all packages and pre-commit checks
- ``self-check`` - run self-checks/linters/etc. on your repository
- ``run-tests`` - run your in-repo test suite
- ``build-docs`` - build repo documentation locally
- ``build-and-push-docs`` - both build the docs, then publish to your gh-pages branch

Details for each script can be found by calling with the ``--help`` flag.

Configuration
-------------

A number of the actions to be called can be customized
in a ``[tool.jgt_tools]`` in your ``pyproject.toml`` file.
Available values are:

- ``env_setup_commands`` - a list of commands to be run under the ``env-setup`` call
- ``self_check_commands`` - a list of commands to be run under the ``self-check`` call
- ``run_tests_commands`` - a list of commands to be run under the ``run-tests`` call
- ``doc_build_types`` - a list of types for doc construction:
  - ``api`` is currently the only supported option

For example::

    [tools.jgt_tools]
    env_setup_commands = [
        "poetry install",
        "poetry run pip install other_package",
        "./my_custom_setup_script.sh"
    ]
    doc_build_types = []

would run your specified commands for ``env-setup`` and skip the ``api`` doc builder.
