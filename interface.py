import streamlit as st 
import numpy as np
import random

st.set_page_config(layout="wide")
a,b,c = st.tabs(["dés", "fiche","résultats"])

#lancé de dés
lance=a.columns(3)
def dice():
    rst=[]

    desp=de.split("+")
    des=desp[0].strip(" ").split("d")
    addd=desp[1].strip(" ")
    for i in range(int(des[0])):
        rst+=[random.randint(1,int(des[1]))+int(addd)]
        lance[2].text("=> "+str(rst[-1])+" ("+str(rst[-1]-int(addd))+")")
    lance[2].text("SOMME : "+str(np.sum(rst)))

de=lance[0].text_input("dé")
lance[1].button("lancer les dés",on_click=dice)

#*--------------------------- fiche de perso

fichier=open("data.txt")
data=fichier.read().split(",")
fichier.close()
print(data[:7])
for i in range(len(data)):
    data[i]=int(data[i])

values=data[:7]

    
stats=b.columns(7)
stat_nb=[]
name_stats=["FOR","ESP","CHA","FIN","LUC","CEL","CON"]


for i in range(7):
    stat_nb+=[stats[i].number_input(name_stats[i],value=values[i],key=str(i)+"stats")]
PV,prd,esq,PE=b.columns(4)


prdt=(stat_nb[-1]+stat_nb[-3])/2
prdt=int(prdt+int(prdt!=float(int(prdt))))
esqt=(stat_nb[-2]+stat_nb[-3])/2
esqt=int(esqt+int(esqt!=float(int(esqt))))
pvt=int(stat_nb[0]/10)+int(stat_nb[-1]/10)+5
pet=int(stat_nb[1]/10)+int(stat_nb[-3]/10)+5



pvnb=PV.number_input("PV",value=pvt)
prdnb=prd.number_input("PRD",value=prdt)
esqnb=esq.number_input("ESQ",value=esqt)    
penb=PE.number_input("PE",value=pet)

if np.sum(stat_nb)>55*7:
    b.text("il y a "+str(np.sum(stat_nb)-55*7)+" points en trop ")
if np.sum(stat_nb)<55*7:
    b.text("il y a "+str(+55*7-np.sum(stat_nb))+" points qui manque ")
if np.min(stat_nb)<25:
    b.text("le minimum est 25")
if np.max(stat_nb)>80:
    b.text("le minimum est 80")


fichier=open("data.txt","w")
fichier.write(str(stat_nb).strip("[]"))
fichier.write(","+str([pvnb,prdnb,esqnb,penb]).strip("[]"))
fichier.close()
