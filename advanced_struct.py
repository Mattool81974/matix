# Import librairies
import base_struct as bs
import glm
import model
import moderngl as mgl
import pygame as pg

class Advanced_Struct:
    """Class representing all the advanced struct in the game
    """

    def __init__(self, base_struct: bs.Base_Struct) -> None:
        """Create an advanced struct class
        """
        self.all_textures = {}
        self.all_vbos = {}
        self.base_struct = base_struct
        self.camera = bs.Camera(self.get_base_struct())
        self.graphic = {"chair": "cube", "cercle": "triangle", "cube": "cube", "cylinder": "cube", "plan": "triangle", "square": "triangle", "table": "cube"}

        cercle_vbo = model.Loaded_VBO(self.get_base_struct(), "vbos/polygon20.vbo")
        chair_vbo = model.Loaded_VBO(self.get_base_struct(), "vbos/chair.vbo")
        cube_vbo = model.Cube_VBO(self.get_base_struct())
        cylinder_vbo = model.Loaded_VBO(self.get_base_struct(), "vbos/polygon_3d20.vbo")
        plan_vbo = model.Triangle_VBO(self.get_base_struct())
        square_vbo = model.Square_VBO(self.get_base_struct())
        table_vbo = model.Loaded_VBO(self.get_base_struct(), "vbos/table.vbo")

        self.all_vbos["cercle"] = cercle_vbo
        self.all_vbos["chair"] = chair_vbo
        self.all_vbos["cube"] = cube_vbo
        self.all_vbos["cylinder"] = cylinder_vbo
        self.all_vbos["plan"] = plan_vbo
        self.all_vbos["square"] = square_vbo
        self.all_vbos["table"] = table_vbo

    def get_all_textures(self) -> dict:
        """Return a dict of alls the textures

        Returns:
            dict: dict of alls the textures
        """
        return self.all_textures

    def get_all_vbos(self) -> dict:
        """Return a dict of alls the VBOs

        Returns:
            dict: dict of alls the VBOs
        """
        return self.all_vbos

    def get_base_struct(self) -> bs.Base_Struct:
        """Return the base struct of the game

        Returns:
            bs.Base_Struct: base struct of the game
        """
        return self.base_struct
    
    def get_camera(self) -> bs.Camera:
        """Return the camera into the game

        Returns:
            bs.Camera: camera into the game
        """
        return self.camera
    
    def get_graphic(self) -> dict:
        """Return a dict of graphic type by type

        Returns:
            list: graphic type by type
        """
        return self.graphic