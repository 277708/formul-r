import pandas as pd
import streamlit as st

# Načtení dat
machines_df = pd.read_excel("zoznamy.xlsx", sheet_name="STROJE")
clients_df = pd.read_excel("zoznamy.xlsx", sheet_name="KLIENTI")

# Filtr dostupných strojů
machines_df = machines_df[machines_df['dostupnosť'] == "ANO"].reset_index(drop=True)

st.title("Půjčovna strojů")

# Výběr klienta
client_name = st.selectbox("název klientské firmy", options=list(clients_df['název firmy']))

if client_name:
    client_discount = clients_df.loc[clients_df['název firmy'] == client_name, 'sleva'].values[0]
    st.info(f"Sleva pro vaši firmu: **{client_discount}%**")

# Výběr strojů
st.write("Vyberte stroje (dostupné):")
selected_machines = st.multiselect(
    "Stroje", 
    options=[f"{row['názov']} - {row['popis']} ({row['cena [kč]/den']} Kč/den)" for i, row in machines_df.iterrows()]
)

# Počet dní
days = st.number_input("Počet dní", min_value=1, value=1)

# Výpočet ceny
if st.button("Spočítat půjčovné"):
    if not client_name or not selected_machines:
        st.warning("Vyberte klienta a alespoň jeden stroj!")
    else:
        client_discount = clients_df.loc[clients_df['název firmy'] == client_name, 'sleva'].values[0]
        total_price = 0
        for machine_text in selected_machines:
            # najdeme index stroje podle názvu
            machine_name = machine_text.split(" - ")[0]
            price_per_day = machines_df.loc[machines_df['názov'] == machine_name, 'cena [kč]/den'].values[0]
            total_price += price_per_day * days
        
        total_price = total_price * (1 - client_discount / 100)
        st.success(f"Celková cena půjčovného: {total_price:.2f} Kč")




