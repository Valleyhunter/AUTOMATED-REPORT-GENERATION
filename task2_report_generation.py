import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Load CSV file (your crypto data)
df = pd.read_csv("crypto_data.csv")

# Normalize column names (just in case)
df.columns = df.columns.str.strip().str.lower()

# Summaries
summary = {
    "Top Coin by Market Cap": df.loc[df["market_cap"].idxmax(), "id"],
    "Top Coin by Price": df.loc[df["current_price"].idxmax(), "id"],
    "Top Coin by Volume": df.loc[df["total_volume"].idxmax(), "id"],
    "Average Price": round(df["current_price"].mean(), 2),
    "Average Market Cap": round(df["market_cap"].mean(), 2),
}

# Create PDF Report
pdf_file = "crypto_report.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)
c.setFont("Helvetica-Bold", 16)
c.drawString(200, 750, "Cryptocurrency Report")

c.setFont("Helvetica", 12)
c.drawString(50, 710, "Summary:")

y = 690
for key, value in summary.items():
    c.drawString(70, y, f"{key}: {value}")
    y -= 20

c.drawString(50, y-10, "Detailed Data:")

# Table-like details
y -= 30
for i, row in df.iterrows():
    text = f"{row['id']} ({row['symbol']}) - Price: {row['current_price']}, Market Cap: {row['market_cap']}, Volume: {row['total_volume']}"
    c.drawString(70, y, text[:90])  # keep within page width
    y -= 20
    if y < 50:  # new page if space runs out
        c.showPage()
        y = 750

c.save()

print(f"Report generated: {pdf_file}")
