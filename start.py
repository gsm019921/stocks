import pandas as pd

# pointless percent function
def return_as_percent(x):
    return x * 100

# calculate functions 
def calculate_return(start_price, end_price):
    return (end_price - start_price) / start_price

def calculate_dollar_change(starting_value, ending_value):
    return (ending_value - starting_value)

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
    return end_allocation - start_allocation

def calculate_sector_summary(stocks):
    sectors = {}
    sector_values = {}
    sector_allocation = {}
    sector_starting_values = {}
    sector_starting_allocation = {}
    sector_allocation_drift = {}
    
    largest_sector = None
    largest_sector_value = 0
    smallest_sector = None
    smallest_sector_value = None
    largest_sector_drift = 0
    largest_sector_drift_name = None

    total_starting_value = 0
    total_ending_value = 0

    for stock in stocks:
        starting_value = stock["start_price"] * stock["shares"]
        ending_value = stock["end_price"] * stock["shares"]
        total_starting_value += starting_value
        total_ending_value += ending_value

    for stock in stocks:
        sector = stock["sector"]
        starting_value = stock["start_price"] * stock["shares"]
        ending_value = stock["end_price"] * stock["shares"]

        if sector not in sectors:
            sectors[sector] = 1
        else: 
            sectors[sector] += 1

        if sector not in sector_values:
            sector_values[sector] = ending_value
        else: 
            sector_values[sector] += ending_value

        if sector not in sector_starting_values:
            sector_starting_values[sector] = starting_value
        else:
            sector_starting_values[sector] += starting_value
    
    if total_ending_value > 0: 
        for sector in sectors:
            sector_allocation[sector] = sector_values[sector] / total_ending_value * 100
    
    if total_starting_value > 0:
        for sector in sectors:
            sector_starting_allocation[sector] = sector_starting_values[sector] / total_starting_value * 100

    for sector in sectors:
        sector_allocation_drift[sector] = sector_allocation[sector] - sector_starting_allocation[sector]
        
        if abs(sector_allocation_drift[sector]) > abs(largest_sector_drift):
            largest_sector_drift = sector_allocation_drift[sector]
            largest_sector_drift_name = sector

    for sector in sector_values:
        if sector_values[sector] > largest_sector_value:
            largest_sector = sector
            largest_sector_value = sector_values[sector]
        
        if smallest_sector_value is None:
            smallest_sector = sector
            smallest_sector_value = sector_values[sector]
        elif sector_values[sector] < smallest_sector_value:
            smallest_sector = sector
            smallest_sector_value = sector_values[sector]
    
    return {
        "sectors": sectors,
        "sector_values": sector_values,
        "sector_starting_values": sector_starting_values,
        "sector_allocation": sector_allocation,
        "sector_starting_allocation": sector_starting_allocation,
        "sector_allocation_drift": sector_allocation_drift,
        "largest_sector_drift": largest_sector_drift,
        "largest_sector_drift_name": largest_sector_drift_name,
        "largest_sector": largest_sector,
        "largest_sector_value": largest_sector_value,
        "smallest_sector": smallest_sector,
        "smallest_sector_value": smallest_sector_value,
    }

