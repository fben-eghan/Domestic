import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

class MonthlyFinances:
    def __init__(self, income, expenses):
        self.income = income
        self.expenses = expenses
        self.savings = 0
        self.debt = 0
    
    def summary(self):
        total_expenses = sum(self.expenses)
        remaining_income = self.income - total_expenses
        print(f"Total expenses: ${total_expenses}")
        print(f"Remaining income: ${remaining_income}")
        print(f"Total savings: ${self.savings}")
        print(f"Total debt: ${self.debt}")
    
    def predict(self, data, future_months):
        X = np.arange(1, len(data) + 1).reshape(-1, 1)
        y = data
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        future_X = np.arange(len(data) + 1, len(data) + future_months + 1).reshape(-1, 1)
        future_X_scaled = scaler.transform(future_X)
        model = LinearRegression()
        model.fit(X_scaled, y)
        future_y = model.predict(future_X_scaled)
        return future_y.tolist()
    
    @staticmethod
    def load_from_csv(csv_path):
        df = pd.read_csv(csv_path)
        income = df['Income'].tolist()
        expenses = df['Expenses'].tolist()
        return MonthlyFinances(income, expenses)
    
    def visualize_expenses(self, categories=None):
        if categories is None:
            categories = {
                'Rent': 0,
                'Utilities': 0,
                'Groceries': 0,
                'Transportation': 0,
                'Entertainment': 0,
                'Other': 0
            }
        for i, expense in enumerate(self.expenses):
            categories[f'Month {i+1}'] = expense
        expenses_df = pd.DataFrame.from_dict(categories, orient='index', columns=['Amount'])
        expenses_df.plot(kind='pie', y='Amount', figsize=(8, 8))
        plt.show()
