from .registry import CheckRegistry
from .builtins import MANUAL_CHECK_DEFINITION


__all__ = 'registry',


registry: CheckRegistry = CheckRegistry()
registry.register(MANUAL_CHECK_DEFINITION)
