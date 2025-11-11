import os

from dotenv import load_dotenv

from py_subconverter import DlerAPIClient, SubscriptionConverter
from py_subconverter.sub_converter import download_config


def main():
    """Main function to demonstrate the Dler API Client with new converter."""
    load_dotenv()
    api_token = os.environ.get("DLER_API_TOKEN")
    email = os.environ.get("DLER_EMAIL")
    password = os.environ.get("DLER_PASSWORD")

    # --- Authentication ---
    if not api_token:
        if email and password:
            print("Token not found. Attempting to log in with email and password...")
            try:
                api_token = DlerAPIClient.login(email=email, password=password)
                print("Login successful! Token obtained.")
            except Exception as e:
                print(f"Login failed: {e}")
                return
        else:
            print("Error: API credentials not found.")
            print("Please set environment variables:")
            print("  - DLER_EMAIL and DLER_PASSWORD for login, OR")
            print("  - DLER_API_TOKEN for direct access.")
            return

    # --- Initialize Client and Make API Calls ---
    try:
        client = DlerAPIClient(token=api_token)
    except ValueError as e:
        print(f"Client initialization error: {e}")
        return

    print("\n--- 1. Fetching Account Information ---")
    try:
        account_info = client.get_account_info()
        print(f"Plan: {account_info.plan}")
        print(f"Traffic: {account_info.used} used / {account_info.traffic} total")
        print(f"Plan Expires: {account_info.plan_time}")
    except Exception as e:
        print(f"Error fetching account info: {e}")

    print("\n--- 2. Fetching Managed Clash Config ---")
    managed_config = None
    try:
        managed_config = client.get_managed_config()
        print(f"Config Name: {managed_config.name}")
        print(f"ss2022 URL: {managed_config.ss2022}")
    except Exception as e:
        print(f"Error fetching managed config: {e}")

    print("\n--- 3. Fetching Node List ---")
    try:
        node_list = client.get_nodes()
        print(f"Successfully fetched {len(node_list.data)} nodes.")
        if node_list.data:
            print(f"First node: {node_list.data[0].node_name}")
    except Exception as e:
        print(f"Error fetching nodes: {e}")

    # --- 4. Convert Subscription using NEW converter ---
    if managed_config:
        print("\n--- 4. Converting Subscription (New Method) ---")
        clash_url = managed_config.ss2022
        sub_url = clash_url.replace('clash', 'mu')

        try:
            # Old method - save to config_old.yaml
            print("Converting with OLD method...")
            rule_url = 'https://raw.githubusercontent.com/JuneLegency/MyRule/master/ShellClash_Full_Block.ini'
            download_config(sub_url, 'config_old.yaml', True, rule_url)
            print("✓ Old method: config_old.yaml")

            # New method - save to config_new.yaml (without custom rules)
            print("\nConverting with NEW method (using default rules)...")
            converter = SubscriptionConverter()
            converter.convert_from_url(
                subscription_url=sub_url,
                output_file='config_new.yaml',
                rule_url=rule_url
                # Note: Not using rule_url because local converter doesn't support INI format
            )
            print("✓ New method: config_new.yaml (with default rules)")

            print("\n✓ Both conversions completed!")
            print("✓ Compare: config_old.yaml vs config_new.yaml")
        except Exception as e:
            print(f"✗ Error converting subscription: {e}")
    else:
        print("\n--- 4. Skipping conversion (no managed config) ---")


if __name__ == "__main__":
    main()
