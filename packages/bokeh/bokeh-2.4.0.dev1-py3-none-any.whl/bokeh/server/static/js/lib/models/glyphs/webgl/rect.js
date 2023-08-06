import { BaseGLGlyph } from "./base";
import { color_to_uint8_array, prop_as_array, hatch_pattern_prop_as_array, line_join_prop_as_array } from "./webgl_utils";
// Avoiding use of nan or inf to represent missing data in webgl as shaders may
// have reduced floating point precision.  So here using a large-ish negative
// value instead.
const missing_point = -10000;
export class RectGL extends BaseGLGlyph {
    constructor(regl_wrapper, glyph) {
        super(regl_wrapper, glyph);
        this.glyph = glyph;
        this._antialias = 1.5;
    }
    draw(indices, main_glyph, transform) {
        // The main glyph has the data, this glyph has the visuals.
        const mainGlGlyph = main_glyph.glglyph;
        if (mainGlGlyph.data_changed) {
            mainGlGlyph._set_data();
            mainGlGlyph.data_changed = false;
        }
        if (this.visuals_changed) {
            this._set_visuals();
            this.visuals_changed = false;
        }
        const nmarkers = mainGlGlyph._centers.length / 2;
        if (this._show == null)
            this._show = new Uint8Array(nmarkers);
        if (indices.length < nmarkers) {
            this._show_all = false;
            // Reset all show values to zero.
            for (let i = 0; i < nmarkers; i++)
                this._show[i] = 0;
            // Set show values of markers to render to 255.
            for (let j = 0; j < indices.length; j++) {
                this._show[indices[j]] = 255;
            }
        }
        else if (!this._show_all) {
            this._show_all = true;
            for (let i = 0; i < nmarkers; i++)
                this._show[i] = 255;
        }
        if (this._have_hatch) {
            const props = {
                scissor: this.regl_wrapper.scissor,
                viewport: this.regl_wrapper.viewport,
                canvas_size: [transform.width, transform.height],
                pixel_ratio: transform.pixel_ratio,
                center: mainGlGlyph._centers,
                width: mainGlGlyph._widths,
                height: mainGlGlyph._heights,
                angle: mainGlGlyph._angles,
                nmarkers,
                antialias: this._antialias,
                linewidth: this._linewidths,
                line_color: this._line_rgba,
                fill_color: this._fill_rgba,
                line_join: this._line_joins,
                show: this._show,
                hatch_pattern: this._hatch_patterns,
                hatch_scale: this._hatch_scales,
                hatch_weight: this._hatch_weights,
                hatch_color: this._hatch_rgba,
            };
            this.regl_wrapper.rect_hatch()(props);
        }
        else {
            const props = {
                scissor: this.regl_wrapper.scissor,
                viewport: this.regl_wrapper.viewport,
                canvas_size: [transform.width, transform.height],
                pixel_ratio: transform.pixel_ratio,
                center: mainGlGlyph._centers,
                width: mainGlGlyph._widths,
                height: mainGlGlyph._heights,
                angle: mainGlGlyph._angles,
                nmarkers,
                antialias: this._antialias,
                linewidth: this._linewidths,
                line_color: this._line_rgba,
                fill_color: this._fill_rgba,
                line_join: this._line_joins,
                show: this._show,
            };
            this.regl_wrapper.rect_no_hatch()(props);
        }
    }
    _set_data() {
        const nmarkers = this.glyph.sx.length;
        if (this._centers == null || this._centers.length != nmarkers * 2)
            this._centers = new Float32Array(nmarkers * 2);
        for (let i = 0; i < nmarkers; i++) {
            if (isFinite(this.glyph.sx[i]) && isFinite(this.glyph.sy[i])) {
                this._centers[2 * i] = this.glyph.sx[i];
                this._centers[2 * i + 1] = this.glyph.sy[i];
            }
            else {
                this._centers[2 * i] = missing_point;
                this._centers[2 * i + 1] = missing_point;
            }
        }
        this._widths = this.glyph.sw;
        this._heights = this.glyph.sh;
        this._angles = prop_as_array(this.glyph.angle);
    }
    _set_visuals() {
        const fill = this.glyph.visuals.fill;
        const line = this.glyph.visuals.line;
        this._linewidths = prop_as_array(line.line_width);
        this._line_joins = line_join_prop_as_array(line.line_join);
        // These create new Uint8Arrays each call.  Should reuse instead.
        this._line_rgba = color_to_uint8_array(line.line_color, line.line_alpha);
        this._fill_rgba = color_to_uint8_array(fill.fill_color, fill.fill_alpha);
        this._have_hatch = this.glyph.visuals.hatch.doit;
        if (this._have_hatch) {
            const hatch = this.glyph.visuals.hatch;
            this._hatch_patterns = hatch_pattern_prop_as_array(hatch.hatch_pattern);
            this._hatch_scales = prop_as_array(hatch.hatch_scale);
            this._hatch_weights = prop_as_array(hatch.hatch_weight);
            this._hatch_rgba = color_to_uint8_array(hatch.hatch_color, hatch.hatch_alpha);
        }
    }
}
RectGL.__name__ = "RectGL";
//# sourceMappingURL=rect.js.map