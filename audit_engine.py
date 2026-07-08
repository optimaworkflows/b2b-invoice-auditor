import pandas as pd
import os
from datetime import datetime

def execute_autonomous_pipeline(invoice_path, shipping_path, client_name="Client_Corp"):
    print("🤖 INTEGRATED PIPELINE RUNNING...")
    
    # Check for missing file streams safely
    if not os.path.exists(invoice_path) or not os.path.exists(shipping_path):
        return {"status": "error", "message": "Source dataset arrays missing"}

    # Dynamic Timestamp Allocation (Formated precisely as requested: Org_Date)
    current_date = datetime.now().strftime("%Y_%m_%d")
    clean_org_name = client_name.strip().replace(" ", "_")
    base_filename = f"{clean_org_name}_{current_date}"
    
    # Load raw data sets seamlessly
    invoices = pd.read_csv(invoice_path)
    shipping = pd.read_csv(shipping_path)
    
    # Lowercase header translation mapping normalization
    invoices.columns = invoices.columns.str.strip().str.lower()
    shipping.columns = shipping.columns.str.strip().str.lower()
    
    # Run immutable matrix join vector arithmetic
    merged = pd.merge(invoices, shipping, on='product_id', how='inner')
    merged['shortfall'] = merged['billed_qty'] - merged['delivered_qty']
    merged['leakage_usd'] = merged['shortfall'] * merged['unit_price']
    
    # Isolate active financial leak incidents
    active_leaks = merged[merged['shortfall'] > 0].copy()
    
    if not active_leaks.empty:
        total_recovered = active_leaks['leakage_usd'].sum()
        performance_fee_40 = total_recovered * 0.40
        
        # 1. GENERATE PRE-PAYMENT SUMMARY (Safely hidden layout to embed in payment email)
        summary_data = {
            "audited_records": len(merged),
            "leak_incidents": len(active_leaks),
            "capital_loss_uncovered": float(total_recovered),
            "performance_split_40": float(performance_fee_40)
        }
        
        # 2. GENERATE FULL PROTECTED EXPORT FILE (Stored safely until invoice clears)
        protected_report_name = f"{base_filename}_FULL_REPORT.csv"
        report_columns = ['invoice_id', 'product_id', 'billed_qty', 'delivered_qty', 'shortfall', 'unit_price', 'leakage_usd']
        active_leaks[report_columns].to_csv(protected_report_name, index=False)
        
        return {
            "status": "leak_detected",
            "summary": summary_data,
            "report_file": protected_report_name
        }
    else:
        return {"status": "reconciled", "message": "0% discrepancy verified across pipeline"}

if __name__ == "__main__":
    # Test execution matching dynamic generation criteria
    results = execute_autonomous_pipeline('invoices.csv', 'shipping.csv', client_name="Alpha Distribution")
    print(results)
