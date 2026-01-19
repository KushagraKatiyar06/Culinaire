import { BASE_URL } from '../constants/Config';

export const ApiService = {
  getRecipe: async (url: string) => {
    const response = await fetch(`${BASE_URL}/get-recipe`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });
    
    if (!response.ok) throw new Error('Backend failed to generate recipe');
    return response.json(); 
  }
};