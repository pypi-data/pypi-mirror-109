import ctypes
import sys

if sys.platform.startswith("win"):
    lib = ctypes.cdll.LoadLibrary( '\\'.join(__file__.split("\\")[:-1]) + "\\libminesweeper.dll")
else:
    lib = ctypes.cdll.LoadLibrary( '/'.join(__file__.split("/")[:-1]) + "/libminesweeper.so")

lib.DELETE.argtypes = [ctypes.c_void_p]

lib.MSGrid_Set1.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
lib.MSGrid_Set2.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_char]
lib.MSGrid.restype = ctypes.c_void_p
lib.MSGrid.argtypes = [ctypes.c_int, ctypes.c_int]
lib.MSGrid_Fill.argtypes = [ctypes.c_void_p, ctypes.c_char]
lib.MSGrid_GetHeight.restype = ctypes.c_int
lib.MSGrid_GetHeight.argtypes = [ctypes.c_void_p]
lib.MSGrid_GetWidth.restype = ctypes.c_int
lib.MSGrid_GetWidth.argtypes = [ctypes.c_void_p]
lib.MSGrid_Get.restype = ctypes.c_void_p
lib.MSGrid_Get.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]

lib.MSGridItem_ItemGetter.restype = ctypes.c_char
lib.MSGridItem_ItemGetter.argtypes = [ctypes.c_void_p]
lib.MSGridItem_HiddenGetter.restype = ctypes.c_bool
lib.MSGridItem_HiddenGetter.argtypes = [ctypes.c_void_p]
lib.MSGridItem_FlaggedGetter.restype = ctypes.c_bool
lib.MSGridItem_FlaggedGetter.argtypes = [ctypes.c_void_p]
lib.MSGridItem_XGetter.restype = ctypes.c_int
lib.MSGridItem_XGetter.argtypes = [ctypes.c_void_p]
lib.MSGridItem_YGetter.restype = ctypes.c_int
lib.MSGridItem_YGetter.argtypes = [ctypes.c_void_p]
lib.MSGridItem.restype = ctypes.c_void_p
lib.MSGridItem.argtypes = [ctypes.c_char, ctypes.c_bool, ctypes.c_bool, ctypes.c_int, ctypes.c_int]

lib.MSEngine.restype = ctypes.c_void_p
lib.MSEngine.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
lib.MSEngine_GetSurroundingBombs.restype = ctypes.c_int
lib.MSEngine_GetSurroundingBombs.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
lib.MSEngine_UncoverPoint.restype = ctypes.c_void_p
lib.MSEngine_UncoverPoint.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
lib.MSEngine_GetGrid.restype = ctypes.c_void_p
lib.MSEngine_GetGrid.argtypes = [ctypes.c_void_p]
lib.MSEngine_CountFlags.restype = ctypes.c_int
lib.MSEngine_CountFlags.argtypes = [ctypes.c_void_p]
lib.MSEngine_CheckFlags.restype = ctypes.c_bool
lib.MSEngine_CheckFlags.argtypes = [ctypes.c_void_p]
lib.MSEngine_FlagPoint.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]

class MSGridItem:
    def __init__(self, *inp):
        if len(inp) == 5:
            self.ptr = lib.MSGridItem(*inp)
            self.allocated = True
        else:
            self.ptr = inp[0]
            self.allocated = False

    def __del__(self):
        if self.allocated:
            lib.DELETE(self.ptr)

    def getItem(self):
        return lib.MSGridItem_ItemGetter(self.ptr)

    def hidden(self):
        return lib.MSGridItem_HiddenGetter(self.ptr)

    def flagged(self):
        return lib.MSGridItem_FlaggedGetter(self.ptr)

    def getX(self):
        return lib.MSGridItem_XGetter(self.ptr)

    def getY(self):
        return lib.MSGridItem_YGetter(self.ptr)

    def pyObject(self):
        return {
            "pos": (self.getX(), self.getY()),
            "flagged": self.flagged(),
            "hidden": self.hidden(),
            "data": self.getItem()
        }

    def _test(self):
        self.__repr__();

    def __repr__(self):
        return f"MSGridItem(pos=({self.getX()}, {self.getY()}), flagged={self.flagged()}, hidden={self.hidden()}, data={self.getItem()})"

class MSGrid:
    def __init__(self, *inp):
        if len(inp) == 2:
            self.ptr = lib.MSGrid(*inp)
            self.allocated = True
        else:
            self.ptr = inp[0]
            self.allocated = False

    def __del__(self):
        if self.allocated:
            lib.DELETE(self.ptr)

    def set(self, x, y, value):
        lib.MSGrid_Set1(self.ptr, x, y, value.ptr)

    def fill(self, value):
        lib.MSGrid_Fill(self.ptr, value)

    def getHeight(self):
        return lib.MSGrid_GetHeight(self.ptr)

    def getWidth(self):
        return lib.MSGrid_GetWidth(self.ptr)

    def get(self, x, y):
        return MSGridItem(lib.MSGrid_Get(self.ptr, x, y))

    def pyObject(self):
        array = []
        for y in range(self.getHeight()):
            row = []
            for x in range(self.getWidth()):
                item = self.get(x, y)
                row.append(item.pyObject())
            array.append(row)
        return array

    def _test(self):
        self.__repr__();

    def __repr__(self):
        return f"MSGrid(grid={self.pyObject()})"

class MSEngine:
    def __init__(self, width, height, bombs):
        self.ptr = lib.MSEngine(width, height, bombs)

    def __del__(self):
        lib.DELETE(self.ptr)

    def _test(self):
        self.getGrid();
        self.getSurroundingBombs(1, 1)
        self.uncoverPoint(1, 3)
        print(f"Flags: {self.countFlags()}")
        self.flagPoint(3, 3)
        print(f"Flags: {self.countFlags()}")
        self.checkFlags()

    def getGrid(self):
        return MSGrid(lib.MSEngine_GetGrid(self.ptr))

    def uncoverPoint(self, x, y):
        return MSGridItem(lib.MSEngine_UncoverPoint(self.ptr, x, y))

    def getSurroundingBombs(self, x, y):
        return lib.MSEngine_GetSurroundingBombs(self.ptr, x, y)

    def countFlags(self):
        return lib.MSEngine_CountFlags(self.ptr)

    def checkFlags(self):
        return lib.MSEngine_CheckFlags(self.ptr)

    def flagPoint(self, x, y):
        lib.MSEngine_FlagPoint(self.ptr, x, y)
