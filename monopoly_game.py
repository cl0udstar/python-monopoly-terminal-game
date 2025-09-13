"""
    Main code
"""
#from tabulate import tabulate
import random
import property_data as pd
import colours as c


nickname_dict = {}
nickname_list = []
player_dice_dict = {}


while True:
    try:
        num_of_players = int(input(f"\n{c.GREEN}Please enter the number of players: {c.END}"))
        while num_of_players > 8 or num_of_players <= 0:
            print(f"{c.RED2}The number of players is between 1 and 8!{c.RED}\n")
            num_of_players = int(input(f"{c.GREEN}Please enter the number of players: {c.END}"))
        break
    except ValueError:
        print(f"{c.RED2}Number of players needs to be an integer{c.END}")


def set_player_nickname():
    """
        Get the player names or nicknames
    """
    for player in range(1, num_of_players+1):
        exists = True
        while exists:
            print()
            player_nickname = str(input(f"{c.BLUE}Player {c.END}{player}, {c.GREEN}create your nickname: {c.END}"))
            if player_nickname not in nickname_dict:
                nickname_dict.update({player_nickname:player})
                nickname_list.append(player_nickname)
                exists = False
            else:
                print(f"{c.RED2}Name already used, enter another one!{c.END}")


def choose_player():
    """
        Choose which player starts first
    """
    #starting_player = random.randrange(num_of_players)
    random.shuffle(nickname_list)

    #return starting_player

#first_player = choose_player()


def roll_dice():
    """
        Rolling the dice
    """
    dice1_num = random.randrange(1, 7)
    dice2_num = random.randrange(1, 7)

    #dice1_num = 1
    #dice2_num = 1

    return dice1_num, dice2_num #total_dice_num


dice_list = []
players_data = []
property_dict = {}
house_dict = {}

