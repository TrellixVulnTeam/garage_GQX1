from .models import Review,Cluster
from django.contrib.auth import get_user_model
User = get_user_model()
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix
import numpy as np

#update_clusters function performs cluster assignment in three steps
#and only updates if the number of total reviews in the system satisfies a certain equation


def update_clusters():
    num_reviews = Review.objects.count()
    print (num_reviews)
    # update_step = ((num_reviews/100)+1) * 5
    update_step = 1
    print (update_step)
    if num_reviews % update_step==0:
        # get a list of all user_names
        #get a list of mechprofile ids
        all_user_names = list(map(lambda x: x.username, User.objects.only("username")))
        all_mechprofile_ids=set(map(lambda x: x.mechprofile.id, Review.objects.only("mechprofile")))
        num_users= len(all_user_names)
        ratings_m=dok_matrix((num_users,max(all_mechprofile_ids)+1),dtype=np.float32)
        for i in range(num_users):# each user corresponds to a row ,in the order of all_user_names
            user_reviews=Review.objects.filter(user_name=all_user_names[i])
            for user_review in user_reviews:
                ratings_m[i,user_review.mechprofile.id]=user_review.rating


                #Perform kmeans clustering
                k = int(num_users /100) + 4
                kmeans=KMeans(n_clusters=k)
                clustering = kmeans.fit(ratings_m.tocsr())

      # Update clusters

        Cluster.objects.all().delete()
        new_clusters = {i: Cluster(name=i) for i in range(k)}
        for cluster in new_clusters.values(): # clusters need to be saved before refering to users
            cluster.save()
        for i,cluster_label in enumerate(clustering.labels_):
            new_clusters[cluster_label].users.add(User.objects.get(username=all_user_names[i]))


        print (new_clusters)



# def update_clusters():
#     num_reviews = Review.objects.count()
#     print (num_reviews)
#     # update_step = ((num_reviews/100)+1) * 5
#     update_step = 6
#     print (update_step)
#     if num_reviews % update_step == 0: # using some magic numbers here, sorry...
#         # Create a sparse matrix from user reviews
#         all_user_names = list(map(lambda x: x.username, User.objects.only("username")))
#         all_mechprofile_ids = set(map(lambda x: x.mechprofile.id, Review.objects.only("mechprofile")))
#         num_users = len(all_user_names)
#         ratings_m = dok_matrix((num_users, max(all_mechprofile_ids)+1), dtype=np.float32)
#         for i in range(num_users): # each user corresponds to a row, in the order of all_user_names
#             user_reviews = Review.objects.filter(user_name=all_user_names[i])
#             for user_review in user_reviews:
#                 ratings_m[i,user_review.mechprofile.id] = user_review.rating
#
#         # Perform kmeans clustering
#         k = int(num_users / 3) + 2
#         kmeans = KMeans(n_clusters=k)
#         clustering = kmeans.fit(ratings_m.tocsr())
#
#         # Update clusters
#         Cluster.objects.all().delete()
#         new_clusters = {i: Cluster(name=i) for i in range(k)}
#         for cluster in new_clusters.values(): # clusters need to be saved before referring to users
#             cluster.save()
#         for i,cluster_label in enumerate(clustering.labels_):
#             new_clusters[cluster_label].users.add(User.objects.get(username=all_user_names[i]))
#
#         print (new_clusters)
#



