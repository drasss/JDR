import streamlit as st
import os 
def d_lore(exp):
    exp.write(str(os.listdir("lore")))
    fichier=open("lore/lore.txt", "r",encoding="utf-8")
    contenu=fichier.read()
    fichier.close()
    ct=contenu.split("---")
    for i in range(len(ct)):
        temp=ct[i].split("|||")
        t=exp.expander(temp[0])
        t.write(temp[1])

