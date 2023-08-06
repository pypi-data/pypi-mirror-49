# from shapely.geometry import Polygon
import pkg_resources

from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np

from layer import Layer
from vertice import Vertex
from edge import Edge
from edge_loop import EdgeLoop
from polyline import Polyline
from face import Face
from material import Material, MatLayer, Window
from zone import Zone
from building import Building
from proxy_geometry import ProxyGeometry

from import_dae import *
from import_obj import *
from import_stl import *


def import_geometry(filename, encoding_format='utf16'):
    # file picker for debugging surposes
    # Tk().withdraw()
    # file = askopenfilename()

    with open(filename, 'r', encoding=encoding_format) as f:
        print('reading file')
        content = f.read()

    return parse_content(content)


def parse_content(content):
    # file format description:
    # https://github.com/bph-tuwien/SIMULTAN/wiki/FORMAT_geosim
    print('processing header')

    # remove all newline characters
    content = content.rstrip('\r\n').replace('\n', ';')
    # split string:
    data = content.split(';')

    # ------------------------------------------------------------------
    # read Header
    # ------------------------------------------------------------------

    header_fields = ['FormatType',                   # 0        str
                     'Version',                      # 1        int
                     'ModelID',                      # 2        ulong
                     'ModelPermissions',             # 3        ulong
                     'GeometryPermissions',          # 4
                     'LayerPermissions',             # 5
                     'LayerCount',                   # 6
                     'VertexCount',                  # 7
                     'EdgeCount',                    # 8
                     'EdgeLoopCount',                # 9
                     'PolylineCount',                # 10
                     'FaceCount',                    # 11
                     'VolumeCount',                  # 12
                     'LinkedModelCount',             # 13
                     'ProxyCount',                   # 14
                     'GeoRefCount'                   # 15
                     ]

    header_formats = []

    data[1:15] = map(int, data[1:15])

    # header
    header = dict(zip(header_fields[2:], data[1:15]))
    header['FormatType'] = data[0][0]
    header['Version'] = data[0][1]
    data = data[16:]

    # Model
    model = {'Name': data[1][0:int(data[0])], 'IsVisible': bool(data[1][int(data[0])])}
    # remove model entry:
    data = data[2:]

    # -----------------------------------------------------------------------------------
    # read layers
    # -----------------------------------------------------------------------------------

    layer_header = ['ID',		        # ulong
                    'ParentID',	        # ulong (or empty when no parent exists)
                    'Name',		        # string
                    'IsVisible',	    # bool
                    'ColorR',		    # byte
                    'ColorG',		    # byte
                    'ColorB',		    # byte
                    'ColorA',		    # byte
                    'ColorFromParent'   # bool
                    ]

    print('reading layers')

    layers_data = list()

    for i in range(header['LayerCount']):
        layers_data.append(data[0:8])
        data = data[8:]

    # -----------------------------------------------------------------------------------
    # read vertices
    # -----------------------------------------------------------------------------------

    vertices_data = list()

    print('reading vertices')
    for i in range(header['VertexCount']):
        vertices_data.append(data[0:11])
        data = data[11:]

    # -----------------------------------------------------------------------------------
    # read edges
    # -----------------------------------------------------------------------------------

    edges_data = list()

    print('reading edges')
    for i in range(header['EdgeCount']):
        edges_data.append(data[0:10])
        data = data[10:]

    # -----------------------------------------------------------------------------------
    # read edge-loops
    # -----------------------------------------------------------------------------------

    edge_loops_data = list()

    print('reading edge loops')
    for i in range(header['EdgeLoopCount']):
        edge_count = int(data[3][1:])
        edge_loops_data.append(data[0:edge_count+9])
        data = data[edge_count + 9:]

    # -----------------------------------------------------------------------------------
    # read polylines
    # -----------------------------------------------------------------------------------

    polylines_data = list()

    print('reading polylines')
    for i in range(header['PolylineCount']):
        edge_count = int(data[3][1:])
        polylines_data.append(data[0:edge_count + 9])
        data = data[edge_count + 9:]

    # -----------------------------------------------------------------------------------
    # read faces
    # -----------------------------------------------------------------------------------

    faces_data = list()

    print('reading faces')
    for i in range(header['FaceCount']):
        hole_count = int(data[4])
        faces_data.append(data[0:hole_count + 11])
        data = data[hole_count + 11:]

    # -----------------------------------------------------------------------------------
    # read volumes
    # -----------------------------------------------------------------------------------

    volumes_data = list()

    print('reading volumes')
    for i in range(header['VolumeCount']):
        face_count = int(data[3][1:])
        volumes_data.append(data[0:9+face_count])
        data = data[9+face_count:]

    # -----------------------------------------------------------------------------------
    # read ProxyGeometry
    # -----------------------------------------------------------------------------------

    proxy_geometries_data = list()
    proxy_geometries = list()

    print('reading proxy geometries')
    for i in range(header['ProxyCount']):
        proxy_geometries_data.append(data[0:16])
        data = data[16:]

    # -----------------------------------------------------------------------------------
    # process ProxyGeometry
    # -----------------------------------------------------------------------------------

    layers = parse_layers(layers_data)
    vertices = parse_vertices(vertices_data, layers)
    edges = parse_edges(edges_data, vertices, layers)
    edge_loops = parse_edge_loops(edge_loops_data, edges, layers)
    polylines = parse_polylines(polylines_data, edges, layers)
    faces = parse_faces(faces_data, edge_loops, layers)
    volumes = parse_volumes(volumes_data, faces)

    # -----------------------------------------------------------------------------------
    # create building
    # -----------------------------------------------------------------------------------

    my_building = Building(is_visible=model['IsVisible'],
                           vertices=vertices,
                           faces=faces,
                           zones=volumes,
                           name=model['Name'],
                           layers=layers,
                           edges=edges,
                           geometry_permissions=header["GeometryPermissions"],
                           layer_permissions=header['LayerPermissions'],
                           model_permissions=header["ModelPermissions"],
                           edge_loops=edge_loops,
                           polylines=polylines,
                           geo_ref_count=header["GeoRefCount"],
                           linked_model_count=header["LinkedModelCount"],
                           building_id=header["ModelID"])

    return my_building


