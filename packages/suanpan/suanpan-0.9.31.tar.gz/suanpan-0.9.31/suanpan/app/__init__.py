# coding=utf-8
from __future__ import absolute_import, print_function

import os

from suanpan.proxy import Proxy


class App(Proxy):
    MAPPING = {
        "spark": "suanpan.app.spark.SparkApp",
        "docker": "suanpan.app.docker.DockerApp",
        "stream": "suanpan.app.stream.StreamApp",
    }

    def __init__(self, *args, **kwargs):
        super(App, self).__init__()
        self.setBackend(*args, **kwargs)


TYPE = os.environ.get("SP_APP_TYPE")
app = App(type=TYPE)
