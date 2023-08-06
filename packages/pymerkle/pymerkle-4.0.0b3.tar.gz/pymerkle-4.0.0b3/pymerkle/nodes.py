"""Provides the classes for the Merkle-tree's leaves and internal nodes
"""

from .serializers import NodeSerializer, LeafSerializer
from .exceptions import NoChildException, NoDescendantException, NoParentException, LeafConstructionError, UndecodableArgumentError, UndecodableRecordError
from .utils import NONE
import json

# Prefices to be used for nice tree printing

L_BRACKET_SHORT = '\u2514' + '\u2500'           # └─
L_BRACKET_LONG  = '\u2514' + 2 * '\u2500'       # └──
T_BRACKET       = '\u251C' + 2 * '\u2500'       # ├──
VERTICAL_BAR    = '\u2502'                      # │


class _Node(object):
    """Base class for ``Leaf`` and ``Node``
    """

    __slots__ = ('__encoding', '__child',)

    def __init__(self, encoding):
        self.__encoding = encoding

    @property
    def encoding(self):
        return self.__encoding

    @property
    def child(self):
        """
        :raises NoChildException: if the node has no ``__child`` attribute
        """
        try:
            return self.__child
        except AttributeError:
            raise NoChildException

    def set_child(self, child):
        self.__child = child

    @property
    def left(self):
        """
        :raises NoChildException: if the node has no ``__left`` attribute
        """
        try:
            return self.__left
        except AttributeError:
            raise NoParentException

    @property
    def right(self):
        """
        :raises NoChildException: if the node has no ``__right`` attribute
        """
        try:
            return self.__right
        except AttributeError:
            raise NoParentException

    def is_left_parent(self):
        """Checks if the node is a left parent

        :returns: ``True`` iff the node is the ``.left`` attribute of some other node inside the containing Merkle-tree
        :rtype:   bool
        """
        try:
            _child = self.child
        except NoChildException:
            return False

        return self == _child.left

    def is_right_parent(self):
        """Checks if the node is a right parent

        :returns: ``True`` iff the node is the ``.right`` attribute of some other node inside the containing Merkle-tree
        :rtype:   bool
        """
        try:
            _child = self.child
        except NoChildException:
            return False

        return self == _child.right

    def is_parent(self):
        """Checks if the node is a parent

        :returns: ``True`` iff the node is the ``.right`` attribute of some other node inside the containing Merkle-tree
        :rtype:   bool
        """
        try:
            self.child
        except NoChildException:
            return False

        return True

    def descendant(self, degree):
        """ Detects and returns the node that is ``degree`` steps upwards within the containing Merkle-tree

        .. note:: Descendant of degree ``0`` is the node itself, descendant of degree ``1`` is the node's child, etc.

        :param degree: depth of descendancy. Must be non-negative
        :type degree:  int
        :returns:      the descendant corresdponding to the requested depth
        :rtype:        nodes.Node

        :raises NoDescendantException: if the provided degree exceeds possibilities
        """
        if degree == 0:
            return self
        else:

            try:
                _child = self.child
            except NoChildException:
                raise NoDescendantException

            return _child.descendant(degree - 1)

    def __repr__(self):
        """Overrides the default implementation

        Sole purpose of this function is to easy print info about a node by just invoking it at console

        .. warning:: Contrary to convention, the output of this implementation is *not* insertible into the ``eval`` function
        """
        def memory_id(obj): return str(hex(id(obj)))

        try:
            child_id = memory_id(self.child)
        except NoChildException:
            child_id = NONE

        try:
            left_id  = memory_id(self.left)
        except NoParentException:
            left_id  = NONE
            right_id = NONE
        else:
            right_id = memory_id(self.right)

        return '\n    memory-id    : {self_id}\
                \n    left parent  : {left_id}\
                \n    right parent : {right_id}\
                \n    child        : {child_id}\
                \n    hash         : {hash}\n'\
                .format(
                    self_id=memory_id(self),
                    left_id=left_id,
                    right_id=right_id,
                    child_id=child_id,
                    hash=self.digest.decode(self.encoding)
                )

    def __str__(self, encoding=None, level=0, indent=3, ignore=[]):
        """Overrides the default implementation. Designed so that inserting the node as an argument to ``print` displays
        the subtree having that node as root.

        Sole purpose of this function is to be used for printing Merkle-trees in a terminal friendly way, similar to what
        is printed at console when running the ``tree`` command of Unix based platforms.

        :param encoding: [optional] encoding type to be used for decoding the node's current stored hash
        :type encoding:  str
        :param level:    [optional] Defaults to ``0``. Must be left equal to the *default* value when called externally by the
                         user. Increased by one whenever the function is recursively called, in order for track be kept of depth
                         while printing
        :type level:     int
        :param indent:   [optional] Defaults to ``3``. The horizontal depth at which each level of the tree will be indented with
                         respect to the previous one. Increase it to achieve better visibility of the tree's structure.
        :type indent:    int
        :param ignore:   [optional] Defaults to ``[]``. Must be left equal to the *default* value when called externally by the
                         user. Augmented appropriately whenever the function is recursively called, in order for track to be kept
                         of the positions where vertical bars should be omitted
        :type ignore:    list of integers
        :rtype:          str

        .. note:: The left parent of each node is printed *above* the right one
        """
        if level == 0:
            output = '\n'

            if not self.is_left_parent() and not self.is_right_parent():        # root case
                output += ' %s' % L_BRACKET_SHORT
        else:
            output = (indent + 1) * ' '

        for _ in range(1, level):
            if _ not in ignore:

                output += ' %s' % VERTICAL_BAR                                  # Include vertical bar
            else:
                output += 2 * ' '

            output += indent * ' '

        new_ignore = ignore[:]
        del ignore

        if self.is_left_parent():

            output += ' %s' % T_BRACKET

        if self.is_right_parent():

            output += ' %s' % L_BRACKET_LONG
            new_ignore.append(level)

        encoding = encoding if encoding else self.encoding
        output += '%s\n' % self.digest.decode(encoding=encoding)

        if not isinstance(self, Leaf):                                          # Recursive step

            output += self.left.__str__(
                encoding=encoding,
                level=level + 1,
                indent=indent,
                ignore=new_ignore
            )

            output += self.right.__str__(
                level=level + 1,
                encoding=encoding,
                indent=indent,
                ignore=new_ignore
            )

        return output


