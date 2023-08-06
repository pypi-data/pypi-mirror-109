export class BaseGLGlyph {
    constructor(regl_wrapper, glyph) {
        this.glyph = glyph;
        this.nvertices = 0;
        this.size_changed = false;
        this.data_changed = false;
        this.visuals_changed = false;
        this.regl_wrapper = regl_wrapper;
    }
    set_data_changed() {
        const { data_size } = this.glyph;
        if (data_size != this.nvertices) {
            this.nvertices = data_size;
            this.size_changed = true;
        }
        this.data_changed = true;
    }
    set_visuals_changed() {
        this.visuals_changed = true;
    }
    render(_ctx, indices, mainglyph) {
        if (indices.length == 0) {
            return true;
        }
        const { width, height } = this.glyph.renderer.plot_view.canvas_view.webgl.canvas;
        const trans = {
            pixel_ratio: this.glyph.renderer.plot_view.canvas_view.pixel_ratio,
            width,
            height,
        };
        this.draw(indices, mainglyph, trans);
        return true;
    }
    // Return array from FloatBuffer, creating it if necessary.
    get_buffer_array(float_buffer, length) {
        if (float_buffer == null || float_buffer.array.length != length)
            return new Float32Array(length);
        else
            return float_buffer.array;
    }
    // Update FloatBuffer with data contained in array.
    update_buffer(float_buffer, array) {
        if (float_buffer == null) {
            // Create new buffer.
            float_buffer = {
                array,
                buffer: this.regl_wrapper.buffer({
                    usage: "dynamic",
                    type: "float",
                    data: array,
                }),
            };
        }
        else {
            // Reuse existing buffer.
            float_buffer.array = array;
            float_buffer.buffer({ data: array });
        }
        return float_buffer;
    }
}
BaseGLGlyph.__name__ = "BaseGLGlyph";
//# sourceMappingURL=base.js.map