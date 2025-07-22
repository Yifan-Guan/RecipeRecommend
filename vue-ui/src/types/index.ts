
export interface ChatMessage {
  role: string
  content: string
}

export interface ChatHistory {
  id: string
  title: string
  messages: ChatMessage[]
}

export interface User {
  id: string
  name: string
  password: string
}