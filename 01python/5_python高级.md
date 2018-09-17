 

# 第一部分 面向对象进阶

# 1. 元类

## 1.1 类是一种对象

包括python在内的大多数语言中，类是一组用来描述如何生成一个对象的代码段。不过除此之外，在python中，**类还是一种对象**。只要你使⽤关键字class， Python解释器在执⾏的时候就会创建⼀个对象。

```python
[class  ]()ObjectCreator(object):
	pass

#将在内存中创建⼀个对象， 名字就是ObjectCreator。拥有创建对象的能力，可赋值给一个变量、拷贝、增加属性、作为函数参数传递。
```


## 1.2 动态创建类

因为类是对象，可在运⾏时动态的创建它们，就像其他任何对象⼀样。如在函数中创建类。

```python
def choose_class(name):
    if name == 'foo':
        class  Foo(object):
            pass
        return  Foo # 返回的是类， 不是类的实例
    else:
        class  Bar(object):
            pass
        return  Bar 
    
    
>>> MyClass = choose_class('foo')
>>> print MyClass # 函数返回的是类， 不是类的实例
    <class '__main__'.Foo>
>>> print MyClass() # 你可以通过这个类创建类实例， 也就是对象
    <__main__.Foo object at 0x89c6d4c>

>>> print type(ObjectCreator()) #实例对象的类型
	<class '__main__.ObjectCreator'>
>>> print type(ObjectCreator) #类的类型
	<type 'type'>
```
## 1.3 使用type创建类
​        type还有种完全不同的功能，动态的创建类。type可以接受一个类的描述作为参数，然后返回一个类。（此功能为了向后兼容）
```python
type(类名, 由父类名称组成的元组（ 针对继承的情况， 可以为空） ， 包含属
性的字典（ 名称和值） )

#例子
Test2 = type("Test2",(),{}) #定了⼀个Test2类
In [5]: Test2() #创建了⼀个Test2类的实例对象
Out[5]: <__main__.Test2 at 0x10d406b38>
In [10]: help(Test) #⽤help查看Test类
Help on class Test in module __main__:
class Test(builtins.object)
| Data descriptors defined here:
| 
| __dict__
| dictionary for instance variables (if defined)
|
| __weakref__
| list of weak references to the object (if defined)
```
- **使用type创建带有属性的类**
  - type的第2个参数， 元组中是父类的名字， 不是字符串
  - 添加的属性是类属性， 并不是实例属性
```python
>>> Foo = type('Foo', (), {'bar':True}) #创建的类可当成普通类使用
#可翻译为
>>> class Foo(object):
… bar = True

#也可用来继承
>>> FooChild = type('FooChild', (Foo,),{})
>>> print FooChild
	<class '__main__.FooChild'>
>>> print FooChild.bar # bar属性是由Foo继承而来
	True
```
- **使用type创建带有方法的类**
  最终你会希望为你的类增加⽅法。 只需要定义⼀个有着恰当签名的函数并将其作为属性赋值就可以了。

  - 添加实例方法
    ```python
    In [46]: def echo_bar(self): #定义了⼀个普通的函数
           : print(self.bar)
    In [47]: FooChild = type('FooChild', (Foo,), {'echo_bar': echo_bar})
    In [48]: hasattr(Foo, 'echo_bar') #判断Foo类中， 是否有echo_bar这个属性
    Out[48]: False
    In [49]:
    In [49]: hasattr(FooChild, 'echo_bar') #判断FooChild类中， 是否有echo_bar这个
    Out[49]: True
    In [50]: my_foo = FooChild()
    In [51]: my_foo.echo_bar()
    True
    ```

  - 添加静态方法
  
    ```python
    In [36]: @staticmethod
    ...: def testStatic():
    ...: print("static method ....")
    ...:
    In [37]: Foochild = type('Foochild', (Foo,), {"echo_bar":echo_bar,
    ...: testStatic})
    In [38]: fooclid = Foochild()
    In [39]: fooclid.testStatic
    Out[39]: <function __main__.testStatic>
    In [40]: fooclid.testStatic()
    static method ....
    In [41]: fooclid.echo_bar()
    True
    ```

  - 添加类方法
  
    ```python
    In [42]: @classmethod
    ...: def testClass(cls):
    ...: print(cls.bar)
    ...:
    In [43]:
    In [43]: Foochild = type('Foochild', (Foo,), {"echo_bar":echo_bar,
    ...: testStatic, "testClass":testClass})
    In [44]:
    In [44]: fooclid = Foochild()
    In [45]: fooclid.testClass()
    True
    ```

