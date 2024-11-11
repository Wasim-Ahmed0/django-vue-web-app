<template>
  <div>
    <h2>Ingredients</h2>
    
    <button class="btn btn-primary mb-3" data-bs-toggle="modal" data-bs-target="#addIngredientModal">
      Add New Ingredient
    </button>

    <table class="table table-striped">
      <thead>
        <tr>
          <th>Name</th>
          <th>Description</th>
          <th>Organic</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ingredient in ingredients" :key="ingredient.id">
          <td>{{ ingredient.name }}</td>
          <td>{{ ingredient.description }}</td>
          <td>{{ ingredient.is_organic ? 'Yes' : 'No' }}</td>
          <td>
            <button class="btn btn-sm btn-primary me-2" @click="openEditModal(ingredient)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="openDeleteModal(ingredient)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Add Modal -->
    <div class="modal fade" id="addIngredientModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add New Ingredient</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <input class="form-control" v-model="newIngredient.name" placeholder="Ingredient name">
            </div>
            <div class="mb-3">
              <textarea class="form-control" v-model="newIngredient.description" placeholder="Description"></textarea>
            </div>
            <div class="form-check mb-3">
              <input class="form-check-input" type="checkbox" v-model="newIngredient.is_organic" id="newIsOrganic">
              <label class="form-check-label" for="newIsOrganic">Is Organic</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="createIngredient">Save</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div class="modal fade" id="editIngredientModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Ingredient</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="editingIngredient">
            <div class="mb-3">
              <input class="form-control" v-model="editingIngredient.name" placeholder="Ingredient name">
            </div>
            <div class="mb-3">
              <textarea class="form-control" v-model="editingIngredient.description" placeholder="Description"></textarea>
            </div>
            <div class="form-check mb-3">
              <input class="form-check-input" type="checkbox" v-model="editingIngredient.is_organic" id="editIsOrganic">
              <label class="form-check-label" for="editIsOrganic">Is Organic</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="updateIngredient">Save</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Modal -->
    <div class="modal fade" id="deleteIngredientModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Delete Ingredient</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            Are you sure you want to delete this ingredient?
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
  name: 'Ingredients',
  data() {
    return {
      ingredients: [],
      editingIngredient: null,
      deleteIngredientId: null,
      newIngredient: {
        name: '',
        description: '',
        is_organic: false
      }
    }
  },
  mounted() {
    this.fetchIngredients()
  },
  methods: {
    openEditModal(ingredient) {
      this.editingIngredient = { ...ingredient }
      const modal = new Modal(document.getElementById('editIngredientModal'))
      modal.show()
    },
    openDeleteModal(ingredient) {
      this.deleteIngredientId = ingredient.id
      const modal = new Modal(document.getElementById('deleteIngredientModal'))
      modal.show()
    },
    async confirmDelete() {
      if (this.deleteIngredientId) {
        await this.deleteIngredient(this.deleteIngredientId)
        const modal = Modal.getInstance(document.getElementById('deleteIngredientModal'))
        modal.hide()
      }
    },
    async fetchIngredients() {
      try {
        const response = await fetch('http://localhost:8000/api/ingredients/')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        this.ingredients = data
      } catch (error) {
        console.error('Error fetching ingredients:', error)
      }
    },

    editIngredient(ingredient) {
      this.editingIngredient = { ...ingredient }
    },

    async updateIngredient() {
      try {
        const response = await fetch(`http://localhost:8000/api/ingredients/${this.editingIngredient.id}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: this.editingIngredient.name,
            description: this.editingIngredient.description,
            is_organic: this.editingIngredient.is_organic
          })
        })

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
        
        const updatedIngredient = await response.json()
        const index = this.ingredients.findIndex(i => i.id === updatedIngredient.id)
        if (index !== -1) {
          this.ingredients[index] = updatedIngredient
        }
        
        // Close modal and reset form
        const modal = Modal.getInstance(document.getElementById('editIngredientModal'))
        modal.hide()
        this.editingIngredient = null
      } catch (error) {
        console.error('Error updating ingredient:', error)
      }
    },

    async deleteIngredient(id) {
      try {
        const response = await fetch(`http://localhost:8000/api/ingredients/${id}/`, {
          method: 'DELETE'
        })
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
        
        this.ingredients = this.ingredients.filter(ingredient => ingredient.id !== id)
        
        // Close modal
        const modal = Modal.getInstance(document.getElementById('deleteIngredientModal'))
        modal.hide()
        this.deleteIngredientId = null
      } catch (error) {
        console.error('Error deleting ingredient:', error)
      }
    },

    async createIngredient() {
      try {
        const response = await fetch('http://localhost:8000/api/ingredients/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.newIngredient)
        })
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
        
        // Fetch the updated list of ingredients
        await this.fetchIngredients()
        
        // Close modal and reset form
        const modal = Modal.getInstance(document.getElementById('addIngredientModal'))
        modal.hide()
        this.newIngredient = {
          name: '',
          description: '',
          is_organic: false
        }
      } catch (error) {
        console.error('Error creating ingredient:', error)
      }
    },

    cancelAdd() {
      this.showAddForm = false
      this.newIngredient = {
        name: '',
        description: '',
        is_organic: false
      }
    }
  }
}
</script>
