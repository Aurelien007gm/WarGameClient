import tkinter as tk
from action import Action

import tkinter as tk
from tkinter import messagebox

class Form:
    def __init__(self,territory,server,view):
        self.root = tk.Tk()
        self.root.title("Sélection du Formulaire")

        description_label = tk.Label(self.root, text=f"This is territory {territory.name}")
        description_label.pack(pady=10)

        if(territory.eventOn):
            description_label = tk.Label(self.root, text=f"Event On !")
            description_label.pack(pady=10)

        description_label = tk.Label(self.root, text= territory.effect)
        description_label.pack(pady=10)

        # Boutons pour sélectionner le formulaire
        tk.Button(self.root, text="Déploiement", command=self.open_deploy_form).pack(pady=10)
        tk.Button(self.root, text="Attaque", command=self.open_attack_form).pack(pady=10)
        tk.Button(self.root, text="Transfert", command=self.open_transfer_form).pack(pady=10)
        tk.Button(self.root, text="Fermer", command=self.close_main_window).pack(pady=10)
        self.territory = territory # id and not instance of a territory
        self.server = server
        self.view = view
        self.run()

    def run(self):
        self.root.mainloop()

    def open_deploy_form(self):
        FormDeploy(self.root,self.territory,self.server)

    def open_attack_form(self):
        ##FormAttack(self.root,self.territory,self.server)

        self.view.viewhandler.SetAttack()
        self.view.viewhandler.SetSource(self.territory)
        self.close_main_window()

    def open_transfer_form(self):
        FormTransfer(self.root,self.territory,self.server,self.view)


    def close_main_window(self):
        self.root.destroy()


class FormDeploy:
    def __init__(self, parent,territory,server):
        self.server = server
        
        self.parent = parent
        self.form = tk.Toplevel(parent)
        self.territory = territory
        self.player = self.territory.owner
        self.form.title(f"Deployment Form - {self.territory.name}")

        # Variables pour le nombre de troupes
        self.field = tk.IntVar()
        self.navy = tk.IntVar()
        self.para = tk.IntVar()
        self.cost = tk.IntVar()
        self.money = tk.IntVar()

        #Tracabilité des modifications
        self.field.trace_add('write', self.Update)
        self.navy.trace_add('write', self.Update)
        self.para.trace_add('write', self.Update)


        # Initialisation de l'interface
        self.initialize_interface()

        self.form.mainloop()

    def initialize_interface(self):
        # Widgets pour sélectionner le nombre de troupes
        tk.Label(self.form, text="Troupes Terrestres:").grid(row=0, column=0, sticky=tk.W)
        tk.Spinbox(self.form, from_=0, to=999, textvariable=self.field).grid(row=0, column=1)

        tk.Label(self.form, text="Troupes Marines:").grid(row=1, column=0, sticky=tk.W)
        tk.Spinbox(self.form, from_=0, to=999, textvariable=self.navy).grid(row=1, column=1)

        tk.Label(self.form, text="Troupes Aériennes:").grid(row=2, column=0, sticky=tk.W)
        tk.Spinbox(self.form, from_=0, to=999, textvariable=self.para).grid(row=2, column=1)

        # Labels pour afficher le coût du déploiement et l'argent du joueur
        tk.Label(self.form, text="Coût du Déploiement:").grid(row=3, column=0, sticky=tk.W)
        tk.Label(self.form, textvariable=self.cost).grid(row=3, column=1)

        tk.Label(self.form, text="Argent du Joueur:").grid(row=4, column=0, sticky=tk.W)
        tk.Label(self.form, textvariable=self.money).grid(row=4, column=1)

        # Boutons pour valider le déploiement et fermer la fenêtre
        tk.Button(self.form, text="Valider Déploiement", command=self.ValidateDeployment).grid(row=5, column=0, columnspan=2)
        tk.Button(self.form, text="Fermer", command=self.form.destroy).grid(row=6, column=0, columnspan=2)
        self.error_label = tk.Label(self.form, text="Pas assez d'argent!", fg="white", bg="red")

    def ValidateDeployment(self):
        # Logique pour valider le déploiement, mettre à jour le territoire, etc.
        # Vous devrez adapter cette fonction selon les besoins spécifiques de votre jeu
        field = self.field.get()
        navy = self.navy.get()
        para = self.para.get()

        self.ComputeCost()

        if self.cost.get() > self.player.money:
            # Afficher un message d'erreur si le joueur n'a pas assez d'argent
            tk.Label(self.form, text="Pas assez d'argent!", fg="white", bg="red").grid(row=7, column=0, columnspan=2)
            self.field.set(0)
            self.navy.set(0)
            self.para.set(0)
            self.Update()
            return
        
                # Cacher le message d'erreur s'il était affiché
        self.error_label.grid_remove()

        # Mise à jour du territoire avec les nouvelles troupes
        self.territory.troop["field"] += field
        self.territory.troop["navy"] += navy
        self.territory.troop["para"] += para

        # Mise à jour de l'argent du joueur
        self.player.money -= self.cost.get()
        act = Action("Deploy",**{"t0":self.territory.id,"field":field,"navy":navy,"para":para})
        self.server.Call(act)
        self.form.destroy()

    def Update(self, *args):
        self.ComputeCost()
        self.money.set(self.player.money)




    def ComputeCost(self):
        price = {"field": 1000, "navy": 1500, "para": 2000}
        troops = {"field": self.field.get() or 0, "navy": self.navy.get()or 0, "para": self.para.get() or 0}
        cost = 0
        for key, value in troops.items():
            cost += price[key] * value

        # Mettre à jour la variable cost pour afficher le coût dans l'interface
        self.cost.set(cost)
  