## 1.4 元类

元类就是⽤来创建类的“东西”。元类就是用来创建这些类（ 对象） 的， 元类就是类的类， 你可以这样理解 为：

```python
MyClass = MetaClass()  # 使⽤元类创建出⼀个对象， 这个对象称为“类”
MyObject = MyClass()  # 使⽤“类”来创建出实例对象

# 你已经看到了type可以让你像这样做：
MyClass = type('MyClass', (), {})
```

这是因为函数type实际上是一个元类。Python中所有的东西都是对象。 这包括整数、 字符串、 函数以及类。 它们全部都是对象， 它们都是从一个类创建而来， 这个类就是type。

```python
>>> age = 35
>>> age.__class__
<type 'int'>
>>> name = 'bob'
>>> name.__class__
<type 'str'>
>>> def foo(): pass
>>>foo.__class__
<type 'function'>
>>> class Bar(object): pass
>>> b = Bar()
>>> b.__class__
<class '__main__.Bar'>

# 现在， 对于任何⼀个__class__的__class__属性又是什么呢？
>>> a.__class__.__class__
<type 'type'>
>>> age.__class__.__class__
<type 'type'>
>>> foo.__class__.__class__
<type 'type'>
>>> b.__class__.__class__
<type 'type'>
```

因此， 元类就是创建类这种对象的东西。 type就是Python的内建元类， 当然 了， 你也可以创建自己的元类。

## 1.5  \__metaclass__属性

 你可以在定义一个类的时候为其添加\__metaclass__属性。如果你这么做了， Python就会用元类来创建类Foo。

 ```python
 class Foo(object):
	__metaclass__ = something…
	...省略...
 ```

​      你首先写下class Foo(object)， 但是类Foo还没在内存中创建。 Python 会在类的定义中寻找\__metaclass__属性， 如果找到了， Python就会用它来创建类Foo， 如果没找到， 就会用内建的type来创建这个类。 把下面这段话 反复读几次。 当你写如下代码时 :    

```python
class Foo(Bar):
    pass
```

 Python做了如下的操作：

1. Foo中有\_\_metaclass\__这个属性吗？如果是，Python会通过\_\_metaclass__创建一个名字为Foo的类(对象)
2. 如果Python没有找到\_\_metaclass\__，它会继续在Bar（父类）中寻找\_\_metaclass__属性，并尝试做和前面同样的操作。
3. 如果Python在任何父类中都找不到\_\_metaclass\_\_，它就会在模块层次中去寻找\_\_metaclass\__，并尝试做同样的操作。
4. 如果还是找不到\__metaclass__,Python就会用内置的type来创建这个类对象。

现在的问题就是，你可以在\__metaclass__中放置些什么代码呢？答案就是：可以创建一个类的东西。那么什么可以用来创建一个类呢？type，或者任何使用到type或者子类化type的东东都可以。

## 1.6  自定义元类

元类的主要目的就是为了当创建类时能够自动地改变类。通常，你会为API做这样的事情，你希望可以创建符合当前上下文的类。

假想一个很傻的例子，你决定在你的模块里所有的类的属性都应该是大写形式。有好几种方法可以办到，但其中一种就是通过在模块级别设定__metaclass__。采用这种方法，这个模块中的所有类都会通过这个元类来创建，我们只需要告诉元类把所有的属性都改成大写形式就万事大吉了。

幸运的是，__metaclass__实际上可以被任意调用，它并不需要是一个正式的类。所以，我们这里就先以一个简单的函数作为例子开始。

- python2中
```python
#-*- coding:utf-8 -*-
def upper_attr(future_class_name, future_class_parents, future_class_attr):

    #遍历属性字典，把不是__开头的属性名字变为大写
    newAttr = {}
    for name,value in future_class_attr.items():
        if not name.startswith("__"):
            newAttr[name.upper()] = value

    #调用type来创建一个类
    return type(future_class_name, future_class_parents, newAttr)

class Foo(object):
    __metaclass__ = upper_attr #设置Foo类的元类为upper_attr
    bar = 'bip'

print(hasattr(Foo, 'bar'))
print(hasattr(Foo, 'BAR'))

f = Foo()
print(f.BAR)
```

- python3中

