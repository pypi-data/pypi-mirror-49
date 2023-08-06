:mod:`funk`
============

.. module:: funk

.. function:: with_mocks

    A decorator for test methods. Supplies an instance of :class:`~funk.Mocks`
    as the keyword argument *mocks*::
    
        @with_mocks
        def test_some_function(mocks):
            # mocks is an instance of Mocks
            some_mock = mocks.mock()
            ...
            
    At the end of test, ``mocks.verify()`` will be called, so there is no
    need to call it yourself.

.. class:: Mocks

    .. method:: __init__
    
        Create a new mocks, with no expectations set up.
        
    .. method:: mock
    
        Create a new :class:`~funk.Mock` tied to this mocks.
        
    .. method:: sequence
    
        Create a new sequence that can be used as an argument to :func:`~funk.call.Call.in_sequence`.
        
    .. method:: verify
    
        Verifies that all mocks created with this mocks have had their
        expectations satisified. If this is not the case, an :class:`AssertionError`
        will be raised.
        
.. class:: Mock

    When a method is called, the first mocked call that will accept the given
    arguments is used. For instance::
    
        database = mocks.mock()
        expects(database).save("positional").returns(return_one)
        expects(database).save(key="word").returns(return_two)
        
        assert database.save(key="word") is return_two
        assert database.save("positional") is return_one
        
    Some calls can only be called a specified number of times -- specifically,
    :func:`~funk.expects` allows exactly one call. For instance::
    
        database = mocks.mock()
        expects(database).save().returns(return_one)
        allows(database.save().returns(return_two)
        
        assert database.save() is return_one
        assert database.save() is return_two
        assert database.save() is return_two
        
    The first call to ``database.save`` returns the first return value since
    the arguments match, and it was declared first. However, subsequent calls
    return the second return value since using :func:`~funk.expects` means that call
    can be matched only once, where the call created by :func:`~funk.allows` can
    be matched any number of times.

.. function:: expects(mock)

    Create an object to expect a method call on *mock*.  If the method is not
    called, an :class:`AssertionError` is raised. For instance, to expect
    a method called save::
    
        database = mocks.mock()
        expects(database).save
    
    By default, this expectation will allow any arguments. Expected arguments 
    can be set by calling the returned value. For instance, to expect
    the keyword argument *sorted* with a value of :const:`False`::
    
        expects(database).save(sorted=False)

    To customise the expectation further, use the methods on :class:`~funk.call.Call`.
    
.. function:: allows(method_name)

    Similar to :func:`funk.expects`, except that the method can be called
    any number of times, including none.

.. function:: data(**kwargs)

    Creates an object with attributes as specified by *kwargs*. For instance::
    
        author = value_object(first_name="Joe", last_name="Bloggs")
        
        assert author.first_name == "Joe"
        assert author.last_name == "Bloggs"


.. module:: funk.call

.. class:: Call
    
    Allows an expected call to be configured. By default, the call will accept
    any parameters, and will return :const:`None`. That is::
    
        database = mocks.mock()
        allows(database).save
        
        assert database.save() is None
        assert database.save("positional") is None
        assert database.save("positional", key="word") is None
    
    .. method:: with_args(*args, **kwargs)
    
        Allow this call to only accept the given arguments. For instance::
        
            database = mocks.mock()
            allows(database).save.with_args('positional', key='word').returns(return_value)
            assert database.save('positional', key='word') is return_value
            database.save() # Raises AssertionError
        
        Note that this is completely equivalent to::
        
            database = mocks.mock()
            allows(database).save('positional', key='word').returns(return_value)
            assert database.save('positional', key='word') is return_value
            database.save() # Raises AssertionError
        
        Matchers from Precisely_ can also be used to specify allowed arguments::
        
            from precisely import instance_of
            
            ...
        
            calculator = mocks.mock()
            allows(calculator).add(instance_of(int), instance_of(int)).returns(return_value)
            assert calculator.add(4, 9) is return_value
            
        .. _Precisely: https://pypi.python.org/pypi/precisely
    
    .. method:: raises(exception)
    
        Causes this call to raise *exception* when called.
    
    .. method:: returns(value)
    
        Causes this call to return *value*::
        
            database = mocks.mock()
            allows(database).save.returns(return_value)
            
            assert database.save() is return_value
            assert database.save("positional") is return_value
            
        The same method can return different values. For instance::
        
            database = mocks.mock()
            expects(database).save.returns(return_one)
            expects(database).save.returns(return_two)
            
            assert database.save() is return_one
            assert database.save() is return_two
        
    .. method:: in_sequence(sequence)
    
        Adds a requirement that this method call only occur in this sequence.
        This allows ordering of method calls to be specified. For instance, say
        we want to close a file after writing to it. We can write the test like so::

            file_ = mocks.mock(file)
            file_ordering = mocks.sequence()

            expects(file_).write("Eggs").in_sequence(file_ordering)
            expects(file_).close().in_sequence(file_ordering)
            
        Then, if ``close`` is called before ``write``, an :class:`AssertionError`
        will be raised.
