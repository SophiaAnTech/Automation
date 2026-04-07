!pip install pandas openpyxl

def merge_sales_reports():
    """Merge quarterly sales reports into one consolidated report"""
    
    print("🔄 Merging quarterly sales reports...\n")
    
    # Read all quarterly sales files
    q1 = pd.read_excel('sales_q1_2024.xlsx')
    q2 = pd.read_excel('sales_q2_2024.xlsx')
    q3 = pd.read_excel('sales_q3_2024.xlsx')
    
    # Add quarter identifier
    q1['Quarter'] = 'Q1'
    q2['Quarter'] = 'Q2'
    q3['Quarter'] = 'Q3'
    
    # Merge all quarters
    all_sales = pd.concat([q1, q2, q3], ignore_index=True)
    
    # Convert date to datetime for analysis
    all_sales['Date'] = pd.to_datetime(all_sales['Date'])
    
    # Sort by date
    all_sales = all_sales.sort_values('Date')
    
    print(f"✅ Merged {len(all_sales)} sales records from 3 quarters")
    
    return all_sales


def create_consolidated_report():
    """Create a comprehensive consolidated report with analysis"""
    
    # Merge sales data
    sales = merge_sales_reports()
    
    # Read supporting data
    customers = pd.read_excel('customer_master.xlsx')
    expenses = pd.read_excel('expenses_2024.xlsx')
    
    # Create Excel writer
    output_file = f'consolidated_report_{datetime.now().strftime("%Y%m%d")}.xlsx'
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        
        # ===== SHEET 1: All Sales Data =====
        sales.to_excel(writer, sheet_name='All_Sales', index=False)
        
        # ===== SHEET 2: Sales by Quarter =====
        sales_by_quarter = sales.groupby('Quarter').agg({
            'Total_Amount': 'sum',
            'Order_ID': 'count',
            'Quantity': 'sum'
        }).rename(columns={'Order_ID': 'Number_of_Orders'})
        
        sales_by_quarter.to_excel(writer, sheet_name='Sales_by_Quarter')
        
        # ===== SHEET 3: Sales by Product =====
        sales_by_product = sales.groupby('Product').agg({
            'Total_Amount': 'sum',
            'Order_ID': 'count',
            'Quantity': 'sum'
        }).rename(columns={'Order_ID': 'Number_of_Orders'}).sort_values('Total_Amount', ascending=False)
        
        sales_by_product.to_excel(writer, sheet_name='Sales_by_Product')
        
        # ===== SHEET 4: Sales by Region =====
        sales_by_region = sales.groupby('Region').agg({
            'Total_Amount': 'sum',
            'Order_ID': 'count',
            'Quantity': 'sum'
        }).rename(columns={'Order_ID': 'Number_of_Orders'}).sort_values('Total_Amount', ascending=False)
        
        sales_by_region.to_excel(writer, sheet_name='Sales_by_Region')
        
        # ===== SHEET 5: Sales Rep Performance =====
        sales_rep_performance = sales.groupby('Sales_Rep').agg({
            'Total_Amount': 'sum',
            'Order_ID': 'count'
        }).rename(columns={'Order_ID': 'Number_of_Orders'}).sort_values('Total_Amount', ascending=False)
        
        sales_rep_performance.to_excel(writer, sheet_name='Sales_Rep_Performance')
        
        # ===== SHEET 6: Monthly Sales Trend =====
        sales['Month'] = sales['Date'].dt.to_period('M').astype(str)
        monthly_sales = sales.groupby('Month').agg({
            'Total_Amount': 'sum',
            'Order_ID': 'count'
        }).rename(columns={'Order_ID': 'Number_of_Orders'})
        
        monthly_sales.to_excel(writer, sheet_name='Monthly_Trend')
        
        # ===== SHEET 7: Customer Master =====
        customers.to_excel(writer, sheet_name='Customer_Master', index=False)
        
        # ===== SHEET 8: Expenses =====
        expenses['Date'] = pd.to_datetime(expenses['Date'])
        expenses_sorted = expenses.sort_values('Date')
        expenses_sorted.to_excel(writer, sheet_name='Expenses', index=False)
        
        # ===== SHEET 9: Expense by Category =====
        expenses_by_category = expenses.groupby('Category').agg({
            'Amount': 'sum',
            'Expense_ID': 'count'
        }).rename(columns={'Expense_ID': 'Number_of_Expenses'}).sort_values('Amount', ascending=False)
        
        expenses_by_category.to_excel(writer, sheet_name='Expenses_by_Category')
        
        # ===== SHEET 10: Executive Summary =====
        summary_data = {
            'Metric': [
                'Total Sales Revenue',
                'Total Orders',
                'Average Order Value',
                'Total Units Sold',
                'Total Expenses',
                'Net Profit (Sales - Expenses)',
                'Number of Quarters',
                'Number of Products',
                'Number of Regions',
                'Number of Sales Reps',
                'Number of Customers'
            ],
            'Value': [
                f"${sales['Total_Amount'].sum():,.2f}",
                len(sales),
                f"${sales['Total_Amount'].mean():,.2f}",
                sales['Quantity'].sum(),
                f"${expenses['Amount'].sum():,.2f}",
                f"${sales['Total_Amount'].sum() - expenses['Amount'].sum():,.2f}",
                sales['Quarter'].nunique(),
                sales['Product'].nunique(),
                sales['Region'].nunique(),
                sales['Sales_Rep'].nunique(),
                len(customers)
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Executive_Summary', index=False)
    
    print(f"\n✅ Consolidated report created: {output_file}")
    print(f"\n📊 Report contains {len(writer.sheets)} sheets:")
    print("   1. All_Sales - Complete sales data from all quarters")
    print("   2. Sales_by_Quarter - Quarterly breakdown")
    print("   3. Sales_by_Product - Product performance")
    print("   4. Sales_by_Region - Regional analysis")
    print("   5. Sales_Rep_Performance - Sales rep rankings")
    print("   6. Monthly_Trend - Month-by-month sales")
    print("   7. Customer_Master - Customer database")
    print("   8. Expenses - All expense records")
    print("   9. Expenses_by_Category - Expense breakdown")
    print("  10. Executive_Summary - Key metrics overview")
    
    return output_file


# ============================================
# MAIN EXECUTION
# ============================================

def main():
    print("=" * 60)
    print("EXCEL CONSOLIDATION TOOL")
    print("=" * 60)
    print()
    
    # merge and create consolidated report
    print("\nSTEP 1: Creating consolidated report...")
    print("-" * 60)
    output_file = create_consolidated_report()
    
    print("\n" + "=" * 60)
    print("✅ COMPLETE!")
    print("=" * 60)
    print(f"\n📁 Open '{output_file}' to view the consolidated report")
    
    # Optional: Open the file automatically
    import webbrowser
    import os
    webbrowser.open(os.path.abspath(output_file))


if __name__ == "__main__":
    main()

'''
# generate sample files

import pandas as pd
import openpyxl
from datetime import datetime, timedelta
import random

def generate_sample_files():
    """Generate sample Excel files for testing"""
    
    # Sample data generators
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    regions = ['North', 'South', 'East', 'West']
    sales_reps = ['Alice Tan', 'Bob Lee', 'Charlie Wong', 'Diana Lim', 'Eric Ng']
    
    # ===== FILE 1: Q1 Sales Report =====
    q1_data = []
    start_date = datetime(2024, 1, 1)
    for i in range(50):
        q1_data.append({
            'Date': (start_date + timedelta(days=random.randint(0, 89))).strftime('%Y-%m-%d'),
            'Order_ID': f'ORD-Q1-{1001+i}',
            'Product': random.choice(products),
            'Quantity': random.randint(1, 20),
            'Unit_Price': random.choice([50, 75, 100, 150, 200]),
            'Region': random.choice(regions),
            'Sales_Rep': random.choice(sales_reps)
        })
    
    df_q1 = pd.DataFrame(q1_data)
    df_q1['Total_Amount'] = df_q1['Quantity'] * df_q1['Unit_Price']
    df_q1.to_excel('sales_q1_2024.xlsx', index=False)
    print("✅ Created: sales_q1_2024.xlsx")
    
    # ===== FILE 2: Q2 Sales Report =====
    q2_data = []
    start_date = datetime(2024, 4, 1)
    for i in range(50):
        q2_data.append({
            'Date': (start_date + timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d'),
            'Order_ID': f'ORD-Q2-{2001+i}',
            'Product': random.choice(products),
            'Quantity': random.randint(1, 20),
            'Unit_Price': random.choice([50, 75, 100, 150, 200]),
            'Region': random.choice(regions),
            'Sales_Rep': random.choice(sales_reps)
        })
    
    df_q2 = pd.DataFrame(q2_data)
    df_q2['Total_Amount'] = df_q2['Quantity'] * df_q2['Unit_Price']
    df_q2.to_excel('sales_q2_2024.xlsx', index=False)
    print("✅ Created: sales_q2_2024.xlsx")
    
    # ===== FILE 3: Q3 Sales Report =====
    q3_data = []
    start_date = datetime(2024, 7, 1)
    for i in range(50):
        q3_data.append({
            'Date': (start_date + timedelta(days=random.randint(0, 92))).strftime('%Y-%m-%d'),
            'Order_ID': f'ORD-Q3-{3001+i}',
            'Product': random.choice(products),
            'Quantity': random.randint(1, 20),
            'Unit_Price': random.choice([50, 75, 100, 150, 200]),
            'Region': random.choice(regions),
            'Sales_Rep': random.choice(sales_reps)
        })
    
    df_q3 = pd.DataFrame(q3_data)
    df_q3['Total_Amount'] = df_q3['Quantity'] * df_q3['Unit_Price']
    df_q3.to_excel('sales_q3_2024.xlsx', index=False)
    print("✅ Created: sales_q3_2024.xlsx")
    
    # ===== FILE 4: Customer Data =====
    customer_data = []
    for i in range(30):
        customer_data.append({
            'Customer_ID': f'CUST-{1001+i}',
            'Customer_Name': f'Company {chr(65+i%26)}',
            'Region': random.choice(regions),
            'Customer_Type': random.choice(['Enterprise', 'SME', 'Startup']),
            'Credit_Limit': random.choice([10000, 25000, 50000, 100000])
        })
    
    df_customers = pd.DataFrame(customer_data)
    df_customers.to_excel('customer_master.xlsx', index=False)
    print("✅ Created: customer_master.xlsx")
    
    # ===== FILE 5: Expense Report =====
    expense_data = []
    categories = ['Travel', 'Marketing', 'Office Supplies', 'Software', 'Training']
    start_date = datetime(2024, 1, 1)
    
    for i in range(40):
        expense_data.append({
            'Date': (start_date + timedelta(days=random.randint(0, 270))).strftime('%Y-%m-%d'),
            'Expense_ID': f'EXP-{4001+i}',
            'Category': random.choice(categories),
            'Amount': random.randint(100, 5000),
            'Department': random.choice(['Sales', 'Marketing', 'IT', 'HR']),
            'Approved_By': random.choice(sales_reps)
        })
    
    df_expenses = pd.DataFrame(expense_data)
    df_expenses.to_excel('expenses_2024.xlsx', index=False)
    print("✅ Created: expenses_2024.xlsx")
    
    print("\n📊 All sample files generated!\n")

generate_sample_files()


'''

