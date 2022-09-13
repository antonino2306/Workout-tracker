let addEx = document.querySelector(".add-exercise");
        let form = document.querySelector("[name = 'scheda']")
        let exerciseBox = document.querySelector(".exercise-box");
        let counter = 1;


        addEx.addEventListener('click', function() {
            let exercise = document.createElement("div");
            exercise.setAttribute('class', "exercise-box");

            let name = document.createElement("input");
            name.setAttribute("class", "exercise-input");
            name.setAttribute("type", "text");
            name.setAttribute("name", `exercise-name-${counter}`);
            name.setAttribute("placeholder", "Nome esercizio");
            name.setAttribute("autocomplete", "off");

            let data = document.createElement("div");
            data.setAttribute('class', "table three");

            let sets = document.createElement("input");
            sets.setAttribute("type", "number");
            sets.setAttribute("name", `sets-${counter}`);
            sets.setAttribute("placeholder", "Sets");

            let reps = document.createElement("input");
            reps.setAttribute("type", "number");
            reps.setAttribute("name", `reps-${counter}`);
            reps.setAttribute("placeholder", "Reps");

            let rest = document.createElement("input");
            rest.setAttribute("type", "number");
            rest.setAttribute("name", `rest-${counter}`);
            rest.setAttribute("placeholder", "Rest");

            form.appendChild(exercise);
            exercise.appendChild(name);
            exercise.appendChild(data);
            data.appendChild(sets);
            data.appendChild(reps);
            data.appendChild(rest);
 
            counter++;
                       
        });