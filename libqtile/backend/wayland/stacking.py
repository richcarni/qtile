from libqtile.backend.base.stacking import LayerGroup, _StackingManager
from libqtile.log_utils import logger

try:
    from libqtile.backend.wayland._ffi import ffi, lib

except ModuleNotFoundError:
    print("Warning: Wayland backend not built. Backend will not run.")

    from libqtile.backend.wayland.ffi_stub import lib

_LAYER_TO_WLR: dict[LayerGroup, int] = {
    LayerGroup.BACKGROUND: lib.LAYER_BACKGROUND,
    LayerGroup.BOTTOM: lib.LAYER_BOTTOM,
    LayerGroup.KEEP_BELOW: lib.LAYER_KEEPBELOW,
    LayerGroup.INTERNAL: lib.LAYER_LAYOUT,  # Add internal layer?
    LayerGroup.LAYOUT: lib.LAYER_LAYOUT,
    LayerGroup.KEEP_ABOVE: lib.LAYER_KEEPABOVE,
    LayerGroup.MAX: lib.LAYER_MAX,
    LayerGroup.FULLSCREEN: lib.LAYER_FULLSCREEN,
    LayerGroup.BRING_TO_FRONT: lib.LAYER_BRINGTOFRONT,
    LayerGroup.TOP: lib.LAYER_TOP,
    LayerGroup.OVERLAY: lib.LAYER_OVERLAY,
    LayerGroup.SYSTEM: lib.LAYER_LOCK,  # ??
}


def wlr_layer(group: LayerGroup) -> int:
    return _LAYER_TO_WLR[group]


class WaylandStackingManager(_StackingManager):
    def stack_all(self):
        pass

    def add_window(
        self,
        window: WindowType,
        layer: LayerGroup | None = None,
        position="top",
    ) -> None:

        if layer is None:
            layer = wlr_layer(window.get_layering_information())

        # if layer not in self.layers:
        #     raise ValueError(f"Invalid layer: {layer}")

        parent = window.is_transient_for()

        if parent: # and transient in self.layer_map:
            # parent_node = self.layer_map[parent]

            layer = parent.layer()

            window.transient_parent = parent
            parent.transient_children.append(window)

            # Child must be in parent's layer
            window.reparent(layer)
            window.move_above(parent)

        else:
            if position == "bottom":
                window.reparent(layer)
                window.move_to_bottom()

            else:
                window.reparent(layer)

    def repair_transient_order(self, parent):
        for child in parent.transient_children:
            # Parent and child must share a layer
            child.reparent(parent.layer())
            #TODO: implement grouped_siblings or only move_above if child and
            # parent are in same group?
            child.move_above(parent)

            self.repair_transient_order(child)

    def repair_transients(self):
        for window in self.qtile.windows_map.values():
            if window.transient_parent is None:
                self.repair_transient_order(window)

