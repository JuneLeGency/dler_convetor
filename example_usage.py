#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example usage of the subscription converter
"""

from subscription_converter import SubscriptionConverter
from proxy_parser import parse_proxy_url, parse_subscription
from clash_generator import ClashGenerator


def example1_basic_conversion():
    """示例 1: 基本转换"""
    print("=" * 60)
    print("示例 1: 基本订阅转换")
    print("=" * 60)

    converter = SubscriptionConverter()

    # 模拟订阅内容（实际使用时替换为真实订阅 URL）
    subscription_content = """
ss://YWVzLTI1Ni1nY206cGFzc3dvcmQxMjNAc3MxLmV4YW1wbGUuY29tOjgzODg=#SS-Server-1
ss://YWVzLTI1Ni1nY206cGFzc3dvcmQxMjNAc3MyLmV4YW1wbGUuY29tOjgzODk=#SS-Server-2
trojan://password123@trojan.example.com:443?sni=trojan.example.com#Trojan-Server
"""

    # 解析并生成配置
    config = converter.convert_to_clash(subscription_content, output_file="example1_output.yaml")
    print(f"\n✓ 配置已生成: example1_output.yaml")


def example2_parse_individual_proxies():
    """示例 2: 解析单个代理"""
    print("\n" + "=" * 60)
    print("示例 2: 解析单个代理 URL")
    print("=" * 60)

    # Shadowsocks
    ss_url = "ss://aes-256-gcm:mypassword@example.com:8388#My-SS-Server"
    ss_proxy = parse_proxy_url(ss_url)
    if ss_proxy:
        print(f"\nShadowsocks:")
        print(f"  名称: {ss_proxy.name}")
        print(f"  服务器: {ss_proxy.server}:{ss_proxy.port}")
        print(f"  加密: {ss_proxy.cipher}")

    # Trojan
    trojan_url = "trojan://mypassword@trojan.example.com:443?sni=trojan.example.com#My-Trojan"
    trojan_proxy = parse_proxy_url(trojan_url)
    if trojan_proxy:
        print(f"\nTrojan:")
        print(f"  名称: {trojan_proxy.name}")
        print(f"  服务器: {trojan_proxy.server}:{trojan_proxy.port}")
        print(f"  SNI: {trojan_proxy.sni}")


def example3_custom_proxy_groups():
    """示例 3: 自定义代理组"""
    print("\n" + "=" * 60)
    print("示例 3: 使用自定义代理组")
    print("=" * 60)

    # 创建测试代理
    subscription = """
ss://aes-256-gcm:pass1@hk1.example.com:8388#🇭🇰 HK-1
ss://aes-256-gcm:pass2@hk2.example.com:8388#🇭🇰 HK-2
ss://aes-256-gcm:pass3@us1.example.com:8388#🇺🇸 US-1
ss://aes-256-gcm:pass4@jp1.example.com:8388#🇯🇵 JP-1
"""

    proxies = parse_subscription(subscription)
    proxy_names = [p.name for p in proxies]

    # 自定义代理组
    custom_groups = [
        {
            "name": "🚀 Proxy",
            "type": "select",
            "proxies": ["♻️ Auto", "🇭🇰 Hong Kong", "🇺🇸 US", "🇯🇵 Japan", "DIRECT"]
        },
        {
            "name": "♻️ Auto",
            "type": "url-test",
            "proxies": proxy_names,
            "url": "http://www.gstatic.com/generate_204",
            "interval": 300
        },
        {
            "name": "🇭🇰 Hong Kong",
            "type": "select",
            "proxies": [p for p in proxy_names if "HK" in p]
        },
        {
            "name": "🇺🇸 US",
            "type": "select",
            "proxies": [p for p in proxy_names if "US" in p]
        },
        {
            "name": "🇯🇵 Japan",
            "type": "select",
            "proxies": [p for p in proxy_names if "JP" in p]
        }
    ]

    # 生成配置
    generator = ClashGenerator()
    config = generator.generate_config(proxies, proxy_groups=custom_groups)

    with open("example3_output.yaml", "w") as f:
        f.write(config)

    print(f"✓ 生成带自定义代理组的配置: example3_output.yaml")
    print(f"  代理组: {len(custom_groups)}")


def example4_custom_rules():
    """示例 4: 自定义规则"""
    print("\n" + "=" * 60)
    print("示例 4: 使用自定义规则")
    print("=" * 60)

    subscription = """
