// Récupération des données
// const classe_passager = document.getElementById("classe");
const homme = document.getElementById("homme");
const femme = document.getElementById("femme");
if (homme.currentTarget.checked) {
    console.log(`${homme.value}`)
} else {
    console.log(`${femme.value}`)
}
const age = document.getElementById("age");
const toggle = document.getElementById("toggle-form");

toggle.addEventListener("click", () => {
  alert(`handleClick\n Age: ${age.value}\n Sexe: ${sexe.value}`);
});

/*
// Fetch API method
async function titanic_predict() {
  const body = {
    classe_passager: 2,
    sexe: "femme",
    age: 54,
  };

  await fetch("http://127.0.0.1:8000/predict", {
    method: "POST",
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify(body),
  })
    .then((res) => res.json())
    .then((res) => {
      console.log(res);
      document.getElementById("myModal2").style.display = "block";
      document.getElementById("variety").innerHTML = res.variety_of_iris;
    });
}*/
