# Import librairies
import base_struct as bs
import glm
import moderngl as mgl
import numpy as np
import pygame as pg
import sys

class Shader_Program:
    """Class representing a shader program
    """

    def __init__(self, base_struct: bs.Base_Struct, path: str) -> None:
        """Create a shader program

        Args:
            base_struct (bs.Base_Struct): base struct in the game
            path (str): path of the program
        """
        self.base_struct = base_struct
        self.program = self.load_program(path)

    def destroy(self) -> None:
        """Destroy the shader program
        """
        self.program.release()

    def get_base_struct(self) -> bs.Base_Struct:
        """Return the base struct of the game

        Returns:
            bs.Base_Struct: base struct of the game
        """
        return self.base_struct
    
    def get_program(self) -> mgl.Program:
        """Return the program into the shader program

        Returns:
            mgl.Program: program into the shader program
        """
        return self.program
    
    def load_program(self, path) -> mgl.Program:
        vertex_shader = ""
        with open(path + ".vert") as file:
            vertex_shader = file.read()

        fragment_shader = ""
        with open(path + ".frag") as file:
            fragment_shader = file.read()

        return self.get_base_struct().get_context().program(vertex_shader, fragment_shader)

class VBO:
    """Class representing a base of vertex buffer objects
    """

    def __init__(self, base_struct: bs.Base_Struct) -> None:
        """Create a base of vertex buffer object

        Args:
            base_struct (bs.Base_Struct): base struct in the game
        """
        self.attributes = []
        self.base_struct = base_struct
        self.format = ""
        self.vbo = self.get_base_struct().get_context().buffer(self.get_vertex_data())

    def destroy(self) -> None:
        """Destroy the buffer
        """
        self.vbo.release()

    def get_attributes(self) -> list:
        """Return the attributes of the VBO

        Returns:
            list: attributes of the VBO
        """
        return self.attributes

    def get_base_struct(self) -> bs.Base_Struct:
        """Return the base struct of the game

        Returns:
            bs.Base_Struct: base struct of the game
        """
        return self.base_struct
    
    @staticmethod
    def get_data(vertices, indices):
        """Return the vertices arrange for the data

        Args:
            vertices (_type_): vertices of the polygon
            indices (_type_): indices of vertices order
        """
        data = []
        for triangle in indices:
            for indice in triangle:
                data.append(vertices[indice])
        return np.array(data, dtype="f4")
    
    def get_format(self) -> str:
        """Return the format of the VBO

        Returns:
            str: format of the VBO
        """
        return self.format

    def get_vbo(self) -> mgl.Buffer:
        """Return the buffers for the vertices

        Returns:
            mgl.Buffer: buffers for the vertices
        """
        return self.vbo
    
    def get_vertex_data(self): ...

class Triangle_VBO(VBO):
    """Class representing a 2D triangle VBO heritating from VBO
    """

    def __init__(self, base_struct: bs.Base_Struct) -> None:
        """Create a triangle vertex buffer object

        Args:
            base_struct (bs.Base_Struct): base struct in the game
        """
        super().__init__(base_struct)

        self.attributes = ["in_texcoord_0", "in_normal", "in_position"]
        self.format = "2f 3f 3f"

    def get_vertex_data(self):
        """Return the data with the vertex
        """
        vertices = [(-0.6, -0.8, 0.0), (0.6, -0.8, 0.0), (0.0, 0.8, 0.0),]
        vertex_data = np.array(vertices, dtype="f4")

        tex_coord_vertices = [(0, 0), (1, 0), (1, 1)]
        tex_coord_vertices = np.array(tex_coord_vertices, dtype="f4")

        normals = [(0, 0, 1), (0, 0, 1), (0, 0, 1)]
        normals = np.array(normals, dtype="f4")

        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_vertices, vertex_data])

        return vertex_data

class Square_VBO(VBO):
    """Class representing a 2D plan VBO heritating from VBO
    """

    def __init__(self, base_struct: bs.Base_Struct) -> None:
        """Create a square vertex buffer object

        Args:
            base_struct (bs.Base_Struct): base struct in the game
        """
        super().__init__(base_struct)

        self.attributes = ["in_texcoord_0", "in_normal", "in_position"]
        self.format = "2f 3f 3f"

    def get_vertex_data(self):
        """Return the data with the vertex
        """
        vertices = [(-1, -1, 0.0), (1, 1, 0.0), (1, -1, 0.0),
                    (-1, -1, 0.0), (-1, 1, 0.0), (1, 1, 0.0)]
        vertex_data = np.array(vertices, dtype="f4")

        tex_coord_vertices = [(0, 0), (1, 1), (1, 0), (0, 0), (0, 1), (1, 1)]
        tex_coord_vertices = np.array(tex_coord_vertices, dtype="f4")

        normals = [(0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1)]
        normals = np.array(normals, dtype="f4")

        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_vertices, vertex_data])

        return vertex_data

