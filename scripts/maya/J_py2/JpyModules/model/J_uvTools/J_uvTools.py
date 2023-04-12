# -*- coding:utf-8 -*-
##  @package model
#
# @date    : 2019/10/26 23:00
# @Author  : KaiJun Fan
# @Email   : qq826530928@163.com
# ================================
"""
maya check functions:
    J_uvTools_find_triangle_edge: 检查三边面
    J_uvTools_find_many_edge: 检查多边面
    J_uvTools_find_non_manifold_edges： 检查非流形边
    J_uvTools_find_lamina_faces： 检查薄边面
    J_uvTools_find_bivalent_faces: 检查两个边共享一个点的同时两个面共享一个点
    J_uvTools_find_zero_area_faces: 检查不足面积的面
    J_uvTools_find_mesh_border_edges: 检查边界边
    J_uvTools_find_zero_length_edges: 检查不足长度的边
    J_uvTools_find_unfrozen_vertices: 检查点的世界坐标是否为0.0进而判断点未进行冻结变换

    J_uvTools_uv_face_cross_quadrant: 检查跨越uv象限的面
    J_uvTools_missing_uv_faces: 检查面的uv时候丢失
    J_uvTools_check_uv_overlapping:检查uv重叠面
    J_uvTools_find_double_faces：检查两个面共用所有点
"""
import maya.cmds as cmds
import maya.api.OpenMaya as om2

def J_uvTools_find_triangle_edge(mesh_name):
    """
    check triangle edge
    :param str mesh_name: object long name eg.'|group3|pSphere1'
    :return: Component list
    :rtype: list
    """
    mesh_list = om2.MSelectionList()
    mesh_list.add(mesh_name)

    dag_path = mesh_list.getDagPath(0)

    mfn_mesh = om2.MFnMesh(dag_path)
    face_numbers = mfn_mesh.numPolygons

    triangle_face_list=[]
    for item in xrange(face_numbers):
        if  mfn_mesh.polygonVertexCount(item) <= 3:
            component_name = '{0}.e[{1}]'.format(mesh_name, item)
            triangle_face_list.append( component_name)

    return triangle_face_list


def J_uvTools_find_many_edge(mesh_name):
    """
    Check faces larger than 4 sides
    :param str mesh_name: object long name eg.'|group3|pSphere1'
    :return: Component list
    :rtype: list
    """
    mesh_list = om2.MSelectionList()
    mesh_list.add(mesh_name)

    dag_path = mesh_list.getDagPath(0)

    mfn_mesh = om2.MFnMesh(dag_path)
    face_numbers = mfn_mesh.numPolygons

    triangle_face_list=[]
    for item in xrange(face_numbers):
        if  mfn_mesh.polygonVertexCount(item) >= 5:
            component_name = '{0}.e[{1}]'.format(mesh_name, item)
            triangle_face_list.append( component_name)
    return triangle_face_list


def J_uvTools_find_non_manifold_edges(mesh_name):
    """
    Check for non-manifold edges
    :param str mesh_name: object long name eg.'|group3|pSphere1'
    :return: edge index
    :rtype: list
    """
    mesh_list = om2.MSelectionList()
    mesh_list.add(mesh_name)
    dag_path = mesh_list.getDagPath(0)
    edge_it = om2.MItMeshEdge(dag_path)
    edge_indices = []

    while not edge_it.isDone():
        face_count = edge_it.numConnectedFaces()
        if face_count > 2:
            component_name = '{0}.e[{1}]'.format(mesh_name, int(edge_it.index()))
            edge_indices.append(component_name)
        edge_it.next()
    return edge_indices


def J_uvTools_find_lamina_faces(mesh_name):
    """
    Check lamina faces
    :param str mesh_name: object long name eg.'|group3|pSphere1'
    :return: face index
    :rtype: list
    """

    mesh_list = om2.MSelectionList()
    mesh_list.add(mesh_name)
    dag_path = mesh_list.getDagPath(0)

    poly_it = om2.MItMeshPolygon(dag_path)
    poly_indices = []

    while not poly_it.isDone():

        if poly_it.isLamina():
            component_name = '{0}.f[{1}]'.format(mesh_name, poly_it.index())
            poly_indices.append(component_name)
        poly_it.next(1)

    return poly_indices


