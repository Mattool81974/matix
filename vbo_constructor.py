# vbo_contructor.py
# File used to build complex VBO

# Import librairies
import math

def get_data(vertices: list, indices: list) -> list:
    """Return a list of vertices ordered by indices

    Args:
        vertices (list): list of vertices
        indices (list): list of indices

    Returns:
        list: vertices ordered by indices
    """
    data = []
    for triangle in indices:
        for indice in triangle:
            data.append(vertices[indice])
    return data

def cube(face: list = [0, 1, 2, 3, 4, 5], indices_start: int = 0, indices_texture_start: int = 0, position: tuple = (0, 0, 0), scale: tuple = (1, 1, 1)) -> str:
    """Return the data for a cube

    Returns:
        list: data for a cube
    """
    to_return = ""
    vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]
    indices = [(0, 2, 3), (0, 1, 2),
                (1, 7, 2), (1, 6, 7),
                (6, 5, 4), (4, 7, 6),
                (3, 4, 5), (3, 5, 0),
                (3, 7, 4), (3, 2, 7),
                (0, 6, 1), (0, 5, 6)]
    for i in range(len(indices)): indices[i] = (indices[i][0] + indices_start, indices[i][1] + indices_start, indices[i][2] + indices_start)
    
    vertices_texture = [(0, 0), (1, 0), (1, 1), (0, 1)]
    indices_texture = [(0, 2, 3), (0, 1, 2),
                       (0, 2, 3), (0, 1, 2),
                       (0, 1, 2), (2, 3, 0),
                       (2, 3, 0), (2, 0, 1),
                       (0, 2, 3), (0, 1, 2),
                       (3, 1, 2), (3, 0, 1)]
    for i in range(len(indices_texture)): indices_texture[i] = (indices_texture[i][0] + indices_texture_start, indices_texture[i][1] + indices_texture_start, indices_texture[i][2] + indices_texture_start)
    
    for v in range(len(vertices)):
        vertices[v] = (vertices[v][0] * scale[0] + position[0], vertices[v][1] * scale[1] + position[1], vertices[v][2] * scale[2] + position[2])
    
    faces = []
    for i in face:
        for _ in range(6):
            faces.append((i,))

    for v in vertices:
        for g in v:
            to_return += str(g) + " "
    to_return = to_return[:-1] + "\n"
    for i in indices:
        for g in i:
            to_return += str(g) + " "
    to_return = to_return[:-1] + "\n"
    for v in vertices_texture:
        for g in v:
            to_return += str(g) + " "
    to_return = to_return[:-1] + "\n"
    for i in indices_texture:
        for g in i:
            to_return += str(g) + " "
    to_return = to_return[:-1] + "\n"
    for i in faces:
        for g in i:
            to_return += str(g) + " "
    return to_return[:-1]

def points_polygon(diagonal: float, edge: int = 4, position: tuple = (0, 0, 0)) -> list:
    """Return a list of the point into a polygon

    Returns:
        list: point into a polygon
    """
    vertices = [position]
    for i in range(edge):
        theta = (2 * math.pi * i) / edge + math.pi / 4.0
        x = math.cos(theta)
        y = math.sin(theta)
        vertices.append((x * diagonal + position[0], y * diagonal + position[1], position[2]))
    return vertices

def polygon(diagonal: float, edge: int = 4, position: tuple = (0, 0, 0)) -> str:
    """Return the data for a polygon

    Returns:
        list: data for a polygon
    """
    to_return = ""
    vertices = points_polygon(diagonal, edge, position)

    indices = []
    for i in range(edge - 1):
        indices.append((0, i + 1, i + 2))
    indices.append((0, len(vertices) - 1, 1))

    vertices_texture = points_polygon(diagonal, edge)
    for i in range(len(vertices_texture)):
        pos = (vertices_texture[i][0], vertices_texture[i][1])
        vertices_texture[i] = ((1 + pos[0]) / 2.0, (1 + pos[1]) / 2.0)

    indices_texture = []
    for i in range(edge - 1):
        indices_texture.append((0, i + 1, i + 2))
    indices_texture.append((0, len(vertices_texture) - 1, 1))

    for v in vertices:
        for g in v:
            to_return += str(g) + " "
    to_return = to_return[:-1] + "\n"
    for i in indices:
        for g in i:
            to_return += str(g) + " "
    to_return = to_return[:-1] + "\n"
    for v in vertices_texture:
        for g in v:
            to_return += str(g) + " "
    to_return = to_return[:-1] + "\n"
    for i in indices_texture:
        for g in i:
            to_return += str(g) + " "
    to_return = to_return[:-1] + "\n"

    return to_return[:-1]