def calculate_portfolio_summary(stocks):
    # initialize portfolio tracking variables
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
    allocation_drift = 0
    largest_allocation_drift = 0
    largest_allocation_drift_ticker = None
    largest_stock_allocation = 0
    largest_stock_allocation_ticker = None

    stock_summaries = []

    # first loop: calculate total starting/ending value
    for stock in stocks:
        starting_value = stock["start_price"] * stock["shares"]
        ending_value = stock["end_price"] * stock["shares"]
        total_starting_value += starting_value
        total_ending_value += ending_value

    # second loop: analyze each stock
    for stock in stocks:
        ticker = stock["ticker"]
        start_price = stock["start_price"]
        end_price = stock["end_price"]
        shares = stock["shares"]
        sector = stock["sector"]
        starting_value = start_price * shares
        ending_value = end_price * shares
        starting_allocation = starting_value / total_starting_value
        ending_allocation = ending_value / total_ending_value
        stock_return = calculate_return(start_price, end_price) 
        total_return += stock_return
        allocation_drift = calculate_allocation_drift(starting_allocation, ending_allocation)

        if abs(allocation_drift) > abs(largest_allocation_drift): 
            largest_allocation_drift = allocation_drift
            largest_allocation_drift_ticker = ticker
        
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
        
        if ending_allocation > largest_stock_allocation:
            largest_stock_allocation = ending_allocation
            largest_stock_allocation_ticker = ticker

        stock_summary = {
            "ticker": ticker,
            "start_price": start_price,
            "end_price": end_price,
            "starting_value": starting_value,
            "ending_value": ending_value,
            "shares": shares,
            "starting_allocation": starting_allocation,
            "ending_allocation": ending_allocation,
            "sector": sector,
        }

        stock_summaries.append(stock_summary)

    # calculate final summary metrics
    total_stocks = gainers + losers + break_evens

    if total_stocks > 0:
        gainer_percentage = gainers / total_stocks * 100
        loser_percentage = losers / total_stocks * 100
        break_even_percentage = break_evens / total_stocks * 100
        average_return = return_as_percent(total_return / total_stocks)
        best_return = return_as_percent(best_return)
        worst_return = return_as_percent(worst_return)
        portfolio_return = calculate_portfolio_return(total_starting_value, total_ending_value)
        win_ratio = calculate_win_ratio(gainers, losers)
    else:
        gainer_percentage = None
        loser_percentage = None
        break_even_percentage = None
        average_return = None
        best_return = None
        worst_return = None
        portfolio_return = None
        win_ratio = None

    return {
        "total_stocks": total_stocks,
        "gainers": gainers,
        "losers": losers,
        "break_evens": break_evens,
        "gainer_percentage": gainer_percentage,
        "loser_percentage": loser_percentage,
        "break_even_percentage": break_even_percentage,
        "average_return": average_return,
        "total_gainer_return": total_gainer_return,
        "total_loser_return": total_loser_return,
        "best_ticker": best_ticker,
        "best_return": best_return,
        "worst_ticker": worst_ticker,
        "worst_return": worst_return,
        "total_starting_value": total_starting_value,
        "total_ending_value": total_ending_value,
        "largest_stock_allocation": largest_stock_allocation,
        "largest_stock_allocation_ticker": largest_stock_allocation_ticker,
        "largest_allocation_drift": largest_allocation_drift,
        "largest_allocation_drift_ticker": largest_allocation_drift_ticker,
        "portfolio_return": portfolio_return,
        "win_ratio": win_ratio,
        "stock_summaries": stock_summaries
    }

