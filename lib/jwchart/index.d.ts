/** Types for jwchart (lib/jwchart), which is plain JS so it can render anywhere. */

export interface Datum { label: string; value: number; color?: string; note?: string | null; }

export interface DonutOptions {
  data: Array<Datum | number>;
  /** viewBox width / height. Defaults 720 x 380. */
  size?: number;
  height?: number;
  /** Ring width as a fraction of the outer radius; 1 renders a filled pie. Default 0.34. */
  thickness?: number;
  /** Degrees of space between slices. Default 1.4. */
  gap?: number;
  /** Outer radius; derived from the box when omitted. */
  radius?: number;
  /** Leader-line labels around the ring. Default true. */
  labels?: boolean;
  /** Value list under the chart. Default true. */
  legend?: boolean;
  colors?: string[];
  unit?: string;
  decimals?: number;
  centerCaption?: string;
  /** Overrides the formatted total shown in the middle. */
  centerValue?: string | null;
  /** Translucent "glass" slices (default) or solid fills. */
  transparent?: boolean;
  /** Entrance animation. Set false for a chart re-rendered as its data changes. */
  animate?: boolean;
  title?: string;
  desc?: string;
  className?: string;
  /** Fixes the generated element ids; derived from the chart's content when omitted. */
  id?: string;
}

export function renderDonut(options: DonutOptions): string;
export function enhance(root?: ParentNode | Document | null): () => void;
export function mountDonut(target: string | Element, options: DonutOptions): () => void;

export const PALETTE: string[];
export function esc(v: unknown): string;
export function tag(name: string, attrs: Record<string, unknown> | null, children?: string): string;
export function num(v: number, dp?: number): string;
export function compact(v: number, dp?: number): string;
export function pct(v: number, total: number, dp?: number): string;
export function polar(cx: number, cy: number, r: number, turn: number): [number, number];
export function arcPath(cx: number, cy: number, innerR: number, outerR: number, from: number, to: number): string;
export function series(data: Array<Datum | number>, colors?: string[]): Required<Datum>[];
export function uid(prefix?: string, key?: unknown): string;
