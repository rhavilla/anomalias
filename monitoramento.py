import pandas as pd
import matplotlib.pyplot as plt

# === Carregar os CSVs ===
csv1 = pd.read_csv("dados1.csv")
csv2 = pd.read_csv("dados2.csv")

# === Converter hora para tipo categórico ordenado ===
horas = [f"{h:02}h" for h in range(24)]
csv1["time"] = pd.Categorical(csv1["time"], categories=horas, ordered=True)
csv2["time"] = pd.Categorical(csv2["time"], categories=horas, ordered=True)

# === Função para detectar anomalias com base na diferença da média ===
def detectar_anomalias(df, limite=2.0):
    df["media"] = df[["avg_last_week", "avg_last_month"]].mean(axis=1)
    df["desvio"] = (df["today"] - df["media"]) / df["media"]
    df["anomaly"] = df["desvio"] > limite
    return df

csv1 = detectar_anomalias(csv1)
csv2 = detectar_anomalias(csv2)

# === Exibir alertas ===
def alertas(df, nome_csv):
    print(f"\n🔔 ALERTAS PARA {nome_csv}")
    for _, row in df[df["anomaly"]].iterrows():
        print(f"⏰ Hora: {row['time']} - Hoje: {row['today']} | Média: {row['media']:.2f} | Desvio: {row['desvio']:.2f}")

alertas(csv1, "CSV 1")
alertas(csv2, "CSV 2")

# === Gráficos ===
def plotar(df, nome):
    plt.figure(figsize=(12, 6))
    plt.plot(df["time"], df["today"], label="Hoje", marker='o')
    plt.plot(df["time"], df["avg_last_week"], label="Média semana", linestyle="--")
    plt.plot(df["time"], df["avg_last_month"], label="Média mês", linestyle="--")
    plt.scatter(df[df["anomaly"]]["time"], df[df["anomaly"]]["today"], color='red', label="Anomalias", zorder=5)
    plt.title(f"📊 Volume de Vendas por Hora - {nome}")
    plt.xlabel("Hora do Dia")
    plt.ylabel("Número de Transações")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()

# === Plotar e analisar dados do CSV 1 ===
plotar(csv1, "CSV 1")

# === Resumo das anomalias ===
def resumo_anomalias(df, nome):
    anomalias = df[df["anomaly"]].sort_values(by="desvio", ascending=False)
    print(f"\nResumo das maiores anomalias em {nome}:")
    if anomalias.empty:
        print("Nenhuma anomalia detectada.")
    else:
        for _, row in anomalias.iterrows():
            print(f"Hora: {row['time']} | Hoje: {row['today']} | Média: {row['media']:.2f} | Desvio: {row['desvio']:.2f}")

resumo_anomalias(csv1, "CSV 1")

# === Simulação de consulta SQL ===
print("\nExemplo de consulta SQL equivalente:")
print("""
SELECT time, today, avg_last_week, avg_last_month, (today - (avg_last_week + avg_last_month)/2) / ((avg_last_week + avg_last_month)/2) AS deviation
FROM sales_data
ORDER BY deviation DESC
LIMIT 5;
""")

# === Explicação do comportamento das anomalias ===
print("""
Explicação:
As anomalias detectadas representam horários em que o volume de vendas de hoje está significativamente acima da média histórica (última semana e último mês). Isso pode indicar eventos atípicos, promoções, falhas sistêmicas ou mudanças de comportamento dos clientes. Recomenda-se investigar os horários destacados para entender a causa dessas variações.
""")