import csv

from models.hotel import *


# def save_venues_to_csv(venues: list, filename: str):
#     if not venues:
#         print("No venues to save.")
#         return

#     # Use field names from the Venue model
#     fieldnames = Venue.model_fields.keys()

#     with open(filename, mode="w", newline="", encoding="utf-8") as file:
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(venues)
#     print(f"Saved {len(venues)} venues to '{filename}'.")
