"""
Application Streamlit indépendante pour ajouter des étudiants.
Pas d'authentification - accès direct à la table students de Supabase.
Formulaire simple pour remplir la base de données.
Utilise .env pour les variables d'environnement.
"""

import os
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime

# Charger les variables depuis .env
load_dotenv('.env')

# Configuration de la page
st.set_page_config(
    page_title="Ajouter Étudiant - Torii",
    page_icon="👥",
    layout="centered"
)

st.title("📝 Inscription des Étudiants")
st.markdown("*Formulaire d'inscription*")
st.divider()

try:
    # Initialiser le client Supabase
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        st.error("❌ Variables d'environnement manquantes dans .env (SUPABASE_URL et SUPABASE_KEY)")
        st.stop()

    supabase = create_client(supabase_url, supabase_key)

    # Récupérer l'année académique actuelle
    response = supabase.table('academic_years').select('*').eq('is_current', True).execute()
    if response.data and len(response.data) > 0:
        current_year = response.data[0]
    else:
        st.error("⚠️ Aucune année académique active trouvée dans Supabase.")
        st.stop()

    # Afficher l'année académique en cours
    st.info(f"📅 Année académique : **{current_year['year_label']}** (Préfixe : {current_year['prefix']})")

    # Formulaire d'ajout
    with st.form("add_student_form"):
        col1, col2 = st.columns(2)

        with col1:
            first_name = st.text_input("Prénom *")
            last_name = st.text_input("Nom *")
            email = st.text_input("Email *")
            phone_number = st.text_input("Téléphone")

        with col2:
            birth_date = st.date_input(
                "Date de naissance",
                value=None,
                min_value=datetime(1940, 1, 1),
                max_value=datetime.now()
            )

        st.markdown("*Les champs marqués d'un astérisque sont obligatoires*")
        st.markdown(f"*Le code étudiant sera automatiquement généré avec le préfixe **{current_year['prefix']}***")

        submitted = st.form_submit_button("✅ Soumettre", use_container_width=True, type="primary")

        if submitted:
            if first_name and last_name and email:
                try:
                    # Vérifier si l'email existe déjà
                    existing = supabase.table('students').select('*').eq('email', email).execute()

                    if existing.data:
                        st.error("❌ Un étudiant avec cet email existe déjà")
                    else:
                        # Insérer le nouvel étudiant
                        new_student = {
                            'first_name': first_name,
                            'last_name': last_name,
                            'email': email,
                            'phone_number': phone_number if phone_number else None,
                            'academic_year_id': current_year['id'],
                            'birth_date': birth_date.isoformat() if birth_date else None
                        }

                        response = supabase.table('students').insert(new_student).execute()

                        if response.data:
                            student_code = response.data[0].get('student_code', 'N/A')
                            st.success(f"✅ Étudiant ajouté avec succès!")
                            st.info(f"📝 Code étudiant : **{student_code}**")
                            st.rerun()
                        else:
                            st.error("Erreur lors de l'ajout de l'étudiant")

                except Exception as e:
                    st.error(f"Erreur : {str(e)}")
            else:
                st.warning("⚠️ Veuillez remplir tous les champs obligatoires (Prénom, Nom, Email)")

except Exception as e:
    st.error(f"❌ Erreur d'initialisation : {str(e)}")
    import traceback
    st.code(traceback.format_exc())
