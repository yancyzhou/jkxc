# -*- encoding:utf-8 -*-
import motor
from tornado import httpserver, ioloop, options as Options, web
from config import *
from utils import *
from tornado.options import define, options
import tornado
import click
from sqlalchemy.orm import scoped_session, sessionmaker
from model.models import *


@click.command()
@click.option('--port', default=ServersPort, help='webui port')
def cli(**kwargs):
    define("port", default=kwargs['port'], help="run on the given port", type=int)
    Options.parse_command_line()
    http_server = httpserver.HTTPServer(Application(),xheaders=True)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()

    def column_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

    Base.column_dict = column_dict #add data for select to dict


# def init_db():
    # Base.metadata.create_all(EngineInsert)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = Handlers
        # settings = Settings
        # client = motor.motor_tornado.MotorClient(DB)
        # self.dbs = client[Collections]
        web.Application.__init__(self, handlers)
        self.DbRead = scoped_session(sessionmaker(bind=EngineRead, autocommit=False,autoflush=True, expire_on_commit=True))

if __name__ == "__main__":
    cli()
