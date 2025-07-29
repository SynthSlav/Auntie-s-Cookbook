document.addEventListener('DOMContentLoaded', function () {
    console.log('All functionality loading...');

    // Filter functionality
    if (document.getElementById('recipeContainer')) {
        initializeFilterFunctionality();
    }

    // Recipe detail page functionality
    if (document.querySelector('.recipe-image-container')) {
        initializeRecipeDetailFeatures();
    }

    // Add recipe form functionality
    if (document.getElementById('add-recipe-form')) {
        initializeAddRecipeForm();
    }

    // Filter Functionality
    function initializeFilterFunctionality() {
        const applyFiltersBtn = document.getElementById('applyFilters');
        const clearFiltersBtn = document.getElementById('clearFilters');
        const clearAllFiltersBtn = document.getElementById('clearAllFilters');
        const activeFiltersDiv = document.getElementById('activeFilters');
        const filterTagsDiv = document.getElementById('filterTags');

        if (!applyFiltersBtn) return; // Exit if no filter elements
        // Get selected filters
        // This function collects the values of all checked checkboxes and returns them as an object
        function getSelectedFilters() {
            const filters = {
                mealTypes: [],
                difficulties: [],
                dietary: []
            };

            document.querySelectorAll('input[id^="meal-"]:checked').forEach(function (checkbox) {
                filters.mealTypes.push(checkbox.value);
            });

            document.querySelectorAll('input[id^="diff-"]:checked').forEach(function (checkbox) {
                filters.difficulties.push(checkbox.value);
            });

            document.querySelectorAll('input[id^="diet-"]:checked').forEach(function (checkbox) {
                filters.dietary.push(checkbox.value);
            });

            return filters;
        }
        // Apply filters
        // This function filters the recipe items based on selected checkboxes
        function applyFilters() {
            const filters = getSelectedFilters();
            const recipeItems = document.querySelectorAll('.recipe-item');
            let visibleCount = 0;

            recipeItems.forEach(function (item) {
                let showItem = true;

                if (filters.mealTypes.length > 0) {
                    if (!filters.mealTypes.includes(item.dataset.mealType)) {
                        showItem = false;
                    }
                }

                if (filters.difficulties.length > 0) {
                    if (!filters.difficulties.includes(item.dataset.difficulty)) {
                        showItem = false;
                    }
                }

                if (filters.dietary.length > 0) {
                    if (!filters.dietary.includes(item.dataset.dietary)) {
                        showItem = false;
                    }
                }

                if (showItem) {
                    item.style.display = 'block';
                    item.classList.remove('filtered-out');
                    visibleCount++;
                } else {
                    item.classList.add('filtered-out');
                    setTimeout(() => {
                        if (item.classList.contains('filtered-out')) {
                            item.style.display = 'none';
                        }
                    }, 300);
                }
            });

            updateFilterTags(filters);
            updateRecipeCount(visibleCount);

            // Fix aria-hidden warning
            if (applyFiltersBtn) {
                applyFiltersBtn.blur();
            }
        }
        // Update recipe count
        // This function updates the recipe count displayed on the page
        function updateRecipeCount(count) {
            const countElement = document.querySelector('.text-muted');
            if (countElement && countElement.textContent.includes('recipe')) {
                countElement.textContent = `Discover ${count} delicious recipes`;
            }
        }
        // Update filter tags
        // This function updates the filter tags displayed above the recipe list based on selected filters
        function updateFilterTags(filters) {
            if (!filterTagsDiv) return;

            filterTagsDiv.innerHTML = '';
            let hasFilters = false;

            function capitalize(str) {
                return str.charAt(0).toUpperCase() + str.slice(1).replace('_', ' ');
            }

            filters.mealTypes.forEach(function (mealType) {
                addFilterTag(capitalize(mealType), mealType);
                hasFilters = true;
            });

            filters.difficulties.forEach(function (difficulty) {
                addFilterTag(capitalize(difficulty), difficulty);
                hasFilters = true;
            });

            filters.dietary.forEach(function (dietary) {
                addFilterTag(capitalize(dietary), dietary);
                hasFilters = true;
            });

            if (activeFiltersDiv) {
                activeFiltersDiv.style.display = hasFilters ? 'block' : 'none';
            }
        }
        // Add filter tag
        // This function creates a tag for each selected filter and adds it to the filter tags div
        function addFilterTag(displayText, value) {
            if (!filterTagsDiv) return;

            const tag = document.createElement('span');
            tag.className = 'filter-tag';
            tag.innerHTML = `${displayText} <span class="filter-close">×</span>`;

            tag.addEventListener('click', function (e) {
                e.stopPropagation();
                const checkbox = document.querySelector(`input[value="${value}"]`);
                if (checkbox) {
                    checkbox.checked = false;
                }
                applyFilters();
            });

            tag.style.cursor = 'pointer';
            filterTagsDiv.appendChild(tag);
        }
        // Clear all filters
        // This function resets all filters and shows all recipes
        function clearAllFilters() {
            document.querySelectorAll('#filterModal input[type="checkbox"]').forEach(function (checkbox) {
                checkbox.checked = false;
            });

            document.querySelectorAll('.recipe-item').forEach(function (item) {
                item.style.display = 'block';
                item.classList.remove('filtered-out');
            });

            if (activeFiltersDiv) {
                activeFiltersDiv.style.display = 'none';
            }
            if (filterTagsDiv) {
                filterTagsDiv.innerHTML = '';
            }

            const totalRecipes = document.querySelectorAll('.recipe-item').length;
            updateRecipeCount(totalRecipes);
        }

        // Event listeners
        if (applyFiltersBtn) {
            applyFiltersBtn.addEventListener('click', applyFilters);
        }

        if (clearFiltersBtn) {
            clearFiltersBtn.addEventListener('click', clearAllFilters);
        }

        if (clearAllFiltersBtn) {
            clearAllFiltersBtn.addEventListener('click', clearAllFilters);
        }

        console.log('Filter functionality initialized');
    }

    // Recipe Detail Features
    // This function initializes the features on the recipe detail page
    // It sets up ingredient checkboxes, action buttons, and their event listeners
    function initializeRecipeDetailFeatures() {
        function initializeIngredientCheckboxes() {
            const checkboxes = document.querySelectorAll('.form-check-input');

            checkboxes.forEach(function (checkbox) {
                checkbox.addEventListener('change', function () {
                    const ingredientText = this.parentElement.nextElementSibling.querySelector('.ingredient-text');
                    updateIngredientStyle(checkbox, ingredientText);
                });
            });
        }
        // Update ingredient style based on checkbox state
        // This function applies a line-through style to the ingredient text when the checkbox is checked
        function updateIngredientStyle(checkbox, ingredientText) {
            if (checkbox.checked) {
                ingredientText.style.textDecoration = 'line-through';
                ingredientText.style.opacity = '0.6';
            } else {
                ingredientText.style.textDecoration = 'none';
                ingredientText.style.opacity = '1';
            }
        }
        // Initialize action buttons
        // This function sets up event listeners for the action buttons on the recipe detail page
        function initializeActionButtons() {
            const editBtn = document.querySelector('.btn-outline-warning');
            if (editBtn) {
                editBtn.addEventListener('click', function (e) {
                    e.preventDefault();
                    console.log('Edit recipe clicked');
                });
            }

            const deleteBtn = document.querySelector('.btn-outline-danger');
            if (deleteBtn) {
                deleteBtn.addEventListener('click', function (e) {
                    e.preventDefault();
                    if (confirm('Are you sure you want to delete this recipe?')) {
                        console.log('Delete recipe confirmed');
                    }
                });
            }
            // Toggle favorite button
            // This function toggles the favorite state of the recipe when the button is clicked
            const favoriteBtn = document.querySelector('.btn-outline-primary');
            if (favoriteBtn) {
                favoriteBtn.addEventListener('click', function (e) {
                    e.preventDefault();
                    const icon = this.querySelector('i');
                    if (icon.classList.contains('fas')) {
                        icon.classList.remove('fas');
                        icon.classList.add('far');
                        this.classList.remove('btn-outline-primary');
                        this.classList.add('btn-primary');
                    } else {
                        icon.classList.remove('far');
                        icon.classList.add('fas');
                        this.classList.remove('btn-primary');
                        this.classList.add('btn-outline-primary');
                    }
                    console.log('Favorite toggled');
                });
            }
        }

        initializeIngredientCheckboxes();
        initializeActionButtons();
        console.log('Recipe detail features initialized');
    }

    // Add Recipe Form Functionality
    function initializeAddRecipeForm() {
        const addIngredientBtn = document.getElementById('add-ingredient-btn');
        const ingredientFormsContainer = document.getElementById('ingredient-forms');
        const totalFormsInput = document.getElementById('id_ingredients-TOTAL_FORMS');
        const ingredientCount = document.getElementById('ingredient-count');
        const emptyMessage = document.getElementById('empty-ingredients');

        if (!addIngredientBtn || !ingredientFormsContainer || !totalFormsInput) {
            console.log('Add recipe form elements not found');
            return;
        }

        // Clear any pre-filled data on page load
        clearAllForms();

        // Initialize
        updateIngredientCount();
        updateIngredientNumbers();

        const firstForm = ingredientFormsContainer.querySelector('.ingredient-form');
        if (firstForm) {
            firstForm.classList.remove('d-none');
            updateEmptyState();
        }

        addIngredientBtn.addEventListener('click', function () {
            addNewIngredientForm();
        });

        ingredientFormsContainer.addEventListener('click', function (e) {
            if (e.target.closest('.delete-ingredient-btn')) {
                e.preventDefault();
                const ingredientForm = e.target.closest('.ingredient-form');
                deleteIngredientForm(ingredientForm);
            }
        });

        function clearAllForms() {
            const allForms = ingredientFormsContainer.querySelectorAll('.ingredient-form');
            allForms.forEach(form => {
                clearFormInputs(form);
            });
        }
        // Add new ingredient form
        // This function adds a new ingredient form to the formset
        function addNewIngredientForm() {
            const hiddenForms = ingredientFormsContainer.querySelectorAll('.ingredient-form.d-none');

            if (hiddenForms.length > 0) {
                const nextForm = hiddenForms[0];

                nextForm.classList.add('ingredient-entering');
                nextForm.classList.remove('d-none');

                setTimeout(() => {
                    nextForm.classList.remove('ingredient-entering');
                }, 400);

                const nameInput = nextForm.querySelector('input[name$="-ingredient_name"]');
                if (nameInput) {
                    setTimeout(() => nameInput.focus(), 100);
                }

                updateIngredientCount();
                updateIngredientNumbers();
                updateEmptyState();
            } else {
                const currentFormCount = parseInt(totalFormsInput.value);
                const maxForms = 25;

                if (currentFormCount >= maxForms) {
                    showNotification('You can only add up to 25 ingredients.', 'warning');
                    return;
                }

                const lastForm = ingredientFormsContainer.querySelector('.ingredient-form:last-child');
                if (!lastForm) return;

                const newForm = lastForm.cloneNode(true);

                updateFormIndexes(newForm, currentFormCount);
                clearFormInputs(newForm);

                newForm.classList.add('ingredient-entering');
                newForm.classList.remove('d-none');
                newForm.setAttribute('data-form-index', currentFormCount);

                ingredientFormsContainer.appendChild(newForm);

                setTimeout(() => {
                    newForm.classList.remove('ingredient-entering');
                }, 400);

                totalFormsInput.value = currentFormCount + 1;

                const nameInput = newForm.querySelector('input[name$="-ingredient_name"]');
                if (nameInput) {
                    setTimeout(() => nameInput.focus(), 100);
                }

                updateIngredientCount();
                updateIngredientNumbers();
                updateEmptyState();
            }
        }
        // Delete ingredient form
        // This function marks the form for deletion and hides it after a short animation
        function deleteIngredientForm(ingredientForm) {
            const deleteCheckbox = ingredientForm.querySelector('input[name$="-DELETE"]');
            const visibleForms = ingredientFormsContainer.querySelectorAll('.ingredient-form:not(.d-none)');

            if (visibleForms.length <= 1) {
                showNotification('You must have at least one ingredient.', 'warning');
                return;
            }

            if (deleteCheckbox) {
                deleteCheckbox.checked = true;
            }

            ingredientForm.classList.add('ingredient-removing');

            setTimeout(() => {
                ingredientForm.classList.add('d-none');
                ingredientForm.classList.remove('ingredient-removing');
                updateIngredientCount();
                updateIngredientNumbers();
                updateEmptyState();
            }, 400);
        }
        // Update form indexes for name, id, and for attributes
        // This ensures that the formset works correctly with Django's form management
        function updateFormIndexes(form, newIndex) {
            form.querySelectorAll('[name]').forEach(element => {
                const name = element.getAttribute('name');
                if (name.includes('ingredients-')) {
                    element.setAttribute('name', name.replace(/ingredients-\d+/, `ingredients-${newIndex}`));
                }
            });

            form.querySelectorAll('[id]').forEach(element => {
                const id = element.getAttribute('id');
                if (id.includes('ingredients-')) {
                    element.setAttribute('id', id.replace(/ingredients-\d+/, `id_ingredients-${newIndex}`));
                }
            });

            form.querySelectorAll('[for]').forEach(element => {
                const forAttr = element.getAttribute('for');
                if (forAttr && forAttr.includes('ingredients-')) {
                    element.setAttribute('for', forAttr.replace(/ingredients-\d+/, `id_ingredients-${newIndex}`));
                }
            });
        }
        // Clear form inputs
        // This function resets all inputs in a form to their default state
        function clearFormInputs(form) {
            form.querySelectorAll('input, select, textarea').forEach(input => {
                if (input.type !== 'hidden') {
                    if (input.type === 'checkbox') {
                        input.checked = false;
                    } else {
                        input.value = '';
                    }
                    input.classList.remove('is-valid', 'is-invalid');
                }
            });
        }
        // Update ingredient count, numbers, and empty state
        // These functions handle the dynamic updates of the ingredient form count and display
        function updateIngredientCount() {
            const visibleForms = ingredientFormsContainer.querySelectorAll('.ingredient-form:not(.d-none)');
            if (ingredientCount) {
                const oldCount = parseInt(ingredientCount.textContent);
                const newCount = visibleForms.length;

                ingredientCount.textContent = newCount;

                if (oldCount !== newCount) {
                    ingredientCount.style.animation = 'none';
                    ingredientCount.offsetHeight;
                    ingredientCount.style.animation = 'pulse 0.3s ease';
                }
            }
        }
        // Update ingredient numbers in each form
        // This function updates the displayed number of each ingredient form based on its position
        function updateIngredientNumbers() {
            const visibleForms = ingredientFormsContainer.querySelectorAll('.ingredient-form:not(.d-none)');
            visibleForms.forEach((form, index) => {
                const numberBadge = form.querySelector('.number-badge');
                if (numberBadge) {
                    numberBadge.textContent = index + 1;
                }
            });
        }
        // Update empty state message
        // This function shows or hides the empty state message based on the number of visible ingredient forms
        function updateEmptyState() {
            const visibleForms = ingredientFormsContainer.querySelectorAll('.ingredient-form:not(.d-none)');
            if (emptyMessage) {
                emptyMessage.style.display = visibleForms.length === 0 ? 'block' : 'none';
            }
        }
        // Show notification function
        // This function creates a notification element and displays it on the screen
        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
            notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
            notification.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;

            document.body.appendChild(notification);

            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 4000);
        }

        // Form validation
        const form = document.getElementById('add-recipe-form');
        form.addEventListener('submit', function (e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            const visibleForms = ingredientFormsContainer.querySelectorAll('.ingredient-form:not(.d-none)');
            let hasIngredient = false;

            visibleForms.forEach(form => {
                const nameInput = form.querySelector('input[name$="-ingredient_name"]');
                const deleteCheckbox = form.querySelector('input[name$="-DELETE"]');

                if (nameInput && nameInput.value.trim() && (!deleteCheckbox || !deleteCheckbox.checked)) {
                    hasIngredient = true;
                }
            });

            if (!hasIngredient) {
                e.preventDefault();
                showNotification('Please add at least one ingredient with a name.', 'danger');

                const firstNameInput = ingredientFormsContainer.querySelector('.ingredient-form:not(.d-none) input[name$="-ingredient_name"]');
                if (firstNameInput) {
                    firstNameInput.focus();
                    firstNameInput.classList.add('is-invalid');
                }
                return false;
            }

            if (submitBtn) {
                submitBtn.classList.add('loading');
                submitBtn.disabled = true;

                setTimeout(() => {
                    submitBtn.classList.remove('loading');
                    submitBtn.disabled = false;
                }, 10000);
            }
        });

        // Real-time validation
        ingredientFormsContainer.addEventListener('input', function (e) {
            if (e.target.name && e.target.name.includes('ingredient_name')) {
                if (e.target.value.trim()) {
                    e.target.classList.remove('is-invalid');
                    e.target.classList.add('is-valid');
                } else {
                    e.target.classList.remove('is-valid');
                }
            }
        });

        console.log('Add recipe form initialized successfully');
    }
});