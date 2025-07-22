document.addEventListener('DOMContentLoaded', function () {

    // DOM Elements
    const applyFiltersBtn = document.getElementById('applyFilters');
    const clearFiltersBtn = document.getElementById('clearFilters');

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
        console.log('Applying filters..');

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

            // Show/hide item
            if (showItem) {
                item.style.display = 'block';
                visibleCount++;
            } else {
                item.style.display = 'none';
            }
        });

        console.log('Visible recipes:', visibleCount);
    }

    // Clear Filters Function
    function clearAllFilters() {
        console.log('Clearing all filters...');

        // Uncheck all checkboxes
        document.querySelectorAll('#filterModal input[type="checkbox"]').forEach(function (checkbox) {
            checkbox.checked = false;
        });

        // Show all recipes
        document.querySelectorAll('.recipe-item').forEach(function (item) {
            item.style.display = 'block';
        });
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

    console.log('Filter functionality initialized');
});