from django.shortcuts import render ,get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.template.loader import render_to_string
from weasyprint import HTML
from  .models import Demande
import pickle
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import numpy as np
from django.http import JsonResponse
from .functions import recom
from .functions import expliquer
from .gemini import generate
secteur_to_index = {
    'ACT MENAGES EMPLOYEUR DE PERSONNEL DOMESTIQUE': 0,
    'ACTIVITES A CARACTERE COLLECTIF OU PERSONNEL': 1,
    "ACTIVITES D'ADMINISTRATIONS PUBLIQUES": 2,
    'ACTIVITES DE FABRICATION': 3,
    "ACTIVITES DE SANTE ET D'ACTION SOCIALE": 4,
    'ACTIVITES EXTRACTIVES': 5,
    'ACTIVITES FINANCIERES': 6,
    'AGRICULTURE, ELEVAGE, CHASSE ET SYLVICULTURE': 7,
    'AUTRES ACTIVITES': 8,
    'COMMERCE': 9,
    'CONSOMMATION': 10,
    'CONSTRUCTION': 11,
    'EDUCATION, ARTS ET CULTURE': 12,
    'HOTELS, RESTAURANTS ET TOURISME': 13,
    'IMMOBILIER, LOCATIONS ET SERVICES AUX ENTREPRISES': 14,
    'PECHE, PISCICULTURE, AQUACULTURE': 15,
    "PRODUCTION ET DISTRIBUTION D'ELECTRICITE, DE GAZ, ET D'EAU": 16,
    "REPARATION DE VEHICULE AUTOM ET D'ARTICLE DOMESTIQUE ": 17,
    'TRANSPORT, ACTIVITES AUXILIAIRES ET COMMUNICATIONS': 18
}
another_mapping = {
    'C': 0,
    'D': 1,
    'O': 2,
    'S': 3,
    'V': 4
}
#C:\Users\HOME\Documents\IA\App\app\Demande\ML_Model.pkl
chemin="./Demande/1pp_model.pkl"
with open(chemin,'rb') as f:
    mod=pickle.load(f)
    
def index(request):
    demandes={"Demandes":Demande.objects.all()}
    return render(request,"demande/index.html",demandes)

def non_traite(request):
    demandes={"Demandes":Demande.objects.all()}
    return render(request,"demande/non_traite.html",demandes)
def traite(request):
    demandes={"Demandes":Demande.objects.all()}
    return render(request,"demande/traite.html",demandes)
def valide(request):
    demandes={"Demandes":Demande.objects.all()}
    return render(request,"demande/valide.html",demandes)

def inwdex(request):
    cont={"Message":"C'est le  message fgf"}
    template =loader.get_template("demande/index.html")
    return HttpResponse(template.render(cont,request))




def get_data(request, id):
    data = {'message': 'Hello, World!'}
    instance = get_object_or_404(Demande, pk=id)
    instance.statut = 1
    instance.save()
    return JsonResponse(data)
def get_valide1(request, id):
    data = {'message': 'Hello, World!'}
    instance = get_object_or_404(Demande, pk=id)
    instance.statut_traite = 'accept'
    instance.save()
    return JsonResponse(data)
def get_valide2(request, id):
    data = {'message': 'Hello, World!'}
    instance = get_object_or_404(Demande, pk=id)
    instance.statut_traite = 'rejet'
    instance.save()
    return JsonResponse(data)

