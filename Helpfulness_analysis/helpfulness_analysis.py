import pandas as pd
import numpy as np
import json
import gc


# ─── Configuration ──────────────────────────────────────────────────────────────

CATEGORIES = [
    "Appliances",
    "All_Beauty",
    "Handmade_Products",
    "Software",
    "Magazine_Subscriptions",
]

REVIEW_DIR = "review_categories"
META_DIR = "meta_categories"
OUTPUT_CSV = "helpfulness_summary.csv"

LENGTH_BINS = [0, 3, 20, 50, 100, 200, 400, 10000]
LENGTH_LABELS = ["0-2", "3-19", "20-49", "50-99", "100-199", "200-399", "400+"]


# ─── Data Loading ───────────────────────────────────────────────────────────────

def load_metadata(meta_path):
    '''Load metadata JSONL with robust handling for malformed lines

    Inputs:
    meta_path: Path to the metadata JSONL file

    Outputs:
    DataFrame with metadata fields
    '''
    try:
        return pd.read_json(meta_path, lines=True)
    except (ValueError, json.JSONDecodeError):
        print(f"  Standard parser failed for {meta_path}, using line-by-line fallback")
        records = []
        with open(meta_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    try:
                        records.append(json.loads('{' + line))
                    except json.JSONDecodeError:
                        continue
        return pd.DataFrame(records)


def load_and_merge(category):
    '''Load review and metadata JSONL files and merge on parent_asin

    Inputs:
    category: Name of the Amazon product category (e.g. "All_Beauty")

    Outputs:
    Merged pandas DataFrame with review + metadata fields needed for analysis
    '''
    review_path = f"{REVIEW_DIR}/{category}.jsonl".replace('\\', '/')
    meta_path = f"{META_DIR}/meta_{category}.jsonl".replace('\\', '/')

    print(f"Loading reviews: {review_path}")
    df_reviews = pd.read_json(review_path, lines=True)
    df_reviews = df_reviews[["parent_asin", "rating", "text", "helpful_vote", "verified_purchase"]]

    print(f"Loading metadata: {meta_path}")
    df_meta = load_metadata(meta_path)
    df_meta = df_meta[["parent_asin", "price"]]

    # Drop duplicate metadata rows per parent_asin
    df_meta = df_meta.drop_duplicates(subset="parent_asin")

    print(f"Merging on parent_asin...")
    df = df_reviews.merge(df_meta, on="parent_asin", how="left")

    del df_reviews, df_meta
    gc.collect()

    return df


# ─── Feature Engineering ────────────────────────────────────────────────────────

def create_features(df):
    '''Create derived columns needed for helpfulness analysis

    Inputs:
    df: Merged review DataFrame with rating, text, helpful_vote, verified_purchase, price

    Outputs:
    DataFrame with added columns: helpful_any, word_count, super_short, length_bin
    '''
    df["helpful_any"] = (df["helpful_vote"] > 0).astype(int)
    df["word_count"] = df["text"].fillna("").str.split().str.len()
    df["super_short"] = (df["word_count"] < 3).astype(int)
    df["length_bin"] = pd.cut(df["word_count"], bins=LENGTH_BINS, labels=LENGTH_LABELS, right=False)

    return df


# ─── Metric Computations ───────────────────────────────────────────────────────

def compute_extremity_bias(df):
    '''Compute helpful rate by rating, extract 1-star and 5-star rates

    Inputs:
    df: DataFrame with rating and helpful_any columns

    Outputs:
    one_star,two_star,three_star,four_star, five_star
    '''
    by_rating = df.groupby("rating")["helpful_any"].mean()

    one_star = by_rating.get(1.0, np.nan)
    two_star = by_rating.get(2.0, np.nan)
    three_star = by_rating.get(3.0, np.nan)
    four_star = by_rating.get(4.0, np.nan)
    five_star = by_rating.get(5.0, np.nan)

    return one_star,two_star,three_star,four_star, five_star


def compute_length_effect(df):
    '''Compute helpful rate by length bin, extract 400+ and 50-99 rates

    Inputs:
    df: DataFrame with length_bin and helpful_any columns

    Outputs:
    Tuple of (long_400plus_rate, reference_50_100_rate)
    '''
    by_length = df.groupby("length_bin", observed=False)["helpful_any"].mean()

    
    ref_0_2 = by_length.get("0-2", np.nan)
    ref_3_20 = by_length.get("3-19", np.nan)
    ref_20_50 = by_length.get("20-49", np.nan)
    ref_50_100 = by_length.get("50-99", np.nan)
    ref_100_200 = by_length.get("100-199", np.nan)
    ref_200_400 = by_length.get("200-399", np.nan)
    long_400plus = by_length.get("400+", np.nan)
    return ref_0_2,ref_3_20,ref_20_50,ref_50_100,ref_100_200,ref_200_400,long_400plus

#LENGTH_LABELS = ["0-2", "3-19", "20-49", "50-99", "100-199", "200-399", "400+"]
def compute_super_short_effect(df):
    '''Compute helpful rate for super short reviews (word_count < 3)

    Inputs:
    df: DataFrame with super_short and helpful_any columns

    Outputs:
    Helpful rate for super short reviews
    '''
    by_short = df.groupby("super_short")["helpful_any"].mean()

    return by_short.get(1, np.nan)


def compute_verified_effect(df):
    '''Compute helpful rate by verified purchase status

    Inputs:
    df: DataFrame with verified_purchase and helpful_any columns

    Outputs:
    Tuple of (verified_rate, unverified_rate, delta)
    '''
    by_verified = df.groupby("verified_purchase")["helpful_any"].mean()

    verified = by_verified.get(True, np.nan)
    unverified = by_verified.get(False, np.nan)

    if pd.notna(verified) and pd.notna(unverified):
        delta = verified - unverified
    else:
        delta = np.nan

    return verified, unverified, delta


def compute_price_effect(df):
    '''Compute helpful rate by price bucket (Low/Mid/High terciles)

    Inputs:
    df: DataFrame with price and helpful_any columns

    Outputs:
    Helpful rate for the High price bucket
    '''
    df_price = df.dropna(subset=["price"]).copy()
    df_price["price"] = pd.to_numeric(df_price["price"].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False), errors='coerce')
    df_price = df_price.dropna(subset=["price"])
    df_price = df_price[df_price["price"] > 0]

    if len(df_price) < 10:
        print("  WARNING: Too few rows with valid price data")
        return np.nan,np.nan,np.nan

    df_price = df_price.copy()
    df_price["price_bucket"] = pd.qcut(df_price["price"], q=3, labels=["Low", "Mid", "High"])

    by_price = df_price.groupby("price_bucket", observed=False)["helpful_any"].mean()

    return by_price.get("Low", np.nan), by_price.get("Mid", np.nan), by_price.get("High", np.nan)


# ─── Per-Category Pipeline ──────────────────────────────────────────────────────

def analyze_category(category):
    '''Run full helpfulness analysis for a single category

    Inputs:
    category: Name of the Amazon product category

    Outputs:
    Dictionary with all extracted metrics for this category
    '''
    print(f"\n{'='*60}")
    print(f"Processing: {category}")
    print(f"{'='*60}")

    #Load and merge
    df = load_and_merge(category)
    print(f"  Rows loaded: {len(df)}")

    df = create_features(df)

    #Compute metrics
    one_star,two_star,three_star,four_star, five_star = compute_extremity_bias(df)
    print(f"  Extremity bias — 1-star: {one_star:.3f},2-star: {two_star:.3f},3-star: {three_star:.3f},4-star: {four_star:.3f} 5-star: {five_star:.3f}")

    ref_0_2,ref_3_20,ref_20_50,ref_50_100,ref_100_200,ref_200_400,long_400plus = compute_length_effect(df)
    print(f"  Length effect — 400+: {long_400plus:.3f}, 50-99 ref: {ref_50_100:.3f}")

    verified, unverified, verified_delta = compute_verified_effect(df)
    print(f"  Verified effect — True: {verified:.3f}, False: {unverified:.3f}, Delta: {verified_delta:.3f}")
    
    low_price,mid_price,high_price = compute_price_effect(df)
    print(f"  Price effect — High bucket: {high_price}")

    # Free memory
    del df
    gc.collect()

    return {
        "Category": category,
        "One_Star": round(one_star, 3) if pd.notna(one_star) else np.nan,
        "Two_Star": round(two_star, 3) if pd.notna(two_star) else np.nan,
        "Three_Star": round(three_star, 3) if pd.notna(three_star) else np.nan,
        "Four_Star": round(four_star, 3) if pd.notna(four_star) else np.nan,
        "Five_Star": round(five_star, 3) if pd.notna(five_star) else np.nan,
        "0to2": round(ref_0_2, 3) if pd.notna(ref_0_2) else np.nan,
        "3to19": round(ref_3_20, 3) if pd.notna(ref_3_20) else np.nan,
        "20to49": round(ref_20_50, 3) if pd.notna(ref_20_50) else np.nan,
        "50to99": round(ref_50_100, 3) if pd.notna(ref_50_100) else np.nan,
        "100to199": round(ref_100_200, 3) if pd.notna(ref_100_200) else np.nan,
        "200to399": round(ref_200_400, 3) if pd.notna(ref_200_400) else np.nan,
        "400plus": round(long_400plus, 3) if pd.notna(long_400plus) else np.nan,
        "Verified": round(verified, 3) if pd.notna(verified) else np.nan,
        "Unverified":round(unverified, 3) if pd.notna(unverified) else np.nan,
        "Low_Price": round(low_price, 3) if pd.notna(low_price) else np.nan,
        "Mid_Price": round(mid_price, 3) if pd.notna(mid_price) else np.nan,
        "High_Price": round(high_price, 3) if pd.notna(high_price) else np.nan,
    }

# ─── Main ───────────────────────────────────────────────────────────────────────

def main():
    '''Process all categories and produce summary CSV'''
    results = []

    for category in CATEGORIES:
        row = analyze_category(category)
        results.append(row)

    # Build summary table
    summary = pd.DataFrame(results)
    summary.to_csv(OUTPUT_CSV, index=False)

    print(f"\n{'='*60}")
    print(f"Summary saved to: {OUTPUT_CSV}")
    print(f"{'='*60}")
    print(summary.to_string(index=False))

    return summary


if __name__ == "__main__":
    main()
