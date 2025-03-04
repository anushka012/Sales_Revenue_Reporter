import csv
import sys
import os
import argparse
from collections import defaultdict

# Argument Parsing using argparse
def parse_arguments():
    parser = argparse.ArgumentParser(description="Sales Revenue Reporter")
    parser.add_argument("-t", "--team-map", required=True, help="Path to TeamMap.csv")
    parser.add_argument("-p", "--product-master", required=True, help="Path to ProductMaster.csv")
    parser.add_argument("-s", "--sales", required=True, help="Path to Sales.csv")
    parser.add_argument("--team-report", required=True, help="Path to output TeamReport.csv")
    parser.add_argument("--product-report", required=True, help="Path to output ProductReport.csv")
    
    return parser.parse_args()

# File existence check
def check_file_exists(filename):
    if not os.path.exists(filename):
        print(f"Error: The required file '{filename}' is missing. Please ensure it is in the correct directory.")
        sys.exit(1)  # Exit the program gracefully

# Read Team Map File
def read_team_map(filename):
    check_file_exists(filename)  # Ensure the file exists
    
    team_map = {}
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) != 2:
                    print(f"Error: Incorrect data format in '{filename}'")
                    sys.exit(1)
                team_id, team_name = row
                team_map[int(team_id)] = team_name
    except Exception as e:
        print(f"Error reading '{filename}': {e}")
        sys.exit(1)
    
    return team_map

# Read Product Master File
def read_product_master(filename):
    check_file_exists(filename)  # Ensure the file exists

    product_map = {}
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:  
                if len(row) != 4:
                    print(f"Error: Incorrect data format in '{filename}'")
                    sys.exit(1)
                product_id, name, price, lot_size = row
                product_map[int(product_id)] = {
                    'name': name,
                    'price': float(price),
                    'lot_size': int(lot_size)
                }
    except Exception as e:
        print(f"Error reading '{filename}': {e}")
        sys.exit(1)

    return product_map

# Process Sales Data
def process_sales(filename, team_map, product_map):
    check_file_exists(filename)  # Ensure the file exists

    team_revenue = defaultdict(float)
    product_data = defaultdict(lambda: {'gross_revenue': 0, 'total_units': 0, 'discount_cost': 0})

    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:  
                if len(row) != 5:
                    print(f"Error: Incorrect data format in '{filename}'")
                    sys.exit(1)
                
                sale_id, product_id, team_id, quantity, discount = row
                try:
                    product_id, team_id, quantity = int(product_id), int(team_id), int(quantity)
                    discount = float(discount)
                except ValueError:
                    print(f"Error: Invalid numeric values in '{filename}'")
                    sys.exit(1)

                # Ensure product and team exist in mappings
                if product_id not in product_map:
                    print(f"Error: ProductId {product_id} in '{filename}' does not exist in ProductMaster.csv.")
                    sys.exit(1)
                if team_id not in team_map:
                    print(f"Error: TeamId {team_id} in '{filename}' does not exist in TeamMap.csv.")
                    sys.exit(1)

                product = product_map[product_id]
                units_sold = quantity * product['lot_size']
                revenue = units_sold * product['price']
                discount_cost = revenue * (discount / 100)

                team_revenue[team_map[team_id]] += revenue
                product_data[product['name']]['gross_revenue'] += revenue
                product_data[product['name']]['total_units'] += units_sold
                product_data[product['name']]['discount_cost'] += discount_cost
    except Exception as e:
        print(f"Error reading '{filename}': {e}")
        sys.exit(1)

    return team_revenue, product_data

# Write Team Report CSV
def write_team_report(filename, team_revenue):
    try:
        sorted_teams = sorted(team_revenue.items(), key=lambda x: x[1], reverse=True)
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Team", "GrossRevenue"])
            for team, revenue in sorted_teams:
                writer.writerow([team, f"{revenue:.2f}"])
    except Exception as e:
        print(f"Error writing '{filename}': {e}")
        sys.exit(1)

# Write Product Report CSV
def write_product_report(filename, product_data):
    try:
        sorted_products = sorted(product_data.items(), key=lambda x: x[1]['gross_revenue'], reverse=True)
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "GrossRevenue", "TotalUnits", "DiscountCost"])
            for name, data in sorted_products:
                writer.writerow([name, f"{data['gross_revenue']:.2f}", data['total_units'], f"{data['discount_cost']:.2f}"])
    except Exception as e:
        print(f"Error writing '{filename}': {e}")
        sys.exit(1)

# Main Function
def main():
    args = parse_arguments()  # Use argparse to get arguments

    team_map_file = args.team_map
    product_master_file = args.product_master
    sales_file = args.sales
    team_report_file = args.team_report
    product_report_file = args.product_report

    team_map = read_team_map(team_map_file)
    product_map = read_product_master(product_master_file)
    team_revenue, product_data = process_sales(sales_file, team_map, product_map)

    write_team_report(team_report_file, team_revenue)
    write_product_report(product_report_file, product_data)
    print("Reports generated successfully!")

if __name__ == "__main__":
    main()