import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest

from script.code.config import *
from script.code.functions import months_and_hours_review, pie_review, unique, line_review, get_measures, \
    check_relation, hypotesis_analysis


class Data:
    data_json_path = data_path

    def __init__(self) -> None:
        self.data = pd.read_json(data_path)

        self.activity = self.data["Activity"]
        self.ads = self.data['Ads and data']
        self.comments = self.data['Comment']
        self.messages = self.data['Direct Messages']

        self.guard = {}


def messages_analysis(data: Data) -> None:
    chat_history : dict[str, list] = data.messages['Chat History']['ChatHistory']

    info : dict[str, int] = {}
    measures_each_account : np.ndarray = np.array([])
    account_names : np.ndarray = np.array([])

    my_messages = np.array([])
    other_messages = np.array([])

    for key, value in chat_history.items():
        if 10 > len(value):
            try:
                info['Others'] += len(value)

            except KeyError:
                info['Others'] = len(value)

        else:
            info[key.split(' ')[-1].split(':')[0]] = len(value)

        account_names = np.append(account_names, key)
        measures_each_account = np.append(measures_each_account, len(value))

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

    plt.title("Amount of messages by account")
    plt.show()

    # gráfico sobre mensagens enviadas por mim em relação à meses-horas
    m_sent, h_sent = months_and_hours_review(my_messages, "messages", "amount of messages sent by me")

    # gráfico sobre mensagens enviadas por outros em relação à meses-horas
    m_receive, h_receive = months_and_hours_review(other_messages, "messages", "amount of messages sent by other users")

    list_messages = list(info.values())
    max_value = np.max(list_messages)
    label_max = list(info.keys())[list_messages.index(max_value)]

    print(f"With {max_value} messages, the person who I have most messages with is {label_max}")

    line_review(chat_history[f"Chat History with {label_max}:"], 'Date', f"amount of messages with {label_max}")
    plt.ylabel("Messages")
    plt.show()

    measures = get_measures(measures_each_account)
    print(f"Mean : {measures['Mean']}\nMedian : {measures['Median']}\nStandard Deviation : {measures['SD']}")

    data.guard['Messages'] = {'M' : [m_sent, m_receive], 'H' : [h_sent, h_receive]}


def comments_analysis(data : Data) -> None:
    comments = np.array(data.comments['Comments']['CommentsList'])

    # gráfico sobre comentários enviados por mim em relação à meses-horas
    m_comments, h_comments = months_and_hours_review(comments, "comments", "amount of comments")

    sizes = np.array([])
    for comment in comments:
        sizes = np.append(sizes, len(comment['Comment']))

    # média de caracteres por comentário
    print(f"I have an average of typing {np.mean(sizes):.2f} characters per comment")

    data.guard['Comments'] = {'M' : m_comments, 'H' : h_comments}


def activity_analysis(data : Data) -> None:
    fav_video_list = np.array(data.activity['Favorite Videos']['FavoriteVideoList'])

    # gráfico sobre favoritos em relação à meses-horas
    m_fav, h_fav = months_and_hours_review(fav_video_list, "favorites", "amount of favorites")

    like_list = np.array(data.activity['Like List']['ItemFavoriteList'])

    # gráfico sobre likes em relação à meses-horas
    m_likes, h_likes = months_and_hours_review(like_list, "likes", "amount of likes")
    # may - august

    search_history = np.array(data.activity['Search History']['SearchList'])

    # gráfico sobre pesquisas em relação à meses-horas
    m_search, h_search = months_and_hours_review(search_history, "searchs", "amount of searchs")
    # march - august

    share_history = np.array(data.activity['Share History']['ShareHistoryList'])

    # gráfico sobre compartilhamentos em relação à meses-horas
    m_share, h_share = months_and_hours_review(share_history, "shares", "amount of shares")
    # march - august

    video_browsing_history = np.array(data.activity['Video Browsing History']['VideoList'])

    # gráfico sobre vídeos assistidos em relação à meses-horas
    m_video, h_video = months_and_hours_review(video_browsing_history, "watched videos", "amount of watched videos")
    # february - august

    login_history = np.array(data.activity['Login History']['LoginHistoryList'])

    # gráfico sobre quantidade de logins em relação à meses-horas
    months_and_hours_review(login_history, "logins", "amount of logins", return_data=False)
    # march - august

    # gráfico sobre tipos de login
    pie_review(login_history, 'NetworkType', "logins per networks type")

    check_relation(h_video, h_likes, "Videos p/ hour", "Likes p/ hour")
    check_relation(h_likes, h_share, "Likes p/ hour", "Shares p/ hour")
    check_relation(h_search, h_video, "Searchs p/ hour", "Videos p/ hour")

    search_term = unique(search_history, 'SearchTerm')

    # quantidades de termos diferentes pesquisados
    print(f"I've searched {len(search_term)} different terms on tiktok")

    data.guard['Favorites'] = {'M': m_fav, 'H': h_fav}
    data.guard['Search'] = {'M' : m_search, 'H' : h_search}
    data.guard['Share'] = {'M': m_share, 'H': h_share}
    data.guard['Watched'] = {'M' : m_video}


