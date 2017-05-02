# -*- coding: utf-8 -*-
"""
Abstract Base Class for all the `*Sync` modules.
"""
import abc


class BaseSync(abc.ABC):  # noqa

    @abc.abstractmethod
    def mongo_to_pg(session, mongo_entry, instance):  # noqa
        pass
