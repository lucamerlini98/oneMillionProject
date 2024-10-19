import streamlit as st
import plotly.graph_objs as go

# Input dall'utente con valori massimi ragionevoli
eta = st.number_input("Quanti anni hai?", min_value=0, max_value=120, value=30, step=1)
patrimonio_investito = st.number_input("A quanto ammonta il tuo patrimonio investito?", min_value=0.0, max_value=10_000_000.0, value=50_000.0, step=1_000.0)
rendimento_atteso = st.number_input("Qual è il rendimento atteso annuale previsto dai tuoi investimenti?", min_value=0.0, max_value=1.0, value=0.07, step=0.01)
inflazione = st.number_input("Qual è l'inflazione attesa annuale?", min_value=0.0, max_value=1.0, value=0.02, step=0.01)
spese_annuali = st.number_input("A quanto ammontano le tue spese annuali?", min_value=0.0, max_value=1_000_000.0, value=20_000.0, step=1_000.0)
reddito = st.number_input("A quanto ammonta il tuo reddito annuale netto?", min_value=0.0, max_value=1_000_000.0, value=40_000.0, step=1_000.0)

# Parametri fissi
tassazione = 0.26

def calcola_eta_milione(patrimonio_iniziale, guadagni_annuali, spese_annuali, rendimento, inflazione, tassazione, eta_corrente):
    # Controllo preliminare per vedere se è possibile raggiungere un milione
    if patrimonio_iniziale < 1_000_000 and spese_annuali > guadagni_annuali:
        st.write("Mi spiace, ma con questi valori non puoi raggiungere un milione di euro.")
        return None  # Uscita dalla funzione se non è possibile raggiungere l'obiettivo

    patrimonio = patrimonio_iniziale
    eta = eta_corrente + 1
    netto_annuo_cumulato = 0

    # Liste per tracciare i valori
    eta_list = []
    patrimonio_list = []
    netto_annuo_cumulato_list = []
    patrimonio_netto_list = []

    while eta <= 120:  # Limite di età fissato a 120 anni
        # Calcolo del netto tra i guadagni e le spese annuali (non soggetto a tassazione)
        netto_annuo = guadagni_annuali - spese_annuali
        netto_annuo_cumulato += netto_annuo

        # Calcolo rendimento annuale (interesse composto senza tassazione)
        rendimento_annuo = patrimonio * rendimento

        # Aggiorno il patrimonio con il rendimento annuale e il netto annuale
        patrimonio += rendimento_annuo + netto_annuo

        # Adeguamento del patrimonio per l'inflazione (potere d'acquisto reale)
        patrimonio /= (1 + inflazione)

        # Aggiorno il reddito e le spese per tener conto dell'inflazione
        guadagni_annuali *= (1 + inflazione)
        spese_annuali *= (1 + inflazione)

        # Calcolo del patrimonio netto
        patrimonio_tassabile = patrimonio - patrimonio_iniziale - netto_annuo_cumulato
        patrimonio_netto = patrimonio - (patrimonio_tassabile * tassazione)

        # Salva i valori attuali per il grafico
        eta_list.append(eta)
        patrimonio_list.append(patrimonio)
        netto_annuo_cumulato_list.append(netto_annuo_cumulato)
        patrimonio_netto_list.append(patrimonio_netto)

        # Verifica se il patrimonio netto raggiunge un milione di euro
        if patrimonio_netto >= 1_000_000:
            st.write(f"Raggiungerai un milione di euro all'età di {eta} anni.")
            break

        # Incremento dell'età
        eta += 1

    # Se non è stato raggiunto un milione entro 120 anni, informare l'utente
    if eta > 120:
        st.write("Mi spiace, ma con questi valori non riuscirai a raggiungere un milione entro 120 anni.")

    # Grafico dei risultati utilizzando Plotly
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

    return eta

# Chiamata alla funzione con i parametri forniti dall'utente
eta_finale = calcola_eta_milione(
    patrimonio_iniziale=patrimonio_investito,
    guadagni_annuali=reddito,
    spese_annuali=spese_annuali,
    rendimento=rendimento_atteso,
    inflazione=inflazione,
    tassazione=tassazione,
    eta_corrente=eta
)