def calculate_pandas_portfolio_summary(df):
    total_stocks = len(df)

    if total_stocks == 0:
        return {
            "total_stocks": 0,
            "gainers": 0,
            "losers": 0,
            "break_evens": 0,
            "gainer_percentage": None,
            "loser_percentage": None,
            "break_even_percentage": None,
            "average_return": None,
            "average_gainer_return": None,
            "average_loser_return": None,
            "portfolio_return": None,
            "win_loss_ratio": None,
            "total_starting_value": 0,
            "total_ending_value": 0,
            "best_ticker": None,
            "best_return": None,
            "worst_ticker": None,
            "worst_return": None,
            "largest_allocation_drift_ticker": None,
            "largest_allocation_drift": None,
        }

    total_starting_value = df["starting_value"].sum()
    total_ending_value = df["ending_value"].sum()

    largest_drift_row = df.loc[df["abs_allocation_drift"].idxmax()]
    best_return_row = df.loc[df["percent_return"].idxmax()]
    worst_return_row = df.loc[df["percent_return"].idxmin()]

    gainers = (df["percent_return"] > 0).sum()
    losers = (df["percent_return"] < 0).sum()
    break_evens = (df["percent_return"] == 0).sum()

    gainer_percentage = gainers / total_stocks * 100
    loser_percentage = losers / total_stocks * 100
    break_even_percentage = break_evens / total_stocks * 100

    average_return = df["percent_return"].mean()
    average_gainer_return = df.loc[df["percent_return"] > 0, "percent_return"].mean()
    average_loser_return = df.loc[df["percent_return"] < 0, "percent_return"].mean()

    if total_starting_value > 0:
        portfolio_return = (total_ending_value - total_starting_value) / total_starting_value * 100
    else:
        portfolio_return = None

    if losers > 0:
        win_loss_ratio = gainers / losers
    else:
        win_loss_ratio = None

    return {
        "total_stocks": total_stocks,
        "gainers": gainers,
        "losers": losers,
        "break_evens": break_evens,
        "gainer_percentage": gainer_percentage,
        "loser_percentage": loser_percentage,
        "break_even_percentage": break_even_percentage,
        "average_return": average_return,
        "average_gainer_return": average_gainer_return,
        "average_loser_return": average_loser_return,
        "portfolio_return": portfolio_return,
        "win_loss_ratio": win_loss_ratio,
        "total_starting_value": total_starting_value,
        "total_ending_value": total_ending_value,
        "best_ticker": best_return_row["ticker"],
        "best_return": best_return_row["percent_return"],
        "worst_ticker": worst_return_row["ticker"],
        "worst_return": worst_return_row["percent_return"],
        "largest_allocation_drift_ticker": largest_drift_row["ticker"],
        "largest_allocation_drift": largest_drift_row["allocation_drift"],
    }

def prepare_portfolio_dataframe(df):
    df = df.copy()

    df["starting_value"] = df["start_price"] * df["shares"]
    df["ending_value"] = df["end_price"] * df["shares"]
    df["stock_return"] = (df["end_price"] - df["start_price"]) / df["start_price"]
    df["percent_return"] = df["stock_return"] * 100

    total_starting_value = df["starting_value"].sum()
    total_ending_value = df["ending_value"].sum()

    df["starting_allocation"] = df["starting_value"] / total_starting_value
    df["ending_allocation"] = df["ending_value"] / total_ending_value
    df["starting_allocation_percent"] = df["starting_allocation"] * 100
    df["ending_allocation_percent"] = df["ending_allocation"] * 100
    df["allocation_drift"] = df["ending_allocation_percent"] - df["starting_allocation_percent"]
    df["abs_allocation_drift"] = df["allocation_drift"].abs()

    return df

# print functions
def print_stock_summary(stock_summary):
    ticker = stock_summary["ticker"]
    start_price = stock_summary["start_price"]
    end_price = stock_summary["end_price"]
    starting_value = stock_summary["starting_value"]
    ending_value = stock_summary["ending_value"]
    shares = stock_summary["shares"]
    starting_allocation = stock_summary["starting_allocation"]
    ending_allocation = stock_summary["ending_allocation"]
    sector = stock_summary["sector"]

    stock_return = calculate_return(start_price, end_price)
    percent_return = return_as_percent(stock_return)
    dollar_change = abs(calculate_dollar_change(starting_value, ending_value))
    start_allocation = return_as_percent(starting_allocation)
    end_allocation = return_as_percent(ending_allocation)
    allocation_drift = calculate_allocation_drift(start_allocation, end_allocation)

    if stock_return > 0: 
        print(f"{ticker} gained {percent_return:.2f}% | Sector: {sector} | Shares: {shares} | Start allocation: {start_allocation:.2f}% | Ending allocation: {end_allocation:.2f}% | Allocation drift: {allocation_drift:+.2f} pts | Dollar change: +${dollar_change:.2f}")
    elif stock_return < 0: 
        print(f"{ticker} lost {abs(percent_return):.2f}% | Sector: {sector} | Shares: {shares} | Start allocation: {start_allocation:.2f}% | Ending allocation: {end_allocation:.2f}% | Allocation drift: {allocation_drift:+.2f} pts | Dollar change: -${dollar_change:.2f}")
    else: 
        print(f"{ticker} broke even with a {percent_return:.2f}% return | Sector: {sector} | Shares: {shares} | Start allocation: {start_allocation:.2f}% | Ending allocation: {end_allocation:.2f}% | Allocation drift: {allocation_drift:+.2f} pts | Dollar change: ${dollar_change:.2f}")

