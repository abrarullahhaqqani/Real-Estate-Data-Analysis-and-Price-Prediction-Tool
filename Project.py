from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from tkinter import ttk
import matplotlib.pyplot as plt
class RealEstateApp:

    def __init__(self, root):
        # Initialize the RealEstateApp class
        self.root = root
        self.root.title("Real Estate Data Analysis Tool")
        # Define features related to real estate
        self.features = ['Price per sqfoot(avg) in 1990', 'Price per sqfoot(avg) in 2000',
                         'Price per sqfoot(avg) in 2010',
                         'Price per sqfoot(avg) in 2020']
        # Load background image
        background_image = Image.open("C:/Users/Abrarullsh/Desktop/project_image.jpeg")
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()
        background_image = background_image.resize((width, height), Image.BICUBIC)
        background_image = ImageTk.PhotoImage(background_image)

        # Display background image
        background_label = tk.Label(root, image=background_image)
        background_label.place(relwidth=1, relheight=1)
        background_label.image = background_image

        # Create GUI elements
        self.load_button = tk.Button(root, text="Load Data", command=self.load_data)
        self.load_button.pack(side="top", padx=20, pady=10)

        self.place_label = tk.Label(root, text="Select Place:")
        self.place_label.pack(side="top", padx=20, pady=10)
        self.place_var = tk.StringVar()
        self.place_dropdown = tk.OptionMenu(root, self.place_var, "No Data Available")
        self.place_dropdown.pack(side="top", padx=20, pady=10)
        self.place_dropdown.config(state="disabled")

        self.house_type_label = tk.Label(root, text="Select House Type:")
        self.house_type_label.pack(side="top", padx=20, pady=10)
        self.house_type_var = tk.StringVar()
        self.house_type_var.set("2BHK")
        self.house_type_dropdown = tk.OptionMenu(root, self.house_type_var, "2BHK", "3BHK", "4BHK")
        self.house_type_dropdown.pack(side="top", padx=20, pady=10)
        self.house_type_dropdown.config(state="active")

        self.calculated_price_range_label = tk.Label(root, text="Calculated Price Range:")
        self.calculated_price_range_label.pack(side="top", padx=20, pady=10)
        self.calculated_price_range_var = tk.StringVar()
        self.calculated_price_range_label_display = tk.Label(root, textvariable=self.calculated_price_range_var)
        self.calculated_price_range_label_display.pack(side="top", padx=20, pady=10)

        self.property_price_label = tk.Label(root, text="Property Price:")
        self.property_price_label.pack(side="top", padx=20, pady=10)
        self.property_price_var = tk.StringVar()
        self.property_price_label_display = tk.Label(root, textvariable=self.property_price_var)
        self.property_price_label_display.pack(side="top", padx=20, pady=10)

        self.calculate_button = tk.Button(root, text="Calculate Price Range", command=self.calculate_price_range)
        self.calculate_button.pack(side="top", padx=20, pady=10)
        self.calculate_button.config(state="disabled")

        self.loan_button = tk.Button(root, text="Want a Loan?", command=self.ask_for_loan)
        self.loan_button.pack(side="top", padx=20, pady=10)
        self.loan_button.config(state="disabled")

        # Initialize variables
        self.dataset = None
        self.calculated_price_range = None

        self.loan_amount = 0.0
        self.tenure = 0
        self.interest_rate = 0.0
        self.emi = 0.0

        # Display designer information
        designer_label = tk.Label(root, text="Designed by: ABRARULLAH HAQQANI\nGmail ID: abrarullahhaqqani@gmail.com",
                                  font=("Helvetica", 8), fg="white", bg="black")


        designer_label.place(relx=0.5, rely=1.0, anchor="s")




    def load_data(self):
        # Open a file dialog to select an Excel file
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        # Check if a file was selected
        if file_path:

            try:
                self.dataset = pd.read_excel(file_path)
                places = self.dataset["PLACE"].unique()

                self.place_dropdown["menu"].delete(0, "end")
                for place in places:
                    self.place_dropdown["menu"].add_command(label=place, command=tk._setit(self.place_var, place))
                self.place_dropdown.config(state="active")
                self.calculate_button.config(state="active")




                self.visualize_data()

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")



    def visualize_data(self):
        if self.dataset is None:
            messagebox.showerror("Error", "Please load data before visualizing.")
            return


        years = ['1990', '2000', '2010', '2020']

        average_prices = self.dataset[[f'Price per sqfoot(avg) in {year}' for year in years]].mean()


        plt.bar(years, average_prices)
        plt.xlabel('Year')
        plt.ylabel('Average Price per sqfoot')
        plt.title('Average Property Prices Over the Years')
        plt.show()

    def show_graph(self):
        selected_place = self.place_var.get()
        self.visualize_data_for_place(selected_place)
    def visualize_data_for_place(self, selected_place):
        if self.dataset is None:
            messagebox.showerror("Error", "Please load data before visualizing.")
            return


        selected_place_data = self.dataset[self.dataset["PLACE"] == selected_place]


        if selected_place_data.empty:
            messagebox.showwarning("Warning", f"No data available for {selected_place}.")
            return


        years = ['1990', '2000', '2010', '2020']


        prices = selected_place_data[[f'Price per sqfoot(avg) in {year}' for year in years]].iloc[0]


        plt.plot(years, prices)
        plt.xlabel('Year')
        plt.ylabel('Price per sqfoot')
        plt.title(f'Property Prices Over the Years in {selected_place}')
        plt.show()  # Add this line to display the plot

    def calculate_price_range(self):
        if self.dataset is not None:
            selected_place = self.place_var.get()
            selected_house_type = self.house_type_var.get()
            if selected_place and selected_house_type:

                condition = (self.dataset["PLACE"] == selected_place)
                price_per_sqfoot = self.dataset.loc[condition, "Price per sqfoot(avg)"].values[0]

                if selected_house_type == "2BHK":

                    price_range = (100, 150)
                elif selected_house_type == "3BHK":
                    price_range = (200, 250)
                elif selected_house_type == "4BHK":
                    price_range = (300, 350)

                avg_property_price = (price_range[0] * price_per_sqfoot + price_range[1] * price_per_sqfoot) / 2

                self.calculated_price_range = (price_range[0] * price_per_sqfoot, price_range[1] * price_per_sqfoot)
                self.calculated_price_range_var.set(
                    f"₹{self.calculated_price_range[0]:,.2f} - ₹{self.calculated_price_range[1]:,.2f}")
                self.property_price_var.set(
                    f"₹{avg_property_price:,.2f}")

                self.visualize_data_for_place(selected_place)
                self.loan_button.config(state="active")

    def ask_for_loan(self):
        if self.dataset is not None and self.calculated_price_range is not None:
            want_loan = messagebox.askyesno("Want a Loan?", "Do you want a loan for this property?")
            if want_loan:
                self.show_loan_input()

    def show_loan_input(self):
        loan_input_window = tk.Toplevel(self.root)
        loan_input_window.title("Loan Input")
        loan_input_window.geometry("400x150")

        loan_amount_label = tk.Label(loan_input_window, text="Loan Amount (in percentage of property price):")
        loan_amount_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        loan_amount_entry = tk.Entry(loan_input_window)
        loan_amount_entry.grid(row=0, column=1, padx=10, pady=5)

        tenure_label = tk.Label(loan_input_window, text="Loan Tenure (in years):")
        tenure_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tenure_entry = tk.Entry(loan_input_window)
        tenure_entry.grid(row=1, column=1, padx=10, pady=5)

        save_button = tk.Button(loan_input_window, text="Calculate Loan", command=lambda: self.calculate_loan(loan_amount_entry.get(), tenure_entry.get(), loan_input_window))
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

    def calculate_loan(self, loan_amount, tenure, window):
        try:
            loan_amount = float(loan_amount)
            tenure = int(tenure)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid values for Loan Amount and Tenure.")
            return


        if tenure == 5:
            interest_rate = 8.5
        elif tenure == 30:
            interest_rate = 10.15
        else:

            interest_rate = 8.5 + ((tenure - 5) / (30 - 5)) * (10.15 - 8.5)


        property_price = (self.calculated_price_range[1] + self.calculated_price_range[0]) / 2
        loan_amount_value = (loan_amount / 100) * property_price


        monthly_interest_rate = (interest_rate / 100) / 12
        num_monthly_payments = tenure * 12
        emi = (loan_amount_value * monthly_interest_rate * ((1 + monthly_interest_rate) ** num_monthly_payments)) / (
                ((1 + monthly_interest_rate) ** num_monthly_payments) - 1)


        self.loan_amount = loan_amount
        self.tenure = tenure
        self.interest_rate = interest_rate
        self.emi = emi


        loan_details_window = tk.Toplevel(self.root)
        loan_details_window.title("Loan Details")


        loan_details_tree = ttk.Treeview(loan_details_window, columns=(
        "Loan Amount (%)", "Tenure (years)", "Interest Rate (%)", "Monthly EMI"))
        loan_details_tree.heading("#1", text="Loan Amount (%)")
        loan_details_tree.heading("#2", text="Tenure (years)")
        loan_details_tree.heading("#3", text="Interest Rate (%)")
        loan_details_tree.heading("#4", text="Monthly EMI")


        loan_details_tree.insert("", "end", values=(loan_amount, tenure, interest_rate, emi))


        loan_details_tree.pack(padx=20, pady=10)

        window.destroy()
if __name__ == "__main__":
    root = tk.Tk()
    app = RealEstateApp(root)
    root.mainloop()

