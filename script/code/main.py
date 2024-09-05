import json
import matplotlib.pyplot as plt
import numpy as np
from config import*

class Data:
    data_json_path = data_path

    def __init__(self) -> None:
        with open(Data.data_json_path, "r", encoding="utf-8") as file:
            self.data = json.load(file)

            file.close()

        self.get_main_labels()

    def get_main_labels(self) -> None:
        self.activity = self.data["Activity"]
        self.ads = self.data['Ads and data']
        self.settings = self.data['App Settings']
        self.comments = self.data['Comment']
        self.messages = self.data['Direct Messages']
        self.wallet = self.data['Income Plus Wallet Transactions']
        self.POI = self.data['Poi Review']
        self.profile = self.data['Profile']
        self.lives = self.data['Tiktok Live']
        self.shopping = self.data['Tiktok Shopping']
        self.video = self.data['Video']

def messages_analysis(data: Data) -> None:
    # gráfico de pizza em relação à quantidade de mensages de cada usuário, colocar o nome de label com o username
    accounts = np.array([])
    total_messages = np.array([])

    for key, value in data.messages['Chat History']['ChatHistory'].items():
        accounts = np.append(accounts, key.split(' ')[-1].split(':')[0])
        total_messages = np.append(total_messages, len(value))

    # gráfico bom, mudar cores e tentar fazer com que os nomes não se sobressaiam
    # talvez mudar o tipo de gráfico
    plt.style.use('_mpl-gallery-nogrid')
    plt.pie(total_messages, labels=accounts, autopct='%1.1f%%')
    plt.title("Quantidade de mensagens recebidas por conta")
    plt.show()

def comments_analysis(data : Data) -> None:
    months = np.zeros(12, dtype=int)
    timetable = np.zeros(24, dtype=int)

    for comment in data.comments['Comments']['CommentsList']:
        date, time = comment['Date'].split(' ')

        months[int(date.split('-')[1]) - 1] += 1
        timetable[int(time.split(':')[0])] += 1

    # months graphic
    plt.style.use('_mpl-gallery-nogrid')

    plt.bar(
        x=[
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ],
        height=months,
        color=my_colors
    )

    plt.xlabel("Months")
    plt.ylabel("Amount of comments")
    plt.title("Relação entre meses do ano e quantidade de comentários")
    plt.show()

    # timetable graphic
    plt.style.use('_mpl-gallery')

    plt.bar(
        x=[
            '00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
            '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
            '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
        ],
        height=timetable
    )

    plt.xlabel("Hours")
    plt.ylabel("Amount of comments")
    plt.title("Relação entre horas do dia e quantidade de comentários")
    plt.show()

    # podemos fazer uma hipótese qualquer aqui e ajeitar o gráfico, porque só é visivel se ajeitamos
    # a config do matplotlib
    # ver se utilizamos outro gráfico

def activity_review(data : Data):
    pass

def main() -> None:
    data = Data()
    messages_analysis(data)
    comments_analysis(data)

if __name__ == "__main__":
    main()