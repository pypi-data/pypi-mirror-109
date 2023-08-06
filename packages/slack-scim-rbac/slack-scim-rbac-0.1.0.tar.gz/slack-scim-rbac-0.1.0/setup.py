# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slack_scim_rbac']

package_data = \
{'': ['*']}

install_requires = \
['slack-bolt>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'slack-scim-rbac',
    'version': '0.1.0',
    'description': 'Role Based Access Control for Slack-Bolt applications',
    'long_description': '# Role Based Access Control for Slack-Bolt Apps\n\nRole Based Access Control (RBAC) is a term applied to limiting the\nauthorization for a specific operation based on the association of a User to a\n"role".  For example:\n\n    As an application developer, I want to ensure that only specific Users in a\n    given User-Group are allowed to execute the "bounce port" command.\n\nThe Slack Platform does not natively support the concept of "User Groups", but\nit does support the standard protcol: System for Cross-domain Identity\nManagement (SCIM).  A method for implemeting RBAC in Slack can be accomlished\nusing the Slack SCIM API feature.  For example:\n\n    As an IT administrator of Okta, I will create SCIM groups that will designate\n    the specific RBAC User-Groups I want to use in Slack.\n\nThis `slack-scim-rbac` repository provides a Slack-Bolt _middleware_ class.\n\nAs a developer using the SCIM protocol, you must obtain a SCIM Token from your Slack\nadministrator and export the environment variable `SLACK_SCIM_TOKEN`.\n\nThe following code snippet is take from the [example](example/rbacker/app_listeners.py).\nIn this example the User that entered the "bounce port" message must be a member\nof the SCIM group "ChatOps-foo".  If they are not, then an error message is reported\nto the User.\n\n```python\nfrom slack_scim_rbac.middleware import AsyncSlackScimRBAC\n\n@app.message(\n    re.compile("bounce port", re.I),\n    middleware=[AsyncSlackScimRBAC(groups={"ChatOps-foo"})],\n)\nasync def app_bounce_port(request: BoltRequest, context: BoltContext, say: Say):\n    await say(f"bouncing port for you <@{context.user_id}> ... standby")\n```\n\n# Customizing the Error Response\n\nAs a developer you will want to customize the error response to the User.\nThere are two ways to do this. The first way is to provide an `error_response`\nfunction to middleware addition.  For example this code will trigger a Modal\nwhen the User triggers the `/rbacker` command that contains the text "bounce\nport" when they are not part of the "ChatOps-nofuzz" SCIM group.\n\n```python\nasync def is_bounce_port_command(command: dict):\n    return "bounce port" in command["text"]\n\n\nasync def modal_no_you_cant(client: AsyncWebClient, body: dict, context: AsyncBoltContext):\n    msg = f"Nope! Sorry <@{context.user_id}> but you cannot do that!"\n\n    view = View(title="Permission Denied!", type="modal", close="Bummer")\n    view.blocks = [SectionBlock(text=MarkdownTextObject(text=msg))]\n    await client.views_open(trigger_id=body["trigger_id"], view=view)\n\n\n@app.command(\n    command="/rbacker",\n    matchers=[is_bounce_port_command],\n    middleware=[\n        AsyncSlackScimRBAC(\n            app_name=app.name,\n            groups={"ChatOps-nofuzz"},\n            error_response=modal_no_you_cant,\n        )\n    ],\n)\nasync def slash_rbacker_bounce_port(ack: Ack, say: Say, context: Context):\n    await ack()\n    await say(\n        f"Already then, <@{context.user_id}>, let\'s get to bouncing that port for ya!"\n    )\n```\n\nThe other approach is to sub-class the `AsyncSlackScimRBAC` class and\noverriding the `error_response` method.\n\n# Customizing the RBAC Validation Process\n\nBy default the validate process checks the Slack User groups (name) membership\nin any of the required group names.  You can override this behavior (for\nexample if you have a default "admin" group that you want to always allow but\nnot require in each listener declaration) by sub-classing `AsyncSlackScimRBAC`\nand overriding the `is_member` method.\n\n# Limitations\n\nThis `slack-scim-rbac` repository implements middleware for asyncio mode only.\nA sync implementation should be straightforward, but has not been done since it\nis not what I needed.  If you do, please open an issue (or a PR).  Thanks!\n\n# Resources\n\n* [Slack-Bolt for Python](https://slack.dev/bolt-python/tutorial/getting-started)\n* [Video: Getting Started with Python Slack-Bolt PyCon 2021](https://www.youtube.com/watch?v=Mlh8BD7xlgE)\n* [Article: What is SCIM?](https://www.okta.com/blog/2017/01/what-is-scim/)\n',
    'author': 'Jeremy Schulman',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jeremyschulman/slack-scim-rbac',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
