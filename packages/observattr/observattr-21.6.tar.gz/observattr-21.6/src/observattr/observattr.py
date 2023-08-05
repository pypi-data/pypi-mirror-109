import logging, inspect


class ObservableProxy:
    """Observable proxy around arbitrary types
    
    Keeps a reference to an arbitrary object and defines proxy methods
    around all public methods of the object. Has a list of observers
    that is notified upon proxy method calls. Append observers via the
    subscribe() method.
    """
    
    def __init__(self, obj):
        logging.debug(f'__init__ called for class {self.__class__}')
        self.obj = obj
        self.observers = []
        
        for name in dir(obj):
            attr = getattr(obj, name)
            if callable(attr) and not name.startswith('__'):
                def wrapper(*args, attr=attr, name=name, **kwargs):
                    logging.debug(f'proxy method {name} called for {obj}')
                    attr(*args, **kwargs)
                    self.notify()
                
                setattr(self, name, wrapper)
        
    def __getattr__(self, name):
        if name in self.__dict__.keys():
            return self.__dict__[name]
        else:
            return getattr(self.__dict__['obj'], name)
        
    def __invert__(self):
        """Use bitwise NOT (~) syntax to return the underlying object"""
        return self.obj
        
    def subscribe(self, func):
        self.observers.append(func)

    def notify(self):
        for observer in self.observers:
            observer(self.obj)
    
    
class ObservableAttribute:
    """Descriptor for any observable attribute
    
    Needs to be defined as a class variable (not an instance 
    variable). Creates a reference to the underlying _Observable,
    which defines proxy methods around all public methods of an
    arbitrary object.
    """
    
    def __init__(self, observable_type=None):
        logging.debug(f'__init__ of {self} called with type {observable_type}')
        self.observable_type = observable_type
        if self.observable_type is not None:  
            if not inspect.isclass(observable_type):
                raise Exception(f"{self.__class__} can only be instantiated with a type or class")    

    def __set_name__(self, owner, name):
        logging.debug(f'__set_name__ of {self} called by class {owner} for name {name}')
        self.observable_name = '_' + name
        
    def __get__(self, obj, objtype=None):
        logging.debug(f'__get__ of {self} called by instance {obj}')
        try:
            return getattr(obj, self.observable_name)    
        except AttributeError:
            if self.observable_type is not None:
                # Instantiate the observable object in the owner class instance
                new_observable = ObservableProxy(self.observable_type())
                setattr(obj, self.observable_name, new_observable)
                return new_observable
            else:
                # Type should be specified before __get__ is called
                raise Exception(f"Unknown type of observable object") 

    def __set__(self, obj, value):
        logging.debug(f'__set__ of {self} called by instance {obj} with value {value}')
        try:
            old_observable = getattr(obj, self.observable_name)  
        except AttributeError:
            # Observable object does not exist yet
            if self.observable_type is not None:
                # Type was already defined in __init__
                if type(value) != self.observable_type:
                    raise Exception(f"Type of set value does not match observable type")
            else:
                # Type is now being defined
                self.observable_type = type(value)
            
            # Make the new observable
            new_observable = ObservableProxy(value)
        else:
            # Make the new observable and copy old observers
            old_observers = old_observable.observers
            if type(value) != self.observable_type:
                raise Exception(f"Type of set value does not match observable type")
            else:
                new_observable = ObservableProxy(value)
                new_observable.observers.extend(old_observers)
        finally:
            # Replace observable in owner class and notify observers
            setattr(obj, self.observable_name, new_observable)
            new_observable.notify()
            