import json
import matplotlib.pyplot as plt
import numpy as np

from script.code.config import *
from script.code.functions import months_and_hours_review, pie_review, unique

# TO-DO
# fazer testes de hipótese
# tentar fazer um pie_review que abrange o pie de message, colocando a label 'Others'

class Data:
    data_json_path = data_path

    def __init__(self) -> None:
        with open(Data.data_json_path, "r", encoding="utf-8") as file:
            self.data = json.load(file)

            file.close()

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
    info : dict[str, int] = {}

    my_messages = np.array([])
    other_messages = np.array([])

    for key, value in data.messages['Chat History']['ChatHistory'].items():
        if 10 > len(value):
            try:
                info['Others'] += len(value)

            except KeyError:
                info['Others'] = len(value)

        else:
            info[key.split(' ')[-1].split(':')[0]] = len(value)

        for subdata in value:
            if subdata['From'] == "jp__bezerra":
                my_messages = np.append(my_messages, subdata)

            else:
                other_messages = np.append(other_messages, subdata)

    # gráfico sobre mensagens por conta
    plt.pie(
            x=info.values(), labels=info.keys(), autopct='%1.1f%%', colors=my_colors,
            pctdistance=0.85
    )

    plt.title("Quantidade de mensagens por conta")
    plt.show()

    # gráfico sobre mensagens enviadas por mim em relação à meses-horas
    months_and_hours_review(my_messages, "messages", "quantidade de mensagens enviadas por mim")

    # gráfico sobre mensagens enviadas por outros em relação à meses-horas
    months_and_hours_review(other_messages, "messages", "quantidade de mensagens enviadas por outros usuários")

def comments_analysis(data : Data) -> None:
    comments = np.array(data.comments['Comments']['CommentsList'])

    # gráfico sobre comentários enviados por mim em relação à meses-horas
    months_and_hours_review(comments, "comments", "quantidade de comentários")

    sizes = np.array([])
    for comment in comments:
        sizes = np.append(sizes, len(comment['Comment']))

    # média de caracteres por comentário
    print(f"Possuo a média de digitar {np.mean(sizes):.2f} caracteres por comentário feito")

def activity_analysis(data : Data) -> None:
    fav_video_list = np.array(data.activity['Favorite Videos']['FavoriteVideoList'])

    # gráfico sobre favoritos em relação à meses-horas
    months_and_hours_review(fav_video_list, "favorites", "quantidade de favoritos")

    like_list = np.array(data.activity['Like List']['ItemFavoriteList'])

    # gráfico sobre likes em relação à meses-horas
    months_and_hours_review(like_list, "likes", "quantidade de curtidas")
    # may - august

    search_history = np.array(data.activity['Search History']['SearchList'])

    # gráfico sobre pesquisas em relação à meses-horas
    months_and_hours_review(search_history, "searchs", "quantidade de pesquisas")

    search_term = unique(search_history, 'SearchTerm')

    # quantidades de termos diferentes pesquisados
    print(f"I've searched {len(search_term)} different terms on tiktok")
    # march - august

    share_history = np.array(data.activity['Share History']['ShareHistoryList'])

    # gráfico sobre compartilhamentos em relação à meses-horas
    months_and_hours_review(share_history, "shares", "quantidade de compartilhamentos")
    # march - august

    video_browsing_history = np.array(data.activity['Video Browsing History']['VideoList'])

    # gráfico sobre vídeos assistidos em relação à meses-horas
    months_and_hours_review(video_browsing_history, "watched videos", "quantidade de vídeos assistidos")
    # february - august

    login_history = np.array(data.activity['Login History']['LoginHistoryList'])

    # gráfico sobre quantidade de logins em relação à meses-horas
    months_and_hours_review(login_history, "logins", "quantidade de logins")
    # march - august

    # gráfico sobre tipos de login
    pie_review(login_history, 'NetworkType', "logins por networks diferentes")

def ads_analysis(data : Data) -> None:
    ads_activity = np.array(data.ads['Off TikTok Activity']['OffTikTokActivityDataList'])

    # gráfico sobre quantidades de anúncios em relação à meses-horas
    months_and_hours_review(ads_activity, "ads", "quantidade de anúncios", target_label='TimeStamp')

    # gráfico sobre diferentes reações à anúncios
    pie_review(ads_activity, 'Event', "diferentes reações à anúncios")

    sources = unique(ads_activity, 'Source')

    # quantidade de anunciantes diferentes
    print(f"I've had {len(sources)} different source-ads on tiktok")

def main() -> None:
    data = Data()
    messages_analysis(data)
    comments_analysis(data)
    activity_analysis(data)
    ads_analysis(data)

if __name__ == "__main__":
    main()