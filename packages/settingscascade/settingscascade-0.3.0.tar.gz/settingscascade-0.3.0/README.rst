Intro
======

Settings cascade is designed for situations where you need to merge
configuration settings from different hierarchical sources. The model
is the way that CSS cascades onto elements. You can define config
the same way that css rules get specified-

.. code-block:: yaml

	task.default:
	    command: "echo hello"
	    on_complete: "echo world"
	project_name: "my project"

Then your app can use the config

.. code-block:: python

	class Task(SettingsSchema):
		_name_ = task
		command: str
		on_complete: str

	config = SettingsManager(yaml.load("config.yml"), [Task])
	task_config = config.task(class="default")
	run_task(
		command=task_config.command,
		on_complete=task_config.on_complete,
		name=config.project_name,
	)


Installation
==================

You can install settingscascade from pypi-

::

	pip install settingscascade
