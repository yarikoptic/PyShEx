import re
from typing import Optional, Union, Tuple, List, NamedTuple, Iterable

from ShExJSG import ShExJ, ShExC
from ShExJSG.ShExJ import IRIREF

from pyshex.shape_expressions_language.p5_2_validation_definition import isValid
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import FixedShapeMap, ShapeAssociation, START
from pyshex.utils.schema_loader import SchemaLoader
from pyshex.shape_expressions_language.p5_context import Context
from rdflib import Graph, URIRef, Namespace


def evaluate(g: Graph(),
             schema: Union[str, ShExJ.Schema],
             focus: Optional[Union[str, URIRef]],
             start: Optional[Union[str, URIRef]]=None,
             debug_trace: bool = False) -> Tuple[bool, Optional[str]]:
    """ Evaluate focus node `focus` in graph `g` against shape `shape` in ShEx schema `schema`

    :param g: Graph containing RDF
    :param schema: ShEx Schema -- if str, it will be parsed
    :param focus: focus node in g. If not specified, all URI subjects in G will be evaluated.
    :param start: Starting shape.  If omitted, the Schema start shape is used
    :param debug_trace: Turn on debug tracing
    :return: None if success or failure reason if failure
    """
    if isinstance(schema, str):
        schema = SchemaLoader().loads(schema)
    if schema is None:
        return False, "Error parsing schema"
    if not isinstance(focus, URIRef):
        focus = URIRef(str(focus))
    if start is None:
        start = str(schema.start) if schema.start else None
    if start is None:
        return False, "No starting shape"
    if not isinstance(start, URIRef) and start is not START:
        start = IRIREF(str(start))
    cntxt = Context(g, schema)
    # TODO: fix API to allow a bit more refinement here...
    cntxt.debug_context.trace_satisfies =  \
        cntxt.debug_context.trace_nodeSatisfies = debug_trace
    # cntxt.debug_context.trace_satisfies = cntxt.debug_context.trace_matches = \
    #     cntxt.debug_context.trace_nodeSatisfies = debug_trace
    map_ = FixedShapeMap()
    map_.add(ShapeAssociation(focus, start))
    test_result, reasons = isValid(cntxt, map_)
    return test_result, '\n'.join(reasons)
