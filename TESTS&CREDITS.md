# Testing, Bugs & Credits

## Testing

### Automated Testing

#### Python/Django Tests

#### Test Database
The tests use an in-memory SQLite database instead of PostgreSQL to make them run faster. This is pretty standard for Django projects and doesn't affect the test results since Django's ORM works the same way with both databases.

I wrote tests to make sure the basic stuff works properly. The model tests check that recipes get created with the right data and that the slug generation works (so URLs don't break). I also made sure that things like serving sizes only accept positive numbers - nobody wants a recipe that serves -3 people.

For the forms, I tested what happens when users try to submit incomplete or invalid data. The main thing was making sure you can't create a recipe without a title or ingredients without names. I also tested that the ingredient unit dropdown shows "Select Unit" for new ingredients instead of being blank.

The view tests were mostly about security - making sure users can only mess with their own recipes, not delete other people's stuff. I tested the whole process of creating a recipe with ingredients, editing it later, and deleting recipes when needed.

#### JavaScript Tests
I used Jest to test the core JavaScript utility functions. Since the main functionality runs after DOM loads, I extracted the key functions to test them separately. This includes testing the filter selection logic, the ingredient styling updates (like strikethrough text when checked), and basic form validation helpers. The tests are more focused on making sure individual functions work correctly rather than testing the full interactive workflow.

#### Code Validation
- **HTML Validator**: Passed W3C HTML validation (errors and warnings exclusively for DTL - Django Template Language)
- **CSS Validator**: Passed W3C CSS validation with no errors

#### Manual Testing
**Core Functionality:**
- User registration and login process
- Recipe CRUD operations (create, read, update, delete)
- Dynamic ingredient management with add/remove functionality
- Image upload via Cloudinary
- Recipe filtering by meal type, difficulty, and dietary restrictions
- Responsive design across different screen sizes
- Guest user access to browse recipes without login
- Recipe pagination with multiple entries

**Device Testing**
The responsive design was tested primarily on desktop during development, with mobile and tablet views checked using browser developer tools. The sidebar navigation switches to an off-canvas menu on smaller screens, and the ingredient forms adapt well to different screen sizes.

**Browser Testing**
Tested functionality across Chrome (main development browser), Firefox, and Edge to ensure cross-browser compatibility.

#### Lighthouse Testing
All lighthouse tests, mobile and desktop presented satisfying results that averaged on a score above 90. The only issue I found with the lighthouse tests was an issue which I couldnt understand why was showing and how to fix/avoid:
<br>
<strong>
There were issues affecting this run of Lighthouse:

The page may not be loading as expected because your test URL (https://aunties-cookbook-1fa7efd3561a.herokuapp.com/recipes/classic-creamy-egg-tuna-wrap/edit/) was redirected to https://aunties-cookbook-1fa7efd3561a.herokuapp.com/login/?next=/recipes/classic-creamy-egg-tuna-wrap/edit/. Try testing the second URL directly.
<br>
<strong>
AND
</strong>
<br>
<strong>
There were issues affecting this run of Lighthouse:

The page may not be loading as expected because your test URL (https://aunties-cookbook-1fa7efd3561a.herokuapp.com/recipes/add-recipe/) was redirected to https://aunties-cookbook-1fa7efd3561a.herokuapp.com/login/?next=/recipes/add-recipe/. Try testing the second URL directly.
</strong>
</strong>

Performance metrics tested:
- Page load times
- Image optimization through Cloudinary
- Static file delivery via WhiteNoise

## Known Issues & Bug Fixes

### Resolved Issues

#### 1. Ingredient Form Management
**Issue**: Dynamic ingredient forms not updating correctly when adding/removing ingredients.
**Solution**: Implemented proper form indexing and DOM manipulation in JavaScript.

#### 2. Slug Generation
**Issue**: Recipe slugs not generating unique values for similar titles.
**Solution**: Added counter-based uniqueness check in recipe creation view.

#### 3. Mobile Navigation
**Issue**: Navigation menu not displaying correctly on mobile devices.
**Solution**: Implemented Bootstrap off-canvas menu for mobile screens.

#### 4. Recipe Difficulty Display
**Issue**: `recipe.get_difficulty_display` was not parsing the backend data due to indentation issues caused by auto code formatting.
**Solution**: Fixed template indentation to properly display difficulty levels.

#### 5. Filter State Persistence with Pagination
**Issue**: Applied filters were being reset when users navigated between pages in the recipe list.
**Solution**: Implemented URL parameter preservation to maintain filter state across pagination.

#### 6. Ingredients Form & File Upload Checkbox
**Issue**: Ingredients form has a checkbox, it is also present on the image file upload form input.
**Solution**: I have been unable to find a way to target and remove the checkboxes.

## Credits & Acknowledgments

### AI Assistance
- **Gemini**: Used for code generation assistance, particularly for:
  - Sample recipe data generation (`load_sample_recipes.py` management command)
  - Dynamic ingredient management functionality
  - Code in the template and JS/View for fixing the filters resetting during recipe list pagination was sorted with AI assistance

### Development Resources
- **Django Documentation**: Framework Docs and CI Modules
- **Bootstrap 5 Documentation**: UI components
- **MDN Web Docs**
- **Stack Overflow**

### Educational Support
- **Code Institute**: Full Stack Development curriculum and project guidance
- **Django Tutorial**: Step-by-step framework learning

### Third-Party Services & Libraries
- **Cloudinary**: Image storage and management
- **Heroku**: Application hosting platform
- **Font Awesome**: Icon library
- **Bootstrap**: CSS framework
- **Django Widget Tweaks**: Form styling enhancement


### Content & Design
- **Sample Recipes**: Created using AI assistance for testing purposes
- **Color Palette**: Inspired by traditional cookbook aesthetics
- **Mockup Images**: Generated using Website Mockup Generator


### Acknowledgments
- **Code Institute Mentors**: Technical guidance throughout development
- **Testing Volunteers**: Friends and family who tested my application

