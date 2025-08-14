// Functions for filtering recipes, updating ingredient styles, and managing recipe counts
// These functions are used in the recipe app to handle user interactions and data updates
// They are also exported for testing purposes
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

function updateIngredientStyle(checkbox, ingredientText) {
    if (checkbox.checked) {
        ingredientText.style.textDecoration = 'line-through';
        ingredientText.style.opacity = '0.6';
    } else {
        ingredientText.style.textDecoration = 'none';
        ingredientText.style.opacity = '1';
    }
}

function updateRecipeCount(count) {
    const countElement = document.querySelector('.text-muted');
    if (countElement && countElement.textContent.includes('recipe')) {
        countElement.textContent = `Discover ${count} delicious recipes`;
    }
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1).replace('_', ' ');
}

function validateIngredients(ingredientFormsContainer) {
    const visibleForms = ingredientFormsContainer.querySelectorAll('.ingredient-form:not(.d-none)');
    let hasIngredient = false;

    visibleForms.forEach(form => {
        const nameInput = form.querySelector('input[name$="-ingredient_name"]');
        const deleteCheckbox = form.querySelector('input[name$="-DELETE"]');

        if (nameInput && nameInput.value.trim() && (!deleteCheckbox || !deleteCheckbox.checked)) {
            hasIngredient = true;
        }
    });

    return hasIngredient;
}

// Event listener for DOMContentLoaded to initialize functionality
// This ensures that the script runs after the DOM is fully loaded

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

    // Recipe form functionality
    if (document.getElementById('edit-recipe-form') || document.getElementById('add-recipe-form')) {
        initializeAddRecipeForm();
    }

    // Filter Functionality
    function initializeFilterFunctionality() {
        const applyFiltersBtn = document.getElementById('applyFilters');
        const clearFiltersBtn = document.getElementById('clearFilters');
        const clearAllFiltersBtn = document.getElementById('clearAllFilters');

        if (!applyFiltersBtn) {
            return;
        }

        loadFiltersFromURL();
        initializeFilterTagHandlers();

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

        function loadFiltersFromURL() {
            const urlParams = new URLSearchParams(window.location.search);

            const mealTypes = urlParams.getAll('meal_type');
            const difficulties = urlParams.getAll('difficulty');
            const dietary = urlParams.getAll('dietary');

            mealTypes.forEach(type => {
                const checkbox = document.getElementById(`meal-${type}`);
                if (checkbox) checkbox.checked = true;
            });

            difficulties.forEach(diff => {
                const checkbox = document.getElementById(`diff-${diff}`);
                if (checkbox) checkbox.checked = true;
            });

            dietary.forEach(diet => {
                const checkbox = document.getElementById(`diet-${diet}`);
                if (checkbox) checkbox.checked = true;
            });
        }

        function initializeFilterTagHandlers() {
            document.addEventListener('click', function (e) {
                if (e.target.closest('.filter-tag')) {
                    const filterTag = e.target.closest('.filter-tag');
                    const paramName = filterTag.dataset.param;
                    const value = filterTag.dataset.value;

                    if (paramName && value) {
                        removeFilter(paramName, value);
                    }
                }
            });
        }

        function removeFilter(paramName, value) {
            const url = new URL(window.location);
            const currentValues = url.searchParams.getAll(paramName);
            url.searchParams.delete(paramName);
            currentValues.forEach(val => {
                if (val !== value) {
                    url.searchParams.append(paramName, val);
                }
            });
            url.searchParams.delete('page');
            window.location.href = url.toString();
        }

        function applyFilters() {
            const filters = getSelectedFilters();
            const url = new URL(window.location.origin + window.location.pathname);

            filters.mealTypes.forEach(type => {
                url.searchParams.append('meal_type', type);
            });

            filters.difficulties.forEach(diff => {
                url.searchParams.append('difficulty', diff);
            });

            filters.dietary.forEach(diet => {
                url.searchParams.append('dietary', diet);
            });

            window.location.href = url.toString();
        }

        function clearAllFilters() {
            const url = new URL(window.location.origin + window.location.pathname);
            window.location.href = url.toString();
        }

        // Event listeners
        if (applyFiltersBtn) {
            applyFiltersBtn.addEventListener('click', function (e) {
                e.preventDefault();
                applyFilters();
            });
        }

        if (clearFiltersBtn) {
            clearFiltersBtn.addEventListener('click', function (e) {
                e.preventDefault();
                clearAllFilters();
            });
        }

        if (clearAllFiltersBtn) {
            clearAllFiltersBtn.addEventListener('click', function (e) {
                e.preventDefault();
                clearAllFilters();
            });
        }

        window.removeFilter = removeFilter;
        window.clearAllFilters = clearAllFilters;
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
        const isEditPage = document.getElementById('edit-recipe-form');

        if (!addIngredientBtn || !ingredientFormsContainer || !totalFormsInput) {
            console.log('Add recipe form elements not found');
            return;
        }

        // Clear any pre-filled data on page load
        if (!isEditPage) {
            clearAllForms();
        }
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
        const form = document.getElementById('add-recipe-form') || document.getElementById('edit-recipe-form');

        if (!form) {
            console.log('Form not found');
            return;
        }

        form.addEventListener('submit', function (e) {
            const submitBtn = form.querySelector('button[type="submit"]');

            if (!validateIngredients(ingredientFormsContainer)) {
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

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        getSelectedFilters,
        updateIngredientStyle,
        updateRecipeCount,
        capitalize,
        validateIngredients
    };
}