import pdb
import csv
from math import sqrt

rows = []
csvFile = open('user_book.csv', 'r')
reader = csv.reader(csvFile)
for row in reader:
     rows.append(row)
rows.remove(rows[0]) #remove 1st row
print("rows:\n%s\n" % rows)
csvFile.close()

users = {}
for row in rows:
     if row[0] not in users:        
          users[row[0]] = {}
     users[row[0]][row[2]] = float(row[1])
print("users:\n%s\n" % users)


class recommender:
    #k：the nearest k neighbors
    #cnt：recommend count
    def __init__(self, dataset, k=3, cnt=2):
        self.k = k
        self.cnt = cnt
        if type(dataset).__name__ == 'dict':
            self.dataset = dataset
      

    # pearson correlation coefficient
    def pearson(self, touser, dataset):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_xx = 0
        sum_yy = 0
        n = 0
        for key in touser:
            if key in dataset:
                n += 1
                x = touser[key]
                y = dataset[key]
                sum_x += x
                sum_y += y
                sum_xy += x * y
                sum_xx += pow(x, 2)
                sum_yy += pow(y, 2)
        if n == 0:
            return 0
        
        denominator = sqrt(sum_xx - pow(sum_x, 2) / n)  * sqrt(sum_yy - pow(sum_y, 2) / n)
        if denominator == 0:
            return 0
        else:
            numerator = sum_xy - (sum_x * sum_y) / n
            return numerator / denominator

    
    def neighbors(self, username):
        distances = []
        for key in self.dataset:
            if key != username:
                distance = self.pearson(self.dataset[username],self.dataset[key])
                distances.append((key, distance))

        distances.sort(key=lambda artistTuple: artistTuple[1],reverse=True)
        return distances
    

    def recommend_to_user(self, user):
        # store recommended bookid and weight
        recommendations = {}
        neighborlist = self.neighbors(user)
        user_dict = self.dataset[user]
        
        totalDistance = 0.0
        
        # total distance of the nearest k neighbors
        for i in range(self.k):
            totalDistance += neighborlist[i][1]
        if totalDistance==0.0:
            totalDistance=1.0
 
        #recommend books to to_user who never read
        for i in range(self.k):
            weight = neighborlist[i][1] / totalDistance
            
            neighbor_name = neighborlist[i][0]
            #book and score of user i
            neighbor_books = self.dataset[neighbor_name]
            for bookid in neighbor_books:
                if not bookid in user_dict:
                    if bookid not in recommendations:
                        recommendations[bookid] = neighbor_books[bookid] * weight
                    else:
                        recommendations[bookid] += neighbor_books[bookid] * weight
                        
        # convert dict to list
        print("recomend bookid and score weight:\n%s\n" % recommendations)
        recommendations = list(recommendations.items())
        
        # sort descending
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse = True)

        return recommendations[:self.cnt]

def recommend_bookid_to_user(username):
    bookid_list = []
    r = recommender(users)
    bookid_and_weight_list = r.recommend_to_user(username)
    print ("Recommend bookid and weight:",bookid_and_weight_list)
    for i in range(len(bookid_and_weight_list)):
        bookid_list.append(bookid_and_weight_list[i][0])
    print ("Recommended bookid: ", bookid_list)
        
if __name__ == '__main__':
   recommend_bookid_to_user("Li Si")