def ads_analysis(data : Data) -> None:
    ads_activity = np.array(data.ads['Off TikTok Activity']['OffTikTokActivityDataList'])

    # gráfico sobre quantidades de anúncios em relação à meses-horas
    months_and_hours_review(ads_activity, "ads", "amount of ads", target_label='TimeStamp')

    # gráfico sobre diferentes reações à anúncios
    pie_review(ads_activity, 'Event', "different reactions to ads")

    sources = unique(ads_activity, 'Source')

    # quantidade de anunciantes diferentes
    print(f"I've had {len(sources)} different source-ads on tiktok")


def hypoteses(data : Data) -> None:
    # HYPOTESIS 1
    # - The times and months when I receive the most messages tend to be the same times when I send the most
    # - Two-sided hypotesis
    # - H0: the times and months for receiving/sending messages are different
    # - HA: the times and months for receiving/sending messages are the same
    # - 5% significance level

    s_hip1_h, p_hip1_h = stats.pearsonr(data.guard['Messages']['H'][0], data.guard['Messages']['H'][1])
    hypotesis_analysis(s_hip1_h, p_hip1_h, "Pearson correlation coefficient")
    # pode falar que ta proxima de 1, e positiva

    s_hip1_m, p_hip1_m = stats.pearsonr(data.guard['Messages']['M'][0], data.guard['Messages']['M'][1])
    hypotesis_analysis(s_hip1_m, p_hip1_m, "Pearson correlation coefficient")

    # HYPOTESIS 2
    # - The times and months when I share the most tend to be the same times when I research the most
    # - Two-sided hypotesis
    # - H0: sharing/search times and months are different
    # - HA: sharing/search times and months are the same
    # - 5% significance level

    s_hip2_h, p_hip2_h = stats.pearsonr(data.guard['Share']['H'], data.guard['Search']['H'])
    hypotesis_analysis(s_hip2_h, p_hip2_h, "Pearson correlation coefficient")

    s_hip2_m, p_hip2_m = stats.pearsonr(data.guard['Share']['M'], data.guard['Search']['M'])
    hypotesis_analysis(s_hip2_m, p_hip2_m, "Pearson correlation coefficient")

    # HYPOTESIS 3
    # - The proportion of liked videos is similar to the proportion of non-liked videos
    # - Two-sided hypotesis
    # - H0: the proportion of liked videos is the same as the proportion of non-liked videos
    # - HA: the proportion of liked videos is different to the proportion of non-liked videos
    # - 5% significance level

    liked_videos = len(np.array(data.activity['Like List']['ItemFavoriteList']))
    watched_videos = len(np.array(data.activity['Video Browsing History']['VideoList'])) - liked_videos - data.guard['Watched']['M'][1]

    s_hip3, p_hip3 = proportions_ztest(
        np.array([liked_videos, watched_videos]),
        np.array([liked_videos + watched_videos, liked_videos + watched_videos]),
        alternative='two-sided'
    )

    hypotesis_analysis(s_hip3, p_hip3, "Z-Statistic")


def main() -> None:
    data = Data()
    messages_analysis(data)
    comments_analysis(data)
    activity_analysis(data)
    ads_analysis(data)
    hypoteses(data)


if __name__ == "__main__":
    main()