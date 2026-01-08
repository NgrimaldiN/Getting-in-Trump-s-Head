import streamlit as st

def render_about():
    st.header("TrumpSpeech – Autopsie d'une Rhétorique")
    
    st.markdown("### Le contexte : De la spéculation à l'analyse")
    st.write("""
    Aujourd'hui, les discours de Donald Trump ne sont plus seulement scrutés par les politologues, ils sont devenus un véritable objet de spéculation. 
    Sur des marchés prédictifs comme Polymarket, des milliers de parieurs misent sur la probabilité qu'il prononce certains mots ou slogans (comme "America", "Rigged" ou "Fake News"). 
    Cette dimension "prédictive", souligne une réalité fascinante : la parole de Trump est perçue comme un système de motifs répétitifs et identifiables.
    """)

    st.image("images/polymarket.png", caption="Marchés de prédiction sur Polymarket")

    st.markdown("### L’angle philosophique : La « Neuve-Langue » de Barbara Cassin")
    st.write("""
    Cette répétition et cette simplification ne sont pas le fruit du hasard. Pour la philosophe et académicienne Barbara Cassin, auteure de l'ouvrage « Trump, Poutine et l'Europe », nous sommes face à une véritable « Neuve-Langue » (en référence à la Novlangue d'Orwell).
   Elle analyse ce langage comme une parole "efficace" qui ne cherche pas à décrire la vérité, mais à saturer l’espace public. 
    Pour elle, Trump "efface" certains mots du vocabulaire administratif et politique pour imposer une vision binaire et simplifiée du monde.
    """)

    st.markdown("### Notre démarche : Mettre le mythe à l’épreuve des données")
    st.write("""
    C’est ici que notre projet intervient. On entend souvent dire que le langage de Donald Trump est "pauvre", limité au niveau d’un élève de CM2. 
    Nous avons voulu tester cette hypothèse scientifiquement. À partir d'un corpus massif de 885 discours récupérés en libre accès sur Roll Call, nous nous sommes essayés à différentes approches (analyses descriptives, prédictions de mots, thématiques). 
    Notre objectif final s'est concentré sur une question simple :
    """)

    st.info("**Problématique simplifiée** : Le langage de Donald Trump est-il statistiquement plus pauvre et répétitif que celui de ses opposants politiques ?")

    st.markdown("### Ce que nous démontrons")
    st.write("""
    Grâce à des mesures linguistiques précises comme le ratio Type-Token (TTR), qui calcule la richesse du vocabulaire, et l’analyse des N-grammes (les séquences de mots les plus fréquentes), nous montrons comment cette "pauvreté" apparente se traduit concrètement dans les chiffres. 
    En comparant ses résultats à ceux d'autres candidats, nous révélons si cette simplicité est une réalité mesurable ou une simple impression médiatique.
    """)
    
    col_img1, col_img2 = st.columns(2)
    with col_img1:
        st.image("figures/cttr_by_candidate.png", caption="Complexité lexicale (CTTR) par candidat")
    with col_img2:
        st.image("figures/readability_by_candidate.png", caption="Niveau de lecture (Readability) par candidat")
