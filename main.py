import json
import matplotlib.pyplot as plt

class Data:
    data_json_path = "user_data_tiktok.json"

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
    accounts = []
    total_messages = []

    for key, value in data.messages['Chat History']['ChatHistory'].items():
        accounts.append(key.split(' ')[-1].split(':')[0])
        total_messages.append(len(value))

    # gráfico bom, mudar cores e tentar fazer com que os nomes não se sobressaiam
    # talvez mudar o tipo de gráfico
    plt.style.use('_mpl-gallery-nogrid')
    plt.pie(total_messages, labels=accounts, autopct='%1.1f%%')
    plt.title("Quantidade de mensagens recebidas por conta")
    plt.show()

def comments_analysis(data : Data) -> None:
    # pensei em horários de comentários e meses mais comentados

    months = {
        'January' : 0,
        'February' : 0,
        'March' : 0,
        'April' : 0,
        'May': 0,
        'June': 0,
        'July': 0,
        'August': 0,
        'September' : 0,
        'October' : 0,
        'November' : 0,
        'December' : 0
    }

    timetable = {
        '00' : 0,
        '01': 0,
        '02': 0,
        '03': 0,
        '04': 0,
        '05': 0,
        '06': 0,
        '07': 0,
        '08': 0,
        '09': 0,
        '10': 0,
        '11': 0,
        '12': 0,
        '13': 0,
        '14': 0,
        '15': 0,
        '16': 0,
        '17': 0,
        '18': 0,
        '19': 0,
        '20': 0,
        '21': 0,
        '22': 0,
        '23': 0,
    }

    for comment in data.comments['Comments']['CommentsList']:
        date, time = comment['Date'].split(' ')

        # months
        match date.split('-')[1]:
            case '01':
                months['January'] += 1
            case '02':
                months['February'] += 1
            case '03':
                months['March'] += 1
            case '04':
                months['April'] += 1
            case '05':
                months['May'] += 1
            case '06':
                months['June'] += 1
            case '07':
                months['July'] += 1
            case '08':
                months['August'] += 1
            case '09':
                months['September'] += 1
            case '10':
                months['October'] += 1
            case '11':
                months['November'] += 1
            case '12':
                months['December'] += 1

        # timetable
        timetable[time.split(':')[0]] += 1

    # months graphic
    plt.style.use('_mpl-gallery-nogrid')
    plt.bar(months.keys(), months.values())
    plt.title("Relação entre meses do ano e quantidade de comentários")
    plt.show()

    # timetable graphic
    plt.style.use('_mpl-gallery')
    plt.bar(timetable.keys(), timetable.values())
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