class Cube_VBO(VBO):
    """Class representing a VBO of a cube, heritating from VBO
    """

    def __init__(self, base_struct: bs.Base_Struct) -> None:
        """Create a cube vertex buffer object

        Args:
            base_struct (bs.Base_Struct): base struct in the game
        """
        super().__init__(base_struct)

        self.attributes = ["in_texcoord_0", "in_normal", "in_position", "in_face"]
        self.format = "2f 3f 3f f"
    
    def get_vertex_data(self):
        """Return the data with the vertex
        """
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]
        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)

        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1)]
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)

        normals = [(0, 0, 1) *6,
                   (1, 0, 0) * 6,
                   (0, 0, -1) * 6,
                   (-1, 0, 0) * 6,
                   (0, 1, 0) * 6,
                   (0, -1, 0) * 6]
        normals = np.array(normals, dtype="f4").reshape(36, 3)

        face = []
        for i in range(6):
            for _ in range(6):
                face.append((i,))
        face = np.array(face, dtype="f")

        vertex_data = np.hstack([vertex_data, face])
        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        return vertex_data
 
class VAO:
    """Class representing a vertex array object
    """

    def __init__(self, vbo: VBO, base_struct: bs.Base_Struct, shader_path = "shaders/triangle") -> None:
        """Create a vertex array object

        Args:
            vbo (VBO): vbo for this VAO
            base_struct (bs.Base_Struct): base struct in the game
        """
        self.vbo = vbo
        self.base_struct = base_struct
        self.program = Shader_Program(self.get_base_struct(), shader_path)

        self.vao = self.get_base_struct().get_context().vertex_array(self.get_program().get_program(), [(vbo.get_vbo(), vbo.get_format(), *vbo.get_attributes())])
    
    def destroy(self) -> None:
        """Destroy the VAO
        """
        self.vbo.destroy()
        self.get_program().destroy()
        self.get_vao().release()
    
    def get_base_struct(self) -> bs.Base_Struct:
        """Return the base struct of the game

        Returns:
            bs.Base_Struct: base struct of the game
        """
        return self.base_struct
    
    def get_vao(self) -> mgl.VertexArray:
        """Return the VAO of the object

        Returns:
            mgl.VertexArray: VAO of the object
        """
        return self.vao
    
    def get_vbo(self) -> VBO:
        """Return the VBO of the object

        Returns:
            VBO: VBO of the object
        """
        return self.vbo
    
    def get_program(self) -> Shader_Program:
        """Return the program into the VAO

        Returns:
            mgl.Program: program into the VAO
        """
        return self.program
    
    def render(self) -> None:
        """Render the VAO
        """
        self.get_vao().render()

class Texture:
    """Class representating a texture
    """

    def __init__(self, base_struct: bs.Base_Struct, texture_path: str, flip: tuple = (False, True)) -> None:
        """Create a texture object
        """
        self.base_struct = base_struct
        self.flip = flip
        self.number_binded = 0
        self.texture_path = texture_path

        self.texture = self.load_texture(texture_path)

    def get_base_struct(self) -> bs.Base_Struct:
        """Return the base struct of the game

        Returns:
            bs.Base_Struct: base struct of the game
        """
        return self.base_struct
    
    def get_bind_number(self) -> int:
        """Return the number binded for the texture

        Returns:
            int: number binded for the texture
        """
        return self.number_binded
    
    def get_flip(self) -> tuple:
        """Return a tuple of bool is the x and y texture should flip

        Returns:
            tuple: _tuple of bool is the x and y texture should flip
        """
        return self.flip
    
    def get_texture(self) -> mgl.Texture:
        """Return the moderngl texture

        Returns:
            mgl.Texture: moderngl texture
        """
        return self.texture
    
    def get_texture_path(self) -> str:
        """Return the path of the texture

        Returns:
            str: path of the texture
        """
        return self.texture_path

    def load_texture(self, path: str) -> mgl.Texture:
        """Load a texture

        Returns:
            pg.Surface: texture loaded
        """
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, self.get_flip()[0], self.get_flip()[1])
        texture = self.get_base_struct().get_context().texture(size = texture.get_size(), components = 3, data = pg.image.tostring(texture, "RGB"))
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        texture.anisotropy = 32.0

        self.number_binded = self.get_base_struct().get_texture_count()
        self.get_base_struct().set_texture_count(self.get_base_struct().get_texture_count() + 1)
        texture.use(self.get_bind_number())
        return texture

