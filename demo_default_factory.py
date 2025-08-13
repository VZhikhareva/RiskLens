from models import RiskReport, RiskItem

# Создаём два независимых отчёта
r1 = RiskReport()
r2 = RiskReport()

# В r1 добавляем один риск
r1.items.append(
    RiskItem(risk="A", category="Operational", severity=2, likelihood=2)
)

print("r1 items:", len(r1.items))  # Ожидаем: 1
print("r2 items:", len(r2.items))  # Ожидаем: 0 (отдельный список)