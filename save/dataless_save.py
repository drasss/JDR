import streamlit as st 
import numpy as np
import random
from io import StringIO

st.set_page_config(layout="wide")
b,d,p = st.tabs(["Fiche Personnage","Simulation","Equilibrage"])

#lancé de dés
lance=st.sidebar
def dice():
    rst=[]

    desp=de.split("+")
    if len(desp)==1:
        desp+=["0"]
    des=desp[0].strip(" ").split("d")
    addd=desp[1].strip(" ")
    for i in range(int(des[0])):
        rst+=[random.randint(1,int(des[1]))]
    lance.text("SOMME : "+str(np.sum(rst)+int(addd))+" "+str(rst))

de=lance.text_input("dé",value="1d100")
lance.button("lancer les dés",on_click=dice)

#*--------------------------- fiche de perso
#*-------------- lecture du fichier

uploaded_file=b.file_uploader("Upload Data")
try:
    # transformer le fichier en variable str
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    data = stringio.read()
    #traiter le texte
    data=data.split("\n#####\n")
    data[0]=data[0].strip().split(",")
    for i in range(len(data[0])):
        data[0][i]=int(data[0][i].strip())
    data_ext=data[1:]
    data=data[0]
    XPst=data[1]
    LVLst=data[0]
    data=data[2:]
    
    extracted=True
    
except :
    data=[55]*7+[15,15,55,55,15,15]
    XPst=0
    LVLst=1
    extracted=False
    data_ext=["","","0##0","","","",""]
    
values=data[:7]
#- ------------- Name

Name=b.text_input("Nom",value=data_ext[6],label_visibility="hidden")

#--------------- XP
b_xp=b.columns([2,1,1,1,2])
LVL=b_xp[1].number_input("Niveau",LVLst)
XP=b_xp[3].number_input("XP",min_value=0,value=XPst)

#*-------------- 7 Stats capitaux

statistiques=b.expander("Statistiques",True)
    
stats=statistiques.columns(7)
stat_nb=[]
name_stats=["FOR","ESP","CHA","FIN","LUC","CEL","CON"]


for i in range(7):
    stat_nb+=[stats[i].number_input(name_stats[i],value=values[i],key=str(i)+"stats")]
PV,prd,esq,PE=statistiques.columns(4)

#*-------------- 4 stats secondaires
if extracted == False:
    prdt=(stat_nb[-1]+stat_nb[-3])/2
    prdt=int(prdt+int(prdt!=float(int(prdt))))
    esqt=(stat_nb[-2]+stat_nb[-3])/2
    esqt=int(esqt+int(esqt!=float(int(esqt))))
    pvt=int(stat_nb[0]/10)+int(stat_nb[-1]/10)+3
    pet=int(stat_nb[1]/10)+int(stat_nb[-3]/10)+3
    pvmax=pvt
    pemax=pet
else :
    pvt,pvmax,prdt,esqt,pet,pemax=data[-6:]


pvnb=PV.number_input("PV",value=pvt)
pvmaxnb=PV.number_input("PV max",value=pvmax)
prdnb=prd.number_input("PRD",value=prdt)
esqnb=esq.number_input("ESQ",value=esqt)    
penb=PE.number_input("PE",value=pet)
pemaxnb=PE.number_input("PE max",value=pemax)
#*-------------- Vérifications
if np.sum(stat_nb)>55*7:
    b.text("il y a "+str(np.sum(stat_nb)-55*7)+" points en trop ")
if np.sum(stat_nb)<55*7:
    b.text("il y a "+str(+55*7-np.sum(stat_nb))+" points qui manque ")
if np.min(stat_nb)<25:
    b.text("le minimum est 25")
if np.max(stat_nb)>80:
    b.text("le maximum est 80")
    
#*-------------- suite

