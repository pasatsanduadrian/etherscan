import pandas as pd
import plotly.express as px


def generate_summary_report(results):
    """Returnează un scurt raport sumar pentru rezultatele analizelor."""
    if not results:
        return "Nu au fost returnate rezultate."

    total = len(results)
    avg_score = sum(r.get("security_score", 0) for r in results) / total
    risk_counts = {}
    for r in results:
        risk = r.get("risk_level", "NECUNOSCUT")
        risk_counts[risk] = risk_counts.get(risk, 0) + 1

    lines = [
        f"Contracte analizate: {total}",
        f"Scor mediu de securitate: {avg_score:.2f}",
        "Distribuția nivelurilor de risc:"  # Romanian for distribution of risk levels
    ]
    for risk, cnt in risk_counts.items():
        lines.append(f"- {risk}: {cnt}")

    return "\n".join(lines)


def create_security_scores_chart(results):
    """Generează un grafic cu scorurile de securitate pentru fiecare contract."""
    df = pd.DataFrame(results)
    if df.empty:
        return px.bar(title="Fără date")
    fig = px.bar(df, x="name", y="security_score", title="Scoruri de securitate")
    fig.update_layout(yaxis_range=[0, 100])
    return fig


def create_token_distribution_chart(results):
    """Generează un grafic cu distribuția token-urilor vesting."""
    df = pd.DataFrame(results)
    if df.empty:
        return px.pie(title="Fără date")
    values = "vested_amount" if "vested_amount" in df.columns else df.columns[0]
    fig = px.pie(df, values=values, names="name", title="Distribuția token-urilor")
    return fig


def create_risk_distribution_chart(results):
    """Generează un grafic cu distribuția nivelurilor de risc."""
    df = pd.DataFrame(results)
    if df.empty:
        return px.pie(title="Fără date")
    fig = px.pie(df, names="risk_level", title="Distribuția nivelurilor de risc")
    return fig


def create_detailed_table(results):
    """Returnează un DataFrame cu informații detaliate despre contracte."""
    df = pd.DataFrame(results)
    if df.empty:
        return pd.DataFrame()
    columns = [
        "name",
        "address",
        "security_score",
        "risk_level",
        "vested_amount",
        "released_amount",
        "releasable_amount",
    ]
    for col in columns:
        if col not in df.columns:
            df[col] = None
    return df[columns]