class Graphic_Object(bs.Transform_Object):
    """Class representating a graphic object
    """

    def __init__(self, base_struct: bs.Base_Struct, texture: Texture, vbo: VBO, parent: bs.Transform_Object = None, position: tuple = (0, 0, 0), rotation: tuple = (0, 0, 0), scale: tuple = (0, 0, 0), shader_path = "shaders/triangle", type: str = "graphic", do_on_init = True) -> None:
        """Create a graphic object

        Args:
            texture_path (str): path through the texture
            position (tuple, optional): position of the plan. Defaults to (0, 0, 0).
            rotation (tuple, optional): rotation of the plan. Defaults to (0, 0, 0).
            type (str, optional): type of the object. Defaults to "graphic".
        """
        super().__init__(parent, position, rotation, scale)

        self.base_struct = base_struct
        self.texture = texture
        self.type = type

        self.texture = [texture]
        self.vao = VAO(vbo, self.get_base_struct(), shader_path)

        if do_on_init: self.on_init()

    def destroy(self) -> None:
        """Destroy the graphic object
        """
        self.vao.destroy()

    def get_base_struct(self) -> bs.Base_Struct:
        """Return the base struct of the game

        Returns:
            bs.Base_Struct: base struct of the game
        """
        return self.base_struct

    def get_texture_path(self) -> str:
        """Return the path through the texture

        Returns:
            str: path through the texture
        """
        return self.texture_path
    
    def get_type(self) -> str:
        """Return the type of the object

        Returns:
            str: type of the object
        """
        return self.type
    
    def get_vao(self) -> VAO:
        """Return the vao of the model

        Returns:
            VAO: vao of the model
        """
        return self.vao
    
    def on_init(self) -> None:
        """Init the uniform variables into the shader
        """
        self.get_vao().get_program().get_program()["m_model"].write(self.get_model_matrix())
        self.get_vao().get_program().get_program()["m_proj"].write(self.get_base_struct().get_camera_value().get_projection())
        self.get_vao().get_program().get_program()["m_view"].write(self.get_base_struct().get_camera_value().get_view())
        self.get_vao().get_program().get_program()["u_texture_0"] = self.get_base_struct().get_texture_count()
        self.texture[0].get_texture().use(self.get_base_struct().get_texture_count())
        self.get_base_struct().set_texture_count(self.get_base_struct().get_texture_count() + 1)

    def on_render(self) -> None:
        """Function called before the rendering of the object
        """
        pass

    def render(self) -> None:
        """Render the model
        """
        self.on_render()
        self.vao.get_program().get_program()["m_model"].write(self.get_model_matrix())
        self.vao.get_program().get_program()["m_view"].write(self.get_base_struct().get_camera_value().get_view())
        self.get_vao().render()

class Cube_Object(Graphic_Object):
    """Class representating a graphic cube, heritating from Graphics_Object
    """

    def __init__(self, base_struct: bs.Base_Struct, texture: list, vbo: VBO, parent: bs.Transform_Object = None, position: tuple = (0, 0, 0), rotation: tuple = (0, 0, 0), scale: tuple = (0, 0, 0), shader_path: str = "shaders/cube", type: str = "cube") -> None:
        """Create a graphics cube

        Args:
            base_struct (bs.Base_Struct): base struct in the game
            vao (VAO): vertex array object for the cube
            texture (list): list of textures into the cube
            position (tuple, optional): position of the cube. Defaults to (0, 0, 0).
            rotation (tuple, optional): rotation of the cube. Defaults to (0, 0, 0).
            scale (tuple, optional): scale of the cube. Defaults to (0, 0, 0).
            type (str, optional): tpe fo the cube. Defaults to "cube".
        """
        super().__init__(base_struct, texture[0], vbo, parent, position, rotation, scale, shader_path, type, False)

        for i in range(1, 6):
            self.texture.append(texture[i])
        self.on_init()

    def on_init(self) -> None:
        """Init the uniform variables into the shader
        """
        self.get_vao().get_program().get_program()["m_model"].write(self.get_model_matrix())
        self.get_vao().get_program().get_program()["m_proj"].write(self.get_base_struct().get_camera_value().get_projection())
        self.get_vao().get_program().get_program()["m_view"].write(self.get_base_struct().get_camera_value().get_view())
        for t in range(0, len(self.texture)):
            self.get_vao().get_program().get_program()["u_texture_" + str(t)] = self.texture[t].get_bind_number()