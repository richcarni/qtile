from cairocffi.ffi import ffi as cairocffi_ffi
from cffi import FFI

rsvg_ffi = FFI()

rsvg_ffi.include(cairocffi_ffi)

rsvg_ffi.cdef("""
    typedef struct _cairo cairo_t;
    typedef struct _RsvgHandle RsvgHandle;
    typedef int gboolean;  // gboolean is usually defined as int in C
    typedef struct {
      int domain;
      int code;
      char *message;
    } GError;

    typedef struct {
        double x, y, width, height;
    } RsvgRectangle;
    RsvgHandle* rsvg_handle_new_from_file(const char* filename, void* error);
    RsvgHandle* rsvg_handle_new_from_data(const char* data, unsigned long data_len, GError **error);

    gboolean rsvg_handle_render_document(RsvgHandle *handle, cairo_t *cr, const RsvgRectangle *viewport, GError **error);
    """)
