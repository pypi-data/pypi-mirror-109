# Overview

   `xmlrepr` module is used to have a nice representations for objects in xml formats.

## simple

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
            *self.children,
            # don't forget this
            level= level,
            **self.properties,
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
        level= level,
        value= self.value,
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

# Source Code
Here is how `repr` function is implemented.

```python
def repr(arg1, *children, level=0, **props):
    if type(arg1) != str:
        if '__xml__' in dir(arg1):
            # calling '__xml__' method if implemented
            return arg1.__xml__(level)
        else:
            # calling built-in function 'repr'
            return globals()['__builtins__'].repr(arg1)
    
    # 'name', 'indent' and 'props' variables
    name = arg1
    indent = '    ' * level # 4 spaces per level
    props = ' '.join(
        '%s="%s"' % item if item[1] != True else item[0]
        for item in props.items() if item[1] != False
    )
    
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