import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class ForecastAccuracyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Forecast Accuracy Calculator")

        self.forecast_file = None
        self.sales_file = None
        self.output_file = None  # To store the output file location

        # Load Forecast File Button
        self.load_forecast_button = tk.Button(master, text="Load Forecast File", command=self.load_forecast_file)
        self.load_forecast_button.pack(pady=10)

        # Load Sales File Button
        self.load_sales_button = tk.Button(master, text="Load Sales File", command=self.load_sales_file)
        self.load_sales_button.pack(pady=10)

        # Calculate Forecast Accuracy Button
        self.calculate_button = tk.Button(master, text="Calculate Forecast Accuracy", command=self.calculate_forecast_accuracy)
        self.calculate_button.pack(pady=10)

        # Export Location Button
        self.export_location_button = tk.Button(master, text="Show Export Location", command=self.show_export_location)
        self.export_location_button.pack(pady=10)

        # Treeview for displaying the results
        self.tree = ttk.Treeview(master, columns=("Material", "Description", "Sum of Sales", "Sum of Forecast", "Avg MAPE"), show='headings')
        self.tree.heading("Material", text="Material")
        self.tree.heading("Description", text="Material Description")
        self.tree.heading("Sum of Sales", text="Sum of Sales")
        self.tree.heading("Sum of Forecast", text="Sum of Forecast")
        self.tree.heading("Avg MAPE", text="Avg MAPE")
        self.tree.pack(pady=10)

        # Scrollbar for the Treeview
        self.scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_forecast_file(self):
        self.forecast_file = filedialog.askopenfilename(filetypes=[
            ("CSV files", "*.csv"),
            ("Excel files", "*.xls;*.xlsx"),
            ("Text files", "*.txt")
        ])
        if self.forecast_file:
            messagebox.showinfo("Success", "Forecast file loaded successfully!")

    def load_sales_file(self):
        self.sales_file = filedialog.askopenfilename(filetypes=[
            ("CSV files", "*.csv"),
            ("Excel files", "*.xls;*.xlsx")
        ])
        if self.sales_file:
            messagebox.showinfo("Success", "Sales file loaded successfully!")

    def calculate_forecast_accuracy(self):
        if not self.forecast_file or not self.sales_file:
            messagebox.showerror("Error", "Please load both forecast and sales files.")
            return

        try:
            # Load forecast file
            if self.forecast_file.endswith('.csv'):
                forecast_df = pd.read_csv(self.forecast_file)
            elif self.forecast_file.endswith(('.xls', '.xlsx')):
                forecast_df = pd.read_excel(self.forecast_file)
            elif self.forecast_file.endswith('.txt'):
                forecast_df = pd.read_csv(self.forecast_file, delimiter='\t')

            # Load sales file
            if self.sales_file.endswith('.csv'):
                sales_df = pd.read_csv(self.sales_file)
            elif self.sales_file.endswith(('.xls', '.xlsx')):
                sales_df = pd.read_excel(self.sales_file)

            # Ensure required columns exist
            required_forecast_columns = ['plant', 'material', 'material_desc', 'oh', 'minqty', 'maxqty', 'forecast', 'ranged', 'mdq', 'jed_wh', 'ryd_wh']
            required_sales_columns = ['plant', 'material', 'sales_qty']

            missing_forecast_columns = [col for col in required_forecast_columns if col not in forecast_df.columns]
            missing_sales_columns = [col for col in required_sales_columns if col not in sales_df.columns]

            if missing_forecast_columns:
                raise ValueError(f"Forecast file is missing required columns: {', '.join(missing_forecast_columns)}")
            if missing_sales_columns:
                raise ValueError(f"Sales file is missing required columns: {', '.join(missing_sales_columns)}")

            # Normalize column names
            forecast_df['material'] = forecast_df['material'].fillna('').astype(str).str.strip().str.lower()
            sales_df['material'] = sales_df['material'].fillna('').astype(str).str.strip().str.lower()

            # Convert sales quantities to absolute values
            sales_df['sales_qty'] = sales_df['sales_qty'].abs()

            # Aggregate sales and forecast by material (sum for sales and forecast)
            forecast_agg = forecast_df.groupby('material', as_index=False).agg({'forecast': 'sum', 'material_desc': 'first'})
            sales_agg = sales_df.groupby('material', as_index=False).agg({'sales_qty': 'sum'})

            # Merge dataframes on material
            merged_df = pd.merge(forecast_agg, sales_agg, left_on='material', right_on='material', how='left')
            merged_df['sales_qty'] = merged_df['sales_qty'].fillna(0)

            # Calculate MAPE for each entry
            merged_df['mape'] = 0
            for index, row in merged_df.iterrows():
                if row['sales_qty'] > 0:
                    merged_df.at[index, 'mape'] = abs(row['sales_qty'] - row['forecast']) / row['sales_qty'] * 100

            # Calculate average MAPE
            avg_mape = merged_df['mape'].mean()

            # Create final output DataFrame
            final_output = merged_df[['material', 'material_desc', 'sales_qty', 'forecast']].copy()
            final_output['Avg MAPE'] = avg_mape

            # Rename columns for better presentation
            final_output.rename(columns={
                'sales_qty': 'Sum of Sales',
                'forecast': 'Sum of Forecast'
            }, inplace=True)

            # Ask user for output file location
            self.output_file = filedialog.asksaveasfilename(defaultextension=".xlsx", 
                                                             filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
            if not self.output_file:
                return  # User canceled the save dialog

            # Save to Excel
            final_output.to_excel(self.output_file, index=False)

            # Success message with total location
            messagebox.showinfo("Success", f"Calculation complete! Results saved to: {self.output_file}")

            # Display results in the Treeview
            self.display_results(final_output)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_results(self, data):
        # Clear existing data in the Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Insert new data
        for index, row in data.iterrows():
            self.tree.insert("", "end", values=(row['material'], row['material_desc'], row['Sum of Sales'], row['Sum of Forecast'], row['Avg MAPE']))

    def show_export_location(self):
        if self.output_file:
            messagebox.showinfo("Export Location", f"Results exported to: {self.output_file}")
        else:
            messagebox.showwarning("Warning", "No export location available. Please run the calculation first.")

def main():
    root = tk.Tk()
    app = ForecastAccuracyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()