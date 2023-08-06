# Overview
   `xmlrepr` module is used to have a nice representations for objects in xml formats.

## installing
   there are two basic releases:
 - [0.0.6](https://pypi.org/project/xmlrepr/0.0.6/)
 - [0.0.7](https://pypi.org/project/xmlrepr/0.0.7/) _(Recommended)_

## simple introduction

   The module only contains one function called `repr`, which has different
behavior depending on the first positional argument `arg1` as follows:

1. `xmlrepr.repr(x)` is the same as `repr(x)`
   when `x` **is not str** and doesn't implement `__xml__` method.

2. `xmlrepr.repr(x)` will make a call to `x.__xml__(level)`
   method **if available**. otherwise it behaves the same as
   built-in `repr` function.

3. If `arg1` (_the first argument_) **is str**:
   _the function will return xml string which the root tag name is `arg1`_.
   In that case, the function will also accept `*children` and `**props` parameters
   to customize the generated xml string.


**Note:** the source code will be available at the end of this page.


# Examples

Let's see some examples to understand the module easily.

```python
from xmlrepr import repr

# Example 1

print(repr({
    'key1':'value1',
    'key2':'value2',
}))

# Output
# "{'key1': 'value1', 'key2': 'value2'}"

# dict object don't have '__xml__' method

# Example 2

import typing

class Foo1(typing.NamedTuple):
    name: str
    value: int
    
    def __xml__(self, level=0):
        return f'<{self.name} value="{self.value}" />'
    
    __str__ = __xml__

foo = Foo1('foo', 49)
print(foo)

# Output
# '<foo value="49" />'

# Example 3

class Foo2(object):
    def __init__(self, name, children, **properties):
        self.name = name
        self.children = children
        self.props = properties
    
    def __xml__(self, level=0):
        return repr(
            self.name, # str
            # don't forget this
            level,
            self.props,
            self.children,
        )
    
    __repr__ = __str__ = __xml__

parent_foo = Foo2('master', [foo], sympole="$", ignore=True)
print(parent_foo)

''' Output
<master sympole="$" ignore>
<foo value="49" />
</master>
'''

# To fix indentation we should fix __xml__ method of Foo1

def __fix_xml__(self, level=0):
    return repr(
        self.name,
        level,
        {'value': self.value},
    )

setattr(Foo1, '__xml__', __fix_xml__) # fixed

# let's also switch 'ignore' property for testing
parent_foo.props['ignore'] = False

print(parent_foo)

'''Output
<master sympole="$">
    <foo value="49" />
</master>
'''
```
Play around the code above to understand it.

# Notes
 * The function positional argument `level` is optional (0 by default)
   unless `type(arg1) is str` gives True. That behavior to remind you to always
   include level argument when using the function inside `__xml__` method.
   
 * `x.__xml__()` method takes level argument when calling 'xmlrepr.repr(x)'.
   But it's **"A good practice"** to make it optional. So that if you make
   something like `__repr__ = __str__ = __xml__`, any call to `str(x)` will be safe.
   
 * In [0.0.7](https://pypi.org/project/xmlrepr/0.0.7/) release. 'repr' function parameters
   list changed from `(arg1, *children, level=0, **props)` to `(arg1, level=None, props=None, children=None)`.
   the new order makes more sense than the old one.

# Source Code
Here is how `repr` function is implemented.

```python
def repr(arg1, level=None, props=None, children=None):
    if type(arg1) != str:
        if level is None:
            # 'level' is optional
            level = 0
        
        if '__xml__' in dir(arg1):
            # calling '__xml__' method if implemented
            return arg1.__xml__(level)
        else:
            # calling built-in function 'repr'
            builtins = globals()['__builtins__']
            if type(builtins) is dict:
                return builtins['repr'](arg1)
            else: # ModuleType
                return builtins.repr(arg1)
    
    if level is None:
        # 'level' is required
        raise TypeError("level parameter is missing")
    #=====#=====#=====#=====#=====#=====#=====#
    # 'name', 'indent' and 'props' variables
    name = arg1
    indent = '    ' * level # 4 spaces per level
    props = ' '.join(
        '%s="%s"' % item if item[1] != True else item[0]
        for item in props.items() if item[1] != False
    ) if props else '\b'
    
    # returning xml tag string
    if children:
        # regular xml tag
        return '\n'.join([
            f"{indent}<{name} {props}>",
            f"{indent}" + f"\n{indent}".join(
                repr(child, level= level + 1)
                for child in children
            ),
            f"{indent}</{name}>",
        ])
    else:
        # self-closing xml tag
        return f"{indent}<{name} {props} />"
```