def J_uvTools_find_bivalent_faces(mesh_name):
    """
    Check bivalent faces
    :param str mesh_name: object long name eg.'|group3|pSphere1'
    :return: vertex index
    :rtype: list
    """
    mesh_list = om2.MSelectionList()
    mesh_list.add(mesh_name)
    dag_path = mesh_list.getDagPath(0)

    vertex_it = om2.MItMeshVertex(dag_path)
    vertex_indices = []

    while not vertex_it.isDone():
        connect_faces = vertex_it.getConnectedFaces()
        connect_edges = vertex_it.getConnectedEdges()

        if len(connect_faces) == 2 and len(connect_edges) == 2:
            component_name = '{0}.f[{1}]'.format(mesh_name, vertex_it.index())
            vertex_indices.append(component_name)
        vertex_it.next()

    return vertex_indices


def J_uvTools_find_zero_area_faces(mesh_name, max_face_area=0.001):
    """
    Check zero area faces
    :param str mesh_name: object long name eg.'|group3|pSphere1'
    :param float max_face_area: max face area
    :return: face index
    :rtype: list
    """
    mesh_list = om2.MSelectionList()
    mesh_list.add(mesh_name)
    dag_path = mesh_list.getDagPath(0)

    poly_it = om2.MItMeshPolygon(dag_path)
    poly_indices = []

    while not poly_it.isDone():

        if poly_it.getArea() < max_face_area:
            component_name = '{0}.f[{1}]'.format(mesh_name, poly_it.index())
            poly_indices.append(component_name)
        poly_it.next(1)

    return poly_indices


def J_uvTools_find_mesh_border_edges(mesh_name):
    """
    Check mesh border edges
    :param str mesh_name: object long name eg.'|group3|pSphere1'
    :return: edge index
    :rtype: list
    """
    mesh_list = om2.MSelectionList()
    mesh_list.add(mesh_name)
    dag_path = mesh_list.getDagPath(0)

    edge_it = om2.MItMeshEdge(dag_path)

    edge_indices = []

    while not edge_it.isDone():
        if edge_it.onBoundary():
            component_name = '{0}.e[{1}]'.format(mesh_name, int(edge_it.index()))
            edge_indices.append(component_name)
        edge_it.next()
    return edge_indices




def J_uvTools_find_zero_length_edges(mesh_name, min_edge_length=0.001):
    """
    Check mesh border edges
    :param str mesh_name: object long name eg.'|group3|pSphere1'
    :param float min_edge_length: min edge length
    :return: edge index
    :rtype: list
    """
    mesh_list = om2.MSelectionList()
    mesh_list.add(mesh_name)
    dag_path = mesh_list.getDagPath(0)

    edge_it = om2.MItMeshEdge(dag_path)

    edge_indices = []

    while not edge_it.isDone():
        if edge_it.length() < min_edge_length:
            component_name = '{0}.e[{1}]'.format(mesh_name, int(edge_it.index()))
            edge_indices.append(component_name)
        edge_it.next()
    return edge_indices


def J_uvTools_find_unfrozen_vertices(mesh_name):
    """
    Check unfrozen vertices
    :param str mesh_name: object long name eg.'|group3|pSphere1'
    :return: vertice index
    :rtype: list
    """
    mesh_list = om2.MSelectionList()
    mesh_list.add(mesh_name)
    dag_path = mesh_list.getDagPath(0)

    mesh_fn = om2.MFnMesh(dag_path)
    dag_path.extendToShape()

    dag_node = om2.MFnDagNode(dag_path)

    pnts_plug = dag_node.findPlug("pnts", True)

    num_vertices = mesh_fn.numVertices

    vertice_indices = []

    for i in xrange(num_vertices):
        xyz_plug = pnts_plug.elementByLogicalIndex(i)
        if xyz_plug.isCompound:
            xyz = [0.0, 0.0, 0.0]
            for a in range(3):
                xyz[a] = xyz_plug.child(a).asFloat()
            if not (abs(xyz[0]) <= 0.0 and abs(xyz[1]) <= 0.0 and abs(xyz[2]) <= 0.0):
                component_name = '{0}.vtx[{1}]'.format(mesh_name, int(i))
                vertice_indices.append(component_name)
    return vertice_indices


