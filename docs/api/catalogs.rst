dependency_injector.catalogs
----------------------------

.. automodule:: dependency_injector.catalogs


Declarative catalog
-------------------

.. autoclass:: DeclarativeCatalog
    :member-order: bysource
    :members: 

    .. classmethod:: __getattr__(name)

       Return provider with specified name or raise en error.

       :param name: Attribute's name
       :type name: str

       :raise: dependency_injector.UndefinedProviderError

    .. classmethod:: __setattr__(cls, name, value)
        
        Handle setting of catalog attributes.

        Setting of attributes works as usual, but if value of attribute is
        provider, this provider will be bound to catalog correctly.

        :param name: Attribute's name
        :type name: str

        :param value: Attribute's value
        :type value: dependency_injector.Provider | object

        :rtype: None

    .. classmethod:: __delattr__(cls, name)
        
        Handle deleting of catalog attibute.

        Deleting of attributes works as usual, but if value of attribute is
        provider, this provider will be unbound from catalog correctly.

        :param name: Attribute's name
        :type name: str

        :rtype: None

    .. classmethod:: __repr__(cls, name)
        
        Return string representation of the catalog.

        :rtype: str

Dynamic catalog
---------------

.. autoclass:: DynamicCatalog
    :member-order: bysource
    :members: 
    :special-members:
