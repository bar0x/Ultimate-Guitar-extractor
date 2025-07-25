import shodan

api = shodan.Shodan('S73xOqv6zoolf3UNfR9wDJ9JSG3uKtPh')

info = api.info()
print(f"Crediti disponibili: {info['query_credits']}")
