import sqlite3
import pandas as pd
import streamlit as st

# Ρύθμιση σελίδας
st.set_page_config(
    page_title="Εκτροφείο de la Dirfis", page_icon="🐕", layout="wide"
)

st.title("🐕 Εκτροφείο de la Dirfis")
st.markdown("### Σύστημα Διαχείρισης Εκτροφής & Κυνηγετικών Σκύλων (Tablet App)")


# Σύνδεση με τη βάση δεδομένων
@st.cache_resource
def get_connection():
  return sqlite3.connect("de_la_dirfis.db", check_same_thread=False)


conn = get_connection()


def load_data(query):
  return pd.read_sql(query, conn)


# Κεντρικό μενού πλοήγησης (αντί για κουμπιά αρχικής)
menu = st.selectbox(
    "📂 Επιλέξτε Ενότητα Διαχείρισης:", [
        "🐕 Σκύλοι Εκτροφείου",
        "❤️ Ζευγαρώματα",
        "🐶 Γέννες",
        "🐾 Κουτάβια / Πωλήσεις",
        "🎯 Εκπαίδευση Σκύλων",
        "👤 Πελάτες / Waitlist",
        "💰 Οικονομικά & Ταμείο",
        "📊 Αναφορές",
    ]
)

# -----------------------------------------
# 1. ΣΚΥΛΟΙ
# -----------------------------------------
if menu == "🐕 Σκύλοι Εκτροφείου":
  st.subheader("🐕 Μητρώο Σκύλων Εκτροφείου")
  df = load_data(
      "SELECT id, name AS 'Όνομα', sex AS 'Φύλο', birth_date AS 'Γέννηση',"
      " microchip AS 'Microchip', pedigree AS 'Pedigree', father AS 'Πατέρας',"
      " mother AS 'Μητέρα', breeder AS 'Εκτροφέας', color AS 'Χρώμα', notes AS"
      " 'Σημειώσεις' FROM dogs"
  )
  st.dataframe(df, use_container_width=True)

# -----------------------------------------
# 2. ΖΕΥΓΑΡΩΜΑΤΑ
# -----------------------------------------
elif menu == "❤️ Ζευγαρώματα":
  st.subheader("❤️ Διαχείριση Ζευγαρωμάτων")
  df = load_data(
      "SELECT id, male_dog AS 'Πατέρας', female_dog AS 'Μητέρα', mating_date AS"
      " 'Ημ/νία Ζεύξης', expected_birth_date AS 'Πιθανή Γέννα', status AS"
      " 'Κατάσταση', notes AS 'Σημειώσεις' FROM matings"
  )
  st.dataframe(df, use_container_width=True)

# -----------------------------------------
# 3. ΓΕΝΝΕΣ
# -----------------------------------------
elif menu == "🐶 Γέννες":
  st.subheader("🐶 Καταχωρημένες Γέννες")
  df = load_data(
      "SELECT id, mating_info AS 'Ζευγάρωμα', birth_date AS 'Ημ/νία Γέννας',"
      " males_count AS 'Αρσενικά', females_count AS 'Θηλυκά', total_puppies AS"
      " 'Σύνολο', notes AS 'Σημειώσεις' FROM litters"
  )
  st.dataframe(df, use_container_width=True)

# -----------------------------------------
# 4. ΚΟΥΤΑΒΙΑ / ΠΩΛΗΣΕΙΣ
# -----------------------------------------
elif menu == "🐾 Κουτάβια / Πωλήσεις":
  st.subheader("🐾 Κουτάβια & Κατάσταση Πωλήσεων")
  df = load_data(
      "SELECT id, litter_info AS 'Γέννα', name AS 'Όνομα/Κωδικός', sex AS"
      " 'Φύλο', color AS 'Χρώμα', microchip AS 'Microchip', status AS"
      " 'Κατάσταση', price AS 'Τιμή (€)', deposit AS 'Προκαταβολή (€)',"
      " buyer_name AS 'Αγοραστής', buyer_phone AS 'Τηλέφωνο' FROM puppies"
  )
  st.dataframe(df, use_container_width=True)

