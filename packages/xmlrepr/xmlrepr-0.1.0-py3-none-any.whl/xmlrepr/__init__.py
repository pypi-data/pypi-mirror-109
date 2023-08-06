
"""used to give representation of objects in xml format
	
def repr(arg1, level=None, props=None, children=None):
	the function has three uses:
		1. same as built-in repr function when arg1
		doesn't implement __xml__ method.
		2. calls __xml__ method for objects that
		implements it.
		3. used in __xml__ method itself
	
	return
		<Note date="21/4/12" title="TO-DOs" />
		(or)
		<Actions>
			<Read from="line:10" to="line:19" />
			<Replace target="banann" with="banana" />
		</Actions>
	
	arg1:
		could be any object. when used inside __xml__
		method, arg1 must be str.
	
	children:
		could be any object that should implement __xml__
		so that its repr would be inserted within the start
		and end tags of its parent.
	
	level:
		specifies the indent level. default is 0 that
		means 'no indent'. value is increased for every
		recursive call for the function.
	
	props:
		properties to be inserted inside the start tag.
"""


__version__ = '0.1.0'
__all__ = ['repr']


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


def xmlrepr(name, props=None, children=None):
	props = ' '+' '.join(
		'%s="%s"' %(
			key.replace('\n', r'\n'),
			value.replace('\n', r'\n')
		) if value != True else key
		for key, value in props.items()
		if value != False
	) if props else ''
	if children:
		# regular tag, recursion
		return "<{name}{props}>\n{indent}{inners}\n</{name}>".format(
			name=name,
			props=props,
			indent= ' '*4,
			inners= '\n'.join(
				str(child)
				for child in children
			).replace('\n', '\n    ')
		)
	else:
		# self-closing tag, stop recursion
		return "<%s%s />" %(name, props)
	

#input = xmlrepr('input', dict(name='text', type='text', value='welcome', required=True))
#span = xmlrepr('span')
#p = xmlrepr('p', 0, [span])
#a = xmlrepr('a', dict(href='\n'), [p])

#print(s:= xmlrepr('form', None, [input, a, "some text \nand lines"]))

#with open('test', 'w') as file:
#	file.write(s)