ss://aes-256-gcm:pass@example.com:8388#Server-1
"""

    proxies = parse_subscription(subscription)

    # 自定义规则
    custom_rules = [
        # 广告拦截
        "DOMAIN-SUFFIX,doubleclick.net,REJECT",
        "DOMAIN-SUFFIX,googleadservices.com,REJECT",

        # 流媒体
        "DOMAIN-SUFFIX,netflix.com,🚀 Proxy",
        "DOMAIN-SUFFIX,youtube.com,🚀 Proxy",

        # 常用网站
        "DOMAIN-SUFFIX,google.com,🚀 Proxy",
        "DOMAIN-SUFFIX,github.com,🚀 Proxy",
        "DOMAIN-SUFFIX,stackoverflow.com,🚀 Proxy",

        # 国内网站直连
        "DOMAIN-SUFFIX,baidu.com,DIRECT",
        "DOMAIN-SUFFIX,qq.com,DIRECT",
        "DOMAIN-SUFFIX,taobao.com,DIRECT",

        # IP 规则
        "GEOIP,CN,DIRECT",
        "GEOIP,LAN,DIRECT",

        # 默认规则
        "MATCH,🚀 Proxy"
    ]

    # 相应的代理组
    proxy_names = [p.name for p in proxies]
    custom_groups = [
        {
            "name": "🚀 Proxy",
            "type": "select",
            "proxies": proxy_names + ["DIRECT"]
        }
    ]

    generator = ClashGenerator()
    config = generator.generate_config(
        proxies,
        rules=custom_rules,
        proxy_groups=custom_groups
    )

    with open("example4_output.yaml", "w") as f:
        f.write(config)

    print(f"✓ 生成带自定义规则的配置: example4_output.yaml")
    print(f"  规则数: {len(custom_rules)}")


def example5_merge_subscriptions():
    """示例 5: 合并多个订阅"""
    print("\n" + "=" * 60)
    print("示例 5: 合并多个订阅源")
    print("=" * 60)

    # 订阅源 1
    sub1 = """
ss://aes-256-gcm:pass1@provider1-hk.com:8388#Provider1-HK
ss://aes-256-gcm:pass1@provider1-us.com:8388#Provider1-US
"""

    # 订阅源 2
    sub2 = """
trojan://pass2@provider2-sg.com:443#Provider2-SG
trojan://pass2@provider2-jp.com:443#Provider2-JP
"""

    # 订阅源 3
    sub3 = """
ss://chacha20-ietf-poly1305:pass3@provider3-tw.com:8388#Provider3-TW
"""

    # 解析所有订阅
    proxies1 = parse_subscription(sub1)
    proxies2 = parse_subscription(sub2)
    proxies3 = parse_subscription(sub3)

    # 合并
    all_proxies = proxies1 + proxies2 + proxies3

    print(f"\n合并结果:")
    print(f"  订阅源 1: {len(proxies1)} 个节点")
    print(f"  订阅源 2: {len(proxies2)} 个节点")
    print(f"  订阅源 3: {len(proxies3)} 个节点")
    print(f"  总计: {len(all_proxies)} 个节点")

    # 生成配置
    generator = ClashGenerator()
    config = generator.generate_config(all_proxies)

    with open("example5_output.yaml", "w") as f:
        f.write(config)

    print(f"\n✓ 合并后的配置已保存: example5_output.yaml")


def example6_filter_proxies():
    """示例 6: 过滤节点"""
    print("\n" + "=" * 60)
    print("示例 6: 过滤特定节点")
    print("=" * 60)

    subscription = """
ss://aes-256-gcm:pass@hk1.example.com:8388#🇭🇰 HK-1
ss://aes-256-gcm:pass@hk2.example.com:8388#🇭🇰 HK-2
ss://aes-256-gcm:pass@us1.example.com:8388#🇺🇸 US-1
ss://aes-256-gcm:pass@jp1.example.com:8388#🇯🇵 JP-1
ss://aes-256-gcm:pass@jp2.example.com:8388#🇯🇵 JP-2
trojan://pass@sg1.example.com:443#🇸🇬 SG-1
"""

    all_proxies = parse_subscription(subscription)
    print(f"原始节点数: {len(all_proxies)}")

    # 过滤：只保留香港和日本节点
    filtered_proxies = [p for p in all_proxies if "HK" in p.name or "JP" in p.name]
    print(f"过滤后节点数: {len(filtered_proxies)}")

    # 过滤：只保留 Shadowsocks 节点
    from proxy_parser import ProxyType
    ss_only = [p for p in all_proxies if p.type == ProxyType.SHADOWSOCKS]
    print(f"仅 Shadowsocks: {len(ss_only)}")

    # 生成配置
    generator = ClashGenerator()
    config = generator.generate_config(filtered_proxies)

    with open("example6_output.yaml", "w") as f:
        f.write(config)

    print(f"\n✓ 过滤后的配置已保存: example6_output.yaml")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("订阅转换器使用示例")
    print("=" * 60)

    try:
        example1_basic_conversion()
        example2_parse_individual_proxies()
        example3_custom_proxy_groups()
        example4_custom_rules()
        example5_merge_subscriptions()
        example6_filter_proxies()

        print("\n" + "=" * 60)
        print("✓ 所有示例运行完成！")
        print("=" * 60)
        print("\n生成的文件:")
        print("  - example1_output.yaml  (基本转换)")
        print("  - example3_output.yaml  (自定义代理组)")
        print("  - example4_output.yaml  (自定义规则)")
        print("  - example5_output.yaml  (合并订阅)")
        print("  - example6_output.yaml  (过滤节点)")
        print()

    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
