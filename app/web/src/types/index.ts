export interface ThemeMeta {
  fonts: {
    title: string;
    body: string;
  };
  colors: Record<string, string>;
  page_size: {
    w: number;
    h: number;
  };
}

export interface LayoutInfo {
  layout_id: string;
  name: string;
  placeholders: {
    title?: boolean;
    bodies: number;
    pictures: number;
    table?: boolean;
  };
  bbox?: any;
}

export interface TemplateData {
  template_id: string;
  theme_meta: ThemeMeta;
  layout_catalog: LayoutInfo[];
}

export interface PageSignature {
  title: boolean;
  bullets: number;
  columns: number;
  images: number;
  table: boolean;
  coverage: {
    image: number;
    text: number;
  };
}

export interface PageInfo {
  idx: number;
  signature: PageSignature;
  warnings: string[];
}

export interface SourceData {
  source_id: string;
  type: 'pptx' | 'pdf';
  pages: PageInfo[];
}

export interface SlideMapping {
  idx: number;
  chosen_layout_id: string;
  score: number;
  issues: string[];
}

export interface PlanData {
  plan_id: string;
  slides: SlideMapping[];
}

export interface JobStatus {
  status: 'queued' | 'running' | 'done' | 'error';
  artifact_url?: string;
  preview_pngs?: string[];
  report?: {
    greens: number;
    yellows: number;
    issues_by_type: Record<string, number>;
  };
}