import streamlit as st 
import numpy as np
import random
from io import StringIO

st.set_page_config(layout="wide")
b,d = st.tabs(["Fiche Personnage","résultats"])

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
    extracted=True
    
except :
    data=[55]*7+[15,15,55,55,15,15]
    extracted=False
    data_ext=["","","0##0","","",""]
    
values=data[:7]

#*-------------- 7 Stats capitaux

    
stats=b.columns(7)
stat_nb=[]
name_stats=["FOR","ESP","CHA","FIN","LUC","CEL","CON"]


for i in range(7):
    stat_nb+=[stats[i].number_input(name_stats[i],value=values[i],key=str(i)+"stats")]
PV,prd,esq,PE=b.columns(4)

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
    b.text("le minimum est 80")
    
#*-------------- suite

b_xp=b.expander("Infos")
text_fiche=b_xp.columns([3,4,2,2])
competences=text_fiche[0].text_area("Competences",value=data_ext[0])
Inventaire=text_fiche[1].text_area("Inventaire",value=data_ext[1])
PO=text_fiche[2].number_input("PO",value=int(data_ext[2].split("##")[0]))
PA=text_fiche[3].number_input("PA",value=int(data_ext[2].split("##")[1]))
Aptitudes=b_xp.text_area("Aptitudes",value=data_ext[3])
Sorts=b_xp.text_area("Sorts",value=data_ext[4])

#--------------- Notes
notes = b.text_area("notes",value=data_ext[5])


#--------------- Compagnons


#*-------------- recolte et téléchargement des données
data_txt=str(stat_nb).strip("[]")+", "+str([pvnb,pvmaxnb,prdnb,esqnb,penb,pemaxnb]).strip("[]") 
data_txt+="\n#####\n"+competences
data_txt+="\n#####\n"+Inventaire
data_txt+="\n#####\n"+str(PO)+"##"+str(PA)
data_txt+="\n#####\n"+Aptitudes
data_txt+="\n#####\n"+Sorts
data_txt+="\n#####\n"+notes
b.download_button("Download Data",data_txt,file_name="data.txt")

