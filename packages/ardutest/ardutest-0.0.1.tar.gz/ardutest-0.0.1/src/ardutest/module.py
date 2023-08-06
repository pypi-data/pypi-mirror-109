from __future__ import annotations

from importlib import import_module
from os import getcwd
from sys import path
from typing import Any, Dict, Callable, Optional

from numpy import ndarray
from pydantic import BaseModel, Field
from arductl.models import Mission, ArduStackConfig

from staliro.options import StaliroOptions
from staliro.optimizers import Optimizer
from staliro.results import StaliroResult

from tltk_mtl import Predicate

from .config import ArduPilotTestConfig

path.append(getcwd())


class Module(BaseModel):
    phi: str
    predicates: Dict[str, Predicate]
    optimizer: Optimizer[None, StaliroResult]
    options: StaliroOptions
    mission_factory: Optional[Callable[[ndarray, ndarray, ndarray], Mission]] = None
    stack_config: ArduStackConfig = Field(default_factory=ArduStackConfig)
    config: ArduPilotTestConfig = Field(default_factory=ArduPilotTestConfig)

    class Config:
        arbitrary_types_allowed = True


def load_module(module_name: str) -> Module:
    module = import_module(module_name)
    module_attrs = {
        attr: getattr(module, attr) for attr in dir(module) if not attr.startswith("_")
    }

    return Module.parse_obj(module_attrs)