def print_stock_summaries(portfolio_summary):
    stock_summaries = portfolio_summary["stock_summaries"]

    if not stock_summaries: 
        return

    for stock_summary in stock_summaries:
        print_stock_summary(stock_summary)

def print_win_ratio(win_ratio, gainers, losers):
    if win_ratio is not None:
        print(f"Win/loss ratio: {win_ratio:.2f}")
    elif gainers == 0 and losers == 0:
        print("Win/loss ratio: N/A - no gaining or losing stocks")
    else: 
        print("Win/loss ratio: N/A - no losing stocks")
    
def print_average_returns(gainers, losers, total_gainer_return, total_loser_return):
    if losers != 0 and gainers != 0: 
        average_gainer_return = return_as_percent(total_gainer_return / gainers)
        average_loser_return = return_as_percent(total_loser_return / losers)
        print(f"Average gainer return: {average_gainer_return:.2f}%")
        print(f"Average loser return: {average_loser_return:.2f}%")
    elif losers == 0 and gainers != 0: 
        average_gainer_return = return_as_percent(total_gainer_return / gainers)
        print(f"Average gainer return: {average_gainer_return:.2f}%")
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
    change_amount = abs(calculate_dollar_change(starting_value, ending_value))
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

def print_largest_allocation_drift(largest_allocation_drift, largest_allocation_drift_ticker):
    if largest_allocation_drift_ticker is None: 
        print("Largest allocation drift: N/A - no allocation drift")
    
    else:
        largest = largest_allocation_drift * 100
        if largest_allocation_drift > 0:
            print(f"Largest allocation drift: {largest_allocation_drift_ticker} with {largest:+.2f} pts")
        elif largest_allocation_drift < 0: 
            print(f"Largest allocation drift: {largest_allocation_drift_ticker} with {largest:+.2f} pts")
        else:
            print(f"Largest allocation drift: {largest_allocation_drift_ticker} with {largest:.2f} pts")

def print_sector_allocation_summary(sector_summary):
    sectors = sector_summary["sectors"]
    sector_values = sector_summary["sector_values"]
    sector_allocation = sector_summary["sector_allocation"]
    sector_starting_allocation = sector_summary["sector_starting_allocation"]
    sector_allocation_drift = sector_summary["sector_allocation_drift"]

    sorted_sectors = sorted(
        sector_allocation,
        key=sector_allocation.get,
        reverse=True
    )

    print("\n--- Sector Allocation Summary ---")
    print("Sorted by allocation: highest to lowest")

    for sector in sorted_sectors:
        value = sector_values[sector]
        allocation = sector_allocation[sector]
        starting_allocation = sector_starting_allocation[sector]
        allocation_drift = sector_allocation_drift[sector]
        count = sectors[sector]

        print(f"{sector}: {count} stocks | Start: {starting_allocation:.2f}% | End: {allocation:.2f}% | Drift: {allocation_drift:+.2f} pts | ${value:.2f}")

def print_largest_sector(sector_summary):
    largest_sector = sector_summary["largest_sector"]
    largest_sector_value = sector_summary["largest_sector_value"]

    if largest_sector is None: 
        print("Largest sector: N/A")
    else: 
        print(f"Largest sector: {largest_sector} with ${largest_sector_value:.2f}")

def print_smallest_sector(sector_summary):
    smallest_sector = sector_summary["smallest_sector"]
    smallest_sector_value = sector_summary["smallest_sector_value"]

    if smallest_sector is None: 
        print("Smallest sector: N/A")
    else: 
        print(f"Smallest sector: {smallest_sector} with ${smallest_sector_value:.2f}")

