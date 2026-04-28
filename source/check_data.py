import pandas as pd

df = pd.read_parquet('phase 2/data/cleaned_restaurants.parquet')

print("=== Dataset Overview ===")
print(f"Total restaurants: {len(df)}")
print(f"Unique locations: {df['Location'].nunique()}")

print("\n=== Top 30 Locations ===")
locations = df['Location'].value_counts().head(30)
for loc, count in locations.items():
    print(f"{loc}: {count} restaurants")

print("\n=== Rating Distribution ===")
print(f"Min rating: {df['Rating'].min()}")
print(f"Max rating: {df['Rating'].max()}")
print(f"Mean rating: {df['Rating'].mean():.2f}")

print("\n=== Budget Distribution ===")
print(f"Min cost: ₹{df['Cost'].min()}")
print(f"Max cost: ₹{df['Cost'].max()}")
print(f"Mean cost: ₹{df['Cost'].mean():.2f}")
