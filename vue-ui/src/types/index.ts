
export interface ChatMessage {
  id: string
  role: string
  content: string
}

export interface ChatHistory {
  id: string
  title: string
  messages: ChatMessage[]
}

export interface ChatHistoryInfo {
  id: string
  title: string
  userId: string
}

export interface ChatHistoryContent {
  id: string
  index: number 
  role: string
  content: string
}

export interface User {
  id: string
  name: string
  password: string
}