from flask import Flask, render_template, request
from item_to_item_rec import Check_corr
import numpy as np

app = Flask(__name__)

corr = Check_corr()
product_names = corr.amazon_ratings.Product_Title.unique().tolist()

@app.route('/',methods=["GET","POST"])
def homePage():
    if request.method == "GET":
        return render_template("index.html", product_names = product_names)

    if request.method == "POST":
        searchedProductName = request.form.get("searchPrdName")
        print(searchedProductName)
        print(corr.trained)
        if not corr.trained:
            corr.check_corr(searchedProductName)

        if  searchedProductName != "":
            data = corr.recommend_product(searchedProductName)
            if type(data) is np.ndarray:
                return render_template("recommend_template.html", data=data,product_names = product_names)
            return render_template("error_template.html",product_names = product_names)
    return render_template("index.html",product_names = product_names)

if __name__ == "__main__":
    app.run(debug=False)