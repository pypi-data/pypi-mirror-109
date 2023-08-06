# ObservAttr: Observable Attributes
Pure Python implementation of observable class instance attributes (or a sort of reactive variables). It uses a descriptor that returns a proxy object which can be observed. 

The proxy object defines all public methods of the underlying object, and notifies subscribers after method calls. Callables can be subscribed to the proxy object and are notified with the underlying object as argument.

The descriptor instantiates the proxy object after instantiating an instance of the parent class. So it is not an observable class attribute, but an observable instance attribute. For immutable types (e.g. Number), the `__set__` implementation copies the observers and returns a new proxy upon variable assignment. No change of type is allowed upon new descriptor variable assignment.

## Usage
```
from observattr import ObservableAttribute
```
Declare as class attribute with no type specified:
```
class Example:
    # This instantiates the descriptor for this class
    observable = ObservableAttribute()

    def __init__(self, anything, subscribed_function):
        # This calls the __set__ method of the descriptor:
        # - The descriptor instantiates 'hidden' proxy self._observable with 'anything' as the underlying object
        # - type(anything) is now the fixed type of self.observable
        self.observable = anything
        self.observable.subscribe(subscribed_function)
```
Declare as class attribute with a fixed specified type:
```
class Example:
    # This instantiates the descriptor for this class
    observable = ObservableAttribute(list)

    def __init__(self, value, subscribed_function):
        # This calls the __get__ method of the descriptor:
        # - The descriptor instantiates 'hidden' proxy self._observable with 'list()' as the underlying object
        self.observable.append(value)
        self.observable.subscribe(subscribed_function)
```
