def return_as_percent(stock_return):
    return stock_return * 100

def calculate_return(start_price, end_price):
    return (end_price - start_price) / start_price

def calculate_dollar_change(starting_value, ending_value):
    return abs(ending_value - starting_value)

def calculate_portfolio_return(starting_value, ending_value):
    if starting_value != 0:
        return ((ending_value - starting_value) / starting_value) * 100
    else: 
        return None
    
def calculate_win_ratio(gainers, losers):
    if losers != 0:
        return gainers / losers
    else: 
        return None
    
def calculate_allocation_drift(start_allocation, end_allocation):
    return abs(end_allocation - start_allocation)

def print_stock_summary(ticker, start_price, end_price, starting_value, ending_value, shares, starting_allocation, ending_allocation):
    stock_return = calculate_return(start_price, end_price)
    percent_return = return_as_percent(stock_return)
    dollar_change = calculate_dollar_change(starting_value, ending_value)
    start_allocation = return_as_percent(starting_allocation)
    end_allocation = return_as_percent(ending_allocation)
    allocation_drift = calculate_allocation_drift(start_allocation, end_allocation)

    if stock_return > 0: 
        print(f"{ticker} gained {percent_return:.2f}% | Shares: {shares} | Start allocation: {start_allocation:.2f}% | Ending allocation: {end_allocation:.2f}% | Allocation drift: +{allocation_drift:.2f} pts | Dollar change: +${dollar_change:.2f}")
    elif stock_return < 0: 
        print(f"{ticker} lost {abs(percent_return):.2f}% | Shares: {shares} | Start allocation: {start_allocation:.2f}% | Ending allocation: {end_allocation:.2f}% | Allocation drift: -{allocation_drift:.2f} pts | Dollar change: -${dollar_change:.2f}")
    else: 
        print(f"{ticker} broke even with a {percent_return:.2f}% return | Shares: {shares} | Start allocation: {start_allocation:.2f}% | Ending allocation: {end_allocation:.2f}% | Allocation drift: {allocation_drift:.2f} pts | Dollar change: ${dollar_change:.2f}")

def print_win_ratio(win_ratio, gainers, losers):
    if win_ratio is not None:
        print(f"Win/loss ratio: {win_ratio:.2f}")
    elif gainers == 0 and losers == 0:
        print("Win/loss ratio: N/A - no gaining or losing stocks")
    else: 
        print("Win/loss ratio: N/A - no losing stocks")
    
def calculate_averages(gainers, losers, total_gainer_return, total_loser_return):
    if losers != 0 and gainers != 0: 
        average_gainer_return = total_gainer_return / gainers
        average_loser_return = total_loser_return / losers
        average_gainer_percent = return_as_percent(average_gainer_return)
        average_loser_percent = return_as_percent(average_loser_return)
        print(f"Average gainer return: {average_gainer_percent:.2f}%")
        print(f"Average loser return: {average_loser_percent:.2f}%")
    elif losers == 0 and gainers != 0: 
        average_gainer_return = total_gainer_return / gainers
        average_gainer_percent = return_as_percent(average_gainer_return)
        print(f"Average gainer return: {average_gainer_percent:.2f}%")
        print("Average loser return: N/A - no losers") 
    elif gainers == 0 and losers != 0: 
        average_loser_return = total_loser_return / losers
        average_loser_percent = return_as_percent(average_loser_return)
        print("Average gainer return: N/A - no gainers") 
        print(f"Average loser return: {average_loser_percent:.2f}%")
    else: 
        print("Average gainer return: N/A - no gainers") 
        print("Average loser return: N/A - no losers") 

def print_portfolio_dollar_change(starting_value, ending_value):
    change_amount = calculate_dollar_change(starting_value, ending_value)
    if starting_value > ending_value: 
        print(f"Portfolio lost ${change_amount:.2f}")
    elif starting_value < ending_value:
        print(f"Portfolio gained ${change_amount:.2f}")
    else: 
        print("Portfolio broke even with a $0.00 change")

def print_portfolio_return(portfolio_return):
    if portfolio_return is not None:
        print(f"Portfolio return: {portfolio_return:.2f}%")
    else: 
        print(f"Portfolio return: N/A - starting value of $0.00")

stocks = [
    ["AAPL", 100, 150, 5],
    ["TSLA", 100, 50, 5],
    ["MSFT", 100, 100, 5]
]

gainers = 0
losers = 0
break_evens = 0
total_return = 0
best_ticker = ""
best_return = None
worst_ticker = ""
worst_return = None
total_gainer_return = 0
total_loser_return = 0
starting_value = 0
ending_value = 0
total_starting_value = 0
total_ending_value = 0

for ticker, start_price, end_price, shares in stocks:
    starting_value = start_price * shares
    ending_value = end_price * shares
    total_starting_value += starting_value
    total_ending_value += ending_value

for ticker, start_price, end_price, shares in stocks:
    starting_value = start_price * shares
    ending_value = end_price * shares
    starting_allocation = starting_value / total_starting_value
    ending_allocation = ending_value / total_ending_value
    stock_return = calculate_return(start_price, end_price) 
    total_return += stock_return

    if stock_return > 0:
        gainers += 1
        total_gainer_return += stock_return
    elif stock_return < 0: 
        losers +=1
        total_loser_return += stock_return
    else: 
        break_evens += 1

    if worst_return is None or stock_return < worst_return:
        worst_return = stock_return
        worst_ticker = ticker
    if best_return is None or stock_return > best_return:
        best_return = stock_return
        best_ticker = ticker

    print_stock_summary(ticker, start_price, end_price, starting_value, ending_value, shares, starting_allocation, ending_allocation)


total_stocks = gainers + losers + break_evens
gainer_percentage = gainers / total_stocks * 100
loser_percentage = losers / total_stocks * 100
break_even_percentage = break_evens / total_stocks * 100
average_return = total_return / total_stocks
average_return_percent = return_as_percent(average_return)
best_return = return_as_percent(best_return)
worst_return = return_as_percent(worst_return)
portfolio_return = calculate_portfolio_return(total_starting_value, total_ending_value)
win_ratio = calculate_win_ratio(gainers, losers)
    
print("\n--- Portfolio Summary ---")
print(f"Total stocks analyzed: {total_stocks}")
print(f"Number of gainers: {gainers}")
print(f"Number of losers: {losers}")
print(f"Number of break-evens: {break_evens}")
print(f"Percentage of stocks that gained: {gainer_percentage:.2f}%")
print(f"Percentage of stocks that lost: {loser_percentage:.2f}%")
print(f"Percentage of stocks that broke even: {break_even_percentage:.2f}%")
print(f"Average return: {average_return_percent:.2f}%")
calculate_averages(gainers, losers, total_gainer_return, total_loser_return)
print(f"Best performer: {best_ticker} with {best_return:.2f}%")
print(f"Worst performer: {worst_ticker} with {worst_return:.2f}%")
calculate_win_ratio(gainers, losers)
print(f"Total starting value: ${total_starting_value:.2f}")
print(f"Total ending value: ${total_ending_value:.2f}")
print_portfolio_dollar_change(total_starting_value, total_ending_value)
print_portfolio_return(portfolio_return)
print_win_ratio(win_ratio, gainers, losers)

