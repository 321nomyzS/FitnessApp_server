// Add exercise mechanic
document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('exercises-container');
    let exerciseId = 0;

    // Deafult element
    exerciseId++;
    const defaultExercise = createExerciseElement(exerciseId, document.getElementById('exercise').cloneNode(true));
    container.appendChild(defaultExercise);

    //
    document.getElementById('add-exercise').addEventListener('click', function () {
        exerciseId++;
        const newExercise = createExerciseElement(exerciseId, document.getElementById('exercise').cloneNode(true));
        container.appendChild(newExercise);
    });

    function createExerciseElement(id, element) {
        element.id = 'exercise-' + id;
        element.style.display = "";

        element.querySelector('.delete-button').id = 'exercise-delete-' + id;
        element.querySelector('.duplicate-button').id = 'exercise-duplicate-' + id;

        element.querySelector('select').name = 'exercise-id-' + id;
        element.querySelector('textarea').name = 'exercise-tips-' + id;

        element.querySelector('.delete-button').addEventListener('click', function () {
            element.remove();
        });
        element.querySelector('.duplicate-button').addEventListener('click', function () {
            exerciseId++;
            const duplicatedExercise = createExerciseElement(exerciseId, element.cloneNode(true));
            container.appendChild(duplicatedExercise);
        });

        return element;
    }
});


// Toggle mechanic
function toggleFields() {
    const isPersonalTraining = document.getElementById('personal-training-radio').checked;
    document.getElementById('training-date').disabled = !isPersonalTraining;
    document.getElementById('training-person').disabled = !isPersonalTraining;
}

document.getElementById('personal-training-radio').addEventListener('change', toggleFields);
document.getElementById('general-training-radio').addEventListener('change', toggleFields);
window.onload = toggleFields;
