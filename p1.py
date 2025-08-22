from tkinter import *
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from tkinter import messagebox
import re

root = Tk()
root.title("Sales Volume Predictor")
root.geometry("650x600+50+50")
root.configure(background='azure')
f = ("Calibri", 40, "bold")
f2 = ("Calibri", 30, "bold")
f3 = ("Calibri", 20, "bold")

lab_header = Label(root, text="Sales Volume Predictor", font=f, fg="maroon")
lab_header.pack(pady=30)

lab_items = Label(root, text="Enter items_count:", font=f2)
ent_items = Entry(root, font=f2)
lab_items.pack(pady=5)
ent_items.pack(pady=5)

lab_customers = Label(root, text="Enter daily_customers:", font=f2)
ent_customers = Entry(root, font=f2)
lab_customers.pack(pady=5)
ent_customers.pack(pady=5)

# set focus on the first input field
ent_items.focus_set()

# Define the model outside the function
data = pd.read_csv("E:\kamal sir\machine learning sept 2023\internship\sales_volume_project\Stores.csv")
null_values = data.isnull().sum()
data = data.dropna()
features = data[["Items_Available", "Daily_Customer_Count"]]
target = data["Store_Sales"]
x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=0)
model = LinearRegression()
model.fit(x_train, y_train)

def find():
    try:
        items_available_str = ent_items.get()
        daily_customer_count_str = ent_customers.get()

        # validation: check for null values and disallow spaces
        if not items_available_str.strip() or not daily_customer_count_str.strip():
            messagebox.showerror("Error", "Invalid input values. Please enter numbers without spaces.")

            # clear input fields
            ent_items.delete(0, 'end')
            ent_customers.delete(0, 'end')

            # clear output field
            lab_ans.config(text="")

            # set focus on the first input field
            ent_items.focus_set()
            return

        # validation: check if the input contains alphabets or special characters
        if not re.match(r'^[-]?\d*\.?\d*$', items_available_str):
            messagebox.showerror("Error", "Invalid value for items_count. Please enter a valid number.")

            # clear input fields
            ent_items.delete(0, 'end')
            ent_customers.delete(0, 'end')

            # clear output field
            lab_ans.config(text="")

            # set focus on the first input field
            ent_items.focus_set()
            return

        if not re.match(r'^[-]?\d*\.?\d*$', daily_customer_count_str):
            messagebox.showerror("Error", "Invalid value for daily_customers. Please enter a valid number.")

            # clear input fields
            ent_items.delete(0, 'end')
            ent_customers.delete(0, 'end')

            # clear output field
            lab_ans.config(text="")

            # set focus on the first input field
            ent_items.focus_set()
            return

        items_available = float(items_available_str)
        daily_customer_count = float(daily_customer_count_str)

        # validation: check for negative numbers
        if items_available < 0 or daily_customer_count < 0:
            messagebox.showerror("Error", "Invalid input values. Please enter positive numbers only.")

            # clear input fields
            ent_items.delete(0, 'end')
            ent_customers.delete(0, 'end')

            # clear output field
            lab_ans.config(text="")

            # set focus on the first input field
            ent_items.focus_set()
            return

        def predict_sales(items_available, daily_customer_count):
            input_data = pd.DataFrame([[items_available, daily_customer_count]],
                                      columns=["Items_Available", "Daily_Customer_Count"])

            store_sales_prediction = model.predict(input_data)
            return round(store_sales_prediction[0], 3)

        # make a prediction using the Flask application logic
        store_sales_prediction = predict_sales(items_available, daily_customer_count)

        # display the prediction
        lab_ans.config(text=f"Predicted Store Sales Volume: {store_sales_prediction}")

        # clear input fields
        ent_items.delete(0, 'end')
        ent_customers.delete(0, 'end')

        # set focus on the first input field
        ent_items.focus_set()

    except ValueError:
        messagebox.showerror("Error", "Invalid input values. Please enter valid numbers.")

        # clear input fields
        ent_items.delete(0, 'end')
        ent_customers.delete(0, 'end')

        # clear output field
        lab_ans.config(text="")

        # set focus on the first input field
        ent_items.focus_set()

btn_predict = Button(root, text="Predict Sales Volume", font=f3, command=find)
lab_ans = Label(root, font=f3, fg="darkblue")
btn_predict.pack(pady=30)
lab_ans.pack(pady=10)

root.mainloop()

