#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Subscription Converter - Standalone proxy subscription converter
No server dependency, pure Python implementation
"""

import argparse
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, List

from proxy_parser import parse_subscription, Proxy
from clash_generator import ClashGenerator


class SubscriptionConverter:
    """Standalone subscription converter"""

    def __init__(self):
        self.clash_gen = ClashGenerator()

    def fetch_subscription(self, url: str) -> str:
        """Fetch subscription content from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read().decode('utf-8')
                return content
        except urllib.error.URLError as e:
            raise Exception(f"Failed to fetch subscription: {e}")
        except Exception as e:
            raise Exception(f"Error fetching subscription: {e}")

    def load_local_file(self, filepath: str) -> str:
        """Load subscription from local file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Failed to read file: {e}")

    def convert_to_clash(
        self,
        subscription_content: str,
        output_file: Optional[str] = None,
        rule_url: Optional[str] = None
    ) -> str:
        """Convert subscription to Clash format"""

        # Parse subscription
        print("Parsing subscription...")
        proxies = parse_subscription(subscription_content)

        if not proxies:
            raise ValueError("No valid proxies found in subscription")

        print(f"Found {len(proxies)} proxies")

        # Display proxy types
        type_count = {}
        for proxy in proxies:
            type_name = proxy.type.value
            type_count[type_name] = type_count.get(type_name, 0) + 1

        print("Proxy types:")
        for ptype, count in type_count.items():
            print(f"  - {ptype}: {count}")

        # Load custom rules if provided
        rules = None
        if rule_url:
            print(f"Loading rules from: {rule_url}")
            try:
                rules_content = self.fetch_subscription(rule_url)
                # Parse rules (simple line-by-line for now)
                rules = [line.strip() for line in rules_content.split('\n') if line.strip()]
            except Exception as e:
                print(f"Warning: Failed to load custom rules: {e}")
                print("Using default rules instead")

        # Generate Clash config
        print("Generating Clash configuration...")
        config = self.clash_gen.generate_config(proxies, rules=rules)

        # Save to file if specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(config)
            print(f"✓ Configuration saved to: {output_file}")

        return config

    def convert_from_url(
        self,
        subscription_url: str,
        output_file: str = "clash_config.yaml",
        rule_url: Optional[str] = None
    ):
        """Convert subscription from URL"""
        print(f"Fetching subscription from: {subscription_url}")
        content = self.fetch_subscription(subscription_url)
        return self.convert_to_clash(content, output_file, rule_url)

    def convert_from_file(
        self,
        input_file: str,
        output_file: str = "clash_config.yaml",
        rule_url: Optional[str] = None
    ):
        """Convert subscription from local file"""
        print(f"Loading subscription from: {input_file}")
        content = self.load_local_file(input_file)
        return self.convert_to_clash(content, output_file, rule_url)


def main():
    parser = argparse.ArgumentParser(
        description='Standalone Proxy Subscription Converter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert from URL
  %(prog)s --url https://example.com/subscription -o clash.yaml

  # Convert from local file
  %(prog)s --file subscription.txt -o clash.yaml

  # Use custom rules
  %(prog)s --url https://example.com/sub -o clash.yaml --rules https://example.com/rules.txt

  # Convert and display to stdout
  %(prog)s --url https://example.com/subscription

Supported proxy formats:
  - Shadowsocks (ss://)
  - ShadowsocksR (ssr://)
  - VMess (vmess://)
  - Trojan (trojan://)
  - Hysteria2 (hysteria2://, hy2://)
        """
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--url',
        help='Subscription URL'
    )
    input_group.add_argument(
        '--file',
        help='Local subscription file'
    )

    parser.add_argument(
        '-o', '--output',
        default='clash_config.yaml',
        help='Output file path (default: clash_config.yaml)'
    )

    parser.add_argument(
        '--rules',
        help='Custom rules URL or file'
    )

    parser.add_argument(
        '--stdout',
        action='store_true',
        help='Print to stdout instead of file'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    try:
        converter = SubscriptionConverter()

        # Determine output file
        output_file = None if args.stdout else args.output

        # Convert based on input type
        if args.url:
            config = converter.convert_from_url(
                args.url,
                output_file=output_file,
                rule_url=args.rules
            )
        else:  # args.file
            config = converter.convert_from_file(
                args.file,
                output_file=output_file,
                rule_url=args.rules
            )

        # Print to stdout if requested
        if args.stdout:
            print("\n" + "="*60)
            print("Generated Clash Configuration:")
            print("="*60)
            print(config)

        print("\n✓ Conversion completed successfully!")

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
