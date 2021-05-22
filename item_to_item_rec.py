import pandas as pd
from sklearn.decomposition import TruncatedSVD
import numpy as np


class Check_corr():
    def __init__(self):
        self.trained = False
        self.correlation_matrix = None
        self.X = None
        self.amazon_ratings = pd.read_excel('Dataset/mini_ds1.xlsx', engine='openpyxl')
        self.amazon_ratings = self.amazon_ratings.dropna()
        self.ratings_utility_matrix = None

    def check_corr(self, productId):
        print("Training model.")
        self.ratings_utility_matrix = self.amazon_ratings.pivot_table(values='Rating', index='UserID',
                                                                      columns='ProductID',
                                                                      fill_value=0)
        self.X = self.ratings_utility_matrix.T
        SVD = TruncatedSVD(n_components=10)
        decomposed_matrix = SVD.fit_transform(self.X)
        # print(decomposed_matrix.shape)

        self.correlation_matrix = np.corrcoef(decomposed_matrix)
        # print(self.correlation_matrix.shape)
        # print(self.correlation_matrix)
        self.trained = True

    def recommend_product(self, productName):
        productId = self.amazon_ratings.ProductID[self.amazon_ratings.Product_Title.isin([productName])].unique()
        if len(productId) == 1:
            product_names = list(self.X.index)
            product_index = product_names.index(productId[0])

            correlation_product_ID = self.correlation_matrix[product_index]
            Recommend = list(self.X.index[correlation_product_ID > 0.90])
            Recommend.remove(productId[0])
            recommended_product_id = Recommend[0:10]
            # print(recommended_product_id)
            recommended_product_names = self.amazon_ratings.Product_Title[
                self.amazon_ratings.ProductID.isin(recommended_product_id)].unique()
            return recommended_product_names
        return "No Product found, Please search with exact product name!"
