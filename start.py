def calculate_return(start_price, end_price):
    return (end_price - start_price) / start_price

def return_as_percent(stock_return):
    return stock_return * 100

def print_stock_summary(ticker, start_price, end_price):
    stock_return = calculate_return(start_price, end_price)
    percent_return = return_as_percent(stock_return)

    if stock_return > 0: 
        print(f"{ticker} gained {percent_return:.2f}%")
    elif stock_return < 0: 
        print(f"{ticker} lost {abs(percent_return):.2f}%")
    else: 
        print(f"{ticker} broke even with a {percent_return:.2f}% return")

stocks = [
    ["AAPL", 100, 110],
    ["TSLA", 100, 90],
    ["MSFT", 100, 100],
    ["NVDA", 200, 250],
    ["SPY", 500, 475]
]

gainers = 0
losers = 0
break_evens = 0
total_return = 0

for ticker, start_price, end_price in stocks:
    stock_return = calculate_return(start_price, end_price) 
    total_return += stock_return

    if stock_return > 0:
        gainers += 1
    elif stock_return < 0: 
        losers +=1
    else: 
        break_evens += 1

    print_stock_summary(ticker, start_price, end_price)

total_stocks = gainers + losers + break_evens
gainer_percentage = gainers / total_stocks * 100
loser_percentage = losers / total_stocks * 100
break_even_percentage = break_evens / total_stocks * 100
average_return = total_return / total_stocks
average_return_percent = return_as_percent(average_return)
    
print(f"Number of gainers: {gainers}")
print(f"Number of losers: {losers}")
print(f"Number of break-evens: {break_evens}")
print(f"Total stocks analyzed: {total_stocks}")
print(f"Percentage of stocks that gained: {gainer_percentage:.2f}%")
print(f"Percentage of stocks that lost: {loser_percentage:.2f}%")
print(f"Percentage of stocks that broke even: {break_even_percentage:.2f}%")
print(f"Average returns: {average_return_percent:.2f}%")
    

