# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
'''
from .ConversionSurfaceMCNPToT4 import conversionSurfaceMCNPToT4
from .CSurfaceT4 import CSurfaceT4
from .ESurfaceTypeT4 import ESurfaceTypeT4Eng as T4S
from ..Transformation.ConversionSurfaceTransformed import conversionSurfaceTransformed
from collections import OrderedDict


def constructSurfaceT4(mcnpParser):
    '''
    :brief: method constructing a dictionary with the id
    of the surface as a key and the instance of CSurfaceT4 as a value
    '''
    dic_newSurfaceT4 = OrderedDict()
    dic_surfaceT4, dic_surfaceMCNP = conversionSurfaceMCNPToT4(mcnpParser)
    dic_surfaceT4Tr, dic_surfaceMCNPTr = conversionSurfaceTransformed(mcnpParser)
    dic_surfaceT4.update(dic_surfaceT4Tr)
    dic_surfaceMCNP.update(dic_surfaceMCNPTr)
    free_id = max(int(k) for k in dic_surfaceT4.keys()) + 1
    keyS = 100000
    n_surfaces = len(dic_surfaceT4)
    fmt_string = '\rconverting surface {{:{}d}}/{}'.format(len(str(n_surfaces)),
                                                         n_surfaces)
    for i, (key, surf_coll) in enumerate(dic_surfaceT4.items()):
        print(fmt_string.format(i+1), end='', flush=True)
        fixed_surfs = surf_coll.fixed
        fixed_ids = []
        for surf, side in fixed_surfs:
            dic_newSurfaceT4[free_id] = (surf, [])
            fixed_ids.append(side * free_id)
            free_id += 1
        dic_newSurfaceT4[key] = (surf_coll.main, fixed_ids)
    dic_newSurfaceT4[keyS + 1] = (CSurfaceT4(T4S.PLANEX, [1], ['aux plane for unions']), [])
    dic_newSurfaceT4[keyS + 2] = (CSurfaceT4(T4S.PLANEX, [-1], ['aux plane for unions']), [])
    print('... done', flush=True)
    return dic_newSurfaceT4, dic_surfaceMCNP
