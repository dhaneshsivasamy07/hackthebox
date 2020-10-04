from ipaddress import ip_address, ip_network, summarize_address_range

def parse_targets(target):
    try:
        if '-' in target:
            start_ip, end_ip = target.split('-')
            try:
                end_ip = ip_address(end_ip)
            except ValueError:
                first_three_octets = start_ip.split(".")[:-1]
                first_three_octets.append(end_ip)
                end_ip = ip_address(
                            ".".join(first_three_octets)
                        )

            for ip_range in summarize_address_range(ip_address(start_ip), end_ip):
                for ip in ip_range:
                    yield str(ip)
        else:
            for ip in ip_network(target, strict=False):
                yield str(ip)
    except ValueError:
        yield str(target)
