import { type ChatHistoryContent, type ChatHistoryInfo} from "@/types"

export async function fetchChatHistoryInfo() {
    const response = await fetch('http://localhost:8000/history/get_all_info', {
        method: 'GET',
        headers: {
            'accept': 'application/json'
        }
    });
    if (!response.ok) {
        throw new Error('Failed to fetch chat history info');
    }
    const data = await response.json();
    return data;
}

export async function fetchChatHistoryContentById(id: string) {
    const response = await fetch(`http://localhost:8000/history/get_content/${id}`, {
        method: 'GET',
        headers: {
            'accept': 'application/json'
        },
    });
    if (!response.ok) {
        throw new Error('Failed to fetch chat history content');
    }
    const data = await response.json();
    return data;
}

export async function addChatHistoryInfo(info: ChatHistoryInfo) {
    const response = await fetch('http://localhost:8000/history/add_info', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            history_id: info.id,
            history_name: info.title,
            user_id: info.userId
        })
    });
    if (!response.ok) {
        throw new Error('Failed to add chat history info');
    }
    const data = await response.json();
    return data;
}

export async function addChatHistoryContent(content: ChatHistoryContent) {
    const response = await fetch('http://localhost:8000/history/add_content', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: content.id,
            index: content.index,
            role: content.role,
            content: content.content
        })
    });
    if (!response.ok) {
        throw new Error('Failed to add chat history content');
    }
    const data = await response.json();
    return data;
}

export async function deleteChatHistoryInfo(id: string) {
    const response = await fetch(`http://localhost:8000/history/delete/${id}`, {
        method: 'DELETE',
        headers: {
            'accept': 'application/json'
        }
    });
    if (!response.ok) {
        throw new Error('Failed to delete chat history info');
    }
    const data = await response.json();
    return data;
}

export async function updateChatHistoryNameById(id: string, newName: string) {
    const response = await fetch(`http://localhost:8000/history/update_name/${id}`, {
        method: 'PUT',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ new_name: newName })
    });
    if (!response.ok) {
        throw new Error('Failed to update chat history name');
    }
    const data = await response.json();
    return data;
}