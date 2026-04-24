import pandas as pd

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------
    
    # 1. Deduplicate by 'id' - keep first
    df = df.drop_duplicates(subset=['id'], keep='first')
    
    processed_docs = []
    
    for _, row in df.iterrows():
        # 2. Basic validation: skip if stock_quantity is missing
        if pd.isna(row.get('stock_quantity')):
            continue
            
        # 3. Clean price column
        raw_price = str(row.get('price', ''))
        price_val = None
        
        # Handle cases like "$1200"
        clean_price_str = raw_price.replace('$', '').replace(',', '').strip()
        
        try:
            if clean_price_str.lower() == 'five dollars':
                price_val = 5.0
            elif clean_price_str.lower() in ('n/a', 'null', 'liên hệ'):
                continue
            else:
                price_val = float(clean_price_str)
        except ValueError:
            continue
            
        # Skip negative price
        if price_val < 0:
            continue

        # 4. Normalize date
        raw_date = str(row.get('date_of_sale', ''))
        try:
            # pandas to_datetime is quite flexible
            norm_date = pd.to_datetime(raw_date, dayfirst=False, errors='coerce')
            if pd.isna(norm_date):
                # Try dayfirst=True for 15/01/2026
                norm_date = pd.to_datetime(raw_date, dayfirst=True, errors='coerce')
            
            if not pd.isna(norm_date):
                date_str = norm_date.strftime('%Y-%m-%d')
            else:
                date_str = None
        except:
            date_str = None

        # 5. Create UnifiedDocument dict
        doc = {
            "document_id": f"csv-sale-{row['id']}",
            "content": f"Sale record: {row['product_name']}, price {price_val} {row.get('currency', 'USD')}",
            "source_type": "CSV",
            "author": str(row.get('sales_person_id', 'Unknown')),
            "timestamp": date_str,
            "source_metadata": {
                "sale_id": int(row['id']),
                "product_name": row['product_name'],
                "category": row.get('category'),
                "price": price_val,
                "currency": row.get('currency', 'USD'),
                "stock_quantity": int(row['stock_quantity'])
            }
        }
        processed_docs.append(doc)
    
    return processed_docs

