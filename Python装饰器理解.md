## Python装饰器
### 什么是装饰器？
      
   通俗来讲，把一个普通函数当成人的话装饰器就是人能使用的工具。它可以提供给人一些附加的能力。比如当你把一个菜刀给了一个人，那么这个人就有了切菜的能力可以去切菜。同时这并不影响他本身具有的能力。
   
   从Python上讲，装饰器其实就是一个闭包，他把一个函数当做参数传递给另一个函数然后返回一个组合起来的函数。
   这样组合起来的函数就具备了一个本来没有的功能，是一个加强版的函数。
### 为什么要使用装饰器？

  使用装饰器可以让代码变得简洁，可以独立一个单独的功能。当我们需要使用时就可以使用@标识符进行应用。
### 怎么理解装饰器？
- 命名空间(作用域)和变量解析规则
   
      #1.py
      a_string = "This is a global variable"
      def foo():
      print a_string # 1
      foo()
      This is a global variable
      
      #2.py
      a_string = "This is a global variable"
      def foo():
      a_string = "test" # 1
      print locals()
      foo()
      {'a_string': 'test'}
      a_string # 2
      'This is a global variable'
      
  我们知道，在Python中一个函数是具有一个命名空间的也就是作用域。一个变量创建时，它保存在所处的命名空间里。
  当变量传递给一个函数时，函数也会将收到的变量记录到它的命名空间。
  
  从1.py上面的代码我们可以看到，当a_string变量被创建时，他被保存在了一个外部的全局空间里。函数foo并没有收到传递的a_string参数。
  在使用a_string时他会首先查看自己的命名空间，当没有找到时会去他的
  
  从2.py上看，所谓的保存，实质上是复制了一份引用。我们可以看到对于不可修改对象(string、number、tuples)的赋值是函数外是没有影响。
  在函数内的操作，只是将函数内复制的应用指向了另一个对象。改变了指向地址，并没有在原来的地址上进行改变。

- 变量生存周期

      #3.py
      def foo():
        x = 1
      foo()
      print x # 1
      Traceback (most recent call last):
      NameError: name 'x' is not defined
     
  从3.py我们可以看到，当我们使用函数内所创建的变量时失败了，它是不存在的。因为该变量是随着函数的开始调用创建，当调用完成时它就被销毁了。
  
- 闭包
  
      #4.py
      def outer():
        x = 1
        def inner():
          print x # 1
        return inner
      foo = outer()
      foo.func_closure # doctest: +ELLIPSIS
      (<cell at 0x: int object at 0x>,)
 
  从4.py我们可以看出如果将inner作为一个函数被outer返回时。它内部命名空间保存的变量并没有随着调用的结束被销毁。这就是闭包。
  
  这就是说当一个函数被整体返回时，他是能够记录自己的命名空间的。如果说像虚拟机的快照是不是容易理解一些？
  
- 装饰器

      5.py
      def outer(some_func):
          def inner():
            print "before some_func"
            ret = some_func() # 1
            return ret + 1
          return inner
      def foo():
        return 1
      decorated = outer(foo) # 2
      decorated()
      before some_func
      2
      
  观察5.py，我们可以认为decorated就是函数foo的一个装饰器版本，他是一个加强版的foo函数。
  
  如果我们不想创建一个新函数，而是给foo附加这个功能。我们可以执行foo = outer(foo)，现在这个foo就是一个具有了新的功能的加强版函数。
  这跟使用@标识符是一样的。
  
      foo = outer(foo)
      等同于
      @outer
      def foo():
      
  如果理解起来有困难，我们可以将这个foo函数填充到装饰器函数里来看一下：
  
        def outer(return 1):
          def inner():
            print "before some_func"
            ret = return 1 # 1
            return ret + 1
          return inner
  这样是不是就很好理解了，他们就像是一个组合函数。因为Python具有的闭包特性。
  内部的嵌套函数被返回时保留了自身命名空间内记录的数据，整个函数就能够顺利执行。
  
- 实例
  
      def wrapper(func):
          def checker(a, b): # 1
              if a.x < 0 or a.y < 0:
                 a = Coordinate(a.x if a.x > 0 else 0, a.y if a.y > 0 else 0)
              if b.x < 0 or b.y < 0:
                 b = Coordinate(b.x if b.x > 0 else 0, b.y if b.y > 0 else 0)
              ret = func(a, b)
              if ret.x < 0 or ret.y < 0:
                 ret = Coordinate(ret.x if ret.x > 0 else 0, ret.y if ret.y > 0 else 0)
              return ret
          return checker
          
      class Coordinate(object):
            def __init__(self, x, y):
                  self.x = x
                  self.y = y
            def __repr__(self):
                  return "Coord: " + str(self.__dict__)
      @wrapper
      def add(a, b):
            return Coordinate(a.x + b.x, a.y + b.y)
      @wrapper
      def sub(a, b):
            return Coordinate(a.x - b.x, a.y - b.y)
 
add(a, b)和sum(a, b)是对两个坐标对象进行加减运算的函数。通过装饰器为这两个函数加入了边界检查的特殊功能。

如果难理解还是尝试将被装载的函数写到装饰器函数里看，应该会方便理解。

- 扩展

  
  
  