def J_uvTools_uv_face_cross_quadrant(mesh_name):
    """
    Check uv face cross quadrant
    :param str mesh_name: object long name eg.'|group3|pSphere1'
    :return: face index
    :rtype: list
    """
    mesh_list = om2.MSelectionList()
    mesh_list.add(mesh_name)
    dag_path = mesh_list.getDagPath(0)
    uv_face_list = []

    face_it = om2.MItMeshPolygon(dag_path)

    while not face_it.isDone():
        u_quadrant = None
        v_quadrant = None
        uvs = face_it.getUVs()

        for index, uv_coordinates in enumerate(uvs):
            # u
            if index == 0:
                for u_coordinate in uv_coordinates:
                    if u_quadrant is None:
                        u_quadrant = int(u_coordinate)
                    if u_quadrant != int(u_coordinate):
                        component_name = '{0}.f[{1}]'.format(mesh_name, face_it.index())
                        if component_name not in uv_face_list:
                            uv_face_list.append(component_name)
                        #print index, uv_coordinates
            # v
            if index == 1:
                for v_coordinate in uv_coordinates:
                    if v_quadrant is None:
                        v_quadrant = int(v_coordinate)
                    if v_quadrant != int(v_coordinate):
                        component_name = '{0}.f[{1}]'.format(mesh_name, face_it.index())
                        if component_name not in uv_face_list:
                            uv_face_list.append(component_name)
                        #print index, uv_coordinates

        face_it.next(None)
    cmds.select(uv_face_list)
    return uv_face_list


def J_uvTools_missing_uv_faces(mesh_name):
    """
    Check face has uv
    :param str mesh_name: object long name eg.'|group3|pSphere1'
    :return: face index
    :rtype: list
    """
    miss_uv_face = []
    mesh_list = om2.MSelectionList()
    mesh_list.add(mesh_name)
    dag_path = mesh_list.getDagPath(0)

    face_it = om2.MItMeshPolygon(dag_path)

    while not face_it.isDone():
        if face_it.hasUVs() is False:
            component_name = '{0}.f[{1}]'.format(mesh_name, face_it.index())
            miss_uv_face.append(component_name)
        face_it.next(None)
    cmds.select(miss_uv_face)
    return miss_uv_face


def J_uvTools_find_double_faces(mesh_name):
    """
    Check all points common to both faces
    :param str mesh_name: object long name eg.'|group3|pSphere1'
    :return: vertex index
    :rtype: list
    """
    mesh_list = om2.MSelectionList()
    mesh_list.add(mesh_name)
    dag_path = mesh_list.getDagPath(0)

    vertex_it = om2.MItMeshVertex(dag_path)
    vertex_indices = []

    face_id = []

    while not vertex_it.isDone():
        connect_faces = vertex_it.getConnectedFaces()
        connect_edges = vertex_it.getConnectedEdges()
        # print connect_faces, connect_edges
        if len(connect_faces) == 5 and len(connect_edges) == 4:

            vertex_indices.append(vertex_it.index())
            if face_id == []:
                face_id = list(connect_faces)
            else:
                face_id = list(set(face_id).intersection(set(list(connect_faces))))
            print face_id
        vertex_it.next()
    cmds.select(['{0}.f[{1}]'.format(mesh_name, a) for a in face_id])


def J_uvTools_judge_edge_position(edges_point, edges_point_ju):
    """
    Determine if two edges may intersect
    :param edges_point:
    :param edges_point_ju:
    :return:
    """
    # judge u
    if min(edges_point[0][0], edges_point[1][0]) > max(edges_point_ju[0][0], edges_point_ju[1][0]) or \
            min(edges_point_ju[0][0], edges_point_ju[1][0]) > max(edges_point[0][0], edges_point[1][0]):
        return True
    # judge v
    elif min(edges_point[0][1], edges_point[1][1]) > max(edges_point_ju[0][1], edges_point_ju[1][1]) or\
            min(edges_point_ju[0][1], edges_point_ju[1][1]) > max(edges_point[0][1], edges_point[1][1]):
        return True
    else:
        return False


def J_uvTools_get_max_min_uv(face_point):
    """
    get face max uv value and min uv value
    :param face_point: face point uv value
    :return:
    """
    if len(face_point) == 4:
        return min(face_point[0][0], face_point[1][0], face_point[2][0], face_point[3][0]), \
               max(face_point[0][0], face_point[1][0], face_point[2][0], face_point[3][0]), \
               min(face_point[0][1], face_point[1][1], face_point[2][1], face_point[3][1]), \
               max(face_point[0][1], face_point[1][1], face_point[2][1], face_point[3][1])
    elif len(face_point) == 3:
        return min(face_point[0][0], face_point[1][0], face_point[2][0]), \
               max(face_point[0][0], face_point[1][0], face_point[2][0]), \
               min(face_point[0][1], face_point[1][1], face_point[2][1]), \
               max(face_point[0][1], face_point[1][1], face_point[2][1])


