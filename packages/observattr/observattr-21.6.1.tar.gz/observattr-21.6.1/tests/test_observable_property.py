import logging, pytest
from collections import deque

logging.basicConfig(level=logging.DEBUG)

from observattr import ObservableAttribute


class PropsPassedAsTypes:
    """Class where types are given in the Observable() constructor"""
    observable_deque = ObservableAttribute(deque)
    observable_int = ObservableAttribute(int)
    

class PropsDeclaredAtInit:
    """Class where types are given in the Observable() constructor"""
    observable_deque = ObservableAttribute()
    observable_int = ObservableAttribute()
    
    def __init__(self):
        self.observable_deque = deque()
        self.observable_int = int()


class PropListener:
    def __init__(self, prop):
        self.prop = prop
        self.prop.subscribe(self.receive)
        self.received_obj = None
    
    def receive(self, obj):
        self.received_obj = obj
        

class TestObservableProperty:
    def test_props_passed_as_type(self):
        instance = PropsPassedAsTypes()
        assert isinstance(instance.observable_deque.obj, deque)
        assert isinstance(instance.observable_int.obj, int)

    def test_props_declared_at_init(self):
        instance = PropsDeclaredAtInit()
        assert isinstance(instance.observable_deque.obj, deque)
        assert isinstance(instance.observable_int.obj, int)

    def test_observable_deque(self):
        instance = PropsPassedAsTypes()
        listener = PropListener(instance.observable_deque)
        instance.observable_deque.append(5)
        assert listener.received_obj == instance.observable_deque.obj

    def test_observable_int(self):
        instance = PropsPassedAsTypes()
        listener = PropListener(instance.observable_int)
        instance.observable_int = 5
        assert listener.received_obj == instance.observable_int.obj
        
    def test_underlying_object(self):
        instance = PropsPassedAsTypes()
        assert isinstance(~instance.observable_deque, deque)
        assert isinstance(~instance.observable_int, int)