class FormAttack:
    pass
class FormTransfer:
    def __init__(self, parent,territory,server,view):
        self.server = server
        self.view = view
        self.parent = parent
        self.form = tk.Toplevel(parent)
        self.territory = territory
        self.player = self.territory.owner
        self.form.title(f"Transfer Form - {self.territory.name}")

        # Variables pour le nombre de troupes
        self.field = tk.IntVar()
        self.navy = tk.IntVar()
        self.para = tk.IntVar()


        # Initialisation de l'interface
        self.initialize_interface()

        self.form.mainloop()

    def initialize_interface(self):
        # Widgets pour sélectionner le nombre de troupes
        tk.Label(self.form, text="Troupes Terrestres:").grid(row=0, column=0, sticky=tk.W)
        tk.Spinbox(self.form, from_=0, to=999, textvariable=self.field).grid(row=0, column=1)

        tk.Label(self.form, text="Troupes Marines:").grid(row=1, column=0, sticky=tk.W)
        tk.Spinbox(self.form, from_=0, to=999, textvariable=self.navy).grid(row=1, column=1)

        tk.Label(self.form, text="Troupes Aériennes:").grid(row=2, column=0, sticky=tk.W)
        tk.Spinbox(self.form, from_=0, to=999, textvariable=self.para).grid(row=2, column=1)


        # Boutons pour valider le déploiement et fermer la fenêtre
        tk.Button(self.form, text="ValiderTransfer", command=self.ValidateDeployment).grid(row=5, column=0, columnspan=2)
        tk.Button(self.form, text="Fermer", command=self.form.destroy).grid(row=6, column=0, columnspan=2)

    def ValidateDeployment(self):
        # Logique pour valider le déploiement, mettre à jour le territoire, etc.
        # Vous devrez adapter cette fonction selon les besoins spécifiques de votre jeu
        field = self.field.get()
        navy = self.navy.get()
        para = self.para.get()


        # Mise à jour du territoire avec les nouvelles troupes
        self.territory.troop["field"] -= field
        self.territory.troop["navy"] -= navy
        self.territory.troop["para"] -= para

        troop = {"field":field,"navy":navy,"para":para}
        self.view.viewhandler.SetTransfer(troop)
        self.view.viewhandler.SetSource(self.territory)
        self.form.destroy

class FormEnemy:
    def __init__(self,territory):
        self.root = tk.Tk()
        self.root.title("Territoire")

        description_label = tk.Label(self.root, text=f"This is territory {territory.name}")
        description_label.pack(pady=10)

        description_label = tk.Label(self.root, text= territory.effect)
        description_label.pack(pady=10)

        if(territory.eventOn):
            description_label = tk.Label(self.root, text=f"Event On !")
            description_label.pack(pady=10)


        tk.Button(self.root, text="Fermer", command=self.close_main_window).pack(pady=10)
        self.run()

    def run(self):
        self.root.mainloop()

    def close_main_window(self):
        self.root.destroy()

