from sklearn.metrics.pairwise import cosine_similarity


def generate_playlist_feature(complete_feature_set, playlist_df):

    # Find song features in the playlist
    complete_feature_set_playlist = complete_feature_set[complete_feature_set['id'].isin(playlist_df['id'].values)]
    # Find all non-playlist song features
    complete_feature_set_nonplaylist = complete_feature_set[~complete_feature_set['id'].isin(playlist_df['id'].values)]
    complete_feature_set_playlist_final = complete_feature_set_playlist.drop(columns="id")

    return complete_feature_set_playlist_final.sum(axis=0), complete_feature_set_nonplaylist


def generate_playlist_recos(df, features, nonplaylist_features):

    non_playlist_df = df[df['id'].isin(nonplaylist_features['id'].values)]
    # Find cosine similarity between the playlist and the complete song set
    non_playlist_df['sim'] = cosine_similarity(nonplaylist_features.drop('id', axis=1).values,
                                               features.values.reshape(1, -1))[:, 0]
    non_playlist_df_top_40 = non_playlist_df.sort_values('sim', ascending=False).head(40)

    return non_playlist_df_top_40


def recommend_from_playlist(songDF, complete_feature_set, playlistDF_test):
    # Find feature
    complete_feature_set_playlist_vector, complete_feature_set_nonplaylist = generate_playlist_feature(
        complete_feature_set, playlistDF_test)

    # Generate recommendation
    top40 = generate_playlist_recos(songDF, complete_feature_set_playlist_vector, complete_feature_set_nonplaylist)

    return top40