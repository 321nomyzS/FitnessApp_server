document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM w pełni załadowany i przetworzony');
    const container = document.getElementById('exercises-container');
    let exerciseId = 0;

    const defaultExercise = document.getElementById('exercise');
    if (defaultExercise) {
        exerciseId++;
        const newExercise = createExerciseElement(exerciseId, defaultExercise.cloneNode(true));
        if (newExercise) {
            container.appendChild(newExercise);
        }
    } else {
        console.error('Nie znaleziono domyślnego ćwiczenia');
    }

    document.getElementById('add-exercise').addEventListener('click', function () {
        console.log('Dodaj ćwiczenie kliknięte');
        exerciseId++;
        const newExercise = createExerciseElement(exerciseId, defaultExercise.cloneNode(true));
        if (newExercise) {
            container.appendChild(newExercise);
        }
    });

    function createExerciseElement(id, element) {
        console.log('Tworzenie elementu ćwiczenia', id);
        element.id = 'exercise-' + id;
        element.style.display = "";

        const deleteButton = element.querySelector('.delete-button');
        const duplicateButton = element.querySelector('.duplicate-button');
        const selectElement = element.querySelector('select');
        const textAreaElement = element.querySelector('textarea');

        // Sprawdzanie czy elementy istnieją
        if (!deleteButton || !duplicateButton || !selectElement || !textAreaElement) {
            console.error('Nie znaleziono jednego z wymaganych elementów', {
                deleteButton,
                duplicateButton,
                selectElement,
                textAreaElement
            });
            return null;
        }

        deleteButton.id = 'exercise-delete-' + id;
        duplicateButton.id = 'exercise-duplicate-' + id;
        selectElement.name = 'exercise-id-' + id;
        textAreaElement.name = 'exercise-tips-' + id;

        deleteButton.addEventListener('click', function () {
            console.log('Usuń ćwiczenie kliknięte', id);
            element.remove();
        });

        duplicateButton.addEventListener('click', function () {
            console.log('Duplikuj ćwiczenie kliknięte', id);
            exerciseId++;
            const duplicatedExercise = createExerciseElement(exerciseId, element.cloneNode(true));

            if (!duplicatedExercise) {
                console.error('Błąd podczas duplikacji ćwiczenia', id);
                return;
            }

            // Logowanie wartości oryginalnego elementu select
            console.log("Oryginalna wartość select:", selectElement.value);

            // Ustawienie wartości dla duplikowanego elementu select
            const originalSelectValue = selectElement.value;
            const duplicatedSelectElement = duplicatedExercise.querySelector('select');
            duplicatedSelectElement.name = 'exercise-id-' + exerciseId; // Poprawna nazwa dla duplikowanego elementu
            duplicatedSelectElement.value = originalSelectValue;

            // Upewnij się, że wartość jest poprawnie ustawiona
            if (duplicatedSelectElement.value !== originalSelectValue) {
                for (let i = 0; i < duplicatedSelectElement.options.length; i++) {
                    if (duplicatedSelectElement.options[i].value === originalSelectValue) {
                        duplicatedSelectElement.selectedIndex = i;
                        break;
                    }
                }
            }

            // Logowanie wartości zduplikowanego elementu select
            console.log("Zduplikowana wartość select:", duplicatedSelectElement.value);

            // Ustawienie wartości dla duplikowanego pola textarea
            const originalTextAreaValue = textAreaElement.value;
            const duplicatedTextAreaElement = duplicatedExercise.querySelector('textarea');
            duplicatedTextAreaElement.name = 'exercise-tips-' + exerciseId; // Poprawna nazwa dla duplikowanego elementu
            duplicatedTextAreaElement.value = originalTextAreaValue;

            // Logowanie wartości zduplikowanego elementu textarea
            console.log("Oryginalna wartość textarea:", textAreaElement.value);
            console.log("Zduplikowana wartość textarea:", duplicatedTextAreaElement.value);

            container.appendChild(duplicatedExercise);
        });

        return element;
    }
});

// Mechanizm przełączania pól
function toggleFields() {
    console.log('Wywołanie toggleFields');
    const isPersonalTraining = document.getElementById('personal-training-radio').checked;
    document.getElementById('training-date').disabled = !isPersonalTraining;
    document.getElementById('training-person').disabled = !isPersonalTraining;
}

document.getElementById('personal-training-radio').addEventListener('change', toggleFields);
document.getElementById('general-training-radio').addEventListener('change', toggleFields);
window.onload = toggleFields;
