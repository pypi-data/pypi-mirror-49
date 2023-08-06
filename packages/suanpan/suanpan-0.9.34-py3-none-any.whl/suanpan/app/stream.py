# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan.app.base import BaseApp
from suanpan.stream import Handler, Stream
from suanpan.utils import functional


class TriggerApp(BaseApp):
    def __init__(self, streamApp, *args, **kwargs):
        super(TriggerApp, self).__init__(*args, **kwargs)
        self.streamApp = streamApp
        self.handler = None
        self.interval = None

    def __call__(self, interval):
        self.interval = interval

        def _dec(funcOrApp):
            funcOrApp = (
                self.handler
                if isinstance(funcOrApp, TriggerApp)
                else functional.instancemethod(funcOrApp)
            )
            self.handler = Handler.use(funcOrApp)
            return self

        return _dec

    def input(self, argument):
        def _dec(funcOrApp):
            funcOrApp = (
                self.handler
                if isinstance(funcOrApp, TriggerApp)
                else functional.instancemethod(funcOrApp)
            )
            self.handler = Handler.input(argument)(funcOrApp)
            return self

        return _dec

    def output(self, argument):
        def _dec(funcOrApp):
            funcOrApp = (
                self.handler
                if isinstance(funcOrApp, TriggerApp)
                else functional.instancemethod(funcOrApp)
            )
            self.handler = Handler.output(argument)(funcOrApp)
            return self

        return _dec

    def param(self, argument):
        self.streamApp.arguments.append(argument)

        def _dec(funcOrApp):
            funcOrApp = (
                self.handler
                if isinstance(funcOrApp, TriggerApp)
                else functional.instancemethod(funcOrApp)
            )
            self.handler = Handler.use(funcOrApp)
            return self

        return _dec

    def column(self, argument):
        self.streamApp.arguments.append(argument)

        def _dec(funcOrApp):
            funcOrApp = (
                self.handler
                if isinstance(funcOrApp, TriggerApp)
                else functional.instancemethod(funcOrApp)
            )
            self.handler = Handler.use(funcOrApp)
            return self

        return _dec


class StreamApp(BaseApp):
    def __init__(self, *args, **kwargs):
        super(StreamApp, self).__init__(*args, **kwargs)
        self.triggerApp = TriggerApp(self)
        self.stream = None
        self.handler = None
        self.arguments = []

    def __call__(self, *args, **kwargs):
        if self.handler:
            self.handler.beforeCallHooks.extend(self.beforeCallHooks)
            self.handler.afterCallHooks.extend(self.afterCallHooks)
            self.handler.beforeSaveHooks.extend(self.beforeSaveHooks)
            self.handler.afterSaveHooks.extend(self.afterSaveHooks)

        if self.trigger.handler:
            self.trigger.handler.beforeCallHooks.extend(self.trigger.beforeCallHooks)
            self.trigger.handler.afterCallHooks.extend(self.trigger.afterCallHooks)
            self.trigger.handler.beforeSaveHooks.extend(self.trigger.beforeSaveHooks)
            self.trigger.handler.afterSaveHooks.extend(self.trigger.afterSaveHooks)

        ADSteam = type(
            "ADSteam",
            (Stream,),
            {
                "ARGUMENTS": self.arguments,
                "INTERVAL": self.trigger.interval,
                "call": self.handler,
                "trigger": self.trigger.handler,
                "beforeInitHooks": self.beforeInitHooks + self.trigger.beforeInitHooks,
                "afterInitHooks": self.afterInitHooks + self.trigger.afterInitHooks,
            },
        )
        self.stream = ADSteam(*args, **kwargs)
        return self

    @property
    def trigger(self):
        return self.triggerApp

    def start(self, *args, **kwargs):
        if not self.stream:
            raise Exception("{} is not ready".format(self.name))
        self.stream.start(*args, **kwargs)
        return self

    def input(self, argument):
        def _dec(funcOrApp):
            funcOrApp = (
                self.handler
                if isinstance(funcOrApp, StreamApp)
                else functional.instancemethod(funcOrApp)
            )
            self.handler = Handler.input(argument)(funcOrApp)
            return self

        return _dec

    def output(self, argument):
        def _dec(funcOrApp):
            funcOrApp = (
                self.handler
                if isinstance(funcOrApp, StreamApp)
                else functional.instancemethod(funcOrApp)
            )
            self.handler = Handler.output(argument)(funcOrApp)
            return self

        return _dec

    def param(self, argument):
        def _dec(funcOrApp):
            funcOrApp = (
                self.handler
                if isinstance(funcOrApp, StreamApp)
                else functional.instancemethod(funcOrApp)
            )
            self.handler = Handler.param(argument)(funcOrApp)
            return self

        return _dec

    def column(self, argument):
        def _dec(funcOrApp):
            funcOrApp = (
                self.handler
                if isinstance(funcOrApp, StreamApp)
                else functional.instancemethod(funcOrApp)
            )
            self.handler = Handler.column(argument)(funcOrApp)
            return self

        return _dec
