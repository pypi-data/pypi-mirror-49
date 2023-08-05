# -*- coding: utf-8 -*-
from qtpy.QtQml import qmlRegisterType

from .calculator import Calculator

MODULE_NAME = 'example.module'


def register_types():
    qmlRegisterType(Calculator, MODULE_NAME, 1, 0, Calculator.__name__)