class Leaf(_Node):
    """Class for the leafs of Merkle-tree (i.e., parentless nodes storing digests of encrypted records)

    :param hashfunc: hash function to be used for encryption (only once). Should be the ``.hash``
                     attribute of the containing Merkle-tree
    :type hashfunc:  method
    :param encoding: Encoding type to be used when decoding the hash stored by the node.
                     Should coincide with the containing Merkle-tree's encoding type.
    :type encoding:  str
    :param record:   [optional] The record to be encrypted within the leaf. If provided, then
                     ``digest`` should *not* be provided.
    :type record:    str or bytes or bytearray
    :param digest:   [optional] The hash to be stored at creation by the leaf (after encoding).
                     If provided, then ``record`` should *not* be provided.
    :type digest:    str

    .. warning:: Exactly *one* of *either* ``record`` *or* ``digest`` should be provided

    :raises LeafConstructionError:  if both ``record`` and ``digest`` were provided
    :raises UndecodableRecordError: if the provided ``record`` is a bytes-like object which could not be decoded with
                                    the provided hash-function's configured encoding type

    :ivar digest:   (*bytes*) The digest stored by the leaf
    :ivar child:    (*nodes.Node*) The leaf's current child (if any)
    :ivar encoding: (*str*) The leaf's encoding type. Used for decoding its digest upon printing
    """

    __slots__ = ('__digest')

    def __init__(self, hashfunc, encoding, record=None, digest=None):

        if record and digest is None:

            try:
                _digest = hashfunc(record)

            except UndecodableArgumentError:
                # ~ Provided record cannot be decoded with the configured
                # ~ encoding type of the provided hash function
                raise UndecodableRecordError

            else:
                super().__init__(encoding=encoding)
                self.__digest = _digest

        elif digest and record is None:

            super().__init__(encoding=encoding)
            self.__digest = bytes(digest, encoding)

        else:
            raise LeafConstructionError(
                'Exactly *one* of *either* ``record`` *or* ``digest`` should be provided')

    @property
    def digest(self):

        return self.__digest