def start_game():
    """
        Start the game
    """
    ###
    # Set the needed storing modules for each player
    ###
    for player, _ in zip(nickname_list, range(num_of_players)):
        player_dice_list_generator = []
        # 0 - player name, 1 - player money, 2 - player spendings, 3 - player gains, 4 - player properties, 5 - double or not
        player_data_list_generator = [[player], [pd.PLAYER_MONEY], [], [], [], []]

        dice_list.append(player_dice_list_generator)
        players_data.append(player_data_list_generator)

    ###
    # Start of the loop that checks if the game is finished or not
    ###
    end_game = False
    while not end_game:
        for player, player_id in zip(nickname_list, range(num_of_players)):
            #print()
            ###
            # 'player' holds the nickname of the player
            # 'player_id' holds the id of the player
            ###
            dice_choice_check = True
            while dice_choice_check:
                dice_choice = str(input(f"\n\n{c.BLUE}Player {c.END}{player}, {c.GREEN}roll the dice? {c.END}(y/n) ")).lower()

                if dice_choice in ('y', 'yes'):
                    ###
                    # Call the rolling dice function
                    ###
                    dice = roll_dice()
                    print(f"\n{c.YELLOW}Rolling dice...{c.END}\n")

                    ###
                    # Check for doubles, if 2 are found in a row and the 3rd one in a row is found to be a double then send the player to jail
                    ###
                    #if players_data[player_id][5] == 10 and dice[0] == dice[1]:
                    #    print("A double, you are now free...")

                    if dice[0] == dice[1]:
                        if len(players_data[player_id][5]) == 2:
                            print(f"{c.BLUE}DOUBLE! x3{c.END}\n")
                            print(f"{c.VIOLET}Wow impressive!{c.END}")
                            print(f"{c.VIOLET}You managed to get three doubles in a row, but too bad, you are heading straight to jail. (ps. I'm sorry){c.END}")
                            print(f"{c.VIOLET}Also pay{c.END} £200 {c.VIOLET}to get out next turn.")

                            players_data[player_id][5].clear()
                            dice_list[player_id].clear()
                            property_id = 10
                            dice_list[player_id].append(property_id)

                            players_data[player_id][2].append(200)
                            player_money_left = players_data[player_id][1][0] - 200

                            players_data[player_id][1][0] = player_money_left
                            print(f"\n{c.BLUE}System message{c.END} - {c.RED}£200 taken from your balance.{c.END}")
                            break

                        players_data[player_id][5].append('DOUBLE')
                        if len(players_data[player_id][5]) == 1:
                            print(f"{c.BLUE}DOUBLE!{c.END}\n")
                        elif len(players_data[player_id][5]) == 2:
                            print(f"{c.BLUE}DOUBLE! x2{c.END}\n")
                    else:
                        players_data[player_id][5].clear()

                    ###
                    # Sum up the 2 dice
                    ###
                    dice_num = sum(dice)
                    #dice_num = roll_dice()

                    ###
                    # Append the dice number to the 'dice_list' which has storing modules created in the for loop at the start of the function
                    # Each player has itts own storing module
                    ###
                    dice_list[player_id].append(dice_num)

                    ###
                    # That's the id of the property in 'property_data' module
                    ###
                    property_id = sum(dice_list[player_id])

                    ###
                    # Validation to check if the property id is more than 39 (length of the property list)
                    # This occurs when a lap was completed
                    ###
                    if property_id >= len(pd.property_list):
                        ###
                        # Clear the list of the player with the turn
                        ###
                        dice_list[player_id].clear()

                        ###
                        # Get the new id and add it in the list
                        ###
                        property_id = (property_id - len(pd.property_list))
                        dice_list[player_id].append(property_id)

                        ###
                        # Messages with info for the player
                        ###
                        print(f"{c.VIOLET}You completed one lap!{c.END}")
                        print(f"{c.BLUE}You gained{c.END} £{pd.LAP_MONEY}{c.BLUE}!{c.END}\n")

                        print(f"{c.BLUE}Dice number: {c.END}{dice_num}")
                        print(f"{c.BLUE}Property number: {c.END}{property_id}")
                        print(f"{c.BLUE}Property:{c.END} {pd.property_list[property_id][0]}")

                        ###
                        # Add the lap money (200) to the 4th list which holds the money added to the player account
                        ###
                        players_data[player_id][3].append(pd.LAP_MONEY)
                        player_money_left = players_data[player_id][1][0] + pd.LAP_MONEY

                        ###
                        # Set the new value for money to the 2nd list which holds the total balance
                        ###
                        players_data[player_id][1][0] = player_money_left
                        #print(f"{c.BLUE}You gained{c.END} £{pd.LAP_MONEY}{c.BLUE}!{c.END}")
                    else:
                        ###
                        # Executes only if the property id is lower than the length of the property list
                        ###
                        #print(f"\n{c.YELLOW}Rolling dice...{c.END}\n")
                        print(f"{c.BLUE}Dice number: {c.END}{dice_num}")
                        print(f"{c.BLUE}Property number: {c.END}{property_id}")
                        print(f"{c.BLUE}Property:{c.END} {pd.property_list[property_id][0]}")

                    ###
                    # Checks if the property is ... and does the required operation
                    ###
                    if pd.property_list[property_id][0] == 'Start':
                        break
                    if pd.property_list[property_id][0] == 'Chest':
                        print(f"{c.YELLOW}Opening the chest...{c.END}\n")

                        chest_id = random.choice(pd.chest_list)

                        ###
                        # Check if in the chest is the 1st item in the 'chest_list'
                        ###
                        if chest_id[0] == 0:
                            print(chest_id[1])

                            dice_list[player_id].clear()
                            property_id = 0
                            dice_list[player_id].append(property_id)

                            players_data[player_id][3].append(pd.LAP_MONEY)
                            player_money_left = players_data[player_id][1][0] + pd.LAP_MONEY

                            players_data[player_id][1][0] = player_money_left
                            print(f"{c.BLUE}System message{c.END} - {c.RED}£{pd.LAP_MONEY} added to your balance.{c.END}")

                        ###
                        # Check if in the chest is the 2nd item in the 'chest_list'
                        ###
                        elif chest_id[0] == 1:
                            print(chest_id[1])

                            chest_id_choice = input(f"{c.VIOLET}Collect the money?{c.END} (y/n) ").lower()

                            if chest_id_choice in ('y', 'yes'):
                                print(f"{c.VIOLET}Good, you collected{c.END} £169{c.VIOLET}! Now be proud of yourself...{c.END}")
                            elif chest_id_choice in ('n', 'no'):
                                print(f"{c.VIOLET}Not sure why you would say no to free money, but here you go{c.END} £169{c.VIOLET}!{c.END}")
                            else:
                                print(f"{c.VIOLET}Is it that hard to type yes or no? Anyway, here are{c.END} £169{c.VIOLET}!{c.END}")

                            players_data[player_id][3].append(169)
                            player_money_left = players_data[player_id][1][0] + 169
                            players_data[player_id][1][0] = player_money_left
                            print(f"\n{c.BLUE}System message{c.END} - {c.RED}£169 added to your balance.{c.END}")

                        ###
                        # Check if in the chest is the 3rd item in the 'chest_list'
                        ###
                        elif chest_id[0] == 2:
                            print(chest_id[1])

                            chest_id_choice = str(input(f"{c.VIOLET}Pay?{c.END} (y/n) ")).lower()

                            if chest_id_choice in ('y', 'yes'):
                                print(f"{c.VIOLET}Nice{c.END} -£50{c.VIOLET}! You did a good thing... Future you will say thanks for this :){c.END}")
                            elif chest_id_choice in ('n', 'no'):
                                chest_id_choice_2 = str(input(f"{c.VIOLET}Want it or not, health is important. Now give the Doctor{c.END} £50{c.VIOLET}!{c.END} (y/n) ")).lower()
                                if chest_id_choice_2 in ('sure', 'y', 'yes', 'okay', 'ok'):

                                    print(f"{c.VIOLET}Good! I know it's hard but £50 doesn't make you richer...(or maybe it does idk){c.END}")
                                elif chest_id_choice_2 in ('n', 'no', 'nope','never'):

                                    print(f"{c.RED2}NO! YOU HAVE TO PAY!{c.END} {c.VIOLET}I control your money, so I can just take £50 whenever I want.{c.END}")
                                else:
                                    print(f"{c.VIOLET}It's hard with you! I'll just take the money! (you might say thanks later){c.END}")
                            else:
                                print(f"{c.VIOLET}Not sure why you would type something else than the choises given but just so you know,{c.END} £50{c.VIOLET} are out of your total money!{c.END}")

                            players_data[player_id][2].append(50)
                            player_money_left = players_data[player_id][1][0] - 50
                            players_data[player_id][1][0] = player_money_left
                            print(f"\n{c.BLUE}System message{c.END} - {c.RED}£50 taken from your balance.{c.END}")

                        ###
                        # Check if in the chest is the 4th item in the 'chest_list'
                        ###
                        elif chest_id[0] == 3:
                            print(chest_id[1])

                            print(f"\n{c.VIOLET}So, so, so, look, you have this stock in your account, right.?{c.END}")
                            print(f"{c.VIOLET}And you need to sell it right now. It will give you £50.{c.END}")

                            chest_id_choice = str(input(f"\n{c.VIOLET}Sell it? (it's take it or leave it){c.END} (y/n) ")).lower()

                            if chest_id_choice in ('y', 'yes'):
                                print(f"{c.VIOLET}Great choice! You will not regret this sale.{c.END}")
                            elif chest_id_choice in ('n', 'no'):
                                print(f"{c.RED2}You won't get more money from this stock, it's a once in a game chance to get the £50.{c.END}")

                                chest_id_choice_2 = str(input(f"\n{c.VIOLET}So, what do you say, sell.?{c.END} (y/y) ")).lower()

                                if chest_id_choice_2 in ('y', 'yes'):
                                    print(f"{c.VIOLET}Finally, if you waited a bit longer then the stock would be worth nothing... (probably){c.END}")
                                else:
                                    print(f"{c.RED2}I know that the answer this time is not yes, so I will do you a favour and sell the stock.{c.END}")
                            else:
                                print(f"{c.RED2}I will just give you the money!{c.END}")

                            players_data[player_id][3].append(50)
                            player_money_left = players_data[player_id][1][0] + 50
                            players_data[player_id][1][0] = player_money_left
                            print(f"\n{c.BLUE}System message{c.END} - {c.RED}£50 added to your balance.{c.END}")

                        ###
                        # Check if in the chest is the 5th item in the 'chest_list'
                        ###
                        elif chest_id[0] == 4:
                            print(chest_id[1])

                            dice_list[player_id].clear()
                            property_id = 10
                            dice_list[player_id].append(property_id)

                            print(f"\n{c.BLUE}System message{c.END} - {c.RED}You are now in jail for the next 3 turns!{c.END}")

                        ###
                        # Check if in the chest is the 6th item in the 'chest_list'
                        ###
                        elif chest_id[0] == 5:
                            print(chest_id[1])

                            print(f"\n{c.VIOLET}You know.. maybe sometimes kids are a liability (just saying){c.END}")

                            players_data[player_id][2].append(150)
                            player_money_left = players_data[player_id][1][0] - 150
                            players_data[player_id][1][0] = player_money_left
                            print(f"\n{c.BLUE}System message{c.END} - {c.RED}£150 taken from your balance.{c.END}")

                        ###
                        # Check if in the chest is the 7th item in the 'chest_list'
                        ###
                        elif chest_id[0] == 6:
                            print(chest_id[1])

                        ###
                        # Check if in the chest is the 8th item in the 'chest_list'
                        ###
                        elif chest_id[0] == 7:
                            print(chest_id[1])

                            player_id_money_add = 10 * (num_of_players-1)

                            for player_list in players_data:
                                if player_list[0][0] == player:
                                    player_list[3].append(player_id_money_add)
                                    player_list_money_left = player_list[1][0] + player_id_money_add
                                    player_list[1][0] = player_list_money_left

                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}£{player_id_money_add} added to your balance.{c.END}")
                                else:
                                    player_list[2].append(10)
                                    player_list_money_left = player_list[1][0] - 10
                                    player_list[1][0] = player_list_money_left

                        ###
                        # Check if in the chest is the 9th item in the 'chest_list'
                        ###
                        elif chest_id[0] == 8:
                            print(chest_id[1])

                        ###
                        # Check if in the chest is the 10th item in the 'chest_list'
                        ###
                        elif chest_id[0] == 9:
                            print(chest_id[1])

                            print(f"{c.VIOLET}Roads need care too, so... (you know what to do){c.END}")

                            property_land_counter = 0
                            for _ in players_data[player_id][4]:
                                property_land_counter += 1

                            if property_land_counter == 0:
                                print(f"\n{c.VIOLET}Well, looks like you don't need to pay anything..yet...{c.END}")
                            else:
                                chest_id_choice = str(input(f"{c.VIOLET}Pay{c.END} (y) ")).lower()

                                if chest_id_choice in ('y', 'yes'):
                                    print(f"{c.VIOLET}Taking the money now, glad to be at your service!{c.END}")
                                else:
                                    print(f"{c.VIOLET}Can't change the fact that I already took the money!{c.END}")

                                player_money_take = 20 * property_land_counter
                                players_data[player_id][2].append(player_money_take)
                                player_money_left = players_data[player_id][1][0] - player_money_take
                                players_data[player_id][1][0] = player_money_left
                                print(f"\n{c.BLUE}System message{c.END} - {c.RED}£{player_money_take} taken from your balance.{c.END}")



                    elif pd.property_list[property_id][0] == 'Chance':
                        print("Looking for a chance...")
                    elif pd.property_list[property_id][0] == 'Jail':
                        print(f"\n{c.VIOLET}Oh, just a property named Jail. Nothing to worry about..{c.END}")
                        break
                    elif pd.property_list[property_id][0] == 'Go To Jail':
                        print(f"\n{c.VIOLET}Look, you got arrested, right!?{c.END}")
                        print(f"{c.VIOLET}But no need to be sad, maybe this is for the good, you get to chill for a bit.{c.END}")

                        dice_list[player_id].clear()
                        property_id = 10
                        dice_list[player_id].append(property_id)

                        print(f"{c.VIOLET}Also pay{c.END} £200 {c.VIOLET}to get out next turn.{c.END}")

                        players_data[player_id][2].append(200)
                        player_money_left = players_data[player_id][1][0] - 200

                        if player_money_left <= 0:
                            print(f"{c.VIOLET}What a shame.!{c.END} {player} {c.VIOLET}has no money left! GG{c.END}\n")
                            print(f"{c.YELLOW}Game ending...{c.END}\n")
                            print(f"{c.BEIGE}Many thanks for playing!{c.END}")
                            end_game = True
                            break

                        ###
                        # Set the player money to the money left from the operation above
                        ###
                        players_data[player_id][1][0] = player_money_left

                        ###
                        # Message to the player of how much it paid
                        ###
                        print(f"\n{c.BLUE}System message{c.END} - {c.RED}£200 taken from your balance.{c.END}")

                        #players_data[player_id][1][0] = player_money_left
                        #print(f"\n{c.BLUE}System message{c.END} - {c.RED}£200 taken from your balance.{c.END}")

                    elif pd.property_list[property_id][0] == 'Free Parking':
                        print("You are now part of the rich!")
                    elif (pd.property_list[property_id][0] == 'Income Tax' or
                        pd.property_list[property_id][0] == 'Electric Company' or
                        pd.property_list[property_id][0] == 'Water Works' or
                        pd.property_list[property_id][0] == 'Super Tax'):

                        players_data[player_id][2].append(pd.property_list[property_id][1])
                        player_money_left = players_data[player_id][1][0] - pd.property_list[property_id][1]

                        ###
                        # Validate the money of the player (if less, then end game)
                        ###
                        if player_money_left <= 0:
                            print(f"What a shame.! {player} {c.BLUE}has no money left! GG{c.END}\n")
                            print(f"{c.YELLOW}Game ending...{c.END}\n")
                            print(f"{c.BEIGE}Many thanks for playing!{c.END}")
                            end_game = True
                            break

                        ###
                        # Set the player money to the money left from the operation above
                        ###
                        players_data[player_id][1][0] = player_money_left

                        ###
                        # Message to the player of how much it paid
                        ###
                        print(f"\n{c.BLUE}System message{c.END} - {c.RED}You paid{c.END} £{pd.property_list[property_id][1]} {c.RED}to the government.{c.END}")
                    else:
                        ###
                        # If the property the player is on is not one of the above, then execute the following
                        # Display the price of the property
                        # Display the player's balance
                        ###
                        print(f"{c.BLUE}Price:{c.END} £{pd.property_list[property_id][1]}\n")
                        print(f"{c.BLUE}System message{c.END} - {c.RED}You have: {c.END}£{players_data[player_id][1][0]}")

                        ###
                        # If the property that the player in on, is in another player's inventory do the following below
                        ###
                        if pd.property_list[property_id][0] in property_dict: #player_list[4]
                            ###
                            # If the player is the same player that owns the property, then ask if it wants to buy any houses
                            ###
                            if property_dict[pd.property_list[property_id][0]] == player:
                                print(f"\n{c.VIOLET}Yay, your own property! No need to strees for now... (or maybe...){c.END}")

                                if pd.property_list[property_id][0] in ("King's Cross Station", "Marylebone Station", "Fenchurch St Station", "Liverpool Street Station"):
                                    break

                                if house_dict[pd.property_list[property_id][0]] == 0:
                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}You have {house_dict[pd.property_list[property_id][0]]} houses{c.END}")

                                    house_buy_choice = str(input(f"\n{c.GREEN}Do you want to buy any houses?{c.END} (y/n) ")).lower()

                                    if house_buy_choice in ('y', 'yes'):
                                        house_choice_check = True
                                        if property_id > 0 or property_id < 10:
                                            while house_choice_check:
                                                house_choice = str(input(f"\n{c.GREEN}How many do you want to aquire? (max. 4){c.END} "))

                                                if house_choice == '0':
                                                    print(f"\n{c.VIOLET}Seriously...You chose yes and did not buy any houses. (Dissapointed){c.END}")

                                                    house_choice_check = False

                                                elif house_choice == '1':
                                                    house_pay = pd.HOUSE_PRICE_1

                                                    houses = house_dict[pd.property_list[property_id][0]] + 1
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}1 house aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Look at you, starting slowly to buy stuff. Well done!{c.END}")

                                                    house_choice_check = False

                                                elif house_choice == '2':
                                                    house_pay = pd.HOUSE_PRICE_1 * 2

                                                    houses = house_dict[pd.property_list[property_id][0]] + 2
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"{c.BLUE}System message{c.END} - {c.RED}2 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Have added 2 houses to your land. Well done! (p.s. YOUNG BUSINESS PERSON){c.END}")

                                                    house_choice_check = False

                                                elif house_choice == '3':
                                                    house_pay = pd.HOUSE_PRICE_1 * 3

                                                    houses = house_dict[pd.property_list[property_id][0]] + 3
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}3 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Wow impressive, 3 houses in one payment. Btw, I have added them to your land.{c.END}")

                                                    house_choice_check = False

                                                elif house_choice == '4':
                                                    house_pay = pd.HOUSE_PRICE_1 * 4

                                                    houses = house_dict[pd.property_list[property_id][0]] + 4
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}4 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Since when you can afford this???{c.END}")
                                                    house_choice_check = False

                                                if house_choice not in ('0', '1', '2', '3', '4'):
                                                    print(f"{c.RED2}It needs to be a number between 0 and 4{c.END}")
                                                else:
                                                    players_data[player_id][2].append(house_pay)
                                                    player_money_left = players_data[player_id][1][0] - house_pay
                                                    players_data[player_id][1][0] = player_money_left

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}£{players_data[player_id][1][0]}{c.END} left")

                                        elif property_id > 10 or property_id < 20:
                                            while house_choice_check:
                                                house_choice = str(input(f"\n{c.GREEN}How many do you want to aquire? (max. 4){c.END} "))

                                                if house_choice == '0':
                                                    print(f"\n{c.VIOLET}Seriously...You chose yes and did not buy any houses. (Dissapointed){c.END}")

                                                    house_choice_check = False

                                                elif house_choice == '1':
                                                    house_pay = pd.HOUSE_PRICE_2

                                                    houses = house_dict[pd.property_list[property_id][0]] + 1
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}1 house aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Look at you, starting slowly to buy stuff. Well done!{c.END}")

                                                    house_choice_check = False

                                                elif house_choice == '2':
                                                    house_pay = pd.HOUSE_PRICE_2 * 2

                                                    houses = house_dict[pd.property_list[property_id][0]] + 2
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"{c.BLUE}System message{c.END} - {c.RED}2 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Have added 2 houses to your land. Well done! (p.s. YOUNG BUSINESS PERSON){c.END}")

                                                    house_choice_check = False

                                                elif house_choice == '3':
                                                    house_pay = pd.HOUSE_PRICE_2 * 3

                                                    houses = house_dict[pd.property_list[property_id][0]] + 3
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}3 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Wow impressive, 3 houses in one payment. Btw, I have added them to your land.{c.END}")

                                                    house_choice_check = False

                                                elif house_choice == '4':
                                                    house_pay = pd.HOUSE_PRICE_2 * 4

                                                    houses = house_dict[pd.property_list[property_id][0]] + 4
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}4 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Since when you can afford this???{c.END}")
                                                    house_choice_check = False

                                                if house_choice not in ('0', '1', '2', '3', '4'):
                                                    print(f"{c.RED2}It needs to be a number between 0 and 4{c.END}")
                                                else:
                                                    players_data[player_id][2].append(house_pay)
                                                    player_money_left = players_data[player_id][1][0] - house_pay
                                                    players_data[player_id][1][0] = player_money_left

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}£{players_data[player_id][1][0]}{c.END} left")

                                        elif property_id > 20 or property_id < 30:
                                            while house_choice_check:
                                                house_choice = str(input(f"\n{c.GREEN}How many do you want to aquire? (max. 4){c.END} "))

                                                if house_choice == '0':
                                                    print(f"\n{c.VIOLET}Seriously...You chose yes and did not buy any houses. (Dissapointed){c.END}")

                                                    house_choice_check = False

                                                elif house_choice == '1':
                                                    house_pay = pd.HOUSE_PRICE_3

                                                    houses = house_dict[pd.property_list[property_id][0]] + 1
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}1 house aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Look at you, starting slowly to buy stuff. Well done!{c.END}")

                                                    house_choice_check = False

                                                elif house_choice == '2':
                                                    house_pay = pd.HOUSE_PRICE_3 * 2

                                                    houses = house_dict[pd.property_list[property_id][0]] + 2
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"{c.BLUE}System message{c.END} - {c.RED}2 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Have added 2 houses to your land. Well done! (p.s. YOUNG BUSINESS PERSON){c.END}")

                                                    house_choice_check = False

                                                elif house_choice == '3':
                                                    house_pay = pd.HOUSE_PRICE_3 * 3

                                                    houses = house_dict[pd.property_list[property_id][0]] + 3
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}3 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Wow impressive, 3 houses in one payment. Btw, I have added them to your land.{c.END}")

                                                    house_choice_check = False

                                                elif house_choice == '4':
                                                    house_pay = pd.HOUSE_PRICE_3 * 4

                                                    houses = house_dict[pd.property_list[property_id][0]] + 4
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}4 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Since when you can afford this???{c.END}")
                                                    house_choice_check = False

                                                if house_choice not in ('0', '1', '2', '3', '4'):
                                                    print(f"{c.RED2}It needs to be a number between 0 and 4{c.END}")
                                                else:
                                                    players_data[player_id][2].append(house_pay)
                                                    player_money_left = players_data[player_id][1][0] - house_pay
                                                    players_data[player_id][1][0] = player_money_left

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}£{players_data[player_id][1][0]}{c.END} left")

                                        else:
                                            while house_choice_check:
                                                house_choice = str(input(f"\n{c.GREEN}How many do you want to aquire? (max. 4){c.END} "))

                                                if house_choice == '0':
                                                    print(f"\n{c.VIOLET}Seriously...You chose yes and did not buy any houses. (Dissapointed){c.END}")

                                                    house_choice_check = False

                                                elif house_choice == '1':
                                                    house_pay = pd.HOUSE_PRICE_4

                                                    houses = house_dict[pd.property_list[property_id][0]] + 1
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}1 house aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Look at you, starting slowly to buy stuff. Well done!{c.END}")

                                                    house_choice_check = False

                                                elif house_choice == '2':
                                                    house_pay = pd.HOUSE_PRICE_4 * 2

                                                    houses = house_dict[pd.property_list[property_id][0]] + 2
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"{c.BLUE}System message{c.END} - {c.RED}2 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Have added 2 houses to your land. Well done! (p.s. YOUNG BUSINESS PERSON){c.END}")

                                                    house_choice_check = False

                                                elif house_choice == '3':
                                                    house_pay = pd.HOUSE_PRICE_4 * 3

                                                    houses = house_dict[pd.property_list[property_id][0]] + 3
                                                    house_dict.update({pd.property_list[property_id][0]:houses})
  
                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}3 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Wow impressive, 3 houses in one payment. Btw, I have added them to your land.{c.END}")

                                                    house_choice_check = False

                                                elif house_choice == '4':
                                                    house_pay = pd.HOUSE_PRICE_4 * 4

                                                    houses = house_dict[pd.property_list[property_id][0]] + 4
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}4 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Since when you can afford this???{c.END}")
                                                    house_choice_check = False

                                                if house_choice not in ('0', '1', '2', '3', '4'):
                                                    print(f"{c.RED2}It needs to be a number between 0 and 4{c.END}")
                                                else:
                                                    players_data[player_id][2].append(house_pay)
                                                    player_money_left = players_data[player_id][1][0] - house_pay
                                                    players_data[player_id][1][0] = player_money_left

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}£{players_data[player_id][1][0]}{c.END} left")

                                    elif house_buy_choice in ('n', 'no'):
                                        print(f"\n{c.VIOLET}Woo, not buying any houses, someone is not going to get paid! (WooHoo){c.END}")
                                        break
                                    else:
                                        print(f"\n{c.VIOLET}I will assume that you don't want any houses at the moment...{c.END}")
                                        break

                                elif house_dict[pd.property_list[property_id][0]] == 1:
                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}You have {house_dict[pd.property_list[property_id][0]]} house{c.END}")

                                    house_buy_choice = str(input(f"\n{c.GREEN}Do you want to buy any more houses?{c.END} (y/n) ")).lower()

                                    if house_buy_choice in ('y', 'yes'):
                                        house_choice_check = True

                                        if property_id > 0 or property_id < 10:
                                            while house_choice_check:
                                                house_choice = str(input(f"\n{c.GREEN}How many do you want to aquire? (max. 3){c.END} "))

                                                if house_choice == '0':
                                                    print(f"\n{c.VIOLET}Seriously...You chose yes and did not buy any houses. (Dissapointed){c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '1':
                                                    house_pay = pd.HOUSE_PRICE_1

                                                    houses = house_dict[pd.property_list[property_id][0]] + 1
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}1 house aquired{c.END}")
                                                    print(f"\n{c.VIOLET}I like it, one real estate added on this land! KEEEEEEP IT UP...{c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '2':
                                                    house_pay = pd.HOUSE_PRICE_1 * 2

                                                    houses = house_dict[pd.property_list[property_id][0]] + 2
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}2 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Have added 2 more houses to your land. Well done! (pov: YOUNG BUSINESS PERSON){c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '3':
                                                    house_pay = pd.HOUSE_PRICE_1 * 3

                                                    houses = house_dict[pd.property_list[property_id][0]] + 3
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}3 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Wow impressive, 3 houses in one payment. Btw, I have added them to your land.{c.END}")

                                                    house_choice_check = False

                                                if house_choice not in ('0', '1', '2', '3'):
                                                    print(f"{c.RED2}It needs to be a number between 0 and 3{c.END}")
                                                else:
                                                    players_data[player_id][2].append(house_pay)
                                                    player_money_left = players_data[player_id][1][0] - house_pay
                                                    players_data[player_id][1][0] = player_money_left

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}£{players_data[player_id][1][0]}{c.END} left")

                                        elif property_id > 10 or property_id < 20:
                                            while house_choice_check:
                                                house_choice = str(input(f"\n{c.GREEN}How many do you want to aquire? (max. 3){c.END} "))

                                                if house_choice == '0':
                                                    print(f"\n{c.VIOLET}Seriously...You chose yes and did not buy any houses. (Dissapointed){c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '1':
                                                    house_pay = pd.HOUSE_PRICE_2

                                                    houses = house_dict[pd.property_list[property_id][0]] + 1
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}1 house aquired{c.END}")
                                                    print(f"\n{c.VIOLET}I like it, one real estate added on this land! KEEEEEEP IT UP...{c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '2':
                                                    house_pay = pd.HOUSE_PRICE_2 * 2

                                                    houses = house_dict[pd.property_list[property_id][0]] + 2
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}2 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Have added 2 more houses to your land. Well done! (pov: YOUNG BUSINESS PERSON){c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '3':
                                                    house_pay = pd.HOUSE_PRICE_2 * 3

                                                    houses = house_dict[pd.property_list[property_id][0]] + 3
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}3 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Wow impressive, 3 houses in one payment. Btw, I have added them to your land.{c.END}")

                                                    house_choice_check = False

                                                if house_choice not in ('0', '1', '2', '3'):
                                                    print(f"{c.RED2}It needs to be a number between 0 and 3{c.END}")
                                                else:
                                                    players_data[player_id][2].append(house_pay)
                                                    player_money_left = players_data[player_id][1][0] - house_pay
                                                    players_data[player_id][1][0] = player_money_left

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}£{players_data[player_id][1][0]}{c.END} left")

                                        elif property_id > 20 or property_id < 30:
                                            while house_choice_check:
                                                house_choice = str(input(f"\n{c.GREEN}How many do you want to aquire? (max. 3){c.END} "))

                                                if house_choice == '0':
                                                    print(f"\n{c.VIOLET}Seriously...You chose yes and did not buy any houses. (Dissapointed){c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '1':
                                                    house_pay = pd.HOUSE_PRICE_3

                                                    houses = house_dict[pd.property_list[property_id][0]] + 1
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}1 house aquired{c.END}")
                                                    print(f"\n{c.VIOLET}I like it, one real estate added on this land! KEEEEEEP IT UP...{c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '2':
                                                    house_pay = pd.HOUSE_PRICE_3 * 2

                                                    houses = house_dict[pd.property_list[property_id][0]] + 2
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}2 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Have added 2 more houses to your land. Well done! (pov: YOUNG BUSINESS PERSON){c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '3':
                                                    house_pay = pd.HOUSE_PRICE_3 * 3

                                                    houses = house_dict[pd.property_list[property_id][0]] + 3
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}3 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Wow impressive, 3 houses in one payment. Btw, I have added them to your land.{c.END}")

                                                    house_choice_check = False

                                                if house_choice not in ('0', '1', '2', '3'):
                                                    print(f"{c.RED2}It needs to be a number between 0 and 3{c.END}")
                                                else:
                                                    players_data[player_id][2].append(house_pay)
                                                    player_money_left = players_data[player_id][1][0] - house_pay
                                                    players_data[player_id][1][0] = player_money_left

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}£{players_data[player_id][1][0]}{c.END} left")

                                        else:
                                            while house_choice_check:
                                                house_choice = str(input(f"\n{c.GREEN}How many do you want to aquire? (max. 3){c.END} "))

                                                if house_choice == '0':
                                                    print(f"\n{c.VIOLET}Seriously...You chose yes and did not buy any houses. (Dissapointed){c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '1':
                                                    house_pay = pd.HOUSE_PRICE_2

                                                    houses = house_dict[pd.property_list[property_id][0]] + 1
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}1 house aquired{c.END}")
                                                    print(f"\n{c.VIOLET}I like it, one real estate added on this land! KEEEEEEP IT UP...{c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '2':
                                                    house_pay = pd.HOUSE_PRICE_2 * 2

                                                    houses = house_dict[pd.property_list[property_id][0]] + 2
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}2 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Have added 2 more houses to your land. Well done! (pov: YOUNG BUSINESS PERSON){c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '3':
                                                    house_pay = pd.HOUSE_PRICE_2 * 3

                                                    houses = house_dict[pd.property_list[property_id][0]] + 3
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}3 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Wow impressive, 3 houses in one payment. Btw, I have added them to your land.{c.END}")

                                                    house_choice_check = False
                                                
                                                if house_choice not in ('0', '1', '2', '3'):
                                                    print(f"{c.RED2}It needs to be a number between 0 and 3{c.END}")
                                                else:
                                                    players_data[player_id][2].append(house_pay)
                                                    player_money_left = players_data[player_id][1][0] - house_pay
                                                    players_data[player_id][1][0] = player_money_left

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}£{players_data[player_id][1][0]}{c.END} left")

                                    elif house_buy_choice in ('n', 'no'):
                                        print(f"\n{c.VIOLET}Woo, not buying any houses, someone is not going to get paid! (WooHoo){c.END}")
                                        break
                                    else:
                                        print(f"\n{c.VIOLET}I will assume that you don't want any houses at the moment...{c.END}")
                                        break

                                elif house_dict[pd.property_list[property_id][0]] == 2:
                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}You have {house_dict[pd.property_list[property_id][0]]} houses{c.END}")

                                    house_buy_choice = str(input(f"\n{c.GREEN}Do you want to buy any more houses?{c.END} (y/n) ")).lower()

                                    if house_buy_choice in ('y', 'yes'):
                                        house_choice_check = True

                                        if property_id > 0 or property_id < 10:
                                            while house_choice_check:
                                                house_choice = str(input(f"\n{c.GREEN}How many do you want to aquire? (max. 2){c.END} "))

                                                if house_choice == '0':
                                                    print(f"\n{c.VIOLET}Seriously...You chose yes and did not buy any houses. (Dissapointed){c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '1':
                                                    house_pay = pd.HOUSE_PRICE_1

                                                    houses = house_dict[pd.property_list[property_id][0]] + 1
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}1 house aquired{c.END}")
                                                    print(f"\n{c.VIOLET}I like it, one real estate added on this land! KEEEEEEP IT UP...{c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '2':
                                                    house_pay = pd.HOUSE_PRICE_1 * 2

                                                    houses = house_dict[pd.property_list[property_id][0]] + 2
                                                    house_dict.update({pd.property_list[property_id][0]:houses})
                                                    
                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}2 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Have added 2 more houses to your land. Well done! (pov: YOUNG BUSINESS PERSON){c.END}")

                                                    house_choice_check = False

                                                if house_choice not in ('0', '1', '2'):
                                                    print(f"{c.RED2}It needs to be a number between 0 and 2{c.END}")
                                                else:
                                                    players_data[player_id][2].append(house_pay)
                                                    player_money_left = players_data[player_id][1][0] - house_pay
                                                    players_data[player_id][1][0] = player_money_left

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}£{players_data[player_id][1][0]}{c.END} left")
                                        
                                        elif property_id > 10 or property_id < 20:
                                            while house_choice_check:
                                                house_choice = str(input(f"\n{c.GREEN}How many do you want to aquire? (max. 2){c.END} "))

                                                if house_choice == '0':
                                                    print(f"\n{c.VIOLET}Seriously...You chose yes and did not buy any houses. (Dissapointed){c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '1':
                                                    house_pay = pd.HOUSE_PRICE_2

                                                    houses = house_dict[pd.property_list[property_id][0]] + 1
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}1 house aquired{c.END}")
                                                    print(f"\n{c.VIOLET}I like it, one real estate added on this land! KEEEEEEP IT UP...{c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '2':
                                                    house_pay = pd.HOUSE_PRICE_2 * 2

                                                    houses = house_dict[pd.property_list[property_id][0]] + 2
                                                    house_dict.update({pd.property_list[property_id][0]:houses})
                                                    
                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}2 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Have added 2 more houses to your land. Well done! (pov: YOUNG BUSINESS PERSON){c.END}")

                                                    house_choice_check = False

                                                if house_choice not in ('0', '1', '2'):
                                                    print(f"{c.RED2}It needs to be a number between 0 and 2{c.END}")
                                                else:
                                                    players_data[player_id][2].append(house_pay)
                                                    player_money_left = players_data[player_id][1][0] - house_pay
                                                    players_data[player_id][1][0] = player_money_left

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}£{players_data[player_id][1][0]}{c.END} left")

                                        elif property_id > 20 or property_id < 30:
                                            while house_choice_check:
                                                house_choice = str(input(f"\n{c.GREEN}How many do you want to aquire? (max. 2){c.END} "))

                                                if house_choice == '0':
                                                    print(f"\n{c.VIOLET}Seriously...You chose yes and did not buy any houses. (Dissapointed){c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '1':
                                                    house_pay = pd.HOUSE_PRICE_3

                                                    houses = house_dict[pd.property_list[property_id][0]] + 1
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}1 house aquired{c.END}")
                                                    print(f"\n{c.VIOLET}I like it, one real estate added on this land! KEEEEEEP IT UP...{c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '2':
                                                    house_pay = pd.HOUSE_PRICE_3 * 2

                                                    houses = house_dict[pd.property_list[property_id][0]] + 2
                                                    house_dict.update({pd.property_list[property_id][0]:houses})
                                                    
                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}2 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Have added 2 more houses to your land. Well done! (pov: YOUNG BUSINESS PERSON){c.END}")

                                                    house_choice_check = False

                                                if house_choice not in ('0', '1', '2'):
                                                    print(f"{c.RED2}It needs to be a number between 0 and 2{c.END}")
                                                else:
                                                    players_data[player_id][2].append(house_pay)
                                                    player_money_left = players_data[player_id][1][0] - house_pay
                                                    players_data[player_id][1][0] = player_money_left

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}£{players_data[player_id][1][0]}{c.END} left")

                                        else:
                                            while house_choice_check:
                                                house_choice = str(input(f"\n{c.GREEN}How many do you want to aquire? (max. 2){c.END} "))

                                                if house_choice == '0':
                                                    print(f"\n{c.VIOLET}Seriously...You chose yes and did not buy any houses. (Dissapointed){c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '1':
                                                    house_pay = pd.HOUSE_PRICE_4

                                                    houses = house_dict[pd.property_list[property_id][0]] + 1
                                                    house_dict.update({pd.property_list[property_id][0]:houses})

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}1 house aquired{c.END}")
                                                    print(f"\n{c.VIOLET}I like it, one real estate added on this land! KEEEEEEP IT UP...{c.END}")

                                                    house_choice_check = False
                                                elif house_choice == '2':
                                                    house_pay = pd.HOUSE_PRICE_4 * 2

                                                    houses = house_dict[pd.property_list[property_id][0]] + 2
                                                    house_dict.update({pd.property_list[property_id][0]:houses})
                                                    
                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}2 houses aquired{c.END}")
                                                    print(f"\n{c.VIOLET}Have added 2 more houses to your land. Well done! (pov: YOUNG BUSINESS PERSON){c.END}")

                                                    house_choice_check = False

                                                if house_choice not in ('0', '1', '2'):
                                                    print(f"{c.RED2}It needs to be a number between 0 and 2{c.END}")
                                                else:
                                                    players_data[player_id][2].append(house_pay)
                                                    player_money_left = players_data[player_id][1][0] - house_pay
                                                    players_data[player_id][1][0] = player_money_left

                                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}£{players_data[player_id][1][0]}{c.END} left")

                                    elif house_buy_choice in ('n', 'no'):
                                        print(f"\n{c.VIOLET}Woo, not buying any houses, someone is not going to get paid! (WooHoo){c.END}")
                                        break
                                    else:
                                        print(f"\n{c.VIOLET}I will assume that you don't want any houses at the moment...{c.END}")
                                        break
                                else:
                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}You are now eligible for a Hotel{c.END}")
                                break

                            print(f"\n{c.BLUE}System message{c.END} - {property_dict[pd.property_list[property_id][0]]}{c.END} {c.RED}owns this property!{c.END}")

                            ###
                            # If the property is any of the stations, then do the following
                            ###
                            if pd.property_list[property_id][0] in ("King's Cross Station", "Marylebone Station", "Fenchurch St Station", "Liverpool Street Station"):
                                ###
                                # Check how many stations does the player that owns the property has
                                ###
                                ###
                                # That's for only if 4 stations are owned
                                ###
                                if (set(["King's Cross Station", "Marylebone Station", "Fenchurch St Station", "Liverpool Street Station"]).issubset(set(property_dict))):
                                    print(f"\n{c.BLUE}You now have to pay{c.END} £{pd.STATIONS_RENT_4}{c.BLUE} for rent!{c.END}")
                                    rent_price = pd.STATIONS_RENT_4

                                ###
                                # That's for only if 3 stations are owned
                                ###
                                elif (set(["King's Cross Station", "Marylebone Station", "Fenchurch St Station"]).issubset(set(property_dict)) or
                                    set(["King's Cross Station", "Marylebone Station", "Liverpool Street Station"]).issubset(set(property_dict)) or
                                    set(["King's Cross Station", "Fenchurch St Station", "Liverpool Street Station"]).issubset(set(property_dict)) or
                                    set(["Marylebone Station", "Fenchurch St Station", "Liverpool Street Station"]).issubset(set(property_dict))):
                                    print(f"\n{c.BLUE}You now have to pay{c.END} £{pd.STATIONS_RENT_3}{c.BLUE} for rent!{c.END}")
                                    rent_price = pd.STATIONS_RENT_3

                                ###
                                # That's for only if 2 stations are owned
                                ###
                                elif (set(["King's Cross Station", "Marylebone Station"]).issubset(set(property_dict)) or
                                    set(["King's Cross Station", "Fenchurch St Station"]).issubset(set(property_dict)) or
                                    set(["King's Cross Station", "Liverpool Street Station"]).issubset(set(property_dict)) or
                                    set(["Marylebone Station", "Fenchurch St Station"]).issubset(set(property_dict)) or
                                    set(["Marylebone Station", "Liverpool Street Station"]).issubset(set(property_dict)) or
                                    set(["Fenchurch St Station", "Liverpool Street Station"]).issubset(set(property_dict))):
                                    print(f"\n{c.BLUE}You now have to pay{c.END} £{pd.STATIONS_RENT_2}{c.BLUE} for rent!{c.END}")
                                    rent_price = pd.STATIONS_RENT_2
                                else:
                                    ###
                                    # That's for only if 1 station is owned
                                    ###
                                    print(f"\n{c.BLUE}You now have to pay{c.END} £{pd.STATIONS_RENT_1}{c.BLUE} for rent!{c.END}")
                                    rent_price = pd.STATIONS_RENT_1
                            else:
                                ###
                                # If the property is not a station then do the following
                                ###
                                if house_dict[pd.property_list[property_id][0]] == 0:
                                    print(f"\n{c.BLUE}You now have to pay{c.END} £{pd.property_list[property_id][2]}{c.BLUE} for rent!{c.END}")
                                    rent_price = pd.property_list[property_id][2]
                                elif house_dict[pd.property_list[property_id][0]] == 1:
                                    print(f"\n{c.BLUE}You now have to pay{c.END} £{pd.property_list[property_id][3]}{c.BLUE} for rent!{c.END}")
                                    rent_price = pd.property_list[property_id][3]
                                elif house_dict[pd.property_list[property_id][0]] == 2:
                                    print(f"\n{c.BLUE}You now have to pay{c.END} £{pd.property_list[property_id][4]}{c.BLUE} for rent!{c.END}")
                                    rent_price = pd.property_list[property_id][4]
                                elif house_dict[pd.property_list[property_id][0]] == 3:
                                    print(f"\n{c.BLUE}You now have to pay{c.END} £{pd.property_list[property_id][5]}{c.BLUE} for rent!{c.END}")
                                    rent_price = pd.property_list[property_id][5]
                                elif house_dict[pd.property_list[property_id][0]] == 4:
                                    print(f"\n{c.BLUE}You now have to pay{c.END} £{pd.property_list[property_id][6]}{c.BLUE} for rent!{c.END}")
                                    rent_price = pd.property_list[property_id][6]
                                

                            ###
                            # Get confirmation from the player to pay for rent
                            ###
                            agreement_choice_check = True
                            while agreement_choice_check:
                                agreement_choice = str(input(f"\n{c.GREEN}Pay now!{c.END} (y/n) ")).lower()

                                if agreement_choice in ('y', 'yes'):
                                    ###
                                    # Add the price of the rent to the gained money list of the player that owns the property
                                    # Calculate the money now
                                    # Set the new money value to the second list of the player that owns the property
                                    ###
                                    for player_list in players_data:
                                        if player_list[0][0] == property_dict[pd.property_list[property_id][0]]:
                                            player_list[3].append(rent_price)
                                            player_list_money_add = player_list[1][0] + rent_price
                                            player_list[1][0] = player_list_money_add

                                    ###
                                    # Add the price of the rent to the spendings money list of the player that is on the property
                                    # Calculate the money now
                                    ###
                                    players_data[player_id][2].append(rent_price)
                                    player_list_money_take = players_data[player_id][1][0] - rent_price

                                    ###
                                    # Check if the player has enough money
                                    # If not then end the game
                                    # Otherwise set the new money value to the second list of the player that is on the property
                                    ###
                                    if player_list_money_take <= 0:
                                        print(f"{player} {c.BLUE}has no money left!{c.END}\n")
                                        print(f"{c.YELLOW}Game ending...{c.END}\n")
                                        print("Many thanks for playing!")
                                        end_game = True
                                        break

                                    players_data[player_id][1][0] = player_list_money_take
                                    print(f"{c.BLUE}System message{c.END} - {c.RED}£{rent_price} taken from your balance.{c.END}")
                                    print(f"\n{c.BLUE}System message{c.END} - {c.RED}£{rent_price} added to{c.END} {property_dict[pd.property_list[property_id][0]]}{c.RED}'s balance.{c.END}")
                                    
                                    agreement_choice_check = False
                                else:
                                    print(f"{c.BLUE}System message{c.END} - {c.RED2}You can't pay at another time. It needs to be now.{c.END}")
                        else:
                            ###
                            # If the property is not in any player's inventory, then prompt the player if it wants to buy it
                            ###
                            property_choice_check = True
                            while property_choice_check:
                                property_choice = str(input(f"{c.GREEN}Do you want to buy this property?{c.END} (y/n) ")).lower()

                                if property_choice in ('y', 'yes'):
                                    
                                    #######
                                    # Check if the player has less money than the property price
                                    #######
                                    if players_data[player_id][1][0] < pd.property_list[property_id][1]:
                                        print(f"\n{c.BLUE}System message{c.END} - {c.RED}You don't have enough money to aquire this property!{c.END}")
                                        break

                                    ###
                                    # Add the price of the property to the 3rd list in the player's list
                                    # Add name of the property to the 5th list in the player's list
                                    # Calculate the amount of money left after the player bought the property
                                    # Set the new money value to the second list in the player's list
                                    ###
                                    players_data[player_id][2].append(pd.property_list[property_id][1])
                                    players_data[player_id][4].append(pd.property_list[property_id][0])

                                    property_dict.update({pd.property_list[property_id][0]:player})

                                    if pd.property_list[property_id][0] not in ("King's Cross Station", "Marylebone Station", "Fenchurch St Station", "Liverpool Street Station"):
                                        house_dict.update({pd.property_list[property_id][0]:0})

                                    player_money_left = players_data[player_id][1][0] - pd.property_list[property_id][1]

                                    players_data[player_id][1][0] = player_money_left

                                    print(f"{c.BLUE}Property aquired! ({c.END}{pd.property_list[property_id][0]} {c.BLUE}added to your inventory!){c.END}\n")
                                    print(f"{c.BLUE}System message{c.END} - {c.RED}£{pd.property_list[property_id][1]} taken from your balance.{c.END}")

                                    inventory_choice_check = True
                                    while inventory_choice_check:
                                        inventory_choice = str(input(f"{c.GREEN}Do you want to see your inventory?{c.END} (y/n) ")).lower()

                                        if inventory_choice in ('y', 'yes'):
                                            print(f"{c.BLUE}Your inventory:{c.END}")

                                            ###
                                            # Display player properties
                                            ###
                                            for property_card in players_data[player_id][4]:
                                                print(property_card)

                                            print(f"\n{c.BLUE}Money left:{c.END} £{player_money_left}")

                                            inventory_choice_check = False
                                        elif inventory_choice in ('n', 'no'):
                                            break
                                        else:
                                            print(f"{c.RED}Enter y or n!{c.END}")

                                    property_choice_check = False
                                elif property_choice in ('n', 'no'):
                                    break
                                else:
                                    print(f"{c.RED}Enter y or n!{c.END}")

                    dice_choice_check = False
                elif dice_choice in ('n', 'no'):
                    print(f"{c.RED}Can't skip a turn right now! Choose to roll the dice!{c.END}")
                else:
                    print(f"{c.RED}Enter y or n!{c.END}")
        #print(dice_list)
        # print(players_data)
        # print(property_dict)
        # print(house_dict)

    results_choice = str(input(f"\n{c.GREEN}Show game results?{c.END} (y/n) ")).lower()

    if results_choice in ('y', 'yes'):
        print(f"{c.YELLOW}Displaying results...{c.END}")
        for player_info in players_data:
            print(f"\n{c.BEIGE}Player{c.END} {player_info[0][0]}{c.BEIGE}:{c.END}")

            player_money = player_info[1][0]
            print(f"\t{c.BEIGE}Money left:{c.END} £{player_money}")

            player_spendings = sum(player_info[2])
            print(f"\t{c.BEIGE}Total spendings:{c.END} {player_spendings}")

            player_gains = sum(player_info[3])
            print(f"\t{c.BEIGE}Total gains:{c.END} {player_gains}")

            print(f"\t{c.BEIGE}Properties:{c.END}")
            for player_properties in player_info[4]:
                print(f"\t{player_properties}")
    elif results_choice in ('n', 'no'):
        print("Thanks again for playing!")

        #print(dice_list)
        #print(players_data)
        #print(property_dict)



def main():
    """
        CREATE THE GAME
    """
    set_player_nickname()
    choose_player()
    print(f"\n{c.YELLOW}Picking the starting player...{c.END}")
    print(f"{c.BLUE}Player{c.END} {nickname_list[0]} {c.BLUE}starts first!{c.END}")

    start_game()



if __name__ == "__main__":
    main()