def calc_cpt(stat_nb,human=True):
    cpt=LVL*2+int(human)*2+(stat_nb[2]//10+stat_nb[3]//10)//2
    
    return cpt
IetC=b.expander("Inventaire & Compétences")
is_human=IetC.checkbox("Personnage Humain",value=True)
text_fiche=IetC.columns([3,4,2])

calc_cpt_nb=calc_cpt(stat_nb,is_human)

competences=text_fiche[0].text_area("Competences",value=data_ext[0],height=300)
try:
    competences_s=competences.strip().split("\n")
    for i in range(len(competences_s)):
        competences_s[i]=competences_s[i].split(":")[-1].split("%")[0].strip(" +")
        competences_s[i]=int(competences_s[i])
    text_fiche[0].text("Compétences Disponibles : "+str(calc_cpt_nb-np.sum(competences_s)//5)+"/"+str(calc_cpt_nb))
except:
    text_fiche[0].text("Compétences Disponibles : "+str(calc_cpt_nb))
    pass


Inventaire=text_fiche[1].text_area("Inventaire",value=data_ext[1],height=300)
PO=text_fiche[2].number_input("PO",value=int(data_ext[2].split("##")[0]))
PA=text_fiche[2].number_input("PA",value=int(data_ext[2].split("##")[1]))

apt=b.expander("Aptitudes")

Aptitudes=apt.text_area("Aptitudes",value=data_ext[3],height=600)

sor=b.expander("Sorts")

Sorts=sor.text_area("Sorts",value=data_ext[4],height=500)

#--------------- Notes
notes = b.text_area("notes",value=data_ext[5])


#--------------- Compagnons


#*-------------- recolte et téléchargement des données
data_txt=str(LVL)+", "+str(XP)+", "
data_txt+=str(stat_nb).strip("[]")+", "+str([pvnb,pvmaxnb,prdnb,esqnb,penb,pemaxnb]).strip("[]") 
data_txt+="\n#####\n"+competences
data_txt+="\n#####\n"+Inventaire
data_txt+="\n#####\n"+str(PO)+"##"+str(PA)
data_txt+="\n#####\n"+Aptitudes
data_txt+="\n#####\n"+Sorts
data_txt+="\n#####\n"+notes
data_txt+="\n#####\n"+Name
b.download_button("Download Data",data_txt,file_name="data.txt")

#---------------------------------- 
#---------------------------------- SIMULATIONS
#---------------------------------- 

nb_coups=d.slider("nombre de coups",1,8)

coups=[d.container() for i in range(nb_coups)]

colcoups=[""]*nb_coups

proba_coup=[""]*nb_coups
bonus_coup=[""]*nb_coups
dgt_coup=[""]*nb_coups

for i in range(len(coups)):
    colcoups[i]=coups[i].columns([1,1,4])
    proba_coup[i]=colcoups[i][0].number_input("proba",0,100,55,key="proba"+str(i))
    bonus_coup[i]=colcoups[i][1].number_input("bonus",-50,50,0,key="bonus"+str(i))
    dgt_coup[i]=colcoups[i][2].text_input("dégats","1d6+2",key="dgt"+str(i))

calcul_b=d.button("Calcul")

simur=""

if calcul_b:
    dgt=0
    for i in range(nb_coups):
        desp=dgt_coup[i].split("+")
        if len(desp)==1:
            desp+=["0"]
        des=desp[0].strip(" ").split("d")
        addd=desp[1].strip(" ")
        dgtde=int(des[0])*(int(des[1])+1)/2+int(addd)
        dgt+=dgtde*(proba_coup[i]+bonus_coup[i]+5)/100
    simur=str(dgt)

    
d.text(simur)




#---------------------------------- 
#---------------------------------- équilibrage du fun de la partie
#---------------------------------- p
p.text_area("déja rempli : ",value=competences,height=300)
pc=p.columns(4)

ptitles=["Scénario","Moments calmes","Environnements hostiles","Combat"]
pexemples=["ESP | Connaissance (mythes et croyances)","ESP | Artisanat (apothicaire)","CEL | Subterfuge","ESP | Controle du feu"]
#p.write(stat_nb)
ptext=[]

datap=[]
for i in range(len(pc)):
    pc[i].text(ptitles[i])
    ptext+=[pc[i].text_area("Compétences",value=pexemples[i],height=400,key="textareap"+str(i))]

    tempo=ptext[i].split("\n")
    tempo=[tempo[j].split(" | ") for j in range(len(tempo))]
    datap+=[tempo]
#p.write(datap)

score=[len(datap[0])+stat_nb[1]/100,len(datap[1])+0.8,len(datap[2])+stat_nb[4]/100,len(datap[3])-0.5+max(stat_nb)/100]
p.text("tu t'amuseras + dans "+ptitles[np.argmax(score)])
p.text("tu t'amuseras - dans "+ptitles[np.argmin(score)])
p.text(" si un de ces scores est en dessous de 2, attention ! ")
p.text(str([ptitles[i]+" : "+str(round(score[i],2)) for i in range(len(score))]))


















