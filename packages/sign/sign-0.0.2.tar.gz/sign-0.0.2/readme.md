# Sign 


Decorators to inherit signature form one function to another. 

Mainly useful when a function or method takes `*args, **kwargs` and pass them
(mostly unmodified) to another function or methods. 

This will merge the signature of the decorated function, with the target function to simplify inspection. 


## example

```
def foo(a=1, b=2):
    pass

@sign.inherit(foo):
def bar(*args, **kwargs):
    return foo(*args, **kwargs)

```


`bar` signature should appear as:

```
bar(*args, a=1, b=2, **kwargs)
```

