import {defineStore} from 'pinia';
import type {Recipe} from '@/types';
import { getAllRecipes } from '@/hooks/get-recipe';

export const useRecipeStore = defineStore('recipe', {
    state: () => ({
        recipeList: [] as Recipe[]
    }),
    getters: {
        getRecipes: (state) => state.recipeList,
    },
    actions: {
        async loadRecipes() {
            try {
                this.recipeList = [];
                const recipes = await getAllRecipes();
                if (recipes) {
                    for (const recipe of recipes) {
                        const newRecipe: Recipe = {
                            name: recipe[0],
                            ingredients: recipe[1].split(','),
                            steps: recipe[2].split('.'),
                            img: recipe[3]
                        };
                        this.recipeList.push(newRecipe);
                    }
                }
            } catch (error) {
                console.error("Failed to load recipes:", error);
            }
        }
    }
})