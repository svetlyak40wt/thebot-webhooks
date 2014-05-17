import anyjson
import times
import subprocess
import os.path

from thebot import Plugin, on_command
from pytils.translit import slugify

_URL_PREFIX = '/webhook/'

class Plugin(Plugin):
    def __init__(self, *args, **kwargs):
        super(Plugin, self).__init__(*args, **kwargs)
        self.hooks = {}
        
        filename = self.bot.config.webhooks_config
        assert os.path.exists(filename), 'Unable to find config file "{0}"'.format(
            filename)
        execfile(filename, {}, self.hooks)

        
            
    @staticmethod
    def get_options(parser):
        group = parser.add_argument_group('DraftIn options')
        group.add_argument(
            '--webhooks-config',
            help='A config file with webhooks description.')
        
    @on_command(_URL_PREFIX + '.*')
    def on_callback(self, request):
        hook_name = request.message[len(_URL_PREFIX):]
        params = self.hooks.get(hook_name)
        
        if params is None:
            request.respond('Hook not found')
        else:
            allowed_methods = params.get('allowed_methods', ['POST'])
            
            if request.method not in allowed_methods:
                request.respond('This hook only supports {0}.'.format(
                    ', '.join(allowed_methods)))
            else:
                try:
                    subprocess.check_output(params['command'],
                                            stderr=subprocess.STDOUT,
                                            shell=True)
                except subprocess.CalledProcessError, e:
                    request.respond(u'I tried to run command, but there was an error: ' + e.output.encode('utf-8'))
                else:
                    request.respond('Done')
