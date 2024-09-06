import json
import matplotlib.pyplot as plt
import numpy as np

from script.config import *
from script.functions import months_and_hours_review, pie_review, unique

# TO-DO
# ver se todos os gráficos estão de acordo com a proposta da análise ou se possui algum gráfico melhor para tal análise
# fazer testes de hipótese
# comentar o código

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
    accounts = np.array([])
    total_messages = np.array([])

    my_messages = np.array([])
    other_messages = np.array([])

    for key, value in data.messages['Chat History']['ChatHistory'].items():
        accounts = np.append(accounts, key.split(' ')[-1].split(':')[0])
        total_messages = np.append(total_messages, len(value))

        for info in value:
            if info['From'] == "jp__bezerra":
                my_messages = np.append(my_messages, info)

            else:
                other_messages = np.append(other_messages, info)

    plt.pie(
            x=total_messages, labels=accounts, autopct='%1.1f%%', colors=my_colors,
            pctdistance=0.85
    )

    plt.title("Quantidade de mensagens recebidas por conta")
    plt.show()

    months_and_hours_review(my_messages, "messages", "quantidade de mensagens enviadas por mim")
    months_and_hours_review(other_messages, "messages", "quantidade de mensagens enviadas por outros usuários")

def comments_analysis(data : Data) -> None:
    comments = np.array(data.comments['Comments']['CommentsList'])
    months_and_hours_review(comments, "comments", "quantidade de comentários")

    sizes = np.array([])
    for comment in comments:
        sizes = np.append(sizes, len(comment['Comment']))

    print(f"Possuo a média de digitar {np.mean(sizes):.2f} caracteres por comentário feito")

def activity_analysis(data : Data) -> None:
    fav_video_list = np.array(data.activity['Favorite Videos']['FavoriteVideoList'])
    months_and_hours_review(fav_video_list, "favorites", "quantidade de favoritos")

    like_list = np.array(data.activity['Like List']['ItemFavoriteList'])
    months_and_hours_review(like_list, "likes", "quantidade de curtidas")
    # may - august

    search_history = np.array(data.activity['Search History']['SearchList'])
    months_and_hours_review(search_history, "searchs", "quantidade de pesquisas")
    search_term = unique(search_history, 'SearchTerm')
    print(f"I've searched {len(search_term)} different terms on tiktok")
    # march - august

    share_history = np.array(data.activity['Share History']['ShareHistoryList'])
    months_and_hours_review(share_history, "shares", "quantidade de compartilhamentos")
    # march - august

    video_browsing_history = np.array(data.activity['Video Browsing History']['VideoList'])
    months_and_hours_review(video_browsing_history, "watched videos", "quantidade de vídeos assistidos")
    # february - august

    login_history = np.array(data.activity['Login History']['LoginHistoryList'])
    months_and_hours_review(login_history, "logins", "quantidade de logins")
    # march - august

    pie_review(login_history, 'NetworkType', "logins por networks diferentes")

def ads_analysis(data : Data) -> None:
    ads_activity = np.array(data.ads['Off TikTok Activity']['OffTikTokActivityDataList'])
    months_and_hours_review(ads_activity, "ads", "quantidade de anúncios", target_label='TimeStamp')
    pie_review(ads_activity, 'Event', "diferentes reações à anúncios")
    sources = unique(ads_activity, 'Source')
    print(f"I've had {len(sources)} different source-ads on tiktok")

def main() -> None:
    data = Data()
    messages_analysis(data)
    comments_analysis(data)
    activity_analysis(data)
    ads_analysis(data)

if __name__ == "__main__":
    main()