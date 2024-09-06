import matplotlib.pyplot as plt
import numpy as np

from script.code.config import my_colors, hours_name, months_name

# talvez retornar months e hours pra calcular medidas e realizar hipóteses
def months_and_hours_review(data: np.ndarray, y: str, title: str, target_label='Date') -> None:
    months = np.zeros(12, dtype=int)
    hours = np.zeros(24, dtype=int)

    for label in data:
        date, time = label[target_label].split(' ')

        months[int(date.split('-')[1]) - 1] += 1
        hours[int(time.split(':')[0])] += 1

    # barplot of date
    plt.bar(
        x=months_name,
        height=months,
        color=my_colors
    )

    plt.xlabel("Months")
    plt.ylabel(f"Amount of {y}")
    plt.title(f"Relação entre meses do ano e {title}")
    plt.show()

    # barplot of time
    plt.bar(
        x=hours_name,
        height=hours,
        color=my_colors
    )

    plt.xlabel("Hours")
    plt.ylabel(f"Amount of {y}")
    plt.title(f"Relação entre horas do dia e {title}")
    plt.show()

# talvez retornar o information.values() como uma np.ndarray para realizar medidas e hipóteses
def pie_review(data : np.ndarray, target_label : str, title : str) -> None:
    information : dict[str, int] = {}

    for info in data:
        target = info[target_label]

        try:
            information[target] += 1

        except KeyError:
            information[target] = 1

    plt.pie(
        x=information.values(), labels=information.keys(), autopct='%1.1f%%', colors=my_colors
    )

    plt.title(f"Quantidade de {title}")
    plt.show()

def unique(data : np.ndarray, target_label : str) -> np.ndarray:
    result : np.ndarray = np.array([])

    for info in data:
        result = np.append(result, info[target_label])

    return np.unique(result)