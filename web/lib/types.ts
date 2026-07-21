// Mirrors the backend Pydantic models (adr_advisor.models).

export interface OptionAnalysis {
  option: string;
  pros: string[];
  cons: string[];
  notable_for: string;
}

export interface TradeOff {
  axis: string;
  favoured_option: string;
  note: string;
}

export interface Recommendation {
  option: string;
  rationale: string;
  key_risks: string[];
  revisit_when: string;
}

export interface Advice {
  context_summary: string;
  option_analyses: OptionAnalysis[];
  trade_offs: TradeOff[];
  recommendation: Recommendation;
}

export interface AdrResult {
  decision: string;
  options: string[];
  advice: Advice;
  recommendation_valid: boolean;
}

export interface ExampleResponse {
  decision: string;
  options: string[];
}
