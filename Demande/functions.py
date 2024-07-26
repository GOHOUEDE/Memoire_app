import shap
import pandas as pd
from django.shortcuts import render ,get_object_or_404
from  .models import Demande
variables = [
    "montant_sollicite",
    "duree_pret_souhaitee",
    "taux_interet",
    "Ssecteur_activite",
    "nbr_mois_cotisation",
    "nbr_credits_octroyes",
    "rapport_rembourse",
     "rapport_rembour"]
import shap

def expliquer(demande, mod,seuil=0.1):
    st_N = {}
    st_O = {}
    
    # Création de l'explainer
    explainer = shap.TreeExplainer(mod)
    
    # Calcul des valeurs SHAP pour les instances de test
    Shap = explainer.shap_values(demande)
    Shap = Shap[0,:]
    
    # Non abordables
    for o, variable in enumerate(variables):
        if abs(Shap[o]) >= seuil:
            if Shap[o] > 0:
                st_N[variable] = Shap[o]
            else:
                st_O[variable] = Shap[o]
    
    st_N = dict(sorted(st_N.items(), key=lambda item: item[1], reverse=True))
    st_O = dict(sorted(st_O.items(), key=lambda item: item[1]))
    
    return st_N, st_O

# Exemple d'utilisation:
# variables = ['var1', 'var2', 'var3', ...]
# demande = ...
# mod = ...
# st_N, st_O = expliquer(demande, mod, variables, seuil=0.01)

def recom(id,x,mod):
    instance = get_object_or_404(Demande, pk=id)
    demande=x
    (N,O)=expliquer(demande,mod)
    int_N=next(iter(N))
    int_O=next(iter(O))
    text_N=[]
    text_O=[]
    for int_N in N :
        if int_N =='nbr_mois_cotisation':
            text_N.append("le client ne dispose pas suffisamment d epargne cotisé")
        if int_N =='montant_sollicite':
            text_N.append("la somme demandée  grande pour cette demande ?  (j'y travaille)")    
        if int_N =='rapport_rembourse':
            if instance.nbr_credits_octroyes != 0:
                text_N.append("le client n'a pas entierement payé ses credits passés ")
            else:
                text_N.append("C'est le premier credit demandé de ce client ,faites d'autres vérification ")
        if int_N =='rapport_rembour':
            if instance.nbr_credits_octroyes != 0:
                text_N.append("le client a demandé une somme qu'il n'avait l'habitude d'emprunter ")
            else:
                text_N.append("Somme assez grande pour un premier credit ")    
        
            
        if int_N =='taux_interet':
            if instance.taux_interet < 18: 
                text_N.append("Taux d'inderet à etudier ")     
        if int_N =='ssecteur_activite	':
            text_N.append("la majorité des clients de ce sous secteur avec ces caractéristique n'ont pas soldé ")
        if int_N =='nbr_credits_octroyes':
            if instance.nbr_credits_octroyes < 3: 
                text_N.append("Pas trop de credit à son actif ")    
    for int_O in O :
        if int_O =='nbr_mois_cotisation':
            text_O.append("le client  suffisamment d epargne cotisé pour ce credit")
        #if int_O =='montant_sollicite':
            #if "le client demande beaucoup trop que ce qu'il avait l'habitude d'emprunter " in text_N:
            #continue
            #else
            #"le client demande beaucoup trop que ce qu'il avait l'habitude d'emprunter "
        if int_O =='rapport_rembourse':
            if instance.nbr_credits_octroyes != 0:
                text_O.append("le client a  entierement payé ses credits passés ")
            else:
                text_O.append("Premier credit mais promettant  ,faites d'autres vérification ")
            
        if int_O =='rapport_rembour':
            if instance.nbr_credits_octroyes != 0:
                text_O.append("le client a demandé une somme qu'il avait l'habitude d'emprunter ")
            else:
                text_O.append("Somme assez grande pour un premier credit ")
            
        if int_O =='taux_interet':
            if instance.taux_interet > 18: 
                text_O.append("Taux d'inderet adapté ")     
        #if int_O =='ssecteur_activite	':
            #text_O.append("la majorité des clients de ce sous secteur avec ces caractéristique ont soldé ")
        if int_O =='duree_pret_souhaitee':
            text_O.append("Durée de pret adaptée") 
        if int_O =='nbr_credits_octroyes':
            if instance.nbr_credits_octroyes > 3: 
                text_O.append("Assez de credit à son actif pour ne pas se tromper")    
    return (text_N,text_O)            
