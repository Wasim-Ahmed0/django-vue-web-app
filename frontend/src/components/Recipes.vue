<template>
  <div>
    <h2>Recipes</h2>
    
    <button class="btn btn-primary mb-3" data-bs-toggle="modal" data-bs-target="#addRecipeModal">
      Add New Recipe
    </button>

    <!-- Recipes table -->
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Title</th>
          <th>Description</th>
          <th>Servings</th>
          <th>Date Added</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="recipe in recipes" :key="recipe.id">
          <td>{{ recipe.title }}</td>
          <td>{{ recipe.description }}</td>
          <td>{{ recipe.servings }}</td>
          <td>{{ formatDate(recipe.date_added) }}</td>
          <td>
            <button class="btn btn-sm btn-primary me-2" @click="openEditModal(recipe)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="openDeleteModal(recipe)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Add Modal -->
    <div class="modal fade" id="addRecipeModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add New Recipe</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <input class="form-control" v-model="newRecipe.title" placeholder="Recipe title">
            </div>
            <div class="mb-3">
              <input class="form-control" v-model="newRecipe.description" placeholder="Description">
            </div>
            <div class="mb-3">
              <input class="form-control" v-model.number="newRecipe.servings" type="number" placeholder="Servings">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="createRecipe">Save</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div class="modal fade" id="editRecipeModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Recipe</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="editingRecipe">
            <div class="mb-3">
              <input class="form-control" v-model="editingRecipe.title" placeholder="Recipe title">
            </div>
            <div class="mb-3">
              <input class="form-control" v-model="editingRecipe.description" placeholder="Description">
            </div>
            <div class="mb-3">
              <input class="form-control" v-model.number="editingRecipe.servings" type="number" placeholder="Servings">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="updateRecipe">Save</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Modal -->
    <div class="modal fade" id="deleteRecipeModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Delete Recipe</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            Are you sure you want to delete this recipe?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="confirmDelete">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap'

export default {
  name: 'Recipes',
  data() {
    return {
      recipes: [],
      editingRecipe: null,
      deleteRecipeId: null,
      newRecipe: {
        title: '',
        description: '',
        servings: null
      }
    }
  },
  mounted() {
    this.fetchRecipes()
  },
  methods: {
    async fetchRecipes() {
      try {
        const response = await fetch('http://localhost:8000/api/recipes/')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        this.recipes = data
      } catch (error) {
        console.error('Error fetching recipes:', error)
      }
    },

    openEditModal(recipe) {
      this.editingRecipe = { ...recipe }
      const modal = new Modal(document.getElementById('editRecipeModal'))
      modal.show()
    },
    openDeleteModal(recipe) {
      this.deleteRecipeId = recipe.id
      const modal = new Modal(document.getElementById('deleteRecipeModal'))
      modal.show()
    },
    async confirmDelete() {
      if (this.deleteRecipeId) {
        await this.deleteRecipe(this.deleteRecipeId)
        const modal = Modal.getInstance(document.getElementById('deleteRecipeModal'))
        modal.hide()
      }
    },

    async updateRecipe() {
      try {
        const response = await fetch(`http://localhost:8000/api/recipes/${this.editingRecipe.id}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: this.editingRecipe.title,
            description: this.editingRecipe.description,
            servings: this.editingRecipe.servings
          })
        })

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
        
        const updatedRecipe = await response.json()
        const index = this.recipes.findIndex(r => r.id === this.editingRecipe.id)
        if (index !== -1) {
          this.recipes[index] = updatedRecipe
          this.$emit('recipes-updated')
        }
        
        // Close modal and reset form
        const modal = Modal.getInstance(document.getElementById('editRecipeModal'))
        if (modal) {
          modal.hide()
        }
        this.editingRecipe = null
      } catch (error) {
        console.error('Error updating recipe:', error)
      }
    },

    async deleteRecipe(id) {
      try {
        const response = await fetch(`http://localhost:8000/api/recipes/${id}/`, {
          method: 'DELETE'
        })
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
        
        this.recipes = this.recipes.filter(recipe => recipe.id !== id)
        
        // Emit event to parent
        this.$emit('recipes-updated')
        
        // Close modal
        const modal = Modal.getInstance(document.getElementById('deleteRecipeModal'))
        modal.hide()
        this.deleteRecipeId = null
      } catch (error) {
        console.error('Error deleting recipe:', error)
      }
    },

    async createRecipe() {
      try {
        const response = await fetch('http://localhost:8000/api/recipes/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.newRecipe)
        })
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
        
        // After successful creation, fetch the updated list of recipes
        await this.fetchRecipes()
        this.$emit('recipes-updated')
        // Close modal and reset form
        const modal = Modal.getInstance(document.getElementById('addRecipeModal'))
        modal.hide()
        this.newRecipe = {
          title: '',
          description: '',
          servings: null
        }
      } catch (error) {
        console.error('Error creating recipe:', error)
      }
    },

    cancelAdd() {
      this.showAddForm = false
      this.newRecipe = {
        title: '',
        description: '',
        servings: null
      }
    },

    formatDate(dateString) {
      if (!dateString) return '';
      return new Date(dateString).toLocaleDateString();
    }
  }
}
</script>