# -----------------------------------------
# 5. ΕΚΠΑΙΔΕΥΣΗ
# -----------------------------------------
elif menu == "🎯 Εκπαίδευση Σκύλων":
  st.subheader("🎯 Εκπαίδευση Σκύλων & Πελάτες")
  df = load_data(
      "SELECT id, client_name AS 'Πελάτης', phone AS 'Τηλέφωνο', dog_name AS"
      " 'Σκύλος', dog_breed AS 'Ράτσα', training_type AS 'Πρόγραμμα', status AS"
      " 'Κατάσταση', total_cost AS 'Κόστος (€)', advance_payment AS"
      " 'Προκαταβολή (€)', start_date AS 'Έναρξη', end_date AS 'Λήξη' FROM"
      " trainings"
  )
  st.dataframe(df, use_container_width=True)

# -----------------------------------------
# 6. ΠΕΛΑΤΕΣ / WAITLIST
# -----------------------------------------
elif menu == "👤 Πελάτες / Waitlist":
  st.subheader("👤 Ενδιαφερόμενοι & Λίστα Αναμονής")
  df = load_data(
      "SELECT id, full_name AS 'Ονοματεπώνυμο', phone AS 'Τηλέφωνο', email AS"
      " 'Email', city AS 'Πόλη', pref_sex AS 'Προτίμηση Φύλου', purpose AS"
      " 'Σκοπός', deposit AS 'Προκαταβολή (€)', status AS 'Κατάσταση' FROM"
      " clients"
  )
  st.dataframe(df, use_container_width=True)

# -----------------------------------------
# 7. ΟΙΚΟΝΟΜΙΚΑ
# -----------------------------------------
elif menu == "💰 Οικονομικά & Ταμείο":
  st.subheader("💰 Οικονομικά & Συναλλαγές Ταμείου")
  df = load_data(
      "SELECT id, trans_date AS 'Ημερομηνία', trans_type AS 'Τύπος',"
      " category AS 'Κατηγορία', amount AS 'Ποσό (€)', payment_method AS"
      " 'Τρόπος', description AS 'Περιγραφή' FROM transactions"
  )
  st.dataframe(df, use_container_width=True)

  # Υπολογισμός συνολικών εσόδων και εξόδων
  inc_df = load_data(
      "SELECT SUM(amount) FROM transactions WHERE trans_type = 'Έσοδο'"
  )
  exp_df = load_data(
      "SELECT SUM(amount) FROM transactions WHERE trans_type = 'Έξοδο'"
  )

  total_in = inc_df.iloc[0, 0] if inc_df.iloc[0, 0] is not None else 0.0
  total_out = exp_df.iloc[0, 0] if exp_df.iloc[0, 0] is not None else 0.0

  col1, col2, col3 = st.columns(3)
  col1.metric("📈 Συνολικά Έσοδα", f"€{total_in:.2f}")
  col2.metric("📉 Συνολικά Έξοδα", f"€{total_out:.2f}")
  col3.metric("📌 Υπόλοιπο Ταμείου", f"€{total_in - total_out:.2f}")

# -----------------------------------------
# 8. ΑΝΑΦΟΡΕΣ
# -----------------------------------------
elif menu == "📊 Αναφορές":
  st.subheader("📊 Συγκεντρωτικές Αναφορές Εκτροφείου")

  dogs_count = len(load_data("SELECT id FROM dogs"))
  matings_count = len(load_data("SELECT id FROM matings"))
  litters_count = len(load_data("SELECT id FROM litters"))
  puppies_count = len(load_data("SELECT id FROM puppies"))
  clients_count = len(load_data("SELECT id FROM clients"))
  training_count = len(load_data("SELECT id FROM trainings"))

  col1, col2, col3 = st.columns(3)
  col1.metric("🐕 Συνολικοί Σκύλοι", dogs_count)
  col2.metric("❤️ Ζευγαρώματα", matings_count)
  col3.metric("🐶 Γέννες", litters_count)

  col4, col5, col6 = st.columns(3)
  col4.metric("🐾 Κουτάβια", puppies_count)
  col5.metric("👤 Πελάτες / Waitlist", clients_count)
  col6.metric("🎯 Ενεργές Εκπαιδεύσεις", training_count)
