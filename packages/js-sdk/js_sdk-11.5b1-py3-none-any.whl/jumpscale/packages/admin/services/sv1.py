from jumpscale.loader import j
from jumpscale.tools.servicemanager.servicemanager import BackgroundService
import gevent

class SV1Service(BackgroundService):
    def __init__(self, interval="* * * * *", *args, **kwargs):
        """
            Check disk space every 1 minute
        """
        super().__init__(interval, *args, **kwargs)

    def job(self):
        for i in range(20):
            rc, out, err = j.sals.process.execute("echo sv1")
            print(out)
            gevent.sleep(0)


service = SV1Service()
