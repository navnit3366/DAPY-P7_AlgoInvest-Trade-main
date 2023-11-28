import csv
import datetime

def load_file(file_path):
    data = []

    ### READING CSV FILE
    with open(file_path, mode ='r') as file:
    
        # reading the CSV file
        csvFile = csv.DictReader(file)
    
        # displaying the contents of the CSV file
        for line in csvFile:
            # print(line)
            action = dict(line)
            price = float(action["price"])        
            if price <= 0:
                # print(action)
                next
            else:
                action["gain"] = (price * float(action["profit"])/100)
                action["price"] = float(action['price'])
                data.append(action)
                # use tuple (name, gain) ? 
    return data


def recursive_maximize_profit(data, index_of_action, remaining_money, total_gain, timed=True):
    """Maximize profit recursively"""
    if index_of_action == len(data):
        # reached last action
        return total_gain, []

    action = data[index_of_action]
    # print(f"Questioning whether to buy {action}")
    # say i don't buy
    notbought_profit, notbought_list = recursive_maximize_profit(data, index_of_action+1, remaining_money, total_gain)

    # say i buy this action
    if remaining_money >= action["price"]:
        bought_profit, bought_list = recursive_maximize_profit(data, index_of_action+1, remaining_money-action["price"], total_gain+float(action["gain"]))
    else:
        # allowed by the fact actions are sorted by price
        # if THIS action is too pricey, the following won't be cheaper and we'll reach end of line without buying anything
        # print("Cut short")
        return total_gain, []

    if bought_profit > notbought_profit:
        bought_list.append(action)
        return bought_profit, bought_list
    else:
        return notbought_profit, notbought_list


def print_results(list_of_actions):
    list_of_bought_actions = list_of_actions[1]
    optimized_profit = list_of_actions[0]
    total_cost = 0
    print("Bought:")
    for action in list_of_bought_actions:
        # action = data[action_num]
        price_in_eur = float(action["price"])
        print(f"{action['name']} ({price_in_eur}€)")
        total_cost += price_in_eur

    print(
        f"\nTotal cost: {total_cost}\n",
        f"Profit: {optimized_profit}")


def bruteforce_algo(data, max_spent, timed=True):
    start_time = datetime.datetime.now()

    selected_actions = recursive_maximize_profit(data, 0, max_spent, 0)
    
    if timed:
        print(f"Ran in {datetime.datetime.now()- start_time}s.")
    return selected_actions


def main():
    MAX_INVESTED = 500
    file_path = "./test_datasets/test_dataset.csv" # or "./test_datasets/dataset1_Python+P7.csv" 
    data = load_file(file_path)
    # [print(action) for action in data]
    # 19|500 ~ 0.67s avec la liste descendante et remontante
    # 19|500 ~ 0.59s avec la liste remontante seulement (20|500 = 1.19 s, 100|50 = 0.71s)
    # 19|500 ~ 0.54s avec la liste triée et le return des gens sans le sou (20|500 = 1.12s, 21|500 = 1.94s, ~3.7.10^274 années)
    # 19|500 ~ 0.41s si on fait money restante - price (au lieu de money depensée + price < 500) et convertir les prix en float direct
    data = sorted(data,key= lambda x:x["price"])
    selected_actions = bruteforce_algo(data, MAX_INVESTED)
    print_results(selected_actions)

if __name__ == '__main__':
    main()