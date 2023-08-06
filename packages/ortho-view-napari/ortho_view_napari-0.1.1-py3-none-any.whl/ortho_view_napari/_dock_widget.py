
import napari
from napari.layers.utils._link_layers import link_layers, unlink_layers
from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QVBoxLayout
from magicgui.widgets import Checkbox
from typing import List, Optional


class Widget(QWidget):
    def __init__(self, viewer: napari.Viewer):
        super().__init__()
        assert viewer.dims.ndim == 3 or viewer.dims.ndim == 4

        self.shapes_args = dict(shape_type='line', ndim=3, edge_color='red')
        self.dummy_line = [[0, 0, 0], [0, 0, 0]]

        self.z_viewer = viewer
        self.z_viewer.add_shapes(self.dummy_line, name='slicing', **self.shapes_args)
        self.z_viewer.dims.events.current_step.connect(self.update_all)
        self._register_time_point_signal(self.z_viewer)

        self.x_viewer: Optional[napari.Viewer] = None
        self.y_viewer: Optional[napari.Viewer] = None

        self.setLayout(QVBoxLayout())
        self.x_checkbox = Checkbox(text='Side Ortho View')
        self.y_checkbox = Checkbox(text='Bottom Ortho View')
        self.x_checkbox.changed.connect(self.x_changed)
        self.y_checkbox.changed.connect(self.y_changed)
        self.layout().addWidget(self.x_checkbox.native)
        self.layout().addWidget(self.y_checkbox.native)

    def x_changed(self, event) -> None:
        if self.x_checkbox.value:
            self.init_x_viewer()
        else:
            self.delete_viewer(self.x_viewer)
            self.x_viewer = None

    def y_changed(self, event) -> None:
        if self.y_checkbox.value:
            self.init_y_viewer()
        else:
            self.delete_viewer(self.y_viewer)
            self.y_viewer = None

    @staticmethod
    def delete_viewer(viewer: napari.Viewer) -> None:
        for layer in viewer.layers:
            unlink_layers([layer])
        viewer.dims.events.current_step.disconnect()
        viewer.close()

    def add_layers(self, viewer: napari.Viewer) -> None:
        for layer in self.z_viewer.layers:
            data = layer.as_layer_data_tuple()
            if data[1]['name'] != 'slicing':
                new_layer = viewer._add_layer_from_data(*data)[0]
                link_layers([layer, new_layer])

    def init_x_viewer(self) -> None:
        self.x_viewer = napari.Viewer(title='ortho-view-napari | side')
        self.add_layers(self.x_viewer)

        self.x_viewer.dims._roll()
        self.x_viewer.dims._transpose()

        self.x_viewer.add_shapes(self.dummy_line, name='slicing', **self.shapes_args)
        self.x_viewer.dims.events.current_step.connect(self.update_all)
        self.update_all()
        self._register_time_point_signal(self.x_viewer)

    def init_y_viewer(self) -> None:
        self.y_viewer = napari.Viewer(title='ortho-view-napari | bottom')
        self.add_layers(self.y_viewer)

        self.y_viewer.dims._roll()
        self.y_viewer.dims._roll()
        self.y_viewer.dims._transpose()

        self.y_viewer.add_shapes(self.dummy_line, name='slicing', **self.shapes_args)
        self.y_viewer.dims.events.current_step.connect(self.update_all)
        self.update_all()
        self._register_time_point_signal(self.y_viewer)

    def _register_time_point_signal(self, viewer: napari.Viewer) -> None:
        if viewer.dims.ndim != 4:
            return
        slider = viewer.window.qt_viewer.dims.slider_widgets[0].slider
        slider.valueChanged.connect(self.update_time_point)

    def update_time_point(self, time_point: int) -> None:
        self.z_viewer.dims.set_current_step(0, time_point)
        if self.x_viewer is not None:
            self.x_viewer.dims.set_current_step(0, time_point)
        if self.y_viewer is not None:
            self.y_viewer.dims.set_current_step(0, time_point)

    def update_all(self, event=None) -> None:
        if not (self.x_viewer is None and self.y_viewer is None):
            self.update_z()
        if self.y_viewer is not None:
            self.update_y()
        if self.x_viewer is not None:
            self.update_x()

    def update_z(self) -> None:
        lines = []
        if self.y_viewer is not None:
            lines.append(self.get_x_line())
        if self.x_viewer is not None:
            lines.append(self.get_y_line())
        self.z_viewer.layers['slicing'].data = lines

    def update_x(self) -> None:
        lines = [self.get_y_line()]
        if self.y_viewer is not None:
            lines.append(self.get_z_line())
        self.x_viewer.layers['slicing'].data = lines

    def update_y(self) -> None:
        lines = [self.get_x_line()]
        if self.x_viewer is not None:
            lines.append(self.get_z_line())
        self.y_viewer.layers['slicing'].data = lines

    def get_x_line(self) -> List[List[int]]:
        z_dims = self.z_viewer.dims
        y_dims = self.y_viewer.dims
        line = [
            [z_dims.current_step[-3], y_dims.current_step[-2], z_dims.range[-1][0]],
            [z_dims.current_step[-3], y_dims.current_step[-2], z_dims.range[-1][1]],
        ]
        return line

    def get_y_line(self) -> List[List[int]]:
        z_dims = self.z_viewer.dims
        x_dims = self.x_viewer.dims
        line = [
            [z_dims.current_step[-3], z_dims.range[-2][0], x_dims.current_step[-1]],
            [z_dims.current_step[-3], z_dims.range[-2][1], x_dims.current_step[-1]],
        ]
        return line

    def get_z_line(self) -> List[List[int]]:
        y_dims = self.y_viewer.dims
        x_dims = self.x_viewer.dims
        line = [
            [y_dims.range[-3][0], y_dims.current_step[-2], x_dims.current_step[-1]],
            [y_dims.range[-3][1], y_dims.current_step[-2], x_dims.current_step[-1]],
        ]
        return line


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return Widget, dict(name='Ortho View')
