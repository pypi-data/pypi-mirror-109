#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Distributed under terms of the MIT license.

import enum


@enum.unique
class ErrorCodes(enum.Enum):
    DAG_CIRCLE_ERROR = 1

    def __str__(self):
        return self.name


class BaseError(Exception):

    def __init__(self, code, message):
        self.message = message
        self.code = code

    def __str__(self):
        return f"{self.code}: {self.message}"


class DAGCircleError(BaseError):

    def __init__(self, message, code=None):
        if not code:
            code = ErrorCodes.DAG_CIRCLE_ERROR
        super().__init__(code, message)
