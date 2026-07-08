import pandas as pd
import os

def run_supply_chain_audit(invoice_file, shipping_file, output_report_name="final_audit_report.csv"):
    print("====================================================")
    print("🚀 OPTIMA WORKFLOWS // INITIATING AUTONOMOUS AUDIT ENGINE")
    print("====================================================\n")
    
    # Check if files exist before processing
    if not os.path.exists(invoice_file) or not os.path.exists(shipping_file):
        print("❌ ERROR: Source datasets missing. Ensure data streams are active.")
        return False

    print("📊 Loading transaction streams...")
    # Load client data streams (Supports both CSV and Excel formats)
    try:
        invoices = pd.read_csv(invoice_file) if invoice_file.endswith('.csv') else pd.read_excel(invoice_file)
        shipping = pd.read_csv(shipping_file) if shipping_file.endswith('.csv') else pd.read_excel(shipping_file)
    except Exception as e:
        print(f"❌ ERROR: Failed to read data matrices. Details: {e}")
        return False

    print("🧠 Standardizing incoming database structures...")
    # Force column names to lowercase to neutralize varied ERP structural exports
    invoices.columns = invoices.columns.str.strip().str.lower()
    shipping.columns = shipping.columns.str.strip().str.lower()

    # Define strict schema key targets
    required_invoice_keys = ['invoice_id', 'product_id', 'billed_qty', 'unit_price']
    required_shipping_keys = ['product_id', 'delivered_qty']

    # Validate that the uploaded documents contain the required transactional columns
    if not all(k in invoices.columns for k in required_invoice_keys) or not all(k in shipping.columns for k in required_shipping_keys):
        print("❌ ERROR: Data structure mismatch. Source file column headers do not match target matrix schema.")
        print(f"Required Invoice Columns: {required_invoice_keys}")
        print(f"Required Shipping Columns: {required_shipping_keys}")
        return False

    print("🔀 Executing multi-point relational data join...")
    # Merge datasets matching exactly on unique Product SKU Identifiers
    merged = pd.merge(invoices, shipping, on='product_id', how='inner')

    print("🔢 Computing line-item validation math...")
    # Isolate discrepancies where items billed exceed items physically delivered
    merged['quantity_shortfall'] = merged['billed_qty'] - merged['delivered_qty']
    
    # Calculate the exact financial capital loss leak
    merged['capital_leakage_usd'] = merged['quantity_shortfall'] * merged['unit_price']

    # Isolate only rows representing active financial leaks
    leakage_records = merged[merged['quantity_shortfall'] > 0].copy()

    if not leakage_records.empty:
        total_leak = leakage_records['capital_leakage_usd'].sum()
        total_incidents = len(leakage_records)
        
        print("\n⚠️ ==================== AUDIT ALERT ====================")
        print(f"🚨 CRITICAL LEAKAGE DETECTED ACROSS {total_incidents} LINE-ITEMS.")
        print(f"💰 TOTAL UNCOVERED CAPITAL LOSS: ${total_leak:,.2f} USD")
        print("========================================================\n")
        
        # Organize and format the final management report
        report_columns = [
            'invoice_id', 'product_id', 'billed_qty', 
            'delivered_qty', 'quantity_shortfall', 'unit_price', 'capital_leakage_usd'
        ]
        final_report = leakage_records[report_columns].sort_values(by='capital_leakage_usd', ascending=False)
        
        # Export the document for presentation to client executives
        final_report.to_csv(output_report_name, index=False)
        print(f"💾 Discrepancy file safely generated: '{output_report_name}'")
        return True
    else:
        print("\n✅ ==================== RECONCILIATION SUCCESS ====================")
        print("🎉 Audit complete. 100% data match verified. No financial leakage identified.")
        print("====================================================================\n")
        return True

if __name__ == "__main__":
    # Test execution parameters targeting local simulation datasets
    run_supply_chain_audit('invoices.csv', 'shipping.csv')