def parse_layers(layers_data):

    print('processing layers')

    layers = list()

    for layer_data in layers_data:
        # convert data:

        if layer_data[1]:
            parent_id = int(layer_data[1])
        else:
            parent_id = []

        is_visible = layer_data[3][int(layer_data[2])]
        color = np.array(int(layer_data[3][int(layer_data[2]) + 1:]))
        color = np.append(color, (list(map(int, layer_data[4:7]))))

        layers.append(Layer(layer_id=int(layer_data[0]),
                            parent_id=parent_id,
                            name=layer_data[3][0:int(layer_data[2])],
                            is_visible=is_visible,
                            color=color,
                            color_from_parent=bool(layer_data[7])
                            )
                      )
    return layers


def parse_vertices(vertices_data, layers):

    print('processing vertices')

    vertices = list()
    for vertex_data in vertices_data:

        position = float(vertex_data[3][1:])
        position = np.append(position, (list(map(float, vertex_data[4:6]))))
        color = np.array(list(map(int, vertex_data[6:10])))
        layer_id = int(vertex_data[2][int(vertex_data[1]):])
        layer = next((x for x in layers if x.ID == layer_id), None)

        vertices.append(Vertex(vertex_id=int(vertex_data[0]),
                               layers=layer,
                               name=vertex_data[2][0:int(vertex_data[1])],
                               is_visible=bool(vertex_data[3][0]),
                               position=position,
                               color=color,
                               color_from_parent=bool(vertex_data[10])))

    return vertices


