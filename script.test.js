/**
 * @jest-environment jsdom
 */

const { getSelectedFilters, updateIngredientStyle, updateRecipeCount, capitalize, validateIngredients } = require('./static/js/script');

describe('Recipe App Functions', () => {
    beforeEach(() => {
        document.body.innerHTML = '';
    });

    test('getSelectedFilters returns correct filters', () => {
        document.body.innerHTML = `
            <input type="checkbox" id="meal-breakfast" value="breakfast" checked>
            <input type="checkbox" id="diff-easy" value="easy" checked>
            <input type="checkbox" id="diet-vegan" value="vegan">
        `;

        const filters = getSelectedFilters();

        expect(filters.mealTypes).toContain('breakfast');
        expect(filters.difficulties).toContain('easy');
        expect(filters.dietary).not.toContain('vegan');
    });

    test('updateIngredientStyle works correctly', () => {
        document.body.innerHTML = `
            <input type="checkbox" id="cb">
            <span class="ingredient-text">flour</span>
        `;

        const checkbox = document.getElementById('cb');
        const text = document.querySelector('.ingredient-text');

        checkbox.checked = true;
        updateIngredientStyle(checkbox, text);

        expect(text.style.textDecoration).toBe('line-through');
        expect(text.style.opacity).toBe('0.6');
    });

    test('updateRecipeCount updates text correctly', () => {
        document.body.innerHTML = `
            <p class="text-muted">Discover 20 delicious recipes</p>
        `;

        updateRecipeCount(15);

        expect(document.querySelector('.text-muted').textContent).toBe('Discover 15 delicious recipes');
    });

    test('capitalize function formats text correctly', () => {
        expect(capitalize('breakfast')).toBe('Breakfast');
        expect(capitalize('gluten_free')).toBe('Gluten free');
    });

    test('validateIngredients checks form validation', () => {
        document.body.innerHTML = `
            <div id="container">
                <div class="ingredient-form">
                    <input name="ingredients-0-ingredient_name" value="flour">
                </div>
                <div class="ingredient-form d-none">
                    <input name="ingredients-1-ingredient_name" value="">
                </div>
            </div>
        `;

        const container = document.getElementById('container');
        expect(validateIngredients(container)).toBe(true);

        // Test with empty ingredient
        document.querySelector('input[name="ingredients-0-ingredient_name"]').value = '';
        expect(validateIngredients(container)).toBe(false);
    });
});