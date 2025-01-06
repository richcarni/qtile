from libqtile.rsvg_ffi import rsvg_ffi as ffi

librsvg = ffi.dlopen("librsvg-2.so.2")  # type: ignore

error = ffi.new("GError **")  # type: ignore


class RsvgHandle:
    def __init__(self, handle=ffi.NULL):
        self._handle = handle

    @classmethod
    def new_from_file(cls, file_name):
        file_name = file_name.encode("utf-8")

        handle = librsvg.rsvg_handle_new_from_file(file_name, error)

        if handle == ffi.NULL:
            error_message = ffi.string(error[0].message).decode("utf-8")
            raise Exception(f"{error_message}")

        return cls(handle)

    @classmethod
    def new_from_data(cls, data):
        handle = librsvg.rsvg_handle_new_from_data(data, len(data), error)

        if handle == ffi.NULL:
            error_message = ffi.string(error[0].message).decode("utf-8")
            raise Exception(f"{error_message}")

        return cls(handle)

    def render_document(self, context, viewport):
        ffi_context = ffi.cast("cairo_t*", context._pointer)
        ffi_viewport = ffi.new(
            "RsvgRectangle *",
            {
                "x": viewport[0],
                "y": viewport[1],
                "width": viewport[2],
                "height": viewport[3],
            },
        )

        ret = librsvg.rsvg_handle_render_document(self._handle, ffi_context, ffi_viewport, error)

        if not ret:
            error_message = ffi.string(error[0].message).decode("utf-8")
            raise Exception(f"{error_message}")