def print_concentration_warnings(sector_summary, concentration_threshold):
    sector_allocation = sector_summary["sector_allocation"]
    warning_found = False
    warning_count = 0

    for sector in sector_allocation:
        allocation = sector_allocation[sector]

        if allocation > concentration_threshold:
            warning_count += 1
            print(f"Concentration warning: {sector} is {allocation:.2f}% of the portfolio")
            warning_found = True
    
    if warning_found is False:
        print(f"No sector concentration warnings above {concentration_threshold}%")
    
    print(f"Total concentration warnings: {warning_count}")

def print_stock_concentration_warning(portfolio_summary, stock_concentration_threshold):
    largest_stock_allocation = portfolio_summary["largest_stock_allocation"]
    largest_stock_allocation_ticker = portfolio_summary["largest_stock_allocation_ticker"]
    largest_stock_allocation_percent = return_as_percent(largest_stock_allocation)

    if largest_stock_allocation_ticker is None: 
        print("Stock concentration warning: N/A - no stocks available")
    
    if largest_stock_allocation_percent > stock_concentration_threshold:
        print(f"Stock concentration warning: {largest_stock_allocation_ticker} is {largest_stock_allocation_percent:.2f}% of the portfolio")
    else: 
        print(f"No concentration warnings above {stock_concentration_threshold}%")
    
def print_largest_sector_drift(sector_summary):
    largest_sector_drift = sector_summary["largest_sector_drift"]
    largest_sector_drift_name = sector_summary["largest_sector_drift_name"]

    if largest_sector_drift_name is None:
        print("Largest sector drift: N/A - no sector drift")
    else:
        print(f"Largest sector drift: {largest_sector_drift_name} with {largest_sector_drift:+.2f} pts")

def print_largest_stock_allocation(portfolio_summary):
    largest_stock_allocation = return_as_percent(portfolio_summary["largest_stock_allocation"])
    largest_stock_allocation_ticker = portfolio_summary["largest_stock_allocation_ticker"]

    if largest_stock_allocation_ticker is not None: 
        print(f"Largest stock allocation: {largest_stock_allocation_ticker} with {largest_stock_allocation:.2f}%")
    else:
        print("Largest stock allocation: N/A - no stocks available")

def print_portfolio_summary(portfolio_summary):
    total_stocks = portfolio_summary["total_stocks"]
    gainers = portfolio_summary["gainers"]
    losers = portfolio_summary["losers"]
    break_evens = portfolio_summary["break_evens"]
    gainer_percentage = portfolio_summary["gainer_percentage"]
    loser_percentage = portfolio_summary["loser_percentage"]
    break_even_percentage = portfolio_summary["break_even_percentage"]
    average_return = portfolio_summary["average_return"]
    total_gainer_return = portfolio_summary["total_gainer_return"]
    total_loser_return = portfolio_summary["total_loser_return"]
    best_ticker = portfolio_summary["best_ticker"]
    best_return = portfolio_summary["best_return"]
    worst_ticker = portfolio_summary["worst_ticker"]
    worst_return = portfolio_summary["worst_return"]
    total_starting_value = portfolio_summary["total_starting_value"]
    total_ending_value = portfolio_summary["total_ending_value"]
    largest_allocation_drift = portfolio_summary["largest_allocation_drift"]
    largest_allocation_drift_ticker = portfolio_summary["largest_allocation_drift_ticker"]
    portfolio_return = portfolio_summary["portfolio_return"]
    win_ratio = portfolio_summary["win_ratio"]

    print("\n--- Portfolio Summary ---")

    if total_stocks == 0: 
        print("N/A - no stocks available")
        return
    
    print(f"Total stocks analyzed: {total_stocks}")
    print(f"Number of gainers: {gainers}")
    print(f"Number of losers: {losers}")
    print(f"Number of break-evens: {break_evens}")
    print(f"Percentage of stocks that gained: {gainer_percentage:.2f}%")
    print(f"Percentage of stocks that lost: {loser_percentage:.2f}%")
    print(f"Percentage of stocks that broke even: {break_even_percentage:.2f}%")
    print(f"Average return: {average_return:.2f}%")
    print_average_returns(gainers, losers, total_gainer_return, total_loser_return)
    print(f"Best performer: {best_ticker} with {best_return:.2f}%")
    print(f"Worst performer: {worst_ticker} with {worst_return:.2f}%")
    print(f"Total starting value: ${total_starting_value:.2f}")
    print(f"Total ending value: ${total_ending_value:.2f}")
    print_largest_stock_allocation(portfolio_summary)
    print_stock_concentration_warning(portfolio_summary, stock_concentration_threshold)
    print_largest_allocation_drift(largest_allocation_drift, largest_allocation_drift_ticker)
    print_portfolio_dollar_change(total_starting_value, total_ending_value)
    print_portfolio_return(portfolio_return)
    print_win_ratio(win_ratio, gainers, losers)

