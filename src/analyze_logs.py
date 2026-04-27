import json
import os

import pandas as pd
import matplotlib.pyplot as plt


DATA_FILE = "data/brute_force_data.json"
VISUALS_DIR = "visuals"


def load_data():
    with open(DATA_FILE, encoding="utf-8-sig") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # Each row contains a list of attempted passwords.
    # Explode turns each password attempt into its own row.
    df_expanded = df.explode("passwords")
    df_expanded["timestamp"] = pd.to_datetime(
                df_expanded["timestamp"],
                format="%a %b %d %H:%M:%S %Y"
                )
    df_expanded = df_expanded.rename(columns={"passwords": "password"})

    return df_expanded

def analyze_time_patterns(df):
    # Attacks over time (by hour)
    df["hour"] = df["timestamp"].dt.hour

    attacks_by_hour = df["hour"].value_counts().sort_index()

    print("\nAttacks by hour:")
    print(attacks_by_hour)

    return attacks_by_hour

def print_summary(df):
    print("\nTotal password attempts:")
    print(len(df))

    print("\nTop attacking IPs:")
    print(df["foreign_ip"].value_counts().head(10))

    print("\nMost targeted usernames:")
    print(df["username"].value_counts().head(10))

    print("\nMost common passwords attempted:")
    print(df["password"].value_counts().head(10))



def create_visuals(df):
    os.makedirs(VISUALS_DIR, exist_ok=True)

    # Top attacking IPs
    top_ips = df["foreign_ip"].value_counts().head(10)

    top_ips.plot(kind="bar")
    plt.title("Top Attacking IPs")
    plt.xlabel("IP Address")
    plt.ylabel("Number of Attempts")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{VISUALS_DIR}/top_ips.png")
    plt.clf()

    # Most targeted usernames
    top_users = df["username"].value_counts().head(10)

    top_users.plot(kind="bar")
    plt.title("Most Targeted Usernames")
    plt.xlabel("Username")
    plt.ylabel("Attempts")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{VISUALS_DIR}/top_usernames.png")
    plt.clf()

    # Most common passwords attempted
    top_passwords = df["password"].value_counts().head(10)

    top_passwords.plot(kind="bar")
    plt.title("Most Common Passwords Attempted")
    plt.xlabel("Password")
    plt.ylabel("Attempts")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{VISUALS_DIR}/common_passwords.png")
    plt.clf()

    # Attacks by hour
    df["hour"] = df["timestamp"].dt.hour
    attacks_by_hour = df["hour"].value_counts().sort_index()

    attacks_by_hour.plot(kind="bar")
    plt.title("Attack Attempts by Hour")
    plt.xlabel("Hour of Day (0-23)")
    plt.ylabel("Number of Attempts")
    plt.tight_layout()
    plt.savefig(f"{VISUALS_DIR}/attacks_by_hour.png")
    plt.clf()

def main():
    df = load_data()
    print_summary(df)

    analyze_time_patterns(df)  # <-- add this

    create_visuals(df)

    print("\nVisuals created successfully in the visuals/ folder.")


if __name__ == "__main__":
    main()