def polygon_3d(diagonal: float, edge: int = 4, inversed: bool = False, scale: tuple = (1, 1, 1)) -> str:
    """Return the data for a 3d polygon

    Returns:
        list: data for a 3d polygon
    """
    use_mid = True

    to_return = ""
    vertices = points_polygon(diagonal, edge, position = (0, 0, 1.0)) # Get vertices of the first face of the polygon
    indices = []
    for i in range(edge - 1): # Get the indices of every points in the first face
        indices.append((0, i + 1, i + 2))
    indices.append((0, len(vertices) - 1, 1))

    vertices_2 = points_polygon(diagonal, edge, position = (0, 0, -1.0)) # Get vertices of the second face of the polygon

    indices_2 = []
    offset = len(vertices)
    for i in range(edge - 1): # Get the indices of every points in the second face
        indices_2.append((i + 2 + offset, i + 1 + offset, offset))
    indices_2.append((offset + 1, offset + len(vertices_2) - 1, offset))

    if use_mid:
        indices_mid = []
        for v in range(len(vertices)): # Get the indices of every points in the mids face
            v_plus_1 = v + 1
            v_plus_offset = v + offset + 1
            if v_plus_1 >= len(vertices): v_plus_1 = 1
            if v_plus_offset >= len(vertices) + len(vertices_2): v_plus_offset = offset + 1
            indices_mid.append((v + offset, v_plus_1, v))
            indices_mid.append((v + offset, v_plus_offset, v_plus_1))

    vertices_texture = points_polygon(diagonal, edge) # Get the textures points of the first face
    for i in range(len(vertices_texture)):
        pos = (vertices_texture[i][0], vertices_texture[i][1])
        vertices_texture[i] = ((1 + pos[0]) / 2.0, (1 + pos[1]) / 2.0)

    indices_texture = []
    for i in range(edge - 1): # Get the indices of the points of the first face
        indices_texture.append((0, i + 1, i + 2))
    indices_texture.append((0, len(vertices_texture) - 1, 1))

    vertices_texture_2 = points_polygon(diagonal, edge) # Get the textures points of the second face
    for i in range(len(vertices_texture_2)):
        pos = (vertices_texture_2[i][0], vertices_texture_2[i][1])
        vertices_texture_2[i] = ((1 + pos[0]) / 2.0, (1 + pos[1]) / 2.0)

    indices_texture_2 = []
    offset = len(vertices_texture_2)
    for i in range(edge - 1): # Get the indices of the textures points of the second face
        indices_texture_2.append((i + 2 + offset, i + 1 + offset, offset))
    indices_texture_2.append((offset + 1, offset + len(vertices_texture_2) - 1, offset))

    if use_mid:
        indices_texture_mid = []
        for i in range(len(vertices) - 1): # Get the indices of the textures points of the mids face
            i_plus_1 = i + 2
            i_plus_offset = i + offset + 2
            if i_plus_1 >= len(vertices): i_plus_1 = 1
            if i_plus_offset >= len(vertices) + len(vertices_2): i_plus_offset = offset + 1
            indices_texture_mid.append((i + offset + 1, i_plus_1, i + 1))
            indices_texture_mid.append((i + offset + 1, i_plus_offset, i_plus_1))
        indices_texture_mid.append((len(vertices_2) + offset - 1, 1, i + 1))
        indices_texture_mid.append((len(vertices_2) + offset - 1, offset + 1, i_plus_1))

    faces = []
    for i in range(len(indices) * 3):
        faces.append((0,))

    if use_mid:
        faces_mid = []
        for i in range(len(indices_mid) * 3):
            faces_mid.append((2,))

    faces_2 = []
    for i in range(len(indices_2) * 3):
        faces_2.append((1,))

    for v in vertices:
        for g in v:
            to_return += str(g) + " "
    for v in vertices_2:
        for g in v:
            to_return += str(g) + " "
    to_return = to_return[:-1] + "\n"
    for i in indices:
        for g in i:
            to_return += str(g) + " "
    for i in indices_2:
        for g in i:
            to_return += str(g) + " "
    if use_mid:
        for i in indices_mid:
            for g in i:
                to_return += str(g) + " "
    to_return = to_return[:-1] + "\n"

    for v in vertices_texture:
        for g in v:
            to_return += str(g) + " "
    for v in vertices_texture_2:
        for g in v:
            to_return += str(g) + " "
    to_return = to_return[:-1] + "\n"
    for i in indices_texture:
        for g in i:
            to_return += str(g) + " "
    for i in indices_texture_2:
        for g in i:
            to_return += str(g) + " "
    if use_mid:
        for i in indices_texture_mid:
            for g in i:
                to_return += str(g) + " "
    to_return = to_return[:-1] + "\n"

    for f in faces:
        to_return += str(f[0]) + " "
    for f in faces_2:
        to_return += str(f[0]) + " "
    if use_mid:
        for f in faces_mid:
            to_return += str(f[0]) + " "

    return to_return[:-1]