def J_uvTools_judge_face_position(edges_point, edges_point_ju):
    """
    Determine if two faces may intersect
    :param tuple edges_point: edges point uv value
    :param tuple edges_point_ju: edges point uv value
    :return:
    """

    if edges_point[0] >= edges_point_ju[1] or \
            edges_point_ju[0] >= edges_point[1] or \
            edges_point[2] >= edges_point_ju[3] or \
            edges_point_ju[2] >= edges_point[3]:
        return True
    elif (edges_point[0] == edges_point_ju[0] and edges_point[1] == edges_point_ju[1]) and \
            (edges_point[2] == edges_point_ju[2] and edges_point[3] == edges_point_ju[3]):

        return True
    else:
        return False


def J_uvTools_judge_edge(edges_point, edges_point_ju):
    """
    judge edge intersect
    :param list edges_point: edges point uv value
    :param list edges_point_ju: edges point uv value
    :return: bool
    """

    x1 = edges_point[0][0] - edges_point[1][0]
    y1 = edges_point[0][1] - edges_point[1][1]

    x2 = edges_point_ju[0][0] - edges_point[1][0]
    y2 = edges_point_ju[0][1] - edges_point[1][1]

    x3 = edges_point_ju[1][0] - edges_point[1][0]
    y3 = edges_point_ju[1][1] - edges_point[1][1]

    x4 = edges_point_ju[0][0] - edges_point_ju[1][0]
    y4 = edges_point_ju[0][1] - edges_point_ju[1][1]

    x5 = edges_point[0][0] - edges_point_ju[1][0]
    y5 = edges_point[0][1] - edges_point_ju[1][1]

    x6 = edges_point[1][0] - edges_point_ju[1][0]
    y6 = edges_point[1][1] - edges_point_ju[1][1]

    if (x1 * y2 - x2 * y1) * (x1 * y3 - x3 * y1) < 0.0 and (x4 * y5 - x5 * y4) * (x4 * y6 - x6 * y4) < 0.0:
        return True
    else:
        return False


def J_uvTools_check_uv_overlapping(mesh):
    """
    check overlapping uv
    :param str mesh : object long name eg.'|group3|pSphere1'
    :return: mesh face list
    :rtype: list
    """
    # get MFnMesh
    select_list = om2.MSelectionList()
    select_list.add(mesh)
    dag_path = select_list.getDagPath(0)
    mfn_mesh = om2.MFnMesh(dag_path)

    face_id_over = []   # store overlapping face
    all_uv_value_dict = {}   # store all uv value on the face
    max_min_uv_dict = {}   # store all uv max and min value on the face
    face_edges_dict = {}   # Store all edges on the face

    for face_id in xrange(mfn_mesh.numPolygons):
        face_edges_dict[face_id] = []
        uv_value_list = []
        for point_index in xrange(len(mfn_mesh.getPolygonVertices(face_id))):
            uv_value_list.append(mfn_mesh.getPolygonUV(face_id, point_index))

        all_uv_value_dict[face_id] = uv_value_list
        max_min_uv_dict[face_id] = J_uvTools_get_max_min_uv(uv_value_list)
        for i in xrange(len(uv_value_list)):
            if i == len(uv_value_list) - 1:
                edges_value = [(uv_value_list[i][0], uv_value_list[i][1]), (uv_value_list[0][0], uv_value_list[0][1])]
            else:
                edges_value = [(uv_value_list[i][0], uv_value_list[i][1]), (uv_value_list[i + 1][0], uv_value_list[i+1][1])]

            face_edges_dict[face_id].append(edges_value)

    for face_id in xrange(mfn_mesh.numPolygons):

        edges_list = face_edges_dict[face_id]
        for face_id_next in xrange(face_id + 1, mfn_mesh.numPolygons):
            have = 0   # if edges intersect 'have is 1'
            edg_list_next = face_edges_dict[face_id_next]

            if not J_uvTools_judge_face_position(max_min_uv_dict[face_id], max_min_uv_dict[face_id_next]):

                for edges_point in edges_list:
                    if have == 0:
                        for edg_point_ju in edg_list_next:

                            if not J_uvTools_judge_edge_position(edges_point, edg_point_ju):

                                if J_uvTools_judge_edge(edges_point, edg_point_ju):

                                    if face_id not in face_id_over:
                                        have = 1
                                        face_id_over.append(face_id)
                                    if face_id_next not in face_id_over:
                                        have = 1
                                        face_id_over.append(face_id_next)

                                    break
                    else:
                        break

    return ['{0}.f[{1}]'.format(mesh, face_id_num) for face_id_num in face_id_over]



    
    
    

