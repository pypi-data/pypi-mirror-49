
''' A module for representing laminations on Triangulations. '''

from itertools import permutations

import curver
from curver.kernel.decorators import memoize, topological_invariant, ensure  # Special import needed for decorating.

class Lamination(object):
    ''' This represents a lamination on a triangulation.
    
    Users should create these via Triangulation(...) or Triangulation.lamination(...). '''
    def __init__(self, triangulation, geometric):
        assert isinstance(triangulation, curver.kernel.Triangulation)
        
        self.triangulation = triangulation
        self.zeta = self.triangulation.zeta
        self.geometric = geometric
        
        # Store some additional weights that are often used.
        self._dual = dict()
        self._side = dict()
        for triangle in self.triangulation:
            i, j, k = triangle  # Edges.
            a, b, c = self.geometric[i.index], self.geometric[j.index], self.geometric[k.index]
            af, bf, cf = max(a, 0), max(b, 0), max(c, 0)  # Correct for negatives.
            correction = min(af + bf - cf, bf + cf - af, cf + af - bf, 0)
            self._dual[i] = self._side[k] = curver.kernel.utilities.half(bf + cf - af + correction)
            self._dual[j] = self._side[i] = curver.kernel.utilities.half(cf + af - bf + correction)
            self._dual[k] = self._side[j] = curver.kernel.utilities.half(af + bf - cf + correction)
    
    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.triangulation, self.geometric)
    def __str__(self):
        return '%s %s on %s' % (self.__class__.__name__, self.geometric, self.triangulation)
    def __iter__(self):
        return iter(self.geometric)
    def __call__(self, edge):
        ''' Return the geometric measure assigned to item. '''
        if isinstance(edge, curver.IntegerType): edge = curver.kernel.Edge(edge)  # If given an integer instead.
        
        return self.geometric[edge.index]
    def __bool__(self):
        return not self.is_empty()
    def __nonzero__(self):  # For Python2.
        return self.__bool__()
    def __eq__(self, other):
        return self.triangulation == other.triangulation and self.geometric == other.geometric
    def __ne__(self, other):
        return not self == other
    def __hash__(self):
        return hash(tuple(self.geometric))
    def __add__(self, other):
        # Haken sum.
        if isinstance(other, Lamination):
            if other.triangulation != self.triangulation:
                raise ValueError('Laminations must be on the same triangulation to add them')
            
            geometric = [x + y for x, y in zip(self.geometric, other.geometric)]
            return self.triangulation(geometric)  # Have to promote.
        else:
            return NotImplemented
    def __radd__(self, other):
        return self + other  # Commutative.
    def __mul__(self, other):  # FIXME: Make work for non-integrals.
        assert other >= 0
        
        # TODO: 3) Could save components if they have already been computed.
        geometric = [other * x for x in self]
        
        # In some easy cases we use short-cuts to avoid promote.
        if other == 0:
            return IntegralLamination(self.triangulation, geometric)
        elif other == 1:
            return self.__class__(self.triangulation, geometric)
        elif isinstance(other, curver.IntegerType) and isinstance(self, curver.kernel.MultiArc):  # or Arc.
            return curver.kernel.MultiArc(self.triangulation, geometric)
        elif isinstance(other, curver.IntegerType) and isinstance(self, curver.kernel.MultiCurve):  # or Curve.
            return curver.kernel.MultiCurve(self.triangulation, geometric)
        elif isinstance(other, curver.IntegerType) and isinstance(self, curver.kernel.IntegralLamination):
            return curver.kernel.IntegralLamination(self.triangulation, geometric)
        else:
            return self.triangulation(geometric)  # Have to promote.
    def __rmul__(self, other):
        return self * other  # Commutative.
    
    def __reduce__(self):
        return (self.__class__, (self.triangulation, self.geometric))
    
    def weight(self):
        ''' Return the geometric intersection of this lamination with its underlying triangulation. '''
        
        return sum(max(weight, 0) for weight in self)
    
    def dual_weight(self, edge):
        ''' Return the number of component of this lamination dual to the given edge.
        
        Note that when there is a terminal normal arc then we record this weight with a negative sign. '''
        
        if isinstance(edge, curver.IntegerType): edge = curver.kernel.Edge(edge)  # If given an integer instead.
        
        return self._dual[edge]
    
    def side_weight(self, edge):
        ''' Return the number of component of this lamination dual to the given edge.
        
        Note that when there is a terminal normal arc then we record this weight with a negative sign. '''
        
        if isinstance(edge, curver.IntegerType): edge = curver.kernel.Edge(edge)  # If given an integer instead.
        
        return self._side[edge]
    
    def is_integral(self):
        ''' Return whether this lamination is integral. '''
        
        return all(weight == int(weight) for weight in self) and all(self.dual_weight(edge) == int(self.dual_weight(edge)) for edge in self.triangulation.edges)
    
    def promote(self):
        ''' Return this lamination in its finest form. '''
        
        if self.is_integral():
            return IntegralLamination(self.triangulation, self.geometric).promote()
        else:
            return self
    
    @topological_invariant
    def is_empty(self):
        ''' Return if this lamination has no components. '''
        
        return not any(self)  # self.num_components() == 0
    
    @topological_invariant
    def is_peripheral(self):
        ''' Return whether this lamination consists entirely of parallel components. '''
        
        return self.peripheral() == self
    
    def peripheral(self, promote=True):
        ''' Return the lamination consisting of the peripheral components of this Lamination. '''
        
        geometric = [0] * self.zeta
        for component, (multiplicity, _) in self.peripheral_components().items():
            geometric = [x + multiplicity * y for x, y in zip(geometric, component)]
        
        return self.triangulation(geometric, promote)  # Have to promote.
    
    def non_peripheral(self, promote=True):
        ''' Return the lamination consisting of the non-peripheral components of this Lamination. '''
        
        geometric = [x - y for x, y in zip(self, self.peripheral(promote=False))]
        
        return self.triangulation(geometric, promote)  # Have to promote.
    
    def trace(self, edge, intersection_point, length):
        ''' Return the sequence of edges encountered by following along this lamination.
        
        We start at the given edge and intersection point for the specified number of steps.
        However we terminate early if the lamination closes up before this number of steps is completed. '''
        
        if isinstance(edge, curver.IntegerType): edge = curver.kernel.Edge(edge)  # If given an integer instead.
        
        start = (edge, intersection_point)
        
        assert 0 <= intersection_point < self(edge)  # Sanity.
        dual_weights = dict((edge, self.dual_weight(edge)) for edge in self.triangulation.edges)
        edges = []
        for _ in range(length):
            x, y, z = self.triangulation.corner_lookup[~edge]
            if intersection_point < dual_weights[z]:  # Turn right.
                edge, intersection_point = y, intersection_point
            elif dual_weights[x] < 0 and dual_weights[z] <= intersection_point < dual_weights[z] - dual_weights[x]:  # Terminate.
                break
            else:  # Turn left.
                edge, intersection_point = z, self(z) - self(x) + intersection_point
            if (edge, intersection_point) == start:  # Closes up.
                break
            edges.append(edge)
            assert 0 <= intersection_point < self(edge)  # Sanity.
        
        return edges
    
    def peripheral_components(self):
        ''' Return a dictionary mapping component to (multiplicity, vertex) for each component of self that is peripheral around a vertex. '''
        
        components = dict()
        for vertex in self.triangulation.vertices:
            multiplicity = min(max(self.side_weight(edge), 0) for edge in vertex)
            if multiplicity > 0:
                component = self.triangulation.curve_from_cut_sequence(vertex)
                components[component] = (multiplicity, vertex)
        
        return components
    
    @memoize
    def parallel_components(self):
        ''' Return a dictionary mapping component to (multiplicity, edge) for each component of self that is parallel to an edge. '''
        
        components = dict()
        for edge in self.triangulation.edges:
            if edge.sign() == +1:  # Don't double count.
                multiplicity = -self(edge)
                if multiplicity > 0:
                    component = self.triangulation.edge_arc(edge)
                    components[component] = (multiplicity, edge)
            
            if self.triangulation.vertex_lookup[edge] == self.triangulation.vertex_lookup[~edge]:
                v = self.triangulation.vertex_lookup[edge]  # = self.triangulation.vertex_lookup[~edge].
                v_edges = curver.kernel.utilities.cyclic_slice(v, edge, ~edge)  # The set of edges that come out of v from edge round to ~edge.
                if len(v_edges) > 2:
                    around_v = min(max(self.side_weight(edge), 0) for edge in v_edges)
                    twisting = min(max(self.side_weight(edge) - around_v, 0) for edge in v_edges[1:-1])
                    
                    if self.side_weight(v_edges[0]) == around_v and self.side_weight(v_edges[-1]) == around_v:
                        multiplicity = twisting
                        
                        if multiplicity > 0:
                            component = self.triangulation.curve_from_cut_sequence(v_edges[1:])
                            components[component] = (multiplicity, edge)
        
        return components

