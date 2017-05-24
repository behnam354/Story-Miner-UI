from app import app
from daemon import Daemon
import sys


class MyDaemon(Daemon):
    def run(self):
        while True:
            app.run(host = '0.0.0.0', port='5000')
            
if __name__ == "__main__":
    daemon = MyDaemon('/tmp/serve.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: python %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
