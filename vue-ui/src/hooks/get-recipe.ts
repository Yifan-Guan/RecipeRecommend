export async function getAllRecipes() {
    const response = await fetch('http://localhost:8000/recipes/get_all', {
        method: 'GET',
        headers: {
            'accept': 'application/json'
        }
    });
    if (!response.ok) {
        throw new Error('Failed to fetch recipes');
    }
    const data = await response.json();
    return data;
}