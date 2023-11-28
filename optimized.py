import csv
import datetime


def load_csv(file_path):
    """Opens a csv file"""

    data = []
    with open(file_path, mode ='r') as file:
    
        # reading the CSV file
        csvFile = csv.DictReader(file)
        # simply csv.reader for a list of list
    
        # displaying the contents of the CSV file
        for line in csvFile:
            # print(line)
            action = dict(line)
            if float(action["price"]) > 0 and float(action["profit"]) > 0:
                action["price"] = int(float(action["price"])*100)
                action["gain"] = action["price"] * float(action["profit"])/100
                action["profit"] = float(action["profit"])
                data.append(action)
    return data


def knapsack_algo(data, max_invested):
    """Knapsack algorithm, timed."""

    # Generate the matrix M(0...n, 0...W)
    profit_matrix = make_profit_matrix(data, max_invested)
    # [print(line_num, profit_matrix[line_num]) for line_num in range(len(profit_matrix))]

    # Browse the matrix from maximum gain to 0,0
    results = recursive_knap(profit_matrix, data, len(data)-1, max_invested)

    return results


def make_profit_matrix(data, money_thresholds):
    """Build and fill a profit matrix for knapsack algorithm resolution."""
    min_price = min(data, key= lambda x:x["price"])["price"]
    max_spent = money_thresholds

    data.insert(0, {"name":"action_0", "price":0, "gain":0})
    profit_matrix = []

    for action_index in range(len(data)):
        profit_matrix.append([0]*int(max_spent+1))
        # if data_index%100 == 0:
        #       # To keep track of huge datasets
        #     print(f"Matrix filed for action number {data_index}")
        for remaining_money in range(0,max_spent+1):
            price = data[action_index]["price"]
            if remaining_money < price:
                # If we don't have no money, we can't buy
                profit_matrix[action_index][remaining_money] = profit_matrix[action_index-1][remaining_money]
            else:
                # If we do have the money, we have a choice to make. What is more profitable between us buying and not buying this action ?  
                option_bought = profit_matrix[action_index-1][remaining_money-price] + data[action_index]["gain"]
                option_notbought = profit_matrix[action_index-1][remaining_money]
                profit_matrix[action_index][remaining_money] = max(option_bought, option_notbought)
        
        # print(f'Line {action_index} = {profit_matrix[action_index]}')

    return profit_matrix


def recursive_knap(profit_matrix, data, action_index, remaining_money, list_of_bought_actions = []):
    """Browse profit matrix from maximum gain to first action and/or 0 remaining money."""
    # print(profit_matrix[action_index][remaining_money])
    # print(f"Checking {action_index},{remaining_money} ({profit_matrix[action_index][remaining_money]}) (having already bought {list_of_bought_actions})")

    if action_index == 0:
        return list_of_bought_actions
    
    if action_index not in list_of_bought_actions:
        # print(f"{profit_matrix[action_index][remaining_money]} > {profit_matrix[action_index-1][remaining_money]} ?")
        if profit_matrix[action_index][remaining_money] > profit_matrix[action_index-1][remaining_money]:
            price = data[action_index]['price']
            list_of_bought_actions.append(action_index)
            return recursive_knap(profit_matrix, data, action_index-1, remaining_money-price, list_of_bought_actions)
        else:
            # not bought
            return recursive_knap(profit_matrix, data, action_index-1, remaining_money, list_of_bought_actions)
   

def greedy_algo(data, max_money):
    data = sorted(data, key= lambda action:action["profit"], reverse=True)
    list_of_bought_actions = []
    remaining_money = max_money
    total_gain = 0
    for action in data:       
        if remaining_money > action["price"]:
            list_of_bought_actions.append(action)
            remaining_money -= action["price"]
            total_gain += action["gain"]

    return list_of_bought_actions


def load_fake_data():
    """Fake dataset for demonstration and testing purposes"""
    return [
    {"name":"FS1", "price":1, "profit": 2, "gain": 2},
    {"name":"FS2", "price":10, "profit": 1, "gain": 10},
    # {"name":"FA3", "price":4, "profit": 1.5, "gain": 6},
    ]


def print_results(actions_list, runtime, sep="\t"):
    """Show results Sienna's style"""
    selected_actions = sorted(actions_list, key= lambda action: (action["profit"],action['price']), reverse=True)
    total_cost = 0
    total_gain = 0

    print(f"Results generated in {runtime}. Bought:")
    for action in selected_actions:
        price_in_eur = action["price"]/100
        total_cost += price_in_eur
        gain = action["gain"]/100
        total_gain += gain
        print(f"{action['name']}{sep}{price_in_eur}")
        # print(f"{action['name']}{sep}{price_in_eur}{sep}{action['profit']}{sep}{gain}")
        

    print(
        f"\nTotal cost: {round(total_cost,2)}€\n",
        f"Profit: {round(total_gain,2)}€")


def main():
    ALGO = "knapsack"
    MAX_SPENT = 50000 # in cents (10 is a good pick for fake data tests)

    # Loading dataset
    file_path = "./datasets/dataset2_Python+P7.csv"
    data = load_csv(file_path) #or load_fake_data()
    data = [action for action in data if action["price"] <= MAX_SPENT]
    # [print(action) for action in data]
    if data == []:
        raise Exception("Dataset shouldn't be empty.")

    # Calling algorithms
    start_time = datetime.datetime.now()
    if ALGO == "knapsack":
        # 0:1 Knapsack problem
        results = knapsack_algo(data, MAX_SPENT)
        results = [data[index] for index in results]
    elif ALGO == "greedy":
        results = greedy_algo(data, MAX_SPENT)

    print_results(results, datetime.datetime.now() - start_time)

if __name__ == '__main__':
    main()