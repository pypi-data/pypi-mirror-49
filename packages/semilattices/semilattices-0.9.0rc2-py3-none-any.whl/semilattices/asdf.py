#
# This file is part of semilattices.
#
# semilattices is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# semilattices is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with semilattices.  If not, see <http://www.gnu.org/licenses/>.
#
# semilattices
# Copyright (C) 2018
# 
# Authors: Daniele Bigoni and Joshua Chen
# Contact: dabi@mit.edu / joshuawchen@utexas.edu
# Website: 
# Support:
#

import pickle
from collections import MutableSet
from queue import Queue, LifoQueue
from random import randint

from scipy.sparse import coo_matrix

from . import datastructures
from .datastructures import \
    adjacency_mat
from . import exceptions 
from .exceptions import *
from . import iterables
from .iterables import \
    BreadthFirstSemilatticeIterable, \
    BreadthFirstCoupledIntersectionSemilatticeIterable, \
    BreadthFirstCoupledUnionSemilatticeIterable
from . import misc 
from .misc import \
    default_kwargs, \
    required_kwargs
from . import objectbase
from .objectbase import SLO
from . import vertices
from .vertices import \
    SemilatticeVertex

__all__ = [
    'Semilattice',
]

class Semilattice( SLO ):
    r""" An (order-) semilattice is a rooted connected directed acyclic graph resembling the structure of a tree, i.e. it has a depth/levels. However, unlike a tree, each vertex can have multiple parents.
    
    We denote the in-vertex neighbors of a vertex in the graph as ``parents`` and
    the out-vertex neighbors of a vertex in the graph ``children``.
    ``ancestors`` and ``descentants`` follow the same terminology.

    .. document private functions
    .. automethod:: __init__
    .. automethod:: __len__
    .. automethod:: __contains__
    .. automethod:: __eq__
    .. automethod:: __le__
    .. automethod:: __ge__
    .. automethod:: __iter__
    .. automethod:: __ior__
    .. automethod:: __or__
    .. automethod:: __iand__
    .. automethod:: __and__
    """
    ###########################
    # INITIALIZATION ROUTINES #
    ###########################
    _DefaultVertexConstructor = SemilatticeVertex
    _DefaultVertexSetConstructor = set

    def __init__(self, obj=None, *args, **kwargs): 
        r"""
        Args:
          VertexConstructor (class): a subclass of :class:`SemilatticeVertex`.
        """
        super().__init__()
        self._properties = dict()
        VertexConstructor = kwargs.get('VertexConstructor', self._DefaultVertexConstructor)
        VertexSetConstructor = kwargs.get('VertexSetConstructor',self._DefaultVertexSetConstructor)
        if obj is not None and not isinstance(obj, Semilattice):
            raise SemilatticeException("Can only cast Semilattices")

        print("VertexConstructor",VertexConstructor)
        if not issubclass(VertexConstructor, self._DefaultVertexConstructor):
            raise InvalidVertexConstructor(
                "Semilattice can only be composed by vertices " + \
                "extending " + self._DefaultVertexConstructor.__name__())
        else:
            if obj is not None:
                self.logger.warning("The provided kwarg 'VertexConstructor' will not be used, since the object \
                being cast alrady has a VertexConstructor")
            else:
                self._properties['VertexConstructor'] = VertexConstructor

        if not issubclass(VertexSetConstructor, MutableSet):
            raise InvalidVertexConstructor(
                "VertexSetConstructor specified for this semilattice is invalid. " \
                + "A valid VertexSetConstructor must inherit from collections.MutableSet")
        else:
            if obj is not None:
                self.logger.warning("The provided kwarg 'VertexSetConstructor' will not be used, since the object \
                being cast alrady has a VertexSetConstructor")
            else:
                self._properties['VertexSetConstructor'] = VertexSetConstructor
                #should freeze the properties

        if obj is None:
            print("setting root to none")
            self._root = None
            self._init_vertices()

    def clone(self):
        r""" Create a new empty semilattice with the same properties as ``self``
        """
        return self.__class__(**self._properties)

    def _init_vertices(self):
        self._init_vertices_semilattice()

    def _init_vertices_semilattice(self):
        self._vertices = self.VertexSetConstructor()

    ##############
    # PROPERTIES #
    ##############
    @property
    def properties(self):
        r"""Properties of the semilattice that define construction of a new empty semilattice"""
        return self._properties
    
    @property
    def VertexSetConstructor(self): #FIXME DOCUMENTATION, extends what?
        r""" Class constructor for sets of vertices in the semilattice.

        :type: class
        """
        return self._properties['VertexSetConstructor']     

    @property
    def VertexConstructor(self): #FIXME DOCUMENTATION, extends what?
        r""" Class constructor of the vertices in the semilattice.

        :type: class
        """
        return self._properties['VertexConstructor']

    @property
    def vertices(self):
        r""" The set of vertices in the semilattice

        :type: set
        """
        return self._vertices
    
    @property
    def root(self):
        r""" The root vertex

        :type: :class:`SemilatticeVertex`
        """
        return self._root

    def _set_root(self, new_vertex,**kwargs):
        if self._root is not None:
            raise ChildAlreadyExists("The root vertex already exists.")
        self._root = new_vertex

    def _attr_adjacency_mat(
            self, iter_attribute='children', adjacency_mat_type=coo_matrix):
        r""" Adjacency matrix (type adjacency_mat_type) built by 
        traversing the children """
        # Attach positions to vertices

        #If we end up defining a data structure that keeps track of this position this will be free,
        #
        for i, v in enumerate(BreadthFirstSemilatticeIterable(self)):
            v.position = i

        vtxs = []
        neighbor_vtxs = []
        for r, vtx in enumerate(BreadthFirstSemilatticeIterable(self)):
            for d, neighbor_vtx in getattr(vtx, iter_attribute).items():
                vtxs.append( r )
                neighbor_vtxs.append( neighbor_vtx.position )

        mat = adjacency_mat(vtxs,neighbor_vtxs, \
                            mat_type=adjacency_mat_type)

        #we also wont need to create and destroy 'position'
        # Remove positions from vertices
        for v in self:
            del v.position

        return mat

    @property
    def parents_adjacency_mat(self, adjacency_mat_type=coo_matrix):
        r""" Adjacency matrix built traversing parents

        Returns: 
          Adjacency matrix (type self.adjacency_mat_type) built by 
            traversing the parents 
        """
        return self._attr_adjacency_mat(
            'parents', adjacency_mat_type)

    @property
    def children_adjacency_mat(self, adjacency_mat_type=coo_matrix):
        r""" Adjacency matrix built traversing children

        Returns: 
          Adjacency matrix (type self.adjacency_mat_type) built by 
            traversing the parents
        """
        return self._attr_adjacency_mat(
            'children', adjacency_mat_type)

    ##########################
    # SERIALIZATION ROUTINES #
    ##########################
    def __getstate__(self):
        # This extracts the information necessary to serialize the object.
        # The adjacencies of the semilattice is mapped to positions of the vertices
        # in the partially ordered list.
        dd = dict(self._properties)
        dd['vertices'] = [ pickle.dumps(v) \
                           for v in BreadthFirstSemilatticeIterable(self) ]

        # Attach positions to vertices

        for i, v in enumerate(BreadthFirstSemilatticeIterable(self)):
            v.position = i

        self._getstate_inner(dd)
        
        # Remove positions from vertices
        for v in self:
            del v.position
        
        return dd

    def _getstate_inner(self, dd):
        dd['adjacency_list'] = []
        for child in BreadthFirstSemilatticeIterable(self):
            child_parents_adjacency = []
            for d, parent in child.parents.items():
                child_parents_adjacency.append(
                    (d, parent.position) )
            dd['adjacency_list'].append( child_parents_adjacency )
        dd['frontier_index_list'] = [ v.position for v in self._frontier ]

    def __setstate__(self, dd):
        # See __getstate__ for a description
        self._properties = { k: dd[k] for k in ['VertexConstructor','VertexSetConstructor'] }
        tmp_vertices = [ pickle.loads(v) for v in dd['vertices'] ]
        self._root = tmp_vertices[0] if len(tmp_vertices) > 0 else None

        # Transfer the vertices from the list to the vertices data structure
        self._init_vertices()
        self._vertices.update(tmp_vertices)

        # Update remaining data structures
        self._setstate_inner(dd, tmp_vertices)

    def _setstate_inner(self, dd, tmp_vertices):
        # Restore adjacency
        for child, adjacency in zip(tmp_vertices, dd['adjacency_list']):
            for d, p in adjacency:
                parent = tmp_vertices[p]
                parent.children[d] = child
                child.parents[d] = parent
        # Restore frontier
        self._init_frontier()
        self._frontier.update( tmp_vertices[fidx] for fidx in dd['frontier_index_list'])

            
    def copy(self):
        r""" A deep copy of the semilattice.
        """
        return self.__copy__()

    def __copy__(self):
        return self.__deepcopy__({})

    def __deepcopy__(self, memo):
        semilattice_copy = pickle.loads( pickle.dumps( self ) )
        return semilattice_copy

    ####################
    # RANDOM SELECTION #
    ####################
    
    def random_vertex(self):
        r""" Return a random vertex from the semilattice.
        
        Returns:
          (:class:`SemilatticeVertex`) -- random vertex
        """
        if self._root is not None:
            random_vertex_idx = randint(0,len(self._vertices)-1)
            return self._vertices[random_vertex_idx]
        else:
            raise EmptySemilatticeException()

    #######################################################
    # GRAPH HANDLING OPERATIONS (INSERTION/DELETION/ETC.) #
    #######################################################
    
    @staticmethod
    @required_kwargs('parent','child','edge')
    def _new_edge_between_sans_check(**kwargs):
        parent = kwargs['parent']
        child = kwargs['child']
        parent._add_child_sans_check(**kwargs)
        child._add_parent_sans_check(**kwargs)

    @staticmethod
    @required_kwargs('parent', 'child', 'edge')
    def _new_edge_between(**kwargs):
        parent = kwargs['parent']
        child = kwargs['child']
        parent._add_child(**kwargs)
        child._add_parent(**kwargs)

        # if child._tree_parent is None:
        #     child._add_tree_parent( parent )
        #     parent._add_tree_child( edge, child )

    def _new_vertex_sans_check(self, **kwargs):
        r""" This function should be called to determine and create the
        the relationships (edges) between a new vertex and other existing
        vertices in the semilattice, including `edge' edge with `parent'
        """
        raise NotImplementedError("Not implemented for regular semilattice.")

    @default_kwargs(edge=None, parent=None, check_new_vertex=True)
    def new_vertex(self, **kwargs):
        r""" Adds a new child to ``parent`` along the direction ``edge``

        Args:
          edge (int): edge for child
          vertex (Vertex): vertex to which to add a child
          **kwargs: keyword arguments for the construction of the new vertex,
            to be passed to the vertex constructor

        Returns:
          (:class:`SemilatticeVertex`) -- the added vertex

        Raises:
          InvalidVertex: if the vertex is not an instance of :class:`Vertex`
          ChildAlreadyExists: if ``vertex`` already has a ``edge`` child.
        """
        #edge snd parent should jusf become optional args which we use get() to obtain
        if kwargs.pop('check_new_vertex'):
            self._check_new_vertex(**kwargs)
        return self._new_vertex_sans_check(**kwargs)

    @staticmethod
    @default_kwargs(edge=None)
    @required_kwargs('parent', 'child')
    def _delete_edge_between_sans_check(**kwargs):
        # Do not check if there is an edge between or if it is possible to
        # delete the edge between the two. Should be only used by user when 
        # the user knows there is an edge between (may possibly not specify the edge)
        parent, child = kwargs['parent'], kwargs['child']
        edge = kwargs['edge']
        if edge is None:
            print("no edge provided")
            for edge, c in parent.children.items():
                if c is child:
                    break
            else:
                raise EdgeException("There is no %d-edge between the two vertices." %edge)
        parent._delete_child_sans_check(edge) #_delete_child
        child._delete_parent_sans_check(edge) #_delete_child

    @classmethod
    @default_kwargs(check_delete_edge_between=False, edge=None)
    def _delete_edge_between(cls, *args, **kwargs):
        edge = kwargs['edge']
        if kwargs.pop('check_delete_edge_between'):
            edge = cls._check_delete_edge_between(edge, *args, **kwargs)
        cls._delete_edge_between_sans_check(edge=edge, parent=kwargs['parent'], child=kwargs['child'])

    @staticmethod
    @default_kwargs(check_delete_edge_between=False)
    def _delete_all_parent_edges_of(vertex, **kwargs):
        to_delete = list(vertex.parents.items())
        for edge, parent in to_delete:
            Semilattice._delete_edge_between(
                edge=edge, 
                parent=parent, 
                child=vertex,
                **kwargs
                )

    @staticmethod
    @default_kwargs(check_delete_edge_between=False)
    def _delete_all_child_edges_of(vertex, **kwargs):
        to_delete = list(vertex.children.items())
        for edge, child in to_delete:
            Semilattice._delete_edge_between(
                edge=edge, 
                parent=vertex, 
                child=child,
                **kwargs
                )

    @classmethod
    @default_kwargs(check_delete_edge_between=False)
    def _delete_all_edges_of(cls,vertex, **kwargs):
        cls._delete_all_parent_edges_of(vertex, **kwargs)
        cls._delete_all_child_edges_of(vertex, **kwargs)

    #use default kwargs for these as well later
    def _delete_vertex_sans_check(self, deletion_target, discard_frontier=True):
        # Disconnect vertex
        self._delete_all_edges_of(deletion_target)
        # Remove vertex
        self.vertices.remove(deletion_target)
        if deletion_target is self.root:
            self._root = None
        if discard_frontier:
            self._frontier.discard(deletion_target)

    def _delete_vertex(self, deletion_target, discard_frontier=True):
        # Create a queue for top down deletion of vertices
        iteration_queue = Queue()
        deletion_set = set()
        deletion_set.add(deletion_target)        

        # Disconnect deletion_target and initialize the queue
        for child in deletion_target.children.values(): 
            iteration_queue.put(child)
        self._frontier.update(deletion_target.parents.values())
        Semilattice._delete_all_edges_of(deletion_target)

        # Fill q by BFS through sub-semilattice starting
        # from deletion_target if the parents of vertices are in the queue.
        # The deletion_set keeps track of vertices which have lost all the parents,
        # and then need to be removed (God this is such a Nazi code...)
        while not iteration_queue.empty():
            vertex = iteration_queue.get()
            # if all( v in deletion_set for v in vertex.parents.values() ):
            if len(vertex.parents) == 0:
                deletion_set.add(vertex)
                for child in vertex.children.values():
                    iteration_queue.put(child)
                # Semilattice._delete_all_child_edges_of( vertex )
                Semilattice._delete_all_edges_of( vertex )
                    

        # All vertices have already been disconnected. Just delete them.
        for vertex in deletion_set:
            self._delete_vertex_sans_check(
                vertex, discard_frontier=discard_frontier)

        return deletion_set

    def delete_vertex(self, deletion_target):
        r""" Deletes a vertex from the semilattice.

        Args:
          deletion_target (:class:`SemilatticeVertex`): vertex to be deleted

        Returns:
          (:class:`set`) -- set containing all the vertices removed from the 
            semilattice in the process of remoing ``deletion_target``
        """
        return self._delete_vertex(deletion_target, discard_frontier=True)

    def _frontier_remove(self, vertex, check_frontier_remove=True):
        r"""Checks if the vertex is (at least if nothing is broken) in the frontier
        before trying to remove from it. """
        if check_frontier_remove:
            self._check_frontier_remove(vertex)
        try: #be more explicit to see if our algorithms are correct
            self._frontier_remove_sans_check(vertex)
        except KeyError:
            raise FrontierException("Something is broken. \
                The vertex should be in the frontier but is not.")

    def _frontier_add(self,vertex, check_frontier_add=True):
        r"""Checks if the vertex is in the frontier
        before trying to add it. """
        if check_frontier_add:
            self._check_frontier_add(vertex)
        if vertex in self._frontier:
            self.logger.warn("The vertex is already in the frontier. The algorithm \
                you are employing could be probably be improved to remove duplicate insertions")
        self._frontier_add_sans_check(vertex)

    def _frontier_add_sans_check(self, vertex):
        self._frontier.add( vertex )

    def _frontier_remove_sans_check(self, vertex):
        self._frontier.remove( vertex )

    def _try_frontier_add(self, v):
        try:
            self._check_frontier_add( v )
            self._frontier_add_sans_check( v) 
        except FrontierException:
            return False
        else:
            return True

    def _try_frontier_remove(self, v):
        try:
            self._check_frontier_remove( v )
            self._frontier_remove_sans_check( v )
        except FrontierException:
            return False
        else:
            return True
            
    #############################################################
    # SEMILATTICE CHECK/SAFETY FUNCTIONS                        #
    #############################################################    

    @staticmethod
    @default_kwargs(edge=None)
    @required_kwargs('parent','child')
    def _check_delete_edge_between(**kwargs):
        parent = kwargs['parent']
        child = kwargs['child']
        edge = kwargs['edge']
        if edge is not None:
            try:
                parent.children[edge]
            except VertexException:
                raise EdgeException("%d-out-edge of parent to child is missing" % edge)
            try:
                child.parents[edge]
            except VertexException:
                raise EdgeException("%d-in-edge of child to parent is missing" % edge)
        else:
            for edge, c in parent.children.items():
                found_child = c is child
                found_parent = c.parents[edge] is parent #This isn't rigorous, good enough for now.
                if found_child or found_parent:
                    break
            else:
                raise EdgeException("There is no %d-edge between the two vertices with key " % edge)
            if found_child and not found_parent:
                raise EdgeException("%d-out-edge of parent to child is missing" % edge)
            elif not found_child and found_parent:
                raise EdgeException("%d-in-edge of parent to child is missing" % edge)
        return edge
    
    @default_kwargs(edge=None, parent=None)
    def _check_new_vertex(self, **kwargs):
        edge = kwargs.pop('edge')
        parent = kwargs.pop('parent')
        print("edge",edge,"parent",parent)
        if edge is None:
            if parent is None:
                if self._root is not None:
                    raise ChildAlreadyExists("The root vertex already exists.")
                else:
                    return
        elif parent is None:
            raise SemilatticeException( #confusing to the user, need to clarify 'default' is root
                "You need to provide both or neither edge and parent")
        elif not isinstance(parent, self.VertexConstructor):
            # print("edge",edge,"parent",parent,self.VertexConstructor)
            raise InvalidVertex(
                f"Can not add vertex. Parent specified is not an instance of {self.VertexConstructor}")
        elif parent not in self._vertices:
            raise InvalidParent(
                "Parent is not a member of the semilattice.")
        elif edge in parent.children.keys():
            raise ChildAlreadyExists(
                f"Vertex already has a child with edge-{edge}.")

    #########################################
    # COMPARISON AND PROPERTIES OVERLOADING #
    #########################################
    def __repr__(self):
        self_str = self.__class__.__name__+" at "+str(self.__hash__)+":\n"
        for vertex in (self._vertices):
            self_str+=repr(vertex)
            self_str+="\n"
        return self_str

    def __str__(self):
        self_str = self.__class__.__name__+" at "+str(self.__hash__)+":\n"
        for vertex in (self._vertices):
            self_str+=str(vertex)
            self_str+="\n"
        return self_str

    @staticmethod
    def __name__(self):
        return "Semilattice"

    def cardinality(self):
        r""" Number of vertices
        """
        return self.__len__()
        
    def order(self):
        r""" Same as :func:`cardinality<Semilattice.cardinality>`
        """
        return self.__len__()

    def __len__(self):
        r""" Number of vertices
        """
        return len(self._vertices)

    def __contains__(self, vertex):
        r""" Checks whether a vertex is in the semilattice
        Complexity: O(1)
        """
        return vertex in self._vertices

    def is_comparable_to(self, other):
        r""" Whether the semilattice is comparable to ``other``.

        Two semilattices are comparable if their ``VertexConstructor`` 
        are the same.
        """
        return self._properties['VertexConstructor'] == other.VertexConstructor

    def __hash__(self):
        return id(self)

    def _inner_eq(self,other): #This is not the fastest... requires O(n) rather than terminating once not equal
        intersection_iterable \
            = BreadthFirstCoupledIntersectionSemilatticeIterable(self, other)
        nvert = len(list(intersection_iterable))
        return nvert == len(self) == len(other)

    def __eq__(self, other):
        r""" Checks whether two semilattices have the same structure and ``VertexConstructor``
        """
        if not self.is_comparable_to(other):
            return False
        if len(self._frontier) != len(other._frontier):
            return False
        return self._inner_eq(other)
    
    def __le__(self, other): #habe we checked if these functions work for a pair of different types of semilattices? /-always default to the super class comparison? 
        r""" Checks whether ``self`` contains ``other``
        """
        if not self.is_comparable_to(other):
            return False
        intersection_iterable \
            = BreadthFirstCoupledIntersectionSemilatticeIterable(self, other)
        return len(list(intersection_iterable)) == len(self) 
    
    def issubsemilattice(self, other):
        r""" Checks whether ``self`` contains ``other``
        """
        return self <= other

    def __ge__(self, other):
        r""" Checks whether ``other`` contains ``self``
        """
        return other <= self
        
    def issupersemilattice(self, other):
        r""" Checks whether ``other`` contains ``self``
        """
        return self >= other

    def iterator(
            self, start_vertex=None, iter_attribute='children',
            iter_type=BreadthFirstSemilatticeIterable):
        r""" Returns an iterator for the semilattice.

        See :class:`SemilatticeIterable` for more details.
        """
        if start_vertex is not None and start_vertex not in self._vertices:
            raise SemilatticeException(
                "The vertex provided does not belong to this semilattice")
        return iter(iter_type(
            self, start_vertex = start_vertex, 
            iter_attribute = iter_attribute))
    
    def __iter__(self):
        r"""
        The default iterator iterates over the datastructure defined to contain
        the vertices
        """
        return iter(self._vertices)

    #########
    # UNION #
    #########
    def __ior__(self, other):
        r""" Returns the in-place union of two graphs.

        For the elements in the intersection of ``self`` and ``other`` it always 
        copies vertices from ``self``.

        Args:
          self (RootedDirectedGraph): first graph
          other (RootedDirectedGraph): second graph

        Returns:
          (:class:`RootedDirectedGraph`) -- the union of ``self`` and ``other``
        """
        if not self.is_comparable_to( other ):
            raise SemilatticeException("The two semilattice are not comparable.")
        link = dict()
        vertices = [ (v1,v2) for v1, v2 in \
                  BreadthFirstCoupledUnionSemilatticeIterable(self, other) ]
        for v1, v2 in vertices:
            # All the v1's are already in self so we need to work only on v2
            d = None
            sl_p = None
            if v2 is not None:
                if v1 is not None:
                    # Vertex already present in self, just update link
                    vertex = v1
                else:
                    vertex = v2.copy()
                    for d, p2 in v2.parents.items():
                        try:
                            sl_p = link[p2]
                            break
                        except KeyError:
                            pass
                    self._new_vertex_sans_check(d, sl_p, new_vertex=vertex)
                link[v2] = vertex
        return self
        
    def __or__(self, other):
        r""" Returns the non-in-place union of two graphs.

        For the elements in the intersection of ``self`` and ``other`` it always 
        copies vertices from ``self``.

        Args:
          self (RootedDirectedGraph): first graph
          other (RootedDirectedGraph): second graph

        Returns:
          (:class:`RootedDirectedGraph`) -- the union of ``self`` and ``other``
        """
        if not self.is_comparable_to( other ):
            raise SemilatticeException("The two semilattice are not comparable.")
        sl = self.copy()
        sl |= other
        return sl

    def union(self, other):
        r""" In-place union of two graphs.

        For the elements in the intersection of ``self`` and ``other`` it always 
        copies vertices from ``self``.

        Args:
          self (RootedDirectedGraph): first graph
          other (RootedDirectedGraph): second graph
        """
        self |= other

    ################
    # INTERSECTION #
    ################
    def __iand__(self, other):
        r""" Returns the in-place intersection of two graphs.

        Elements are always retained from ``self``.

        Args:
          self (RootedDirectedGraph): first graph
          other (RootedDirectedGraph): second graph

        Returns:
          (:class:`RootedDirectedGraph`) -- the intersection of ``self`` and ``other``
        """
        if not self.is_comparable_to(other):
            raise SemilatticeException("The two semilattice are not comparable.")
        iter_stack = LifoQueue()
        for v1, v2 in BreadthFirstCoupledUnionSemilatticeIterable(self, other):
            iter_stack.put( (v1, v2) )
        while not iter_stack.empty():
            v1, v2 = iter_stack.get()
            if v1 is not None and v2 is None:
                self.delete_vertex( v1 )
        return self

    def __and__(self, other):
        r""" Returns the non-in-place intersection of two graphs.

        Elements are always retained from ``self``.

        Args:
          self (RootedDirectedGraph): first graph
          other (RootedDirectedGraph): second graph

        Returns:
          (:class:`RootedDirectedGraph`) -- the intersection of ``self`` and ``other``
        """
        if not self.is_comparable_to(other):
            raise SemilatticeException("The two semilattice are not comparable.")
        link = dict()
        sl = self.clone()
        for v1, v2 in BreadthFirstCoupledIntersectionSemilatticeIterable(self, other):
            d1 = None
            sl_p1 = None
            sl_v1 = v1.copy()
            link[v1] = sl_v1
            for d1, p1 in v1.parents.items():
                try:
                    sl_p1 = link[p1]
                    break
                except KeyError:
                    pass
            sl._new_vertex_sans_check( d1, sl_p1, new_vertex=sl_v1 )
        return sl
        
    def intersection(self, other):
        r""" In-place intersection of two graphs.

        Elements are always retained from ``self``.

        Args:
          self (RootedDirectedGraph): first graphs
          other (RootedDirectedGraph): second graphs
        """
        self &= other
