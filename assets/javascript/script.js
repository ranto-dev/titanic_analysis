const toggle = document.getElementById("toggle-form");

toggle.addEventListener("click", async (e) => {
  e.preventDefault();

  const modal = document.getElementById("modal");
  const close = document.getElementById("close_modal");
  const modal_body = document.getElementById("modal_body");

  const age = document.getElementById("age");
  var ageValue = age.value;

  // Tester si l'age est inférieure à 0, si oui on retour une erreur sinon on le valide
  if (ageValue <= 0) {
    alert(
      `Please! ${ageValue} n'est pas une age exact, veuillez resaisir un autre 🤭`
    );
  } else {
    //Récupération des valeurs du formulaire: La classe du passager et le genre
    const SelectedClassePassenger = document.querySelector(
      'input[name="classe"]:checked'
    );
    const classeValue = SelectedClassePassenger.value;
    const SelectedSexe = document.querySelector('input[name="sexe"]:checked');
    const sexeValue = SelectedSexe.value;

    let classe;
    if (classeValue == "classe1") {
      classe = 1;
    } else if (classe == "classe2") {
      classe = 2;
    } else {
      classe = 3;
    }

    const bodyToAPI = {
      classe_passager: classe,
      sexe: sexeValue,
      age: ageValue,
    };

    console.log(bodyToAPI);

    ageValue = "";

    function modal_content_1() {
      return `
        <h3 class="text-center">🥳🥳🥳🤭😂</h3>
        <p class="text-center">
          Toute mes félicitation, vous avez survéçu au naufrage du
          navire si vous étiez sur le Titanic (une sacré cout de chance ou
          ... "Fitahin'Andriamanitra aby zany")
        </p>
      `;
    }

    function modal_content_0() {
      return `
        <h3 class="text-center">😵🤧🤧🥺🫣</h3>
        <p class="text-center">
          Ooohhh!!! Toute mes condoléances bros, j'assisterai à ton
          funéraille si je suis libre ce week-end! Vous etes l'un des
          victimes qui n'a pas survéçu au naufrage du Titanic
        </p>
      `;
    }

    await fetch("http://127.0.0.1:8000/predict/", {
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify(bodyToAPI),
    })
      .then((res) => res.json())
      .then((res) => {
        const predictionResult = parseInt(res.prediction);
        if (predictionResult == 1) {
          modal_body.innerHTML = modal_content_1();
        } else {
          modal_body.innerHTML = modal_content_0();
        }
        modal.style.display = "block";
      });

    close.addEventListener("click", () => {
      modal.style.display = "none";
    });
  }
});
