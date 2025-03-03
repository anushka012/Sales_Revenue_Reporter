import csv
import sys
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

# Read Team Map File
def read_team_map(filename):
    team_map = {}
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            team_id, team_name = row
            team_map[int(team_id)] = team_name
    return team_map

# Read Product Master File
def read_product_master(filename):
    product_map = {}
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            product_id, name, price, lot_size = row
            product_map[int(product_id)] = {
                'name': name,
                'price': float(price),
                'lot_size': int(lot_size)
            }
    return product_map

# Process Sales Data
def process_sales(filename, team_map, product_map):
    team_revenue = defaultdict(float)
    product_data = defaultdict(lambda: {'gross_revenue': 0, 'total_units': 0, 'discount_cost': 0})
    
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # ✅ Skip the header row
        for row in reader:
            sale_id, product_id, team_id, quantity, discount = row
            product_id, team_id, quantity = int(product_id), int(team_id), int(quantity)
            discount = float(discount)
            
            if product_id in product_map and team_id in team_map:
                product = product_map[product_id]
                
                units_sold = quantity * product['lot_size']
                revenue = units_sold * product['price']
                discount_cost = revenue * (discount / 100)
                
                team_revenue[team_map[team_id]] += revenue
                product_data[product['name']]['gross_revenue'] += revenue
                product_data[product['name']]['total_units'] += units_sold
                product_data[product['name']]['discount_cost'] += discount_cost
    
    return team_revenue, product_data

# Write Team Report CSV
def write_team_report(filename, team_revenue):
    sorted_teams = sorted(team_revenue.items(), key=lambda x: x[1], reverse=True)
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Team", "GrossRevenue"])
        for team, revenue in sorted_teams:
            writer.writerow([team, f"{revenue:.2f}"])

# Write Product Report CSV
def write_product_report(filename, product_data):
    sorted_products = sorted(product_data.items(), key=lambda x: x[1]['gross_revenue'], reverse=True)
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "GrossRevenue", "TotalUnits", "DiscountCost"])
        for name, data in sorted_products:
            writer.writerow([name, f"{data['gross_revenue']:.2f}", data['total_units'], f"{data['discount_cost']:.2f}"])

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