# ------------------------------- Serialization --------------------------

    def serialize(self):
        """ Returns a JSON entity with the leaf's attributes as key-value pairs

        :rtype: dict
        """

        return LeafSerializer().default(self)

    def JSONstring(self):
        """Returns a nicely stringified version of the node's JSON serialized form

        :rtype: str
        """

        return json.dumps(self, cls=LeafSerializer, sort_keys=True, indent=4)


class Node(_Node):
    """Class for the internal nodes of a Merkle-tree (i.e., nodes having both parents)

    :param hashfunc: hash function to be used for encryption. Should be the ``.hash`` method of the containing Merkle-tree
    :type hashfunc:  method
    :param encoding:      Encoding type to be used when decoding the hash stored by the node.
                          Should coincide with the containing Merkle-tree's encoding type.
    :type encoding:       str
    :param left:          [optional] the node's left parent
    :type left:           nodes._Node
    :param right:         [optional] the node's right parent
    :type right:          nodes._Node

    :raises UndecodableRecordError: if the digest stored by some of the provided nodes could not be decoded with the provided
                                    hash-function's configured encoding type

    :ivar digest:   (*bytes*) The digest currently stored by the node
    :ivar left:          (*nodes.Node*) The node's left parent
    :ivar right:         (*nodes.Node*) The node's right parent
    :ivar child:         (*nodes.Node*) The node's (always exists unless the node is currently root of the Merkle-tree)
    :ivar encoding:      (*str*) The node's encoding type. Used for decoding its digest upon printing
    """

    __slots__ = ('__digest', '__left', '__right')

    def __init__(self, hashfunc, encoding, left, right):

        try:
            _digest = hashfunc(left.digest, right.digest)

        except UndecodableArgumentError:
            # ~ Hash stored by some parent could not be decoded with the
            # ~ configured encoding type of the provided hash function
            raise UndecodableRecordError

        else:
            super().__init__(encoding=encoding)

            # Establish descendancy relation between child and parents

            left.__child  = self
            right.__child = self
            self.__left   = left
            self.__right  = right

            # Store hash

            self.__digest = _digest

    @property
    def digest(self):

        return self.__digest

    def set_left(self, left):

        self.__left = left

    def set_right(self, right):

        self.__right = right

    def recalculate_hash(self, hashfunc):
        """Recalculates the node's hash under account of the (possibly new) digests stored by its parents

        :param hashfunc: hash function to be used for recalculation (should be the ``.hash()`` method
                         of the containing Merkle-tree)
        :type hashfunc:  method
        """

        try:
            _new_digest = hashfunc(self.left.digest, self.right.digest)

        except UndecodableRecordError:
            raise

        self.__digest = _new_digest


# ------------------------------- Serialization --------------------------


    def serialize(self):
        """ Returns a JSON entity with the node's attributes as key-value pairs

        :rtype: dict

        .. note:: The ``.child`` attribute is excluded node serialization in order for circular reference error to be avoided.
        """

        return NodeSerializer().default(self)

    def JSONstring(self):
        """Returns a nicely stringified version of the node's JSON serialized form

        :rtype: str
        """

        return json.dumps(self, cls=NodeSerializer, sort_keys=True, indent=4)
