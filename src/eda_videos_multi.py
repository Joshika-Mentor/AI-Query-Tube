print("SCRIPT STARTED (MULTI-CHANNEL EDA - CLEAN VERSION)")

import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "videos_multi_raw.csv")

df = pd.read_csv(DATA_PATH)
print("Rows loaded:", len(df))
print("\n📌 Dataset Loaded Successfully")
print(df.head())
print("\nDataset Shape (Before Cleaning):", df.shape)

# -------- Basic Cleaning --------
# Remove rows with missing critical values
df.dropna(subset=["video_id", "title", "channel_name"], inplace=True)

# Remove duplicate videos (important!)
df.drop_duplicates(subset=["video_id"], inplace=True)

# -------- Date conversion --------
df["publishedAt"] = pd.to_datetime(df["publishedAt"], errors="coerce")

# Remove rows with invalid dates
df.dropna(subset=["publishedAt"], inplace=True)

# -------- Text Normalization (VERY IMPORTANT for Milestone 3) --------
df["title"] = df["title"].astype(str).str.strip()
df["channel_name"] = df["channel_name"].astype(str).str.strip()
df["video_id"] = df["video_id"].astype(str).str.strip()

# -------- Feature Engineering --------
df["title_length"] = df["title"].apply(len)

print("\nDataset Shape (After Cleaning):", df.shape)

# -------- Missing values --------
print("\n🔍 Missing Values After Cleaning:")
print(df.isnull().sum())

# -------- Basic statistics --------
print("\n📊 Basic Statistics:")
print(df.describe(include="all"))

# -------- Create output folder --------
os.makedirs("data", exist_ok=True)

# -------- Plot 1: Upload frequency over time --------
plt.figure()
df.set_index("publishedAt").resample("ME").size().plot()
plt.title("Video Upload Frequency Over Time (Multi-Channel)")
plt.xlabel("Date")
plt.ylabel("Number of Videos")
plt.tight_layout()
plt.savefig("data/plot_multi_upload_frequency.png")
plt.close()

# -------- Plot 2: Title length distribution --------
plt.figure()
df["title_length"].hist(bins=30)
plt.title("Title Length Distribution (Multi-Channel)")
plt.xlabel("Title Length")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("data/plot_multi_title_length.png")
plt.close()

# -------- Plot 3: Videos per channel --------
plt.figure()
df["channel_name"].value_counts().plot(kind="bar")
plt.title("Videos per Channel")
plt.xlabel("Channel Name")
plt.ylabel("Number of Videos")
plt.tight_layout()
plt.savefig("data/plot_videos_per_channel.png")
plt.close()

# -------- Save cleaned dataset for next milestone --------
CLEAN_PATH = "data/videos_multi_clean.csv"
df.to_csv(CLEAN_PATH, index=False)

print("\n💾 Clean dataset saved → data/videos_multi_clean.csv")
print("📁 EDA Plots Saved:")
print(" - plot_multi_upload_frequency.png")
print(" - plot_multi_title_length.png")
print(" - plot_videos_per_channel.png")

print("\n✅ Milestone 2 (Multi-Channel EDA) Completed Successfully!")
