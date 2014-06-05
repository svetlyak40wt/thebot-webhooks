import anyjson
import times
import subprocess
import os.path

from thebot import Plugin, on_command
from thebot.batteries.http import HttpRequest
from pytils.translit import slugify


_URL_PREFIX = '/webhook/'


class Plugin(Plugin):
    """Allows to run shell command on a hit into a webhook.
    """
    def __init__(self, *args, **kwargs):
        super(Plugin, self).__init__(*args, **kwargs)
        self.hooks = {}

        if not hasattr(self.bot.config, 'webhooks_config'):
            raise RuntimeError('Please, specify --webhooks-config option')
            
        filename = self.bot.config.webhooks_config
        if not os.path.exists(filename):
            raise RuntimeError('Unable to find config file "{0}"'.format(
                filename))
        execfile(filename, {}, self.hooks)

        
            
    @staticmethod
    def get_options(parser):
        group = parser.add_argument_group('Webhooks options')
        group.add_argument(
            '--webhooks-config',
            help='A config file with webhooks description.')

    @on_command('show webhooks')
    def on_show_webhooks(self, request):
        if self.hooks:
            request.respond('Here is a list of configured webhooks:\n' + '\n'.join(
                self.hooks.keys()
            ))
        else:
            request.respond('There is no configured webhooks.')

            
    @on_command(_URL_PREFIX + '.*')
    def on_callback(self, request):
        hook_name = request.message[len(_URL_PREFIX):]
        params = self.hooks.get(hook_name)
        
        if params is None:
            request.respond('Hook not found')
        else:
            allowed_methods = params.get('allowed_methods', ['POST'])

            if isinstance(request, HttpRequest) and request.method not in allowed_methods:
                request.respond('This hook only supports {0}.'.format(
                    ', '.join(allowed_methods)))
                return

            try:
                output = subprocess.check_output(params['command'],
                                                 stderr=subprocess.STDOUT,
                                                 shell=True)
                notify = params.get('notify')
                if notify:
                    adapter = self.bot.get_adapter(notify['adapter'])
                    notification_channel = adapter.create_request(**notify['params'])
                    
                    notification_channel.respond(
                        'Command "{0}" returned result:\n{1}'.format(
                            params['command'], output))
                    
            except subprocess.CalledProcessError, e:
                request.respond(u'I tried to run command, but there was an error: ' + e.output.encode('utf-8'))
            else:
                request.respond('Done')
