dict8
=====

features
--------

- No boilerplate: just a, b, path and some code.
- Enables you to define a specific merge behavior for every part of the tree.
- Merge into datclasses or attrs.


internal
--------

The default machinery converts all input data to a Mapper. If **a** and **b** are
mappable, the new, common and old values are taken to a custom function to
decide upon the value precedence. Returning :code:`missing` will omit this key
from the intermediate result. The chosen mapper will decide how to incorporate
the latter.


example
-------

.. code-block:: python

    import dict8


    @dict8.ion
    def merge(a, b, path, /, **kv):
        try:
            # try descent into sub mappings
            return merge(
                a,
                b,
                path,
                **kv,
            )
        except dict8.UnMappable:
            # take b else a
            return b if b is not dict8.missing else a


    assert (
        merge(
            {
                1: 2,
                3: {4: 5},
            },
            {
                3: {4: 2, 5: 1},
            },
        )
        == {1: 2, 3: {4: 2, 5: 1}}
    )


license
=======

This is public domain.