def evaluate_loan_request(id, mod, secteur_to_index, another_mapping):
    demande={"Dm":get_object_or_404(Demande,pk= id)}
    instance = get_object_or_404(Demande, pk=id)
    secteur = 2
    if instance.secteur_activite in secteur_to_index:
        secteur = secteur_to_index[instance.secteur_activite]
    if instance.situation_matrimoniale in another_mapping:
        r = another_mapping[instance.situation_matrimoniale]
        
    nboct=instance.nbr_credits_octroyes
    nbremb=instance.nbr_credits_rembourses
    if nboct != 0:
        rapport_rebourse=nbremb/nboct
    else:
        rapport_rebourse=0
    
    taux_interet=instance.taux_interet
    duree=instance.duree_pret_souhaitee
    montant_s=instance.montant_solicite
    montant_total=instance.montant_credits_accorde
    anc=instance.anciennete_agence
    if nboct != 0:
        rap_d = ((montant_total / nboct) - montant_s) / (montant_total / nboct)
    else:
        rap_d = 0
    # r=get_object_or_404(Demande.situation_matrimoniale,pk=id)
    nbr =instance.nombre_mois_cotisation
    x=[[ anc,montant_s,12,taux_interet,secteur,nbr,nboct,rapport_rebourse,rap_d]]
    pred=mod.predict(x)
    note=mod.predict_proba(x)[:,0] *100
    note =np.around(note).item()
    if(note>80):
        note=note-5
    demande['pred']=pred
    demande['note']=note

    (NN,OO)=expliquer(x,mod)
    demande['NN']=NN
    (N,O)=recom(id,x,mod)
    demande['recom_N']=N
    demande['recom_O']=O
    #demande['secteur']= secteur
    demande['rapport_rebourse']= rapport_rebourse 
    demande['rap_dif']= rap_d
    if (note<50):
        deg=270+(1.8*note)
        demande['deg']=deg
        Nature ="Mauvais"
        demande['Nature']=Nature
        demande['recom']='Nous vous DEconseillons de preter'
    else:
        deg=1.8*note -90    
        demande['deg']=deg
        Nature="Bon"
        demande['Nature']=Nature
        demande['recom']='Nous vous déconseillons de preter'
    request_generate = f"Prend les points positifs en {', '.join(O)} et les points negatifs en {', '.join(N)} d'une demande de credit et reformule bien, sans barvadage de maniere directe,sans des ponctuation un texte direct coherent et pas du copie coller de ce qui est demandé"
    demande['analyse']=generate(request_generate)   
    return demande

def dm_details(request ,id):
    demande=evaluate_loan_request(id, mod, secteur_to_index, another_mapping)
    return render(request,"demande/details.html",demande)

def dm_details_valide(request ,id):
    demande=evaluate_loan_request(id, mod, secteur_to_index, another_mapping)
    return render(request,"demande/details2.html",demande)

def  valide_dm(request):
    demandes={"Demandes":Demande.objects.all()}
    return render(request,"demande/valide.html",demandes)


def view_credit_request(request,id):
    demande={"Dm":get_object_or_404(Demande,pk= id)}
    # Rendre le template en HTML
    instance = get_object_or_404(Demande, pk=id)
    if instance.secteur_activite in secteur_to_index:
        secteur = secteur_to_index[instance.secteur_activite]
    if instance.situation_matrimoniale in another_mapping:
        r = another_mapping[instance.situation_matrimoniale]
        
    nboct=instance.nbr_credits_octroyes
    nbremb=instance.nbr_credits_rembourses
    rapport_rebourse=nbremb/nboct
    taux_interet=instance.taux_interet
    duree=instance.duree_pret_souhaitee
    montant_s=instance.montant_solicite
    montant_total=instance.montant_credits_accorde
    anc=instance.anciennete_agence
    rap_d=((montant_total/nboct)- montant_s)/(montant_total/nboct)
    # r=get_object_or_404(Demande.situation_matrimoniale,pk=id)
    #secteur=9
    nbr =instance.nombre_mois_cotisation
    x=[[ anc,montant_s,duree,taux_interet,secteur,nbr,nboct,rapport_rebourse,rap_d]]
    pred=mod.predict(x)
    note=mod.predict_proba(x)[:,0] *100
    if(note>80):
        note=note-5
    note =np.around(note).item()
    

        
    demande['pred']=pred
    demande['note']=note

    (NN,OO)=expliquer(x,mod)
    demande['NN']=NN
    (N,O)=recom(id,x,mod)
    demande['recom_N']=N
    demande['recom_O']=O
    #demande['secteur']= secteur
    demande['rapport_rebourse']= rapport_rebourse 
    demande['rap_dif']= rap_d
    if (note<50):
        deg=270+(1.8*note)
        demande['deg']=deg
        Nature ="Mauvais"
        demande['Nature']=Nature
        demande['recom']='Nous vous DEconseillons de preter'
    else:
        deg=1.8*note -90    
        demande['deg']=deg
        Nature="Bon"
        demande['Nature']=Nature
        demande['recom']='Nous vous déconseillons de preter'
    html_string = render_to_string('demande/pdf_template.html',demande)

    # Générer le PDF
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    
    # Créer la réponse HTTP avec le PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="credit_request_{id}.pdf"'

    return response 