class VBO_Constructor:
    """Class representating a easy VBO constructor
    """

    def __init__(self, attributes: str, format: str) -> None:
        """Create an easy VBO constructor
        """
        self.attributes = attributes
        self.format = format
        self.vertices = ""
        self.indices = ""
        self.vertices_texture = ""
        self.indices_texture = ""
        self.faces = ""

    def add_form(self, parts: list) -> None:
        """Add a form to the constructor

        Args:
            parts (list): form to add
        """
        if self.vertices == "":
            self.vertices += parts[0]
        else:
            self.vertices += " " + parts[0]
        if self.indices == "":
            self.indices += parts[1]
        else:
            self.indices += " " + parts[1]
        
        if self.vertices_texture == "":
            self.vertices_texture += parts[2]
        else:
            self.vertices_texture += " " + parts[2]
        if self.indices_texture == "":
            self.indices_texture += parts[3]
        else:
            self.indices_texture += " " + parts[3]

        if len(parts) > 4:
            if self.faces == "":
                self.faces += parts[4]
            else:
                self.faces += " " + parts[4]

    def join(self) -> str:
        """Return the vbo content

        Returns:
            str: vbo content
        """
        to_return = self.vertices + "\n" + self.indices + "\n" + self.vertices_texture + "\n" + self.indices_texture
        if self.faces != []:
            to_return += "\n" + self.faces
        return to_return
    
    def save(self, path: str) -> None:
        """Save the vbo into a file

        Args:
            path (str): file where to save the vbo
        """
        file = open(path, "w")
        file.write(self.attributes + "\n" + self.format + "\n")
        file.write(self.join())
        file.close()

def construct_chair() -> None:
    """Construct a simple chair
    """
    constructor = VBO_Constructor("in_texcoord_0 in_position", "2f 3f")
    constructor.add_form(cube(face = [2, 2, 2, 2, 0, 0], position = (0, 0.1, 0), scale = (0.7, 0.1, 0.7)).split("\n"))
    constructor.add_form(cube(face = [1, 1, 1, 1, 3, 3], indices_start = 8, position = (-0.5, -0.5, -0.5), scale = (0.1, 0.5, 0.1)).split("\n"))
    constructor.add_form(cube(face = [1, 1, 1, 1, 3, 3], indices_start = 16, position = (-0.5, -0.5, 0.5), scale = (0.1, 0.5, 0.1)).split("\n"))
    constructor.add_form(cube(face = [1, 1, 1, 1, 3, 3], indices_start = 24, position = (0.5, -0.5, -0.5), scale = (0.1, 0.5, 0.1)).split("\n"))
    constructor.add_form(cube(face = [1, 1, 1, 1, 3, 3], indices_start = 32, position = (0.5, -0.5, 0.5), scale = (0.1, 0.5, 0.1)).split("\n"))
    constructor.add_form(cube(face = [4, 1, 1, 1, 3, 3], indices_start = 40, position = (0.0, 0.6, -0.6), scale = (0.7, 0.4, 0.1)).split("\n"))
    constructor.save("vbos/chair.vbo")

def construct_polygon(diagonal: float, edge: int = 4) -> None:
    """Construct a simple polygon
    """
    constructor = VBO_Constructor("in_texcoord_0 in_position", "2f 3f")
    constructor.add_form(polygon(diagonal, edge).split("\n"))
    constructor.save("vbos/polygon" + str(edge) + ".vbo")

def construct_polygon_3d(diagonal: float, edge: int = 4) -> None:
    """Construct a simple polygon
    """
    constructor = VBO_Constructor("in_texcoord_0 in_position in_face", "2f 3f f")
    constructor.add_form(polygon_3d(diagonal, edge).split("\n"))
    constructor.save("vbos/polygon_3d" + str(edge) + ".vbo")

def construct_table() -> None:
    """Construct a simple table
    """
    constructor = VBO_Constructor("in_texcoord_0 in_position in_face", "2f 3f f")
    constructor.add_form(cube(face = [2, 2, 2, 2, 0, 0], position = (0, 0.9, 0), scale = (1, 0.1, 1)).split("\n"))
    constructor.add_form(cube(face = [1, 1, 1, 1, 3, 3], indices_start = 8, position = (-0.9, -0.1, -0.9), scale = (0.1, 0.9, 0.1)).split("\n"))
    constructor.add_form(cube(face = [1, 1, 1, 1, 3, 3], indices_start = 16, position = (-0.9, -0.1, 0.9), scale = (0.1, 0.9, 0.1)).split("\n"))
    constructor.add_form(cube(face = [1, 1, 1, 1, 3, 3], indices_start = 24, position = (0.9, -0.1, -0.9), scale = (0.1, 0.9, 0.1)).split("\n"))
    constructor.add_form(cube(face = [1, 1, 1, 1, 3, 3], indices_start = 32, position = (0.9, -0.1, 0.9), scale = (0.1, 0.9, 0.1)).split("\n"))
    constructor.save("vbos/table.vbo")

construct_polygon(1, 20)
construct_polygon_3d(1, 20)