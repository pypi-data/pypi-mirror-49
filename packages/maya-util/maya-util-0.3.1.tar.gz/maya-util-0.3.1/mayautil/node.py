"""
Functions for Maya API nodes.
"""

from maya.api import OpenMaya as om2


def asMObject(name):
    """Return the given node as an MObject.

    Args:
        name (str): The name of a Maya node.

    Returns:
        MObject: The MObject for the given node.

    """
    try:
        selection = om2.MGlobal.getSelectionListByName(name)
        mobject = selection.getDependNode(0)
    except RuntimeError:
        mobject = None
    return mobject