```python
#-*- coding:utf-8 -*-
def upper_attr(future_class_name, future_class_parents, future_class_attr):

    #遍历属性字典，把不是__开头的属性名字变为大写
    newAttr = {}
    for name,value in future_class_attr.items():
        if not name.startswith("__"):
            newAttr[name.upper()] = value

    #调用type来创建一个类
    return type(future_class_name, future_class_parents, newAttr)

class Foo(object, metaclass=upper_attr):
    bar = 'bip'

print(hasattr(Foo, 'bar'))
print(hasattr(Foo, 'BAR'))

f = Foo()
print(f.BAR)
```

现在让我们再做一次，这一次用一个真正的class来当做元类。

```python
#coding=utf-8

class UpperAttrMetaClass(type):
    # __new__ 是在__init__之前被调用的特殊方法
    # __new__是用来创建对象并返回之的方法
    # 而__init__只是用来将传入的参数初始化给对象
    # 你很少用到__new__，除非你希望能够控制对象的创建
    # 这里，创建的对象是类，我们希望能够自定义它，所以我们这里改写__new__
    # 如果你希望的话，你也可以在__init__中做些事情
    # 还有一些高级的用法会涉及到改写__call__特殊方法，但是我们这里不用
    def __new__(cls, future_class_name, future_class_parents, future_class_attr):
        #遍历属性字典，把不是__开头的属性名字变为大写
        newAttr = {}
        for name,value in future_class_attr.items():
            if not name.startswith("__"):
                newAttr[name.upper()] = value

        # 方法1：通过'type'来做类对象的创建
        # return type(future_class_name, future_class_parents, newAttr)

        # 方法2：复用type.__new__方法
        # 这就是基本的OOP编程，没什么魔法
        # return type.__new__(cls, future_class_name, future_class_parents, newAttr)

        # 方法3：使用super方法
        return super(UpperAttrMetaClass, cls).__new__(cls, future_class_name, future_class_parents, newAttr)

#python2的用法
class Foo(object):
    __metaclass__ = UpperAttrMetaClass
    bar = 'bip'

# python3的用法
# class Foo(object, metaclass = UpperAttrMetaClass):
#     bar = 'bip'

print(hasattr(Foo, 'bar'))
# 输出: False
print(hasattr(Foo, 'BAR'))
# 输出:True

f = Foo()
print(f.BAR)
# 输出:'bip'
```
就是这样，除此之外，关于元类真的没有别的可说的了。但就元类本身而言，它们其实是很简单的：

拦截类的创建
修改类
返回修改之后的类
究竟为什么要使用元类？
现在回到我们的大主题上来，究竟是为什么你会去使用这样一种容易出错且晦涩的特性？好吧，一般来说，你根本就用不上它：

“元类就是深度的魔法，99%的用户应该根本不必为此操心。如果你想搞清楚究竟是否需要用到元类，那么你就不需要它。那些实际用到元类的人都非常清楚地知道他们需要做什么，而且根本不需要解释为什么要用元类。” —— Python界的领袖 Tim Peters

# 2.  Python是动态语言

##2.1 运行的过程中给对象绑定(添加)属性

```python
>>> class Person(object):
    def __init__(self, name = None, age = None):
        self.name = name
        self.age = age


>>> P = Person("小明", "24")
```
在这里，我们定义了1个类Person，在这个类里，定义了两个初始属性name和age，但是人还有性别啊！如果这个类不是你写的是不是你会尝试访问性别这个属性呢？

```python
>>> P.sex = "male"
>>> P.sex
'male'
>>>
```
这时候就发现问题了，我们定义的类里面没有sex这个属性啊！怎么回事呢？ 这就是动态语言的魅力和坑！ 这里 实际上就是 动态给实例绑定属性！

##2.2 运行的过程中给类绑定(添加)属性

```python
>>> P1 = Person("小丽", "25")
>>> P1.sex

Traceback (most recent call last):
  File "<pyshell#21>", line 1, in <module>
    P1.sex
AttributeError: Person instance has no attribute 'sex'
>>>
```
我们尝试打印P1.sex，发现报错，P1没有sex这个属性！---- 给P这个实例绑定属性对P1这个实例不起作用！ 那我们要给所有的Person的实例加上 sex属性怎么办呢？ 答案就是直接给Person绑定属性！

```python
>>> Person.sex = None #给类Person添加一个属性
>>> P1 = Person("小丽", "25")
>>> print(P1.sex) #如果P1这个实例对象中没有sex属性的话，那么就会访问它的类属性
None #可以看到没有出现异常
>>>
```
##2.3 运行的过程中给类绑定(添加)方法
我们直接给Person绑定sex这个属性，重新实例化P1后，P1就有sex这个属性了！ 那么function呢？怎么绑定？

