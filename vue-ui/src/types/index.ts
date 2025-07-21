
export interface ChatMessage {
  role: string
  content: string
}

export interface ChatHistory {
  id: string
  title: string
  messages: ChatMessage[]
}