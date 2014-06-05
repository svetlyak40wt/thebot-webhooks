thebot-webhooks
===============

A way to run shell scripts in respond to a webhook call.
This way you could trigger an automatic deployment on push
to GitHub. Or run unittests, or something else.

Installation
------------

Run `pip install thebot-webhooks`, then run TheBot with additional
plugin `webhooks` and parameters where you content is stored and how to regenerate a
static content:

    thebot --plugins webhooks --adapters http \
           --http-host 0.0.0.0 --http-port 9991 \
           --webhooks-config hooks.conf

Then place something like that into the `hooks.conf`:

    github_4567GH67 = dict(
        command='sudo salt "*" state.highstate',
    )

Here `github_4567GH67` is a webhook's handle. It will be accessable at `http://0.0.0.0:9991/webhook/github_4567GH67`.
And `command` could be any shell command to be run when a HTTP request will hit the handle.
In this example, we are starting deployment using [SaltStack](http://www.saltstack.com/).

By default, only POST method is allowed. If you need a GET for some wierd reason, then add this such key into
the dict: `allowed_methods=['GET', 'POST']`.

Authors
-------

* Alexander Artemenko &lt;svetlyak.40wt@gmail.com>