def print_sector_summary(sector_summary, concentration_threshold):
    print_sector_allocation_summary(sector_summary)
    print_largest_sector(sector_summary)
    print_smallest_sector(sector_summary)
    print_largest_sector_drift(sector_summary)
    print_concentration_warnings(sector_summary, concentration_threshold)

def print_pandas_portfolio_summary(pandas_portfolio_summary):
    print("\n--- Pandas Portfolio Summary ---")

    if pandas_portfolio_summary["total_stocks"] == 0:
        print("N/A - no stocks available")
        return
    
    print(f"Total stocks analyzed: {pandas_portfolio_summary['total_stocks']}")
    print(f"Number of gainers: {pandas_portfolio_summary['gainers']}")
    print(f"Number of losers: {pandas_portfolio_summary['losers']}")
    print(f"Number of break-evens: {pandas_portfolio_summary['break_evens']}")

    if pandas_portfolio_summary["portfolio_return"] is not None:
        print(f"Portfolio return: {pandas_portfolio_summary['portfolio_return']:.2f}%")
    else:
        print("Portfolio return: N/A")

    print(
        f"Best performer: {pandas_portfolio_summary['best_ticker']} "
        f"with {pandas_portfolio_summary['best_return']:.2f}%"
    )

    print(
        f"Worst performer: {pandas_portfolio_summary['worst_ticker']} "
        f"with {pandas_portfolio_summary['worst_return']:.2f}%"
    )

    print(
        f"Largest allocation drift: {pandas_portfolio_summary['largest_allocation_drift_ticker']} "
        f"with {pandas_portfolio_summary['largest_allocation_drift']:+.2f} pts"
    )

def print_pandas_stock_table(df):
    if df.empty:
        return

    print(df[["ticker", "starting_allocation_percent", "ending_allocation_percent", "allocation_drift"]])

# stock list + concentration thresholds
stocks = [
    {
        "ticker": "AAPL",
        "start_price": 100,
        "end_price": 110,
        "shares": 5,
        "sector": "Technology",
    },
    {
        "ticker": "NVDA",
        "start_price": 100,
        "end_price": 180,
        "shares": 4,
        "sector": "Semiconductors",
    },
    {
        "ticker": "MSFT",
        "start_price": 100,
        "end_price": 100,
        "shares": 6,
        "sector": "Technology",
    },
    {
        "ticker": "JNJ",
        "start_price": 100,
        "end_price": 95,
        "shares": 3,
        "sector": "Healthcare",
    },
    {
        "ticker": "XOM",
        "start_price": 100,
        "end_price": 120,
        "shares": 2,
        "sector": "Energy",
    },
]

stock_columns = ["ticker", "start_price", "end_price", "shares", "sector"]

df = pd.DataFrame(stocks, columns=stock_columns)
df = prepare_portfolio_dataframe(df)

pandas_portfolio_summary = calculate_pandas_portfolio_summary(df)

print_pandas_portfolio_summary(pandas_portfolio_summary)
print_pandas_stock_table(df)

concentration_threshold = 40
stock_concentration_threshold = 50

# sector and portfolio summary dictionaries
portfolio_summary = calculate_portfolio_summary(stocks)
sector_summary = calculate_sector_summary(stocks)

# print + concentration threshold
print_stock_summaries(portfolio_summary)
print_portfolio_summary(portfolio_summary)
print_sector_summary(sector_summary, concentration_threshold)


