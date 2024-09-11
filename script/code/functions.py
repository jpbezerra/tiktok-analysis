import matplotlib.pyplot as plt
import numpy as np
import statistics as st

from script.code.config import my_colors, hours_name, months_name, days_name, significance, font_size


def months_and_hours_review(data: np.ndarray, y: str, title: str, target_label='Date', return_data=True) -> list[np.ndarray] | None:
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
    plt.title(f"Relation between months and {title}")
    plt.xticks(fontsize=font_size)
    plt.grid()
    plt.show()

    # barplot of time
    plt.bar(
        x=hours_name,
        height=hours,
        color=my_colors
    )

    plt.xlabel("Hours")
    plt.ylabel(f"Amount of {y}")
    plt.title(f"Relation between hours and {title}")
    plt.xticks(fontsize=font_size)
    plt.grid()
    plt.show()

    if return_data:
        return [months, hours]

def pie_review(data : np.ndarray, target_label : str, title : str) -> None:
    information : dict[str, int] = {}

    for info in data:
        target = info[target_label]

        try:
            information[target] += 1

        except KeyError:
            information[target] = 1

    temp : dict[str, int] = information.copy()

    for key, value in temp.items():
        if 15 > value:
            try:
                information['Others'] += value

            except KeyError:
                information['Others'] = value

            finally:
                information.pop(key)

    plt.pie(
        x=information.values(), labels=information.keys(), autopct='%1.1f%%', colors=my_colors,
        pctdistance=0.80
    )

    plt.title(f"Percentage of {title}")
    plt.show()

def unique(data : np.ndarray, target_label : str) -> np.ndarray:
    result : np.ndarray = np.array([])

    for info in data:
        result = np.append(result, info[target_label])

    return np.unique(result)

def line_review(data : np.ndarray, target_label : str, title : str) -> None:
    days : np.ndarray = np.zeros(31, dtype=int)

    for info in data:
        days[int(info[target_label].split(' ')[0].split('-')[2]) - 1] += 1

    plt.plot(days_name, days, marker='o')
    plt.title(f"Relation between days and {title}")
    plt.xticks(fontsize=font_size)
    plt.grid()
    plt.xlabel("Days")

def get_measures(data : np.ndarray) -> dict:
    return {'Mean' : st.mean(data), 'Median' : st.median(data), 'SD' : st.stdev(data)}

def check_relation(first_data : np.ndarray, second_data : np.ndarray, first_label : str, second_label : str):
    plt.scatter(x=first_data, y=second_data)
    plt.xlabel(first_label)
    plt.ylabel(second_label)
    plt.grid()
    plt.show()

def hypotesis_analysis(statistics : float, p_value : float, coefficient : str):
    print(f"{coefficient} : {statistics:.4f}\nP-value : {p_value:.4f}")

    if p_value < significance:
        print("The null hypotesis is rejected\n")

    else:
        print("The null hypotesis is not rejected\n")