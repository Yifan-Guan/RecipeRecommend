import { type User } from "@/types";

export async function getAllUsers() {
  const response = await fetch('http://localhost:8000/users/get_all', {
    method: 'GET',
  });
  if (!response.ok) {
    throw new Error('Failed to fetch users');
  }
  const data = await response.json();
  return data;
}

export async function addUser(user: User) {
  const response = await fetch('http://localhost:8000/users/add_user', {
    method: 'POST',
    headers: {
      accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: user.id,
      user_name: user.name,
      user_password: user.password
    }),
  });
  if (!response.ok) {
    throw new Error('Failed to add user');
  }
  const data = await response.json();
  return data;
}