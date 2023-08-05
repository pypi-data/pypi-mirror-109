



class LazyClass():
    """Base class to derive from to enable lazy adding of class methods and properties.
    """
    
    @classmethod
    def method(cls, name=None):
        """Decorator for adding a method to a :class:`LazyClass`

        Args:
            name (str): Name to give the method.  If it is None, the name is automatically determined from the decorated function name.
        """
        def dec(func):
            n = func.__name__ if name is None else name
            setattr(cls, n, func)
            return func
        
        return dec

    @classmethod
    def staticmethod(cls, name=None):
        def dec(func):
            n = func.__name__ if name is None else name
            setattr(cls, n, staticmethod(func))
            return func
        
        return dec
    
    @classmethod
    def attribute(cls, name=None, fset=None, fdel=None, doc=None):
        print("Warning: use LazyClass.property instead")
        def dec(func):
            n = func.__name__ if name is None else name
            setattr(cls, n, property(fget=func, fset=fset, fdel=fdel, doc=doc))
            return func
        
        return dec

    @classmethod
    def property(cls, name=None, fset=None, fdel=None, doc=None):
        """Decorator to add a :class:`python:property` to a :class:`LazyClass`.

        Args:
            name (str):  Name of the property.  If not set, use the name of the decorated function for the property.
            fset (method):  Function to use as a setter for the property (optional)
            fdel (method):  Function to use as a setter for the property (optional)
            doc (str): String to use for the docstring for the property.  If not set will use the docstring of the decorated function

        """
        def dec(func):
            n = func.__name__ if name is None else name
            setattr(cls, n, property(fget=func, fset=fset, fdel=fdel, doc=doc))
            return func
        
        return dec


class dotdict(dict):
    """
    dictionary with property access to string keys in the dict
    
    e.g.    
    dotd['key']
    dotd.key
    
    are the same
    """
#     __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    
    def __getattr__(self, name):
        if name in self:
            return self.get(name)
        else:
            raise AttributeError(f"No attribute '{name}'")
    

    # for pickling
    def __getstate__(self):
        return dict(self)
    
    def __setstate__(self, d):
        self.update(d)

