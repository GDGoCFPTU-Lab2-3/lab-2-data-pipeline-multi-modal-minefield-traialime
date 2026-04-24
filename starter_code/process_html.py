from bs4 import BeautifulSoup

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # ------------------------------------------
    
    table = soup.find('table', id='main-catalog')
    if not table:
        return []
    
    processed_docs = []
    rows = table.find_all('tr')[1:] # Skip header
    
    for i, row in enumerate(rows):
        cols = row.find_all('td')
        if len(cols) < 6:
            continue
            
        p_id = cols[0].text.strip()
        p_name = cols[1].text.strip()
        category = cols[2].text.strip()
        raw_price = cols[3].text.strip()
        raw_stock = cols[4].text.strip()
        rating = cols[5].text.strip()
        
        # Handle price
        if raw_price.lower() in ('n/a', 'liên hệ'):
            continue
            
        try:
            # "28,500,000 VND" -> 28500000
            price_val = int(raw_price.replace('VND', '').replace(',', '').strip())
        except ValueError:
            continue
            
        # Handle stock
        try:
            stock_val = int(raw_stock)
            if stock_val < 0:
                continue
        except ValueError:
            continue
            
        doc = {
            "document_id": f"html-product-{i+1:03d}",
            "content": f"{p_name} - {category} - Price: {price_val} VND - Stock: {stock_val}",
            "source_type": "HTML",
            "author": "VinShop",
            "timestamp": None,
            "source_metadata": {
                "product_id": p_id,
                "product_name": p_name,
                "category": category,
                "price_vnd": price_val,
                "stock": stock_val,
                "rating": rating
            }
        }
        processed_docs.append(doc)
    
    return processed_docs

