import { LineJoin } from "../../../core/enums";
import { Uniform } from "../../../core/uniforms";
import { uint32 } from "../../../core/types";
import { HatchPattern } from "../../../core/property_mixins";
export declare const cap_lookup: {
    butt: number;
    round: number;
    square: number;
};
export declare const join_lookup: {
    miter: number;
    round: number;
    bevel: number;
};
export declare function color_to_uint8_array(color_prop: Uniform<uint32>, alpha_prop: Uniform<number>): Uint8Array;
export declare function prop_as_array(prop: Uniform<number>): number[] | Float32Array;
export declare function hatch_pattern_prop_as_array(prop: Uniform<HatchPattern>): number[] | Float32Array;
export declare function line_join_prop_as_array(prop: Uniform<LineJoin>): number[] | Float32Array;
//# sourceMappingURL=webgl_utils.d.ts.map