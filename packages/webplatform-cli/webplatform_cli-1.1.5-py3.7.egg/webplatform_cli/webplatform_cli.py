"""usage:
   webplatform-cli [ --force --debug ] <command> [<args>...]
   webplatform-cli (--version | --help)

options:
   -h --help                            Print this help message
   --version                            Show version
   -f --force                           Force the action being preformed
   -d --debug                           Enable controller debugging mode,
                                        for controller development only

commands for the controller are:
   setup        Build containters
   update       *not finished* Local dependancy update
   start        Start
   stop         Stop
   restart      Restart
   reset        Reset

See 'webplatform-cli <command> -h' for more information on a specific command.
"""
import os
import sys

sys.dont_write_bytecode = True

cmd = {
   'setup':{'type':'noargs','headless':False},
   'start':{'type':'service','headless':True},
   'restart':{'type':'service','headless':True},
   'stop':{'type':'service','headless':True},
   'reset':{'type':'service','headless':True},
}

def main():
   try:
      from webplatform_cli import base_path
   except:
      controller_path = os.path.dirname(os.path.realpath(__file__))
      base_path = os.path.abspath(os.path.join(controller_path))
   finally:
      if base_path not in sys.path:
         sys.path.append(base_path)

   from webplatform_cli.lib.config import Settings

   settings = Settings(path=base_path)

   from cli import Docker
   from docopt import docopt

   args = docopt(__doc__,
               version='Web Platform CLI Version 1.0.3',
               options_first=True)

   if not args['<command>'] in list(cmd.keys()):
      sys.stderr.write(__doc__)
      sys.exit(1)

   import commands_parser as parser
   subargs = getattr(parser, 'docopt_%s' % (cmd[args['<command>']]['type'],))(args['<command>'], args['<args>'])

   ctrl = {}

   if cmd[args['<command>']]['type'] == 'noargs':
      ctrl['params'] = []
   elif cmd[args['<command>']]['type'] == 'run':
      ctrl['params'] = []
      for i in args['<args>']:
         if i != "run":
            ctrl['params'].append(i)
   else:
      ctrl['params'] = subargs['<args>']

   ctrl['command'] = args['<command>']

   controller = Docker(settings, debug=args['--debug'], force=args['--force'])
   controller.parse_args(**ctrl)

if __name__ == "__main__":
   main()