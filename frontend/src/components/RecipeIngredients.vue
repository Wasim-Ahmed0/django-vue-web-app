<template>
  <div>
    <h2>Recipe Ingredients</h2>
    
    <!-- Recipe selector -->
    <div class="mb-3">
      <label class="form-label">Select Recipe:</label>
      <select class="form-select" v-model="selectedRecipeId" @change="fetchRecipeIngredients">
        <option value="">Choose a recipe...</option>
        <option v-for="recipe in recipes" :key="recipe.id" :value="recipe.id">
          {{ recipe.title }}
        </option>
      </select>
    </div>

    <div v-if="selectedRecipeId">
      <button class="btn btn-primary mb-3" data-bs-toggle="modal" data-bs-target="#addRecipeIngredientModal">
        Add Ingredient to Recipe
      </button>

      <table class="table table-striped">
        <thead>
          <tr>
            <th>Ingredient</th>
            <th>Quantity</th>
            <th>Unit</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ingredient in recipeIngredients" :key="ingredient.id">
            <td>{{ ingredient.ingredient__name }}</td>
            <td>{{ ingredient.quantity }}</td>
            <td>{{ ingredient.unit }}</td>
            <td>
              <button class="btn btn-sm btn-primary me-2" @click="openEditModal(ingredient)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="openDeleteModal(ingredient)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Add Modal -->
      <div class="modal fade" id="addRecipeIngredientModal" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add Ingredient to Recipe</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <select class="form-select" v-model="newRecipeIngredient.ingredient_name">
                  <option value="">Choose an ingredient...</option>
                  <option v-for="ingredient in availableIngredients" 
                          :key="ingredient.id" 
                          :value="ingredient.name">
                    {{ ingredient.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <input class="form-control" v-model.number="newRecipeIngredient.quantity" type="number" placeholder="Quantity">
              </div>
              <div class="mb-3">
                <input class="form-control" v-model="newRecipeIngredient.unit" placeholder="Unit">
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
              <button type="button" class="btn btn-primary" @click="addIngredientToRecipe">Save</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Edit Modal -->
      <div class="modal fade" id="editRecipeIngredientModal" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Edit Recipe Ingredient</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body" v-if="editingIngredient">
              <div class="mb-3">
                <input class="form-control" :value="editingIngredient.ingredient__name" disabled>
              </div>
              <div class="mb-3">
                <input class="form-control" v-model.number="editingIngredient.quantity" type="number" placeholder="Quantity">
              </div>
              <div class="mb-3">
                <input class="form-control" v-model="editingIngredient.unit" placeholder="Unit">
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
              <button type="button" class="btn btn-primary" @click="updateRecipeIngredient">Save</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Delete Modal -->
      <div class="modal fade" id="deleteRecipeIngredientModal" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Delete Recipe Ingredient</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              Are you sure you want to remove this ingredient from the recipe?
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
              <button type="button" class="btn btn-danger" @click="confirmDelete">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap'

export default {
  name: 'RecipeIngredients',
  props: {
    recipes: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      selectedRecipeId: '',
      recipeIngredients: [],
      editingIngredient: null,
      deleteIngredientId: null,
      availableIngredients: [],
      newRecipeIngredient: {
        ingredient_name: '',
        quantity: null,
        unit: ''
      }
    }
  },
  mounted() {
    this.fetchAvailableIngredients()
  },
  methods: {
    async fetchRecipeIngredients() {
      if (!this.selectedRecipeId) return;
      
      try {
        const response = await fetch(`http://localhost:8000/api/recipes/${this.selectedRecipeId}/ingredients/`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        this.recipeIngredients = data;
      } catch (error) {
        console.error('Error fetching recipe ingredients:', error);
      }
    },

    editRecipeIngredient(ingredient) {
      this.editingIngredient = { ...ingredient }
    },

    async updateRecipeIngredient() {
      try {
        const response = await fetch(`http://localhost:8000/api/recipes/${this.selectedRecipeId}/ingredients/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            ingredients: this.recipeIngredients.map(ing => ({
              name: ing.ingredient__name,
              quantity: ing.ingredient__name === this.editingIngredient.ingredient__name 
                ? this.editingIngredient.quantity 
                : ing.quantity,
              unit: ing.ingredient__name === this.editingIngredient.ingredient__name 
                ? this.editingIngredient.unit 
                : ing.unit
            }))
          })
        })

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
        
        await this.fetchRecipeIngredients()
        
        // Close modal and reset form
        const modal = Modal.getInstance(document.getElementById('editRecipeIngredientModal'))
        modal.hide()
        this.editingIngredient = null
      } catch (error) {
        console.error('Error updating recipe ingredient:', error)
      }
    },

    async addIngredientToRecipe() {
      if (!this.newRecipeIngredient.ingredient_name) {
        alert('Please select an ingredient')
        return
      }

      try {
        const response = await fetch(`http://localhost:8000/api/recipes/${this.selectedRecipeId}/ingredients/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            ingredients: [
              ...this.recipeIngredients.map(ing => ({
                name: ing.ingredient__name,
                quantity: ing.quantity,
                unit: ing.unit
              })),
              {
                name: this.newRecipeIngredient.ingredient_name,
                quantity: this.newRecipeIngredient.quantity,
                unit: this.newRecipeIngredient.unit
              }
            ]
          })
        })

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)

        await this.fetchRecipeIngredients()
        
        // Close modal and reset form
        const modal = Modal.getInstance(document.getElementById('addRecipeIngredientModal'))
        modal.hide()
        this.newRecipeIngredient = {
          ingredient_name: '',
          quantity: null,
          unit: ''
        }
      } catch (error) {
        console.error('Error adding ingredient to recipe:', error)
      }
    },

    async fetchAvailableIngredients() {
      try {
        const response = await fetch('http://localhost:8000/api/ingredients/')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        this.availableIngredients = await response.json()
      } catch (error) {
        console.error('Error fetching available ingredients:', error)
      }
    },

    openEditModal(ingredient) {
      this.editingIngredient = { ...ingredient }
      const modal = new Modal(document.getElementById('editRecipeIngredientModal'))
      modal.show()
    },

    openDeleteModal(ingredient) {
      const ingredientId = this.availableIngredients.find(
        i => i.name === ingredient.ingredient__name
      )?.id;
      
      this.deleteIngredientId = ingredientId;
      
      const modal = new Modal(document.getElementById('deleteRecipeIngredientModal'));
      modal.show();
    },

    async confirmDelete() {
      if (this.selectedRecipeId) {
        try {
          const response = await fetch(`http://localhost:8000/api/recipes/${this.selectedRecipeId}/ingredients/`, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              ingredient_name: this.recipeIngredients.find(
                ing => this.availableIngredients.find(
                  ai => ai.id === this.deleteIngredientId
                )?.name === ing.ingredient__name
              )?.ingredient__name
            })
          });

          if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
          
          await this.fetchRecipeIngredients();
          
          // Close modal
          const modal = Modal.getInstance(document.getElementById('deleteRecipeIngredientModal'));
          modal.hide();
          this.deleteIngredientId = null;
        } catch (error) {
          console.error('Error deleting recipe ingredient:', error);
        }
      }
    }
  }
}
</script>