```python
>>> class Person(object):
    def __init__(self, name = None, age = None):
        self.name = name
        self.age = age
    def eat(self):
        print("eat food")


>>> def run(self, speed):
    print("%s在移动, 速度是 %d km/h"%(self.name, speed))


>>> P = Person("老王", 24)
>>> P.eat()
eat food
>>> 
>>> P.run()
Traceback (most recent call last):
  File "<pyshell#5>", line 1, in <module>
    P.run()
AttributeError: Person instance has no attribute 'run'
>>>
>>>
>>> import types
>>> P.run = types.MethodType(run, P)
>>> P.run(180)
老王在移动,速度是 180 km/h
```
既然给类添加方法，是使用类名.方法名 = xxxx，那么给对象添加一个方法也是类似的对象.方法名 = xxxx

完整的代码如下：

```python
import types

#定义了一个类
class Person(object):
    num = 0
    def __init__(self, name = None, age = None):
        self.name = name
        self.age = age
    def eat(self):
        print("eat food")

#定义一个实例方法
def run(self, speed):
    print("%s在移动, 速度是 %d km/h"%(self.name, speed))

#定义一个类方法
@classmethod
def testClass(cls):
    cls.num = 100

#定义一个静态方法
@staticmethod
def testStatic():
    print("---static method----")

#创建一个实例对象
P = Person("老王", 24)
#调用在class中的方法
P.eat()

#给这个对象添加实例方法
P.run = types.MethodType(run, P)
#调用实例方法
P.run(180)

#给Person类绑定类方法
Person.testClass = testClass
#调用类方法
print(Person.num)
Person.testClass()
print(Person.num)

#给Person类绑定静态方法
Person.testStatic = testStatic
#调用静态方法
Person.testStatic()
```

##2.4 运行的过程中删除属性、方法
删除的方法:

del 对象.属性名
delattr(对象, "属性名")
通过以上例子可以得出一个结论：相对于动态语言，静态语言具有严谨性！所以，玩动态语言的时候，小心动态的坑！

那么怎么避免这种情况呢？ 请使用\__slots__，


#3. \__slots__
- 动态语言：可以在运行的过程中，修改代码

- 静态语言：编译时已经确定好代码，运行过程中不能修改

如果我们想要限制实例的属性怎么办？比如，只允许对Person实例添加name和age属性。

为了达到限制的目的，Python允许在定义class的时候，定义一个特殊的`__slots__`变量，来限制该class实例能添加的属性：

```python
>>> class Person(object):
    __slots__ = ("name", "age")

>>> P = Person()
>>> P.name = "老王"
>>> P.age = 20
>>> P.score = 100
Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
AttributeError: Person instance has no attribute 'score'
>>>
```
注意:
        使用`__slots__`要注意，`__slots__`定义的属性仅对当前类实例起作用，对继承的子类是不起作用的
```python
In [67]: class Test(Person):
    ...:     pass
    ...:

In [68]: t = Test()
In [69]: t.score = 100
```

#4. 生成器
##4.1 什么是生成器
通过列表生成式，我们可以直接创建一个列表。但是，受到内存限制，列表容量肯定是有限的。而且，创建一个包含100万个元素的列表，不仅占用很大的存储空间，如果我们仅仅需要访问前面几个元素，那后面绝大多数元素占用的空间都白白浪费了。所以，如果列表元素可以按照某种算法推算出来，那我们是否可以在循环的过程中不断推算出后续的元素呢？这样就不必创建完整的list，从而节省大量的空间。**在Python中，这种一边循环一边计算的机制，称为生成器：generator**。

##4.2 创建生成器方法1
要创建一个生成器，有很多种方法。第一种方法很简单，只要把一个列表生成式的 [ ] 改成 ( )

```python
In [15]: L = [ x*2 for x in range(5)]

In [16]: L
Out[16]: [0, 2, 4, 6, 8]

In [17]: G = ( x*2 for x in range(5))

In [18]: G
Out[18]: <generator object <genexpr> at 0x7f626c132db0>

In [19]:
```
创建 L 和 G 的区别仅在于最外层的 [ ] 和 ( ) ， L 是一个列表，而 G 是一个生成器。我们可以直接打印出L的每一个元素，但我们怎么打印出G的每一个元素呢？如果要一个一个打印出来，可以通过 next() 函数获得生成器的下一个返回值：

