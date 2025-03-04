import os
import pytest
import subprocess

# Test Missing ProductMaster.csv
def test_missing_product_master():
    result = subprocess.run(
        ["python", "report.py", "-t", "TeamMap.csv", "-p", "missing.csv", "-s", "Sales.csv", "--team-report=TeamReport.csv", "--product-report=ProductReport.csv"],
        capture_output=True, text=True
    )
    assert "Error: The required file 'missing.csv' is missing." in result.stdout

# Test Missing TeamMap.csv
def test_missing_team_map():
    result = subprocess.run(
        ["python", "report.py", "-t", "missing_team.csv", "-p", "ProductMaster.csv", "-s", "Sales.csv", "--team-report=TeamReport.csv", "--product-report=ProductReport.csv"],
        capture_output=True, text=True
    )
    assert "Error: The required file 'missing_team.csv' is missing." in result.stdout

# Test Malformed ProductMaster.csv (Missing Column)
def test_malformed_product_master():
    with open("ProductMaster.csv", "w") as f:
        f.write("1,Minor Widget,0.25\n")  # Missing LotSize

    result = subprocess.run(
        ["python", "report.py", "-t", "TeamMap.csv", "-p", "ProductMaster.csv", "-s", "Sales.csv", "--team-report=TeamReport.csv", "--product-report=ProductReport.csv"],
        capture_output=True, text=True
    )
    assert "Error: Incorrect data format in 'ProductMaster.csv'" in result.stdout