def parse_edges(edges_data, vertices, layers):

    print('processing edges')

    edges = list()

    for edge_data in edges_data:
        color = np.array(list(map(int, edge_data[5:8])))

        vertex_1 = next((x for x in vertices if x.ID == int(edge_data[3][1:])), None)
        vertex_2 = next((x for x in vertices if x.ID == int(edge_data[4])), None)

        layer_id = int(edge_data[2][int(edge_data[1]):])
        layer = next((x for x in layers if x.ID == layer_id), None)

        edges.append(Edge(vertex_1=vertex_1,
                          vertex_2=vertex_2,
                          edge_id=int(edge_data[0]),
                          name=edge_data[2][0:int(edge_data[1])],
                          layers=layer,
                          is_visible=bool(edge_data[3][0]),
                          color=color,
                          color_from_parent=bool(edge_data[9]))
                     )

    return edges


def parse_edge_loops(edge_loops_data, edges, layers):

    print('processing edge loops')

    edge_loops = list()

    for edge_loop_data in edge_loops_data:
        edge_count = int(edge_loop_data[3][1:])
        edge_ids = list(map(int, edge_loop_data[4:4 + int(edge_loop_data[3][1:])]))

        edge_loop_edges = []
        for edge_id in edge_ids:
            edge_loop_edges.append(next((x for x in edges if x.ID == edge_id), None))

        color = np.array(list(map(
            int, edge_loop_data[4 + int(edge_loop_data[3][1:]):4 + int(edge_loop_data[3][1:]) + 4]
        )))
        color_from_parent = bool(edge_loop_data[4 + edge_count + 4])

        layer_id = int(edge_loop_data[2][int(edge_loop_data[1]):])
        layer = next((x for x in layers if x.ID == layer_id), None)

        edge_loops.append(EdgeLoop(
            edge_loop_id=int(edge_loop_data[0]),
            name=edge_loop_data[2][0:int(edge_loop_data[1])],
            layers=layer,
            is_visible=bool(edge_loop_data[3][0]),
            edge_id=edge_ids,
            color=color,
            color_from_parent=color_from_parent,
            edges=edge_loop_edges
        )
        )

    return edge_loops


def parse_polylines(polylines_data, edges, layers):

    print('processing polylines')

    polylines = list()

    for data in polylines_data:
        edge_count = int(data[3][1:])
        polylines_data.append(data[0:edge_count + 9])
        data = data[edge_count + 9:]

        edge_count = int(data[3][1:])
        edge_ids = list(map(int, data[4:4 + int(data[3][1:])]))

        polyline_edges = []
        for edge_id in edge_ids:
            polyline_edges.append(next((x for x in edges if x.ID == edge_id), None))

        layer_id = int(data[2][int(data[1]):])
        layer = next((x for x in layers if x.ID == layer_id), None)

        polylines.append(Polyline(
            poly_id=int(data[0]),
            name=data[2][0:int(data[1])],
            layers=layer,
            is_visible=bool(data[3][0]),
            edge_ids=edge_ids,
            color=np.append(np.random.rand(1, 3), 0) * 255,
            color_from_parent=False,
            edges=polyline_edges
        )
        )
    return polylines


def parse_faces(faces_data, edge_loops, layers):

    print('processing faces')

    faces = list()

    for data in faces_data:

        # check if face already exists:
        face_exists = next((x for x in edge_loops if x.ID == int(data[0])), None)
        if face_exists:
            continue

        hole_count = int(data[4])
        boundary_id = int(data[3][1:])
        color = np.array(list(map(int, data[5 + hole_count + 1:9 + hole_count + 1])))
        color_from_parent = bool(data[9 + hole_count + 1])
        boundary = next((x for x in edge_loops if x.ID == boundary_id), None)

        if not(hole_count == 0):
            hole_ids = list(map(int, data[5:5+hole_count]))
            holes = list()
            # if there is a hole in the face:
            for hole_id in hole_ids:
                # check if the hole - face already exists
                hole = next((x for x in faces if x.Boundary[0].ID == hole_id), None)

                # check if hole-face is going to be created:
                if not hole:
                    hole_face_indx = []
                    for hole_data in enumerate(faces_data):
                        if int(hole_data[1][3][1:]) == hole_id:
                            hole_face_indx = hole_data[0]
                            break
                    # if a face to be created was found, create the face:
                    if hole_face_indx:
                        hole_data = faces_data[hole_face_indx]
                        hole_count = 0
                        hole_boundary = next((x for x in edge_loops if x.ID == hole_id), None)

                        layer_id = int(hole_data[2][int(hole_data[1]):])
                        layer = next((x for x in layers if x.ID == layer_id), None)

                        hole = Face(name=hole_data[2][0:int(hole_data[1])],
                                    layers=layer,
                                    is_visible=bool(hole_data[3][0]),
                                    boundary=hole_boundary,
                                    orientation=int(data[5 + hole_count]),
                                    color=color,
                                    color_from_parent=color_from_parent)
                    # create new face
                    else:   # if hole_face_indx:
                        hole_boundary = next((x for x in edge_loops if x.ID == hole_id), None)

                        layer_id = int(data[2][int(data[1]):])
                        layer = next((x for x in layers if x.ID == layer_id), None)

                        hole = Face(name='Hole{}'.format(hole_id),
                                    layers=layer,
                                    is_visible=bool(data[3][0]),
                                    boundary=hole_boundary,
                                    orientation=int(data[5 + hole_count]),
                                    color=color,
                                    color_from_parent=color_from_parent,
                                    overwrite_calcable=True)

                holes.append(hole)
                faces.append(hole)
        else:   # if not(hole_count == 0):
            hole_ids = list()
            holes = list()

        layer_id = int(data[2][int(data[1]):])
        layer = next((x for x in layers if x.ID == layer_id), None)

        faces.append(
            Face(face_id=int(data[0]),
                 name=data[2][0:int(data[1])],
                 layers=layer,
                 is_visible=bool(data[3][0]),
                 boundary=boundary,
                 holes=holes,
                 orientation=int(data[5+hole_count]),
                 color=color,
                 color_from_parent=color_from_parent,
                 overwrite_calcable=True)
        )

    return faces


def parse_volumes(volumes_data, faces):

    print('processing volumes')

    volumes = list()

    for data in volumes_data:

        try:
            face_count = int(data[3][1:])
            face_ids = list(map(int, data[4:4+face_count]))
        except Exception as e:
            print('error: {error} \n data-str: {data_str}'.format(error=e, data_str=data))
            face_ids = list()
            face_count = 0

        zone_faces = list()
        for face_id in face_ids:
            zone_faces.append(next((x for x in faces if x.ID == face_id), None))

        color = np.array(list(map(int, data[4 + face_count + 1:9 + face_count])))
        try:
            color_from_parent = bool(data[7 + face_count + 1])
        except Error as e:
            color_from_parent = False

        volumes.append(Zone(
                            zone_id=int(data[0]),
                            name=data[2][0:int(data[1])],
                            is_visible=bool(data[3][0]),
                            face_ids=face_ids,
                            faces=zone_faces,
                            color=color,
                            color_from_parent=color_from_parent
                            )
                       )

    return volumes


def parse_proxy_geometries(proxy_geometries_data):

    print('processing proxy_geometries')

    proxy_geometries = list()

    for data in proxy_geometries_data:
        proxy_geometries.append(ProxyGeometry())

    return proxy_geometries


if __name__ == '__main__':

    # file picker for debugging surposes
    # Tk().withdraw()
    # file = askopenfilename()

    # read default simgeo file:
    file = pkg_resources.resource_filename('resources', 'two_rooms_linked.simgeo')

    # file picker for debugging surposes
    Tk().withdraw()
    file = askopenfilename()

    if file.endswith('.dae'):
        building = read_dae(file)
    elif file.endswith('.obj'):
        building = read_obj(file)
    elif file.endswith('.stl'):
        building = import_stl(file)
    elif file.endswith('.simgeo'):
        building = import_geometry(file)
    else:
        building = Building()

        # scale the building

    print('Geometry successful imported')

    building.write_json()
    # building.plot_faces()

    # building.write_stl()

    # write .simgeo file:
    # building.write_simgeo()