```python
In [19]: next(G)
Out[19]: 0

In [20]: next(G)
Out[20]: 2

In [21]: next(G)
Out[21]: 4

In [22]: next(G)
Out[22]: 6

In [23]: next(G)
Out[23]: 8

In [24]: next(G)
---------------------------------------------------------------------------
StopIteration                             Traceback (most recent call last)
<ipython-input-24-380e167d6934> in <module>()
----> 1 next(G)

StopIteration: 

In [25]:
In [26]: G = ( x*2 for x in range(5))

In [27]: for x in G:
   ....:     print(x)
   ....:     
0
2
4
6
8

In [28]:
```
生成器保存的是算法，每次调用 next(G) ，就计算出 G 的下一个元素的值，直到计算到最后一个元素，没有更多的元素时，抛出 StopIteration 的异常。当然，这种不断调用 next() 实在是太变态了，正确的方法是使用 for 循环，因为生成器也是可迭代对象。所以，我们创建了一个生成器后，基本上永远不会调用 next() ，而是通过 for 循环来迭代它，并且不需要关心 StopIteration 异常。

##4.3 创建生成器方法2
generator非常强大。如果推算的算法比较复杂，用类似列表生成式的 for 循环无法实现的时候，还可以用函数来实现。

比如，著名的斐波拉契数列（Fibonacci），除第一个和第二个数外，任意一个数都可由前两个数相加得到：

1, 1, 2, 3, 5, 8, 13, 21, 34, ...

斐波拉契数列用列表生成式写不出来，但是，用函数把它打印出来却很容易：

```python
In [28]: def fib(times):
   ....:     n = 0
   ....:     a,b = 0,1
   ....:     while n<times:
   ....:         print(b)
   ....:         a,b = b,a+b
   ....:         n+=1
   ....:     return 'done'
   ....: 

In [29]: fib(5)
1
1
2
3
5
Out[29]: 'done'
```
仔细观察，可以看出，fib函数实际上是定义了斐波拉契数列的推算规则，可以从第一个元素开始，推算出后续任意的元素，这种逻辑其实非常类似generator。

也就是说，上面的函数和generator仅一步之遥。要把fib函数变成generator，只需要把print(b)改为yield b就可以了：

```python
In [30]: def fib(times):
   ....:     n = 0
   ....:     a,b = 0,1
   ....:     while n<times:
   ....:         yield b
   ....:         a,b = b,a+b
   ....:         n+=1
   ....:     return 'done'
   ....: 

In [31]: F = fib(5)

In [32]: next(F)
Out[32]: 1

In [33]: next(F)
Out[33]: 1

In [34]: next(F)
Out[34]: 2

In [35]: next(F)
Out[35]: 3

In [36]: next(F)
Out[36]: 5

In [37]: next(F)
---------------------------------------------------------------------------
StopIteration                             Traceback (most recent call last)
<ipython-input-37-8c2b02b4361a> in <module>()
----> 1 next(F)

StopIteration: done
```
在上面fib 的例子，我们在循环过程中不断调用 **yield** ，就会不断中断。当然要给循环设置一个条件来退出循环，不然就会产生一个无限数列出来。同样的，把函数改成generator后，我们基本上从来不会用 next() 来获取下一个返回值，而是直接使用 for 循环来迭代：

