<template>
    <div id="app">
        <h1>Recipe Manager</h1>
        
        <!-- Tabs -->
        <ul class="nav nav-tabs mb-4">
            <li class="nav-item">
                <a class="nav-link" 
                   :class="{ active: activeTab === 'recipes' }"
                   @click.prevent="activeTab = 'recipes'" 
                   href="#">Recipes</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" 
                   :class="{ active: activeTab === 'ingredients' }"
                   @click.prevent="activeTab = 'ingredients'" 
                   href="#">Ingredients</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" 
                   :class="{ active: activeTab === 'recipeIngredients' }"
                   @click.prevent="activeTab = 'recipeIngredients'" 
                   href="#">Recipe Ingredients</a>
            </li>
        </ul>

        <!-- Tab Content -->
        <div v-if="activeTab === 'recipes'">
            <Recipes @recipes-updated="fetchRecipes" />
        </div>
        <div v-if="activeTab === 'ingredients'">
            <Ingredients />
        </div>
        <div v-if="activeTab === 'recipeIngredients'">
            <RecipeIngredients :recipes="recipes" ref="recipeIngredients" />
        </div>
    </div>
</template>

<script>
import Recipes from './components/Recipes.vue'
import Ingredients from './components/Ingredients.vue'
import RecipeIngredients from './components/RecipeIngredients.vue'

export default {
    name: 'App',
    components: {
        Recipes,
        Ingredients,
        RecipeIngredients
    },
    data() {
        return {
            activeTab: 'recipes',
            recipes: []
        }
    },
    methods: {
        async fetchRecipes() {
            try {
                const response = await fetch('http://localhost:8000/api/recipes/')
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`)
                }
                this.recipes = await response.json()
            } catch (error) {
                console.error('Error fetching recipes:', error)
            }
        }
    },
    mounted() {
        this.fetchRecipes()
    }
}
</script>

<style scoped>
.container {
    max-width: 900px;
}
</style>