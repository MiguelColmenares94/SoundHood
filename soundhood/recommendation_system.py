#!/usr/bin/python3
""" Module for the recomendation system calculations """

def jaccard_similarity(tracks, users_tracks):

    tracks = set(tracks)

    jaccard_similarities = {}

    for single_user in users_tracks:
        for user, track in single_user.items():
            user_tracks = set(track)
            intersection = len(tracks.intersection(user_tracks))
            union = len(tracks.union(user_tracks))
            jaccard_similarity = intersection / union
            jaccard_similarities[user] = jaccard_similarity

    print(jaccard_similarities)
    return (jaccard_similarities)

def jaccard_distance(jaccard_similarities):
    
    jaccard_distances = {}

    for user, similarity in jaccard_similarities.items():
        distance = 1 - similarity
        jaccard_distances[user] = distance

    print (jaccard_distances)
    return (jaccard_distances)

def not_common_items(tracks, users_tracks):

    tracks = set(tracks)

    different_items = []

    for single_user in users_tracks:
        for user, track in single_user.items():
            user_tracks = set(track)
            difference = user_tracks.difference(tracks)
            different_items.extend(difference)

    print(set(different_items))
    return (set(different_items))
