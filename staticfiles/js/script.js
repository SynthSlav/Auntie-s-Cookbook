document.addEventListener('DOMContentLoaded', function () {
    console.log('Filter functionality loading...');

    // DOM Elements
    const applyFiltersBtn = document.getElementById('applyFilters');
    const clearFiltersBtn = document.getElementById('clearFilters');
    const clearAllFiltersBtn = document.getElementById('clearAllFilters');
    const activeFiltersDiv = document.getElementById('activeFilters');
    const filterTagsDiv = document.getElementById('filterTags');

    // Get Selected Filters Function
    function getSelectedFilters() {
        const filters = {
            mealTypes: [],
            difficulties: [],
            dietary: []
        };

        // Get checked meal type filters
        document.querySelectorAll('input[id^="meal-"]:checked').forEach(function (checkbox) {
            filters.mealTypes.push(checkbox.value);
        });

        // Get checked difficulty filters
        document.querySelectorAll('input[id^="diff-"]:checked').forEach(function (checkbox) {
            filters.difficulties.push(checkbox.value);
        });

        // Get checked dietary filters
        document.querySelectorAll('input[id^="diet-"]:checked').forEach(function (checkbox) {
            filters.dietary.push(checkbox.value);
        });

        return filters;
    }

    // Apply Filters Function
    function applyFilters() {
        console.log('Applying filters...');

        const filters = getSelectedFilters();
        console.log('Selected filters:', filters);

        const recipeItems = document.querySelectorAll('.recipe-item');
        let visibleCount = 0;

        recipeItems.forEach(function (item) {
            let showItem = true;

            // Check meal type filter
            if (filters.mealTypes.length > 0) {
                if (!filters.mealTypes.includes(item.dataset.mealType)) {
                    showItem = false;
                }
            }

            // Check difficulty filter
            if (filters.difficulties.length > 0) {
                if (!filters.difficulties.includes(item.dataset.difficulty)) {
                    showItem = false;
                }
            }

            // Check dietary filter
            if (filters.dietary.length > 0) {
                if (!filters.dietary.includes(item.dataset.dietary)) {
                    showItem = false;
                }
            }

            // Show/hide item with smooth animation
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

        console.log('Visible recipes:', visibleCount);
        updateFilterTags(filters);
        updateRecipeCount(visibleCount);
    }

    // Update Recipe Count
    function updateRecipeCount(count) {
        const countElement = document.querySelector('.text-muted');
        if (countElement && countElement.textContent.includes('recipe')) {
            countElement.textContent = `Discover ${count} delicious recipes`;
        }
    }

    // Update Filter Tags
    function updateFilterTags(filters) {
        if (!filterTagsDiv) return;

        filterTagsDiv.innerHTML = '';
        let hasFilters = false;

        // Helper function to capitalize first letter
        function capitalize(str) {
            return str.charAt(0).toUpperCase() + str.slice(1).replace('_', ' ');
        }

        // Add meal type tags
        filters.mealTypes.forEach(function (mealType) {
            addFilterTag(capitalize(mealType), mealType);
            hasFilters = true;
        });

        // Add difficulty tags
        filters.difficulties.forEach(function (difficulty) {
            addFilterTag(capitalize(difficulty), difficulty);
            hasFilters = true;
        });

        // Add dietary tags
        filters.dietary.forEach(function (dietary) {
            addFilterTag(capitalize(dietary), dietary);
            hasFilters = true;
        });

        // Show/hide active filters section
        if (activeFiltersDiv) {
            activeFiltersDiv.style.display = hasFilters ? 'block' : 'none';
        }
    }

    // Add Individual Filter Tag 
    function addFilterTag(displayText, value) {
        if (!filterTagsDiv) return;

        const tag = document.createElement('span');
        tag.className = 'filter-tag';
        tag.innerHTML = `${displayText} <span class="filter-close">×</span>`;

        // Make entire tag clickable for better mobile UX
        tag.addEventListener('click', function (e) {
            e.stopPropagation();
            // Find and uncheck the corresponding checkbox
            const checkbox = document.querySelector(`input[value="${value}"]`);
            if (checkbox) {
                checkbox.checked = false;
            }
            applyFilters();
        });

        // Add visual feedback
        tag.style.cursor = 'pointer';

        filterTagsDiv.appendChild(tag);
    }

    // Clear All Filters Function
    function clearAllFilters() {
        console.log('Clearing all filters...');

        // Uncheck all checkboxes
        document.querySelectorAll('#filterModal input[type="checkbox"]').forEach(function (checkbox) {
            checkbox.checked = false;
        });

        // Show all recipes
        document.querySelectorAll('.recipe-item').forEach(function (item) {
            item.style.display = 'block';
            item.classList.remove('filtered-out');
        });

        // Hide active filters
        if (activeFiltersDiv) {
            activeFiltersDiv.style.display = 'none';
        }
        if (filterTagsDiv) {
            filterTagsDiv.innerHTML = '';
        }

        // Update count
        const totalRecipes = document.querySelectorAll('.recipe-item').length;
        updateRecipeCount(totalRecipes);
    }

    // Event Listeners
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', applyFilters);
        console.log('Apply filters event listener added');
    }

    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', clearAllFilters);
        console.log('Clear filters event listener added');
    }

    if (clearAllFiltersBtn) {
        clearAllFiltersBtn.addEventListener('click', clearAllFilters);
        console.log('Clear all filters event listener added');
    }

    console.log('Filter functionality initialized');

    // Recipe Detail Page Features
    // Check if the recipe detail page is loaded
    if (document.querySelector('.recipe-image-container')) {
        initializeRecipeDetailFeatures();
    }

    function initializeRecipeDetailFeatures() {
        // Ingredient checkbox functionality
        initializeIngredientCheckboxes();

        // Action buttons (if you want to add functionality later)
        initializeActionButtons();
    }

    function initializeIngredientCheckboxes() {
        const checkboxes = document.querySelectorAll('.form-check-input');

        checkboxes.forEach(function (checkbox) {
            checkbox.addEventListener('change', function () {
                const ingredientText = this.parentElement.nextElementSibling.querySelector('.ingredient-text');
                updateIngredientStyle(checkbox, ingredientText);
            });
        });
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

    function initializeActionButtons() {
        // Edit Recipe Button
        const editBtn = document.querySelector('.btn-outline-warning');
        if (editBtn) {
            editBtn.addEventListener('click', function (e) {
                e.preventDefault();
                console.log('Edit recipe clicked');
            });
        }

        // Delete Recipe Button
        const deleteBtn = document.querySelector('.btn-outline-danger');
        if (deleteBtn) {
            deleteBtn.addEventListener('click', function (e) {
                e.preventDefault();
                if (confirm('Are you sure you want to delete this recipe?')) {
                    console.log('Delete recipe confirmed');
                }
            });
        }

        // Favorite Button
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
});