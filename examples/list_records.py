"""Simple script that lists the DNS records for the first domain on the account."""

from domeneshop import Client


if __name__ == "__main__":
    client = Client("<token>", "<secret>")

    domains = client.get_domains()
    if not domains:
        exit("No domains found!")

    domain = domains[0]
    print("DNS records for {0}:".format(domain["domain"]))

    for record in client.get_records(domain["id"]):
        print(record["id"], record["host"], record["type"], record["data"])