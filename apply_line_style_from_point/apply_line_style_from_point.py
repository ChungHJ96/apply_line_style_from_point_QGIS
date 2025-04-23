from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.PyQt.QtGui import QIcon
from qgis.core import (
    QgsProject,
    QgsCategorizedSymbolRenderer,
    QgsRendererCategory,
    QgsSymbol,
    QgsVectorLayer
)

from .apply_line_style_dialog import ApplyLineStyleDialog

class ApplyLineStylePlugin:
    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):
        self.action = QAction(QIcon(), "Apply Line Style from Point", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("&Apply Line Style", self.action)

    def unload(self):
        self.iface.removePluginMenu("&Apply Line Style", self.action)

    def run(self):
        # 현재 프로젝트의 벡터 레이어 이름 목록
        point_layer_names = [
            layer.name() for layer in QgsProject.instance().mapLayers().values()
            if isinstance(layer, QgsVectorLayer) and layer.geometryType() == 0  # 0 = Point
        ]

        if not point_layer_names:
            QMessageBox.warning(None, "오류", "포인트 레이어가 없습니다.")
            return

        dialog = ApplyLineStyleDialog(point_layer_names)
        if not dialog.exec_():
            return

        point_layer_name = dialog.selected_layer_name()
        field_name = 'IID'
        line_layer = self.iface.activeLayer()

        point_layer = QgsProject.instance().mapLayersByName(point_layer_name)[0]
        renderer = point_layer.renderer()
        if not isinstance(renderer, QgsCategorizedSymbolRenderer):
            QMessageBox.warning(None, "오류", "포인트 레이어는 반드시 '범주화(Categorized)' 스타일이어야 합니다.")
            return

        color_map = {}
        for category in renderer.categories():
            iid = category.value()
            color = category.symbol().color()
            color_map[iid] = color

        categories = []
        for iid, color in color_map.items():
            symbol = QgsSymbol.defaultSymbol(line_layer.geometryType())
            symbol.setColor(color)
            category = QgsRendererCategory(iid, symbol, str(iid))
            categories.append(category)

        new_renderer = QgsCategorizedSymbolRenderer(field_name, categories)
        line_layer.setRenderer(new_renderer)
        line_layer.triggerRepaint()

        QMessageBox.information(None, "성공", "선 레이어에 스타일이 적용되었습니다.")
