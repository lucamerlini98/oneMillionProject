import streamlit as st
import plotly.graph_objs as go

st.title("Quando sarò milionario?")

# Descrizione
st.header("Calcolo Patrimonio Futuro")
st.write(
    "Questa applicazione ti permette di calcolare quanto tempo ci vorrà per raggiungere un patrimonio netto di un milione di euro. "
    "Inserisci i tuoi dati personali e scopri come il tuo patrimonio potrebbe evolversi nel tempo, "
    "tenendo conto di vari fattori come rendimento degli investimenti, inflazione, spese annuali e reddito."
)

# eta = st.slider("Quanti anni hai?", min_value=0, max_value=120, value=30)
# patrimonio_investito = st.slider("A quanto ammonta il tuo patrimonio investito?", min_value=0.0, max_value=1000000.0, value=50000.0, step=100.0)
# rendimento_atteso = st.slider("Qual è il rendimento atteso annuale previsto dai tuoi investimenti (%)?", min_value=0.0, max_value=100.0, value=7.0, step=0.1) / 100
# inflazione = st.slider("Qual è l'inflazione attesa annuale (%)?", min_value=0.0, max_value=20.0, value=2.0, step=0.1) / 100
# spese_annuali = st.slider("A quanto ammontano le tue spese annuali?", min_value=0.0, max_value=100000.0, value=20000.0, step=100.0)
# reddito = st.slider("A quanto ammonta il tuo reddito annuale netto?", min_value=0.0, max_value=100000.0, value=30000.0, step=100.0)

eta = st.number_input("Quanti anni hai?", min_value=0, max_value=120, value=30, step=1)
patrimonio_investito = st.number_input("A quanto ammonta il tuo patrimonio investito?", min_value=0.0, max_value=10_000_000.0, value=10_000.0, step=500.0)
rendimento_atteso = float(st.number_input("Qual è il rendimento atteso annuale previsto dai tuoi investimenti? (in %)", min_value=0.0, value=7.0, step=0.1)) / 100 
inflazione = float(st.number_input("Qual è l'inflazione attesa annuale? (in %)", min_value=0.0, value=2.0, step=0.1)) / 100 
spese_annuali = st.number_input("A quanto ammontano le tue spese annuali?", min_value=0.0, max_value=1_000_000.0, value=20_000.0, step=500.0)
reddito = st.number_input("A quanto ammonta il tuo reddito annuale netto?", min_value=0.0, max_value=1_000_000.0, value=40_000.0, step=500.0)

obbligazionario = st.radio("I tuoi investimenti saranno totalmente obbligazionari?", ("Sì", "No"), index=1)

if obbligazionario == "Sì":
    tassazione = 0.125
else:
    tassazione = 0.26


def calcola_eta_milione(patrimonio_iniziale, guadagni_annuali, spese_annuali, rendimento, inflazione, tassazione, eta_corrente):

    if patrimonio_iniziale < 1_000_000 and spese_annuali > guadagni_annuali:
        st.write("Mi spiace, ma con questi valori non puoi raggiungere un milione di euro.")
        return None  

    patrimonio = patrimonio_iniziale
    eta = eta_corrente + 1
    netto_annuo_cumulato = 0

    eta_list = []
    patrimonio_list = []
    netto_annuo_cumulato_list = []
    patrimonio_netto_list = []

    while eta <= 120:  
        netto_annuo = guadagni_annuali - spese_annuali
        netto_annuo_cumulato += netto_annuo

        rendimento_annuo = patrimonio * rendimento

        patrimonio += rendimento_annuo + netto_annuo

        patrimonio /= (1 + inflazione)

        guadagni_annuali *= (1 + inflazione)
        spese_annuali *= (1 + inflazione)

        patrimonio_tassabile = patrimonio - patrimonio_iniziale - netto_annuo_cumulato
        patrimonio_netto = patrimonio - (patrimonio_tassabile * tassazione)

        eta_list.append(eta)
        patrimonio_list.append(patrimonio)
        netto_annuo_cumulato_list.append(netto_annuo_cumulato)
        patrimonio_netto_list.append(patrimonio_netto)

        if patrimonio_netto >= 1_000_000:
            st.write(f"Raggiungerai un milione di euro all'età di {eta} anni.")
            break

        eta += 1

    if eta > 120:
        st.write("Mi spiace, ma con questi valori non riuscirai a raggiungere un milione entro 120 anni.")

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=eta_list, y=[patrimonio_iniziale] * len(eta_list),
                             mode='lines', name='Patrimonio Iniziale', line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=eta_list, y=patrimonio_list,
                             mode='lines', name='Patrimonio Totale'))
    fig.add_trace(go.Scatter(x=eta_list, y=netto_annuo_cumulato_list,
                             mode='lines', name='Netto Annuale Cumulato'))
    fig.add_trace(go.Scatter(x=eta_list, y=patrimonio_netto_list,
                             mode='lines', name='Patrimonio Netto'))

    fig.update_layout(title='Evoluzione del Patrimonio in Funzione dell\'Età',
                      xaxis_title='Età',
                      yaxis_title='Valore (€)',
                      legend_title='Componenti',
                      template='plotly_white')

    st.plotly_chart(fig)
    st.markdown("© 2024, Luca Merlini")

    return eta

eta_finale = calcola_eta_milione(
    patrimonio_iniziale=patrimonio_investito,
    guadagni_annuali=reddito,
    spese_annuali=spese_annuali,
    rendimento=rendimento_atteso,
    inflazione=inflazione,
    tassazione=tassazione,
    eta_corrente=eta
)
