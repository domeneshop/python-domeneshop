"""Simple script that lists the WWW forwardings for all domains on the account."""

from domeneshop import Client

if __name__ == "__main__":
    client = Client("<token>", "<secret>")

    domains = client.get_domains()
    if not domains:
        exit("No domains found!")

    for domain in domains:
        print("Forwardings for {0}:".format(domain["domain"]))

        for forward in client.get_forwards(domain["id"]):
            if forward["host"] == "@":
                print("https://{0} -> {1}".format(domain["domain"], forward["url"]))
            else:
                print(
                    "https://{0}.{1} -> {2}".format(
                        forward["host"], domain["domain"], forward["url"]
                    )
                )
