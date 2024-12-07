const counterId = document.querySelector('#counter');

const ingredientsContainer = document.querySelector('.form__field-group-ingredientes-container');
const nameIngredient = document.querySelector('#nameIngredient');
const formDropdownItems = document.querySelector('.form__dropdown-items');
const cantidadVal = document.querySelector('#cantidadVal');
const cantidad = document.querySelector('#cantidad')
const addIng = document.querySelector('#addIng');

const api = new Api(apiUrl);
const header = new Header(counterId);

const defineInitialIndex = function () {
    const ingredients = ingredientsContainer.querySelectorAll('.form__field-item-ingredient')
    if (ingredients.length === 0) { return 1 }
    const data = Array.from(ingredients).map(item => {
        if (!item.getAttribute('id')) { return 0 }
        if (!item.getAttribute('id').split('_')[1]) { return 0 }
        return Number(item.getAttribute('id').split('_')[1])
    })
    data.sort((a, b) => a-b)
    return data[data.length - 1] + 1
}

function Ingredients() {
    const ingredientsContainer = document.querySelector('.form__field-group-ingredientes-container');
    let cur = defineInitialIndex();
    // Функция для добавления ингредиента в DOM
    const addIngredientToDOM = (id, name, value, units) => {
        const elem = document.createElement('div');
        elem.classList.add('form__field-item-ingredient');
        elem.id = `ing_${id}`;
        elem.innerHTML = `<span> ${name} ${value}${units}</span> <span class="form__field-item-delete"></span>
                        <input id="nameIngredient_${id}" name="nameIngredient_${id}" type="hidden" value="${name}">
                        <input id="valueIngredient_${id}" name="valueIngredient_${id}" type="hidden" value="${value}">
                        <input id="unitsIngredient_${id}" name="unitsIngredient_${id}" type="hidden" value="${units}">`;
        ingredientsContainer.appendChild(elem);
    };
    // клик по элементам с сервера
    const dropdown = (e) => {
        if (e.target.classList.contains('form__item-list')) {
            nameIngredient.value = e.target.textContent;
            formDropdownItems.style.display = ''
            cantidadVal.textContent = e.target.getAttribute('data-val');
        }
    };
    // Добавление элемента из инпута
    const addIngredient = (e) => {
        if(nameIngredient.value && cantidad.value) {
            const data = getValue();
            addIngredientToDOM(cur, data.name, data.value, data.units);
            cur++;
        }
    };

    
    // удаление элемента

    const eventDelete = (e) => {
        if(e.target.classList.contains('form__field-item-delete')) {
            const item = e.target.closest('.form__field-item-ingredient');
            item.removeEventListener('click',eventDelete);
            item.remove()
        };
    };
    ingredientsContainer.addEventListener('click', eventDelete);
    // получение данных из инпутов для добавления
    const getValue = (e) => {
        const data = {
            name: nameIngredient.value,
            value: cantidad.value,
            units: cantidadVal.textContent
        };
        clearValue(nameIngredient);
        clearValue(cantidad);
        return data;
    };
    // очистка инпута
    const clearValue = (input) => {
        input.value = '';
    };
    return {
        clearValue,
        getValue,
        addIngredient,
        dropdown,
        addIngredientToDOM
    }
}

const cbEventInput = (elem) => {
    return api.getIngredients(elem.target.value).then( e => {
        if(e.length !== 0 ) {
            const items = e.map( elem => {
                return `<a class="form__item-list" data-val="${elem.dimension}"">${elem.title}</a>`
            }).join(' ')
            formDropdownItems.style.display = 'flex';
            formDropdownItems.innerHTML = items;
        }
    })
    .catch( e => {
        console.log(e)
    })
};

const eventInput = debouncing(cbEventInput, 1000);


const ingredients = Ingredients();

if (typeof existingIngredients !== 'undefined' && existingIngredients.length > 0) {
    existingIngredients.forEach(function (ingredient) {
        ingredients.addIngredientToDOM(ingredients.cur, ingredient.name, ingredient.value, ingredient.units);
        ingredients.cur++;
    });
}

// После предзаполнения обновляем `cur`
let cur = defineInitialIndex();
ingredients.cur = cur;

nameIngredient.addEventListener('input', eventInput);
// вешаем слушатель на элементы с апи
formDropdownItems.addEventListener('click', ingredients.dropdown);
// вешаем слушатель на кнопку
addIng.addEventListener('click', ingredients.addIngredient);

const form = document.getElementById('recipe_form');

form.addEventListener('submit', function(event) {
    console.log('Обработчик submit сработал');
    // Соберите все ингредиенты
    const ingredients = [];
    const ingredientElements = ingredientsContainer.querySelectorAll('.form__field-item-ingredient');
    ingredientElements.forEach(elem => {
        const name = elem.querySelector('input[name^="nameIngredient_"]').value;
        const value = elem.querySelector('input[name^="valueIngredient_"]').value;
        const units = elem.querySelector('input[name^="unitsIngredient_"]').value;
        ingredients.push({ name: name, value: value, units: units });
    });
    // Поместите данные в скрытое поле
    document.getElementById('ingredients_data').value = JSON.stringify(ingredients);
});

