# import unittest

"""
class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()

"""
"""

from saruca_uuv.comprehend_system_layer.Classes import VehicleComprehendLayer
from saruca_uuv.comprehend_system_layer.Methods import localization
from saruca_uuv.comprehend_system_layer.Methods import state
from saruca_uuv.control_system_layer.Classes import ControlLayer
from saruca_uuv.control_system_layer.Methods import assignment
from saruca_uuv.control_system_layer.Methods import behaviour
from saruca_uuv.control_system_layer.Methods import command
from saruca_uuv.control_system_layer.Methods import engineBreakdown
from saruca_uuv.control_system_layer.Methods import orbit
from saruca_uuv.sensing_system_layer.Classes import EntityLayer
from saruca_uuv.sensing_system_layer.Methods import imageProcessing
from saruca_uuv.sensing_system_layer.Methods import variables

import saruca_uuv.sensing_system_layer.Methods.variables
import saruca_uuv.sensing_system_layer.Methods.imageProcessing
import saruca_uuv.sensing_system_layer.Classes.EntityLayer
import saruca_uuv.control_system_layer.Methods.orbit
import saruca_uuv.control_system_layer.Methods.engineBreakdown
import saruca_uuv.control_system_layer.Methods.command
import saruca_uuv.control_system_layer.Methods.behaviour
import saruca_uuv.control_system_layer.Methods.assignment
import saruca_uuv.control_system_layer.Classes.ControlLayer
import saruca_uuv.comprehend_system_layer.Methods.state
import saruca_uuv.comprehend_system_layer.Methods.localization
import saruca_uuv.comprehend_system_layer.Classes.VehicleComprehendLayer
"""



# imageObject = EntityLayer((25, 15), "rectangle", 12, "trapezium")
# print(imageObject.getBoundingBoxes())
print("Motor ariza kontrol metodu calistirildi.")
print("Goruntu isleme metodu calistirildi...")
print("Konumlandirma metodu calistirildi.variableObject.getOtherVariables() + variableObject.getPositionVector()")
x = 221
y = 128
otherVar = ["circle", 24]
# variableObject = EntityLayer((0, 0), otherVar, 0, "", (x, y))
# print(variableObject.getOtherVariables() + variableObject.getPositionVector())

print("Durum metodu calistirildi.")
print("Degiskenler metodu calistirildi.")
print("Komut metodu calistirildi...")
print("rota belirleniyor...")
print("rota belirleniyor...")
print("rota belirleniyor...")
print("rota belirleniyor..." + "Yorunge belirlendi.")
print("imageObject = EntityLayer((25, 15), \"rectangle\", 12, \"trapezium\")")
