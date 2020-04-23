from sys import stdout, exit
from argparse import ArgumentParser
from logging import getLogger, disable, StreamHandler, Formatter, INFO, DEBUG, NOTSET
from socketserver import UDPServer

from ipmisim.ipmisim import IpmiServer, IpmiServerContext

def arg_parser():
  parser = ArgumentParser(description='IPMISIM Server')
  parser.add_argument('-i', '--ipaddr', type=str, default='0.0.0.0', help='Bind IPAddress')
  parser.add_argument('-p', '--port', type=int, default=623, help='Listen Port')
  parser.add_argument('-s', '--state', type=str, default='off', choices=['off', 'on'], help='Initialize power state')
  parser.add_argument('--debug', action='store_true', help='Enable debug mode')
  args = parser.parse_args()
  return [ getattr(args, arg) for arg in vars(args) ]

def main(ipaddr, port, state, debug):
  logger = getLogger('ipmisim')
  disable(NOTSET)
  if debug:
    logger.setLevel(DEBUG)
  else:
    logger.setLevel(INFO)

  handler = StreamHandler(stdout)
  handler.setLevel(DEBUG)
  formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  handler.setFormatter(formatter)
  logger.addHandler(handler)

  IpmiServerContext().bmc.powerstate = state
  logger.info('Initialize power state: %s' % state)

  try:
    server = UDPServer((ipaddr, port), IpmiServer)
    logger.info('Started IPMISIM Server. Bind IPAddress: %s, Listen Port: %s' % (ipaddr, port))
    server.serve_forever()

  except KeyboardInterrupt:
    server.shutdown()
    server.server_close()
    exit(0)

if __name__ == '__main__':
    args = arg_parser()
    main(*args)