class IntegralLamination(Lamination):
    ''' This represents a lamination in which all weights are integral. '''
    
    @topological_invariant
    def is_multicurve(self):
        ''' Return if this lamination is actually a multicurve. '''
        
        return not self.is_empty() and all(isinstance(component, curver.kernel.Curve) for component in self.components())
    
    @topological_invariant
    def is_curve(self):
        ''' Return if this lamination is actually a curve. '''
        
        return self.is_multicurve() and self.num_components() == 1
    
    @topological_invariant
    def is_multiarc(self):
        ''' Return if this lamination is actually a multiarc. '''
        
        return not self.is_empty() and all(isinstance(component, curver.kernel.Arc) for component in self.components())
    
    @topological_invariant
    def is_arc(self):
        ''' Return if this lamination is actually a multiarc. '''
        
        return self.is_multiarc() and self.num_components() == 1
    
    def promote(self):
        if self.is_multicurve():
            if self.is_curve():
                other = curver.kernel.Curve(self.triangulation, self.geometric)
            else:
                other = curver.kernel.MultiCurve(self.triangulation, self.geometric)
        elif self.is_multiarc():
            if self.is_arc():
                other = curver.kernel.Arc(self.triangulation, self.geometric)
            else:
                other = curver.kernel.MultiArc(self.triangulation, self.geometric)
        else:
            other = self
        
        # Move cache across.
        try:
            other._cache = self._cache  # pylint: disable=attribute-defined-outside-init
        except AttributeError:
            pass  # No cache.
        
        return other
    
    def skeleton(self):
        ''' Return the lamination obtained by collapsing parallel components. '''
        
        return self.triangulation.sum(self.components())
    
    def peek_component(self):
        ''' Return one component of this Lamination. '''
        
        return next(iter(self.components()))
    
    def intersection(self, *laminations):
        ''' Return the geometric intersection number between this lamination and the given one(s).
        
        If multiple laminations are given then ``sum(i(self, lamination) for laminations)`` is returned. '''
        
        assert all(isinstance(lamination, Lamination) for lamination in laminations)
        assert all(lamination.triangulation == self.triangulation for lamination in laminations)
        
        intersection = 0
        # Peripheral components.
        for _, (multiplicity, vertex) in self.peripheral_components().items():
            for lamination in laminations:
                intersection += multiplicity * sum(max(-lamination(edge), 0) + max(-lamination.side_weight(edge), 0) for edge in vertex)
        
        short, conjugator = self.shorten()
        short_laminations = [conjugator(lamination) for lamination in laminations]
        
        # Parallel components.
        for component, (multiplicity, p) in short.parallel_components().items():
            if isinstance(component, curver.kernel.Arc):
                for short_lamination in short_laminations:
                    intersection += multiplicity * max(short_lamination(p), 0)
            else:  # isinstance(component, curver.kernel.Curve):
                v = short.triangulation.vertex_lookup[p]  # = self.triangulation.vertex_lookup[~p].
                v_edges = curver.kernel.utilities.cyclic_slice(v, p, ~p)  # The set of edges that come out of v from p round to ~p.
                
                for short_lamination in short_laminations:
                    around_v = min(max(short_lamination.side_weight(edge), 0) for edge in v_edges)
                    out_v = sum(max(-short_lamination.side_weight(edge), 0) for edge in v_edges) + sum(max(-short_lamination(edge), 0) for edge in v_edges[1:])
                    # around_v > 0 ==> out_v == 0; out_v > 0 ==> around_v == 0.
                    intersection += multiplicity * (max(short_lamination(p), 0) - 2 * around_v + out_v)
        
        return intersection
    
    def no_common_component(self, lamination):
        ''' Return that self does not share any components with the given IntegralLamination. '''
        
        assert isinstance(lamination, IntegralLamination)
        
        self_components = self.components()
        return not any(component in self_components for component in lamination.components())
    
    @topological_invariant
    def num_components(self):
        ''' Return the total number of components. '''
        
        return sum(self.components().values())
    
    def sublaminations(self):
        ''' Return all sublaminations that appear within self. '''
        
        components = self.components()
        return [self.triangulation.sum(sub) for i in range(len(components)) for sub in permutations(components, i+1)]  # Powerset.
    
    def multiarc(self):
        ''' Return the maximal MultiArc contained within this lamination. '''
        
        return self.triangulation.sum([multiplicity * component for component, multiplicity in self.components().items() if isinstance(component, curver.kernel.Arc)])
    
    def multicurve(self):
        ''' Return the maximal MultiCurve contained within this lamination. '''
        
        return self.triangulation.sum([multiplicity * component for component, multiplicity in self.components().items() if isinstance(component, curver.kernel.Curve)])
    
    def boundary(self):
        ''' Return the boundary of a regular neighbourhood of this lamination. '''
        
        if self.is_empty():
            return self
        
        return self.multiarc().boundary() + self.multicurve().boundary()
    
    @topological_invariant
    def is_filling(self):
        ''' Return if this IntegralLamination fills the surface, that is, if it intersects all curves on the surface.
        
        Note that this is equivalent to:
            - it meets every non S_{0,3} component of the surface, and
            - its boundary is peripheral.
        
        Furthermore, if any component of this lamination is a non-peripheral curve then it cannot fill. '''
        
        if any(isinstance(component, curver.kernel.Curve) and not component.is_peripheral() for component in self.components()):
            return False
        
        for component in self.triangulation.components():
            V, E = len([vertex for vertex in self.triangulation.vertices if vertex[0] in component]), len(component) // 2
            if (V, E) != (3, 3):  # component != S_{0, 3}:
                if all(self(edge) == 0 for edge in component):
                    return False
        
        return self.boundary().is_peripheral()
    
    @topological_invariant
    def is_polygonalisation(self):
        ''' Return if this IntegralLamination is a polygonalisation, that is, if it cuts the surface into polygons. '''
        
        if any(isinstance(component, curver.kernel.Curve) for component in self.components()):
            return False
        
        short, _ = self.shorten()
       
        avoid = set(index for index in short.triangulation.indices if short(index) < 0)  # All of the edges used.
        dual_tree = short.triangulation.dual_tree(avoid=avoid)
        
        return dual_tree.union(avoid) == set(short.triangulation.indices)  # Every edge is in avoid or dual_tree.
    
    def fills_with(self, other):  # pylint: disable=no-self-use
        ''' Return whether self \\cup other fills. '''
        assert isinstance(other, IntegralLamination)
        
        return NotImplemented  # TODO: 2) Implement! (And remove the PyLint disable when done.)
    
    # @topological_invariant
    def topological_type(self, closed=False):  # pylint: disable=no-self-use, unused-argument
        ''' Return the topological type of this lamination..
        If the closed flag is set the the object returned records the topological type of the multicurve after applying the forgetful map.
        
        Two laminations are in the same mapping class group orbit if and only their topological types are equal.
        These are labelled graphs and so equal means 'label isomorphic', so we return a custom class that uses networkx.is_isomorphic to determine equality. '''
        
        # This should generalise MultiCurve.topological_type().
        # The final code should be very similar but with some additional steps:
        #  6) Let a := crush(self.multiarc()).
        #  7) Label each vertex with the topological type of a restricted to the corresponding component.
        # Note that in order for this to work the topological type MUST be compatible with the permutation of the punctures.
        
        return NotImplemented  # TODO: 2) Implement. (And remove the PyLint disable when done.)
    
    @memoize
    def components(self):
        ''' Return a dictionary mapping components to their multiplicities. '''
        
        components = dict()
        
        for component, (multiplicity, _) in self.peripheral_components().items():
            components[component] = multiplicity
        
        short, conjugator = self.shorten()
        conjugator_inv = conjugator.inverse()
        
        for component, (multiplicity, _) in short.parallel_components().items():
            components[conjugator_inv(component)] = multiplicity
        
        return components
    
    def is_short(self):
        ''' Return whether this lamination is short.
        
        A lamination is short if all of its non-peripheral components are parallel to edges of
        the triangulation that it is defined on. This makes computing its components very easy. '''
        
        lamination = self.non_peripheral(promote=False)
        
        geometric = list(lamination)
        for component, (multiplicity, _) in lamination.parallel_components().items():
            geometric = [x - y * multiplicity for x, y in zip(geometric, component)]
        lamination = Lamination(lamination.triangulation, geometric)
        
        return lamination.is_empty()
    
    @memoize
    @ensure(lambda data: data.result[0].is_short())
    def shorten(self, drop=0.1):
        ''' Return a pair (s, h) where:
         * h is a mapping which maps this lamination to a short one, and
         * s = h(self.non_peripheral()).
        
        In each round, we do not look for an accelerating Dehn twist if a flip can drop the weight by at least `drop`%.
        So if `drop` == 0.0 then acceleration is never done and this returns the Mosher flip sequence.
        As long as `drop` > 0 this method runs in poly(||self||) time.
        
        The original version of this method was based on [Bell16]_ but now a simpler and more efficient technique is used.
        The argument why this version runs in polynomial time follows that of [EricksonNayyeri13]_. '''
        
        assert 0.0 <= drop <= 1.0
        
        lamination = self.non_peripheral(promote=False)
        conjugator = self.triangulation.id_encoding()
        
        def shorten_strategy(self, edge):
            ''' Return a float in [0, 1] describing how good flipping this edge is for making this lamination short. '''
            
            if isinstance(edge, curver.IntegerType): edge = curver.kernel.Edge(edge)  # If given an integer instead.
            
            if not self.triangulation.is_flippable(edge): return 0
            
            ad, bd, cd, dd, ed = [self.dual_weight(edgy) for edgy in self.triangulation.square(edge)]
            
            if ed < 0:  # Non-parallel arc.
                return 1
            
            if ed == 0 and ad > 0 and bd > 0:  # Bipod.
                return 0.5
            
            return 0
        
        def curve_shorten_strategy(self, edge):
            ''' Return a float in [0, 1] describing how good flipping this edge is for making this curve short. '''
            
            if isinstance(edge, curver.IntegerType): edge = curver.kernel.Edge(edge)  # If given an integer instead.
            
            if not self.triangulation.is_flippable(edge): return 0
            
            ai, bi, ci, di, ei = [self(edgy) for edgy in self.triangulation.square(edge)]
            ad, bd, cd, dd, ed = [self.dual_weight(edgy) for edgy in self.triangulation.square(edge)]
            
            if ei == 0:
                return 0
            if max(ai + ci, bi + di) - ei < ei:
                return 1  # Hmmm. We do need this but can we avoid not having 1 as the generic case?
            if bd > 0 and ad == 0:
                return 0.75
            
            return 0.5
        
        def find_twist(lamination, edge):
            ''' Return a twist based at the given edge that drops the weight of this lamination as much as possible.
            
            Raises a ValueError if no twist can be found. '''
            
            # Deps: edge, lamination, old_extra
            trace = lamination.trace(edge, lamination.side_weight(edge), 2*self.zeta)
            trace = trace[:trace.index(edge)+1]  # Will raise a ValueError if edge is not in trace.
            
            curve = lamination.triangulation.lamination_from_cut_sequence(trace)
            if isinstance(curve, curver.kernel.Curve):
                slope = curve.slope(lamination)  # Will raise a ValueError if these are disjoint.
                if abs(slope) > 1:  # Can accelerate. We should probably also skip cases where slope is too close to small to be efficient.
                    return curve.encode_twist(power=-int(slope))  # Round towards zero.
            
            raise ValueError('No accelerating twist exists')
        
        arc_components, curve_components = dict(), dict()
        active_edges = set(lamination.triangulation.edges)  # Edges that are not currently parallel to a component and so can be flipped.
        has_arcs = True
        while True:
            # Subtract.
            geometric = list(lamination)
            for component, (multiplicity, edge) in lamination.parallel_components().items():
                if lamination(edge) <= 0:
                    geometric = [x - y * multiplicity for x, y in zip(geometric, component)]
                    active_edges.discard(edge)
                    active_edges.discard(~edge)
                    if isinstance(component, curver.kernel.Arc):
                        arc_components[edge] = multiplicity
                    else:
                        curve_components[edge] = multiplicity
            
            lamination = IntegralLamination(lamination.triangulation, geometric)
            
            if not lamination: break
            
            has_arcs = has_arcs and any(lamination(edge) < 0 or lamination.dual_weight(edge) < 0 for edge in lamination.triangulation.edges)  # Once they are gone, they are gone.
            extra = []  # High priority edges to check.
            while active_edges:
                # Note that if lamination does not have any arcs then the max value that shorten_strategy can return is 0.5.
                edge = curver.kernel.utilities.maximum(extra + list(active_edges), key=lambda edge: shorten_strategy(lamination, edge), upper_bound=1 if has_arcs else 0.5)
                if shorten_strategy(lamination, edge) == 0: break  # No non-parallel arcs or bipods.
                
                a, b, c, d, e = lamination.triangulation.square(edge)
                move = lamination.triangulation.encode_flip(edge)  # edge is always flippable.
                # Since looking for and applying a twist is expensive, we will not do it if:
                #  * lamination has little weight, or
                #  * flipping drops the weight by at least drop%.
                if 4 * self.zeta < lamination.weight() < move(lamination).weight() / (1 - drop):
                    try:
                        move = find_twist(lamination, edge)
                    except ValueError:
                        extra = [x for x in [c, d] if x in active_edges]
                else:
                    extra = [x for x in [c, d] if x in active_edges]
                
                conjugator = move * conjugator
                lamination = move(lamination)
                if lamination(edge) <= 0:
                    active_edges.discard(edge)
                    active_edges.discard(~edge)
            
            # Now all arcs should be parallel to edges and there should now be no bipods.
            assert all(lamination.side_weight(edge) >= 0 for edge in lamination.triangulation.edges)
            assert all(sum(1 if lamination.side_weight(edge) > 0 else 0 for edge in triangle) != 2 for triangle in lamination.triangulation)
            
            # This is pretty inefficient.
            for edge in active_edges:
                if lamination(edge) > 0 and lamination.side_weight(edge) == 0:
                    trace = [edge] + lamination.trace(edge, 0, 2*self.zeta)
                    curve = lamination.triangulation.curve_from_cut_sequence(trace)
                    extra = []
                    while not curve.is_short():
                        edgey = curver.kernel.utilities.maximum(extra + list(active_edges), key=lambda edge: curve_shorten_strategy(curve, edge), upper_bound=1)  # pylint: disable=cell-var-from-loop
                        # This edge is always flippable.
                        a, b, c, d, e = lamination.triangulation.square(edgey)
                        
                        move = lamination.triangulation.encode_flip(edgey)
                        extra = [x for x in [c, d] if x in active_edges]
                        conjugator = move * conjugator
                        curve = move(curve)
                        lamination = move(lamination)
        
        # Rebuild the image of self under conjugator from its components.
        short = lamination.triangulation.disjoint_sum(
            [multiplicity * lamination.triangulation.edge_arc(edge) for edge, multiplicity in arc_components.items()]
            + [multiplicity * lamination.triangulation.edge_curve(edge) for edge, multiplicity in curve_components.items()]
            )
        
        return short, conjugator

