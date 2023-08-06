import { BaseGLGlyph, Transform } from "./base";
import { ReglWrapper } from "./regl_wrap";
import { RectView } from "../rect";
export declare class RectGL extends BaseGLGlyph {
    readonly glyph: RectView;
    protected _antialias: number;
    protected _centers: Float32Array;
    protected _widths: Float32Array;
    protected _heights: Float32Array;
    protected _angles: number[] | Float32Array;
    protected _linewidths: number[] | Float32Array;
    protected _line_rgba: Uint8Array;
    protected _fill_rgba: Uint8Array;
    protected _line_joins: number[] | Float32Array;
    protected _show: Uint8Array;
    protected _show_all: boolean;
    protected _have_hatch: boolean;
    protected _hatch_patterns?: number[] | Float32Array;
    protected _hatch_scales?: number[] | Float32Array;
    protected _hatch_weights?: number[] | Float32Array;
    protected _hatch_rgba?: Uint8Array;
    constructor(regl_wrapper: ReglWrapper, glyph: RectView);
    draw(indices: number[], main_glyph: RectView, transform: Transform): void;
    protected _set_data(): void;
    protected _set_visuals(): void;
}
//# sourceMappingURL=rect.d.ts.map