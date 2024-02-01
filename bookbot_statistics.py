import pandas as pd
import os

# Get the directory of the current script file
csv_file_path = os.path.join(os.getcwd(), "1000_ISBNs_all.csv")


def count_bookbot_only_providers(data=None):
    """
    Count occurrences where "Bookbot" is the only provider for each ISBN13.

    Parameters:
        - csv_file: str or None
                    Path to the CSV file containing columns 'ISBN13' and 'Provider'.

    Returns:
    - total_bookbot_only: int
                          Total occurrences where "Bookbot" is the only provider.
    """

    try:
        # df = pd.read_csv(data)
        df = data
    except Exception as e:
        return f"Error loading data: {e}"

    # Group by ISBN13 and check if Bookbot is the only provider
    bookbot_only = df.groupby('ISBN13')['Provider'].apply(lambda x: (x == "Bookbot").all())
    
    # Count how many times "Bookbot" is the only Provider
    total_bookbot_only = bookbot_only.sum()

    return total_bookbot_only


def count_outliers_bookbot_prices(data=None):
    """
    Count outliers in Bookbot prices based on percentiles (0,25 and 0,75).

    Parameters:
    - csv_file: str or None
                Path to the CSV file containing columns 'ISBN13', 'Provider', and 'Prices'.

    Returns:
    - num_outliers: int
                    Number of outliers found.
    """

    try:
        # df = pd.read_csv(data)
        df = data
    except Exception as e:
        return f"Error loading data: {e}"

    # Filter the DataFrame to include only rows where Bookbot is mentioned at least once
    bookbot_isbns = df[df['Provider'] == "Bookbot"]['ISBN13'].unique()
    bookbot_df = df[df['ISBN13'].isin(bookbot_isbns)]

    # Group by ISBN and calculate the 25th and 75th percentile for each ISBN
    percentiles = bookbot_df.groupby('ISBN13')['Price'].quantile([0.25, 0.75]).unstack()

    # Only include rows (prices) where the Provider is 'Bookbot'
    bookbot_prices = df[df['Provider'] == "Bookbot"][['ISBN13', 'Price']]

    # Merge dataframes on ISBN13
    merged_df = pd.merge(bookbot_prices, percentiles, on='ISBN13', suffixes=('_price', '_percentile'))

    # Compare prices with percentiles and check if price is smaller than 25th percentile or bigger than 75th percentile
    merged_df['is_outlier'] = (merged_df['Price'] < merged_df[0.25]) | (merged_df['Price'] > merged_df[0.75])

    # Count number of outliers
    num_outliers = merged_df['is_outlier'].sum()

    return num_outliers


def lower_priced_providers_than_bookbot(data=None):
    """
    Identify providers more likely to have a lower price than BookBot.

    Parameters:
    - csv_file: str or None
                Path to the CSV file containing columns 'ISBN13', 'Provider', and 'Prices'.

    Returns:
    - lower_priced_provider_names_str: str
                                       Comma-separated string of provider names
                                       more likely to have a lower price than BookBot.
    """

    try:
        # df = pd.read_csv(data)
        df = data
    except Exception as e:
        return f"Error loading data: {e}"

    # Filter rows where Bookbot is mentioned at least once
    bookbot_isbns = df[df['Provider'] == 'Bookbot']['ISBN13'].unique()
    bookbot_df = df[df['ISBN13'].isin(bookbot_isbns)]

    # Calculate average price for each provider
    average_prices = bookbot_df.groupby('Provider')['Price'].mean()

    # Identify providers with average price lower than BookBot
    lower_priced_providers = average_prices[average_prices < df[df['Provider'] == 'Bookbot']['Price'].mean()]

    # Extracting just the names from lower_priced_providers index and ordering alphabetically
    lower_priced_provider_names = lower_priced_providers.index.sort_values().values

    # Convert the array to a comma-separated string
    lower_priced_provider_names_str = ', '.join(lower_priced_provider_names)

    return lower_priced_provider_names_str


def average_deviation_from_lowest_price(data=None):
    """
    Calculate the average deviation of Bookbot's offers from the lowest price for each ISBN.

    Parameters:
    - csv_file: str or None
                Path to the CSV file containing columns 'ISBN13', 'Provider', and 'Prices'.

    Returns:
    - average_deviation: float
                         Average deviation of Bookbot's offers from the lowest price.
    """

    try:
        # df = pd.read_csv(data)
        df = data
    except Exception as e:
        return f"Error loading data: {e}"

    # Get ISBNs where Bookbot Provider is present
    bookbot_isbns = df[df['Provider'] == "Bookbot"]['ISBN13'].unique()

    # Get Bookbot prices
    bookbot_prices = df[df['Provider'] == "Bookbot"]['Price'].tolist()

    # Lowest price for each ISBN where Bookbot is present
    lowest_prices = []
    for isbn in bookbot_isbns:
        lowest_prices.append(df[df['ISBN13'] == isbn]['Price'].min())

    # Deviation of each Bookbot's offer from the lowest price
    deviations = [price - lowest_price for price, lowest_price in zip(bookbot_prices, lowest_prices)]

    # Average deviation of Bookbot's offers from the lowest price
    average_deviation = sum(deviations) / len(deviations)

    return average_deviation


def calculate_foreign_offers_representation(country, data=None):
    """
    Calculate the relative representation of foreign offers (home country is the Czech Republic).

    Parameters:
    - csv_file: str or None
                Path to the CSV file containing column 'Country'.
    - country: str
                The country to be excluded from the calculation.

    Returns:
    - relative_representation: float
                               Relative representation of foreign offers as a percentage.
    """

    try:
        # df = pd.read_csv(data)
        df = data
    except Exception as e:
        return f"Error loading data: {e}"

    # Extracting foreign offers (excluding Czech Republic)
    foreign_offers = df[df['Country'] != country]

    # Counting the number of foreign offers
    foreign_offers_count = len(foreign_offers)

    # Total number of offers
    total_offers = len(df)

    # Calculating the relative representation of foreign offers
    relative_representation = foreign_offers_count / total_offers * 100

    return relative_representation
