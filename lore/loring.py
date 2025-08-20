import streamlit as st
def d_lore(exp):
    fichier=open("lore\\lore.txt", "r",encoding="utf-8")
    contenu=fichier.read()
    fichier.close()
    ct=contenu.split("---")
    for i in range(len(ct)):
        temp=ct[i].split("|||")
        t=exp.expander(temp[0])
        t.write(temp[1])

