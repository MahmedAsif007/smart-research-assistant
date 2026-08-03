export interface ChatResponse {
  answer: string;
  rag_used: boolean;
  csv_used: boolean;
}