```python
In [38]: for n in fib(5):
   ....:     print(n)
   ....:     
1
1
2
3
5

In [39]:
```
但是用for循环调用generator时，发现拿不到generator的return语句的返回值。如果想要拿到返回值，必须捕获StopIteration错误，返回值包含在StopIteration的value中：
```python
In [39]: g = fib(5)

In [40]: while True:
   ....:     try:
   ....:         x = next(g)
   ....:         print("value:%d"%x)      
   ....:     except StopIteration as e:
   ....:         print("生成器返回值:%s"%e.value)
   ....:         break
   ....:     
value:1
value:1
value:2
value:3
value:5
生成器返回值:done

In [41]:
```
##4.4 send
例子：执行到yield时，gen函数作用暂时保存，返回i的值;temp接收下次c.send("python")，send发送过来的值，c.next()等价c.send(None)
```python
In [10]: def gen():
   ....:     i = 0
   ....:     while i<5:
   ....:         temp = yield i
   ....:         print(temp)
   ....:         i+=1
   ....:
```
**使用next函数**
```python
In [11]: f = gen()

In [12]: next(f)
Out[12]: 0

In [13]: next(f)
None
Out[13]: 1

In [14]: next(f)
None
Out[14]: 2

In [15]: next(f)
None
Out[15]: 3

In [16]: next(f)
None
Out[16]: 4

In [17]: next(f)
None
---------------------------------------------------------------------------
StopIteration                             Traceback (most recent call last)
<ipython-input-17-468f0afdf1b9> in <module>()
----> 1 next(f)

StopIteration:
```
**使用__next__()方法**
```python
In [18]: f = gen()

In [19]: f.__next__()
Out[19]: 0

In [20]: f.__next__()
None
Out[20]: 1

In [21]: f.__next__()
None
Out[21]: 2

In [22]: f.__next__()
None
Out[22]: 3

In [23]: f.__next__()
None
Out[23]: 4

In [24]: f.__next__()
None
---------------------------------------------------------------------------
StopIteration                             Traceback (most recent call last)
<ipython-input-24-39ec527346a9> in <module>()
----> 1 f.__next__()

StopIteration:
```
**使用send**
```python
In [43]: f = gen()

In [44]: f.__next__()
Out[44]: 0

In [45]: f.send('haha')
haha
Out[45]: 1

In [46]: f.__next__()
None
Out[46]: 2

In [47]: f.send('haha')
haha
Out[47]: 3

In [48]:
```
总结
生成器是这样一个函数，它记住上一次返回时在函数体中的位置。对生成器函数的第二次（或第 n 次）调用跳转至该函数中间，而上次调用的所有局部变量都保持不变。

生成器不仅“记住”了它数据状态；生成器还“记住”了它在流控制构造（在命令式编程中，这种构造不只是数据值）中的位置。

生成器的特点：

1. 节约内存
2. 迭代到下一次的调用时，所使用的参数都是第一次所保留下的，即是说，在整个所有函数调用的参数都是第一次所调用时保留的，而不是新创建的

#5. 迭代器
迭代是访问集合元素的一种方式。迭代器是一个可以记住遍历的位置的对象。迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束。迭代器只能往前不会后退。

##5.1 可迭代对象
以直接作用于 for 循环的数据类型有以下几种：

一类是集合数据类型，如 list 、 tuple 、 dict 、 set 、 str 等；

一类是 generator ，包括生成器和带 yield 的generator function。

这些可以直接作用于 for 循环的对象统称为可迭代对象： `Iterable` 。

##5.2 判断是否可以迭代
可以使用 isinstance() 判断一个对象是否是 Iterable 对象：
```python
In [50]: from collections import Iterable

In [51]: isinstance([], Iterable)
Out[51]: True

In [52]: isinstance({}, Iterable)
Out[52]: True

In [53]: isinstance('abc', Iterable)
Out[53]: True

In [54]: isinstance((x for x in range(10)), Iterable)
Out[54]: True

In [55]: isinstance(100, Iterable)
Out[55]: False
```
而生成器不但可以作用于 for 循环，还可以被 next() 函数不断调用并返回下一个值，直到最后抛出 StopIteration 错误表示无法继续返回下一个值了。

##5.3 迭代器
可以被next()函数调用并不断返回下一个值的对象称为迭代器：Iterator。

可以使用 isinstance() 判断一个对象是否是 Iterator 对象：
```python
In [56]: from collections import Iterator

In [57]: isinstance((x for x in range(10)), Iterator)
Out[57]: True

In [58]: isinstance([], Iterator)
Out[58]: False

In [59]: isinstance({}, Iterator)
Out[59]: False

In [60]: isinstance('abc', Iterator)
Out[60]: False

In [61]: isinstance(100, Iterator)
Out[61]: False
```
##5.4 iter()函数
生成器都是 Iterator 对象，但 list 、 dict 、 str 虽然是 Iterable ，却不是 Iterator 。

把 list 、 dict 、 str 等 Iterable 变成 Iterator 可以使用 iter() 函数：
```python
In [62]: isinstance(iter([]), Iterator)
Out[62]: True

In [63]: isinstance(iter('abc'), Iterator)
Out[63]: True
```
总结
凡是可作用于 for 循环的对象都是 Iterable 类型；
凡是可作用于 next() 函数的对象都是 Iterator 类型
集合数据类型如 list 、 dict 、 str 等是 Iterable 但不是 Iterator ，不过可以通过 iter() 函数获得一个 Iterator 对象。