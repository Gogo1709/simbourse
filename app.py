from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

capital_depart = 10000
prix_sequences = [
    {'action1': 25, 'action2': 45},
    {'action1': 15, 'action2': 58},
    {'action1': 33, 'action2': 57},
    {'action1': 15, 'action2': 58},
    {'action1': 15, 'action2': 58},
    {'action1': 15, 'action2': 58},
    {'action1': 15, 'action2': 58},
    {'action1': 15, 'action2': 58},
    {'action1': 15, 'action2': 58}
]
sequence_actuelle = 0
prix_actuel = prix_sequences[sequence_actuelle]

actions_achetees = {'action1': 0, 'action2': 0}
actions_vendues = {'action1': 0, 'action2': 0}

def calculer_actions_detenues():
    nb_action1 = actions_achetees['action1'] - actions_vendues['action1']
    nb_action2 = actions_achetees['action2'] - actions_vendues['action2']
    return {'action1': nb_action1, 'action2': nb_action2 }

@app.route('/', methods=['GET', 'POST'])
def index():
    global capital_depart, sequence_actuelle, prix_actuel, actions_achetees, actions_vendues

    if request.method == 'POST':
        action = request.form['action']
        quantite = int(request.form['quantite'])
        type_action = request.form['type_action']  # Utiliser directement la valeur envoyée par le formulaire
        prix_action = prix_actuel[type_action]

        if action == 'acheter':
            montant_total = prix_action * quantite
            if capital_depart >= montant_total:
                capital_depart -= montant_total
                actions_achetees[type_action] += quantite
            else:
                print('Capital insuffisant')
        elif action == 'vendre':
            if actions_achetees[type_action] - actions_vendues[type_action] >= quantite:
                capital_depart += prix_action * quantite
                actions_vendues[type_action] += quantite
            else:
                print('Vous ne pouvez pas vendre plus d\'actions que vous possédez')

    actions_detenues = calculer_actions_detenues()
    return render_template('index.html', capital=capital_depart, prix_actions=prix_actuel,
                           actions_detenues=actions_detenues)

@app.route('/terminer', methods=['POST'])
def terminer_sequence():
    global sequence_actuelle, prix_actuel, capital_depart

    sequence_actuelle += 1
    if sequence_actuelle < len(prix_sequences):
        prix_actuel = prix_sequences[sequence_actuelle]
        # Réinitialisation n'est pas nécessaire ici, elle se fait au début de la session
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
