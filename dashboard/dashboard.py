import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

seller_df = pd.read_csv("https://raw.githubusercontent.com/faizahhanif/ecommerce_dicoding/main/sellers_dataset.csv")
seller_df.head()

product_df = pd.read_csv("https://raw.githubusercontent.com/faizahhanif/ecommerce_dicoding/main/products_dataset.csv")
product_df.head()

order_item_df = pd.read_csv("https://raw.githubusercontent.com/faizahhanif/ecommerce_dicoding/main/order_items_dataset.csv")
order_item_df.head()

seller_df.info()

seller_df.isna().sum()

print("Jumlah duplikasi: ", seller_df.duplicated().sum())

product_df.info()

product_df.isna().sum()

print("Jumlah duplikasi: ", product_df.duplicated().sum())

product_df.describe()


order_item_df.info()

order_item_df.isna().sum()

print("Jumlah duplikasi: ", order_item_df.duplicated().sum())

order_item_df.describe()

product1_df = product_df.dropna()
product1_df.isna().sum()

product_order_df = pd.merge(
    left=product1_df,
    right=order_item_df,
    how="left",
    left_on="product_id",
    right_on="product_id"
)
product_order_df.head()

product_order_df.groupby(by="product_category_name").agg({
    "order_id": "nunique",
    "order_item_id": "sum",
    "price": "sum"
}).sort_values(by="order_item_id", ascending=False)

seller_order_df = pd.merge(
    left=seller_df,
    right=order_item_df,
    how="left",
    left_on="seller_id",
    right_on="seller_id"
)
seller_order_df.head()

seller_order_df.groupby(by="seller_city").agg({
    "order_id": "nunique",
    "order_item_id": "sum",
    "price": "sum"
}).sort_values(by="order_item_id", ascending=False)

product_order_df.info()

seller_order_df.info()

sum_order_items_df = product_order_df.groupby("product_category_name").order_item_id.sum().sort_values(ascending=False).reset_index()
sum_order_items_df.head(15)
st.subheader("Best & Worst Performing Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="order_item_id", y="product_category_name", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Performing Product", loc="center", fontsize=15)
ax[0].tick_params(axis ='y', labelsize=12)

sns.barplot(x="order_item_id", y="product_category_name", data=sum_order_items_df.sort_values(by="order_item_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig)
plt.suptitle("Best and Worst Performing Product Category by Number of Sales", fontsize=20)
plt.show()

seller_city_order_df = seller_order_df.groupby("seller_city").order_item_id.sum().sort_values(ascending=False).reset_index()
seller_city_order_df.head(15)

st.subheader("Kota dengan Seller penerima Order Terbanyak")
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(24, 6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="order_item_id", y="seller_city", data=seller_city_order_df.head(5), palette=colors)
plt.title("Kota dengan Seller Penerima Order Terbanyak", loc="center", fontsize=15)
plt.tick_params(axis ='y', labelsize=12)

st.pyplot(fig)
plt.show()

