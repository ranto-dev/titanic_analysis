Pour analyser les relations entre les passagers à bord du Titanic, l'Analyse en Composantes Principales (ACP ou PCA en anglais) est une méthode idéale si l'on cherche à réduire la dimensionnalité de données multivariées tout en préservant autant d'information que possible. L'ACP peut être utilisée pour déterminer si des relations sous-jacentes existent dans les données des passagers du Titanic.

### Objectif

L'objectif ici est de déterminer si l'ACP peut révéler des relations intéressantes entre différentes variables (comme l'âge, le sexe, la classe, le tarif, etc.) des passagers à bord du Titanic. Pour ce faire, nous allons suivre ces étapes en Python :

1. **Chargement des données** : Utiliser un dataset comme celui de `Titanic` disponible sur des plateformes comme Kaggle.
2. **Préparation des données** : Traitement des données manquantes, des variables catégorielles et des transformations nécessaires.
3. **Application de l'ACP** : Réduction de la dimensionnalité pour analyser les relations entre les variables.
4. **Visualisation des résultats** : Projeter les passagers dans un espace réduit (2D ou 3D) pour observer les groupes ou relations.

### Étape 1 : Charger les données

```python
import pandas as pd
import numpy as np

# Charger le jeu de données Titanic
data = pd.read_csv('titanic.csv')

# Afficher les premières lignes
data.head()
```

### Étape 2 : Préparer les données

Avant d'appliquer l'ACP, il est important de traiter les données. Cela inclut la gestion des valeurs manquantes et la transformation des variables catégorielles.

```python
# Traitement des données manquantes
data = data.fillna(data.mean())  # Remplir les valeurs manquantes par la moyenne (pour les colonnes numériques)

# Transformation des variables catégorielles (exemple : 'Sex' et 'Embarked')
data['Sex'] = data['Sex'].map({'male': 0, 'female': 1})
data['Embarked'] = data['Embarked'].map({'C': 0, 'Q': 1, 'S': 2})

# Sélectionner les colonnes pertinentes pour l'ACP
features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']

# Normalisation des données avant l'ACP
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data[features].dropna())
```

### Étape 3 : Appliquer l'ACP

Maintenant que les données sont prêtes, nous pouvons appliquer l'ACP pour réduire la dimensionnalité et analyser les relations entre les variables.

```python
from sklearn.decomposition import PCA

# Appliquer l'ACP
pca = PCA(n_components=2)  # Réduire les données à 2 dimensions
pca_result = pca.fit_transform(data_scaled)

# Visualiser la variance expliquée par chaque composante
print(f"Variance expliquée par la première composante : {pca.explained_variance_ratio_[0]:.2f}")
print(f"Variance expliquée par la deuxième composante : {pca.explained_variance_ratio_[1]:.2f}")
```

### Étape 4 : Visualiser les résultats

Nous pouvons maintenant visualiser les résultats de l'ACP dans un espace réduit à deux dimensions (2D) pour observer d'éventuelles relations entre les passagers.

```python
import matplotlib.pyplot as plt

# Créer un DataFrame pour les résultats PCA
pca_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])

# Visualisation
plt.figure(figsize=(10, 6))
plt.scatter(pca_df['PC1'], pca_df['PC2'], c=data['Survived'], cmap='viridis', alpha=0.6)
plt.title('Projection des passagers du Titanic dans l\'espace PCA')
plt.xlabel('Première composante principale')
plt.ylabel('Deuxième composante principale')
plt.colorbar(label='Survécu (0 = non, 1 = oui)')
plt.show()
```

### Conclusion

- **Analyse des résultats** : Vous pouvez examiner les composants principaux et la variance expliquée par chaque composante. Si les passagers sont bien séparés selon les composants principaux, cela pourrait indiquer qu'il existe une structure ou une relation sous-jacente intéressante dans les données.
- **Visualisation** : Les points colorés dans la visualisation montrent la relation entre la survie (variable cible) et les autres caractéristiques des passagers. Si des clusters apparaissent, cela pourrait suggérer des facteurs qui influencent la survie (par exemple, les passagers de première classe qui ont survécu).

En résumé, l'ACP est un excellent outil pour identifier des relations latentes dans des ensembles de données multivariées comme celle des passagers du Titanic. L'analyse visuelle peut vous aider à mieux comprendre les groupes et les tendances dans les données.

---

Pour créer une animation de la projection des passagers du Titanic dans un espace réduit à deux dimensions, on peut utiliser la bibliothèque `matplotlib.animation` en Python. L'animation peut, par exemple, animer la couleur des points en fonction de la survie des passagers.

Voici un exemple pour animer la visualisation des résultats de l'ACP, avec une légère animation qui pourrait montrer le passage d'un état à un autre (par exemple, en modifiant les couleurs au fur et à mesure).

### Code pour l'animation

```python
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Créer une figure et des axes pour l'animation
fig, ax = plt.subplots(figsize=(10, 6))

# Créer un DataFrame pour les résultats PCA
pca_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])

# Initialiser un scatter plot (sans points au départ)
scatter = ax.scatter([], [], c=[], cmap='viridis', alpha=0.6)

# Ajouter des labels et un titre
ax.set_title('Projection des passagers du Titanic dans l\'espace PCA')
ax.set_xlabel('Première composante principale')
ax.set_ylabel('Deuxième composante principale')

# Définir la fonction d'initialisation pour l'animation
def init():
    scatter.set_offsets([])  # Initialiser avec un graphique vide
    return scatter,

# Fonction pour mettre à jour les points de l'animation
def update(frame):
    # Colorier les points en fonction de la survie, progressivement
    scatter.set_offsets(pca_df[['PC1', 'PC2']].iloc[:frame])  # Ajouter plus de points à chaque frame
    scatter.set_array(data['Survived'].iloc[:frame].values)  # Mettre à jour les couleurs
    return scatter,

# Créer l'animation avec 100 frames (par exemple)
ani = FuncAnimation(fig, update, frames=len(pca_df), init_func=init, blit=True, interval=30)

# Afficher l'animation
plt.show()
```

### Explication du Code

1. **Création de la figure** : Nous utilisons `matplotlib` pour créer une figure et un axe sur lequel nous afficherons les résultats de l'ACP.
2. **Initialisation du graphique** : `scatter.set_offsets([])` initialise un graphique vide.
3. **Mise à jour des points** : La fonction `update(frame)` est appelée à chaque itération de l'animation pour afficher progressivement les points et changer leur couleur en fonction de la variable cible (ici `Survived`).
4. **Animation avec `FuncAnimation`** : Nous utilisons la classe `FuncAnimation` de `matplotlib.animation` pour créer l'animation. La fonction `update` est appelée pour chaque frame.

### Remarque

Assurez-vous que vous avez les bonnes bibliothèques installées (comme `matplotlib` et `numpy`). Pour afficher cette animation, vous devez exécuter le code dans un environnement supportant les animations (comme un notebook Jupyter ou un script Python avec un environnement graphique).

Si vous souhaitez que l'animation ait un effet plus dynamique, vous pouvez ajuster la vitesse, les couleurs, ou l'ordre d'apparition des points.

---------------------

## Tour de hanoi

Voici un exemple de code Python pour résoudre le problème du **Tour de Hanoi** avec une interface utilisateur utilisant **Flet**. Ce projet implique à la fois une logique de résolution du problème (solution à l'aide de récursion) et une interface graphique pour interagir avec l'utilisateur.

### Prérequis

1. **Python 3.x**
2. **Installation de Flet** : Flet est une bibliothèque pour créer des applications interactives à l'aide de Python. Vous pouvez l'installer avec `pip` :
   ```bash
   pip install flet
   ```

### Structure du projet

1. **Logique du Tour de Hanoi** : Utilisation de la récursion pour déplacer les disques entre trois tiges.
2. **Interface graphique avec Flet** : Créer une interface simple pour montrer les tiges et les disques et suivre les étapes de la solution.

### 1. **Logique de Résolution du Problème de Tour de Hanoi**

La résolution du problème des tours de Hanoi se fait de manière récursive. L'idée de base est de déplacer tous les disques d'une tige source vers une tige destination, en utilisant une tige auxiliaire pour aider au déplacement. Le cas de base de cette récursion est lorsque le nombre de disques est 1.

Voici une implémentation simple du problème avec une approche récursive.

### 2. **Interface Flet**

Flet nous permet de créer des interfaces graphiques en utilisant des composants simples. Nous allons afficher les trois tiges et les disques, et visualiser les étapes de résolution.

### Code Source

```python
import flet as ft

# Logique du Tour de Hanoi
def hanoi(n, source, target, auxiliary, moves):
    if n == 1:
        moves.append((source, target))
    else:
        hanoi(n-1, source, auxiliary, target, moves)
        moves.append((source, target))
        hanoi(n-1, auxiliary, target, source, moves)

# Interface Flet
def main(page: ft.Page):
    # Configuration initiale des tiges et des disques
    num_disks = 3  # Nombre de disques (modifiez-le pour tester avec plus de disques)
    moves = []  # Liste des mouvements pour la solution
    hanoi(num_disks, 'A', 'C', 'B', moves)

    # État initial des tiges
    rods = {
        'A': list(range(num_disks, 0, -1)),  # Tige source avec les disques
        'B': [],  # Tige auxiliaire vide
        'C': [],  # Tige destination vide
    }

    # Crée un affichage pour les tiges
    def create_rods_display():
        return [
            ft.Column(
                [
                    ft.Row([ft.Text("Rod " + rod) for rod in ["A", "B", "C"]], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([
                        ft.Column([ft.Text(str(disk)) for disk in rods[rod]], alignment=ft.MainAxisAlignment.CENTER)
                    ]) for rod in ["A", "B", "C"]
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ]

    # Affichage de l'interface
    page.add(ft.Column([
        ft.Text("Tour de Hanoi - Résolution"),
        *create_rods_display(),
        ft.ElevatedButton("Commencer", on_click=lambda e: start_game(page, moves, rods))
    ]))

    # Démarre la résolution du jeu
    def start_game(page, moves, rods):
        # Animer les déplacements des disques
        for move in moves:
            source, target = move
            # Déplacer le disque de source à target
            disk = rods[source].pop()
            rods[target].append(disk)
            page.update()  # Met à jour l'interface après chaque mouvement
            page.add(ft.Text(f"Déplacement du disque {disk} de {source} vers {target}"))
            page.update()
        page.add(ft.Text("Résolution terminée !"))

# Lancer l'application
ft.app(target=main)
```

### Explication du Code :

1. **Fonction `hanoi(n, source, target, auxiliary, moves)`** : Cette fonction résout le problème des tours de Hanoi de manière récursive et enregistre chaque mouvement dans la liste `moves`. Le principe est de déplacer un disque à la fois et de faire appel à la fonction récursivement pour réduire le nombre de disques.

2. **Fonction `main(page)`** : C'est la fonction principale qui crée l'interface utilisateur à l'aide de Flet. Elle configure les trois tiges (`A`, `B`, `C`) et initie le problème avec un nombre fixe de disques (3 dans ce cas). Elle appelle également `start_game()` pour commencer l'animation des mouvements.

3. **Fonction `start_game(page, moves, rods)`** : Cette fonction anime le mouvement des disques entre les tiges. Chaque mouvement est effectué, et l'interface est mise à jour pour refléter les changements dans l'état des tiges.

4. **Interface Flet** :
   - Utilisation de `ft.Row` et `ft.Column` pour organiser les éléments de l'interface (textes, boutons, etc.).
   - Un bouton "Commencer" lance la résolution du problème de Hanoi et affiche les étapes dans l'interface.

### 3. **Lancer le Code**

Pour exécuter ce projet :

1. Installez Flet avec `pip install flet`.
2. Copiez le code dans un fichier Python, par exemple `hanoi.py`.
3. Exécutez le fichier en utilisant Python :
   ```bash
   python hanoi.py
   ```
   Cela ouvrira une fenêtre avec l'interface graphique et animera la solution du problème des tours de Hanoi.

### Conclusion

Ce projet utilise **Flet** pour créer une interface interactive et visuelle qui résout le **problème des tours de Hanoi**. Vous pouvez ajuster le nombre de disques pour tester le programme avec différentes tailles de problèmes. L'animation de la solution montre comment les disques se déplacent entre les tiges.
