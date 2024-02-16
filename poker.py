test_hands = ["4S 2H 6S 2D JH", "2S 4H 6C 4D JD"]

def best_hands(hands):

    card_order = {
        "2":14,
        "3":13,
        "4":12,
        "5":11,
        "6":10,
        "7":9,
        "8":8,
        "9":7,
        "10":6,
        "J": 5,
        "Q": 4,
        "K": 3,
        "A": 2
    }

    def get_high_card(cards):
        high_card = cards[0]

        if len(cards) > 1:
            for card in cards[1:]:
                if card_order[card[0]] < card_order[high_card[0]]:
                    high_card = card
        return high_card

    def get_player_score(player_hand):
        cards_split = player_hand.split()
        cards_tupled = []
        for card in cards_split:
            cards_tupled.append((''.join(card[:-1]),card[-1]))
        cards = sorted(cards_tupled, key=lambda x: card_order[x[0]])

        score = {
            'handIndex': 0, 
            'kind': None,
            'kickers': [],
            'straight': False,
            'flush': False,
        }

        # be like a human
        # take the highest value card
        # evaluate in order of hand strength index
        
        # Check for five of a kind
        first_value = cards[0][0]
        for card in cards[1:]:
            if card[0] != first_value:
                break
        else:
            score["handIndex"] = 1
            score["kind"] = card[0]
            return score

        # Check for flush
        first_suit = cards[0][1]
        for card in cards[1:]:
            if card[1] != first_suit:
                break
        else:
            score["handIndex"] = 5
            score["flush"] = True
            score["kind"] = get_high_card(cards)[0]
            # no return because need check for straight flush

        # Check for straight
        straight_values = [card_order[card[0]] for card in cards]
        # Ace low for five high straight
        if (2 in straight_values) and all(item in straight_values for item in [11,12,13,14]):
            straight_values.remove(2)
            straight_values.append(15)

        if max(straight_values) - min(straight_values) == 4 and len(set(straight_values)) == 5:
            score["handIndex"] = 6
            score["straight"] = True
            if (15 in straight_values):
                score["kind"] = '5'
            else:
                score["kind"] = get_high_card(cards)[0]
            # no return because need check for straight flush

        # Check for straight flush
        if score["flush"] and score["straight"]:
            score["handIndex"] = 2
            # score["kind"] = get_high_card(cards)[0]
            return score
        elif score["flush"]:
            score["handIndex"] = 5
            # score["kind"] = get_high_card(cards)[0]
            return score
        elif score["straight"]:
            score["handIndex"] = 6
            # score["kind"] = get_high_card(cards)[0]
            return score
        
        # Handle not five of kind, straight, flush, and straight flush
        if score["handIndex"] not in [1, 2, 5, 6]:
            # Make list of just the values, not the suits
            values = [card[0] for card in cards]
            value_instances = {}
            for value in values:
                value_instances[value] = values.count(value)

            highest_count = max(value_instances, key=value_instances.get)
            print(values)
            print(f"Count of HC = {values.count(highest_count)}")
                
            # Check for four of a kind
            if values.count(highest_count) == 4:
                not_quads = [v for v in values if v != value]
                score["handIndex"] = 3
                score["kind"] = highest_count
                score["kickers"] = not_quads
                return score
            # Check for three of a kind
            if values.count(highest_count) == 3:
                
                not_trips = [v for v in values if v != value]
                score["kind"] = highest_count
                # Check for full house
                if not_trips[0] == not_trips[1]:
                    score["handIndex"] = 4
                else:
                    score["handIndex"] = 7
                score["kickers"] = sorted(not_trips, key=lambda x: card_order[x[0]])
                return score
            # Check for pairs
            if values.count(highest_count) == 2:
                print(f"HC = {highest_count}")
                print(f"Value? {value}")
                score["kind"] = highest_count
                # Check for two pair
                not_first_pair = [v for v in values if v != value]
                if (len(set(values)) == 3):
                    for v2 in not_first_pair:
                        if not_first_pair.count(v2) == 2:
                            score["handIndex"] = 8
                            score["kickers"] = sorted(not_first_pair, key=lambda x: card_order[x[0]])
                            return score
                # Handle one pair
                else:
                    score["handIndex"] = 9
                    score["kickers"] = sorted(not_first_pair, key=lambda x: card_order[x[0]])
                    return score
            # Else high card
            high_card = get_high_card(cards)[0]
            score["kind"] = high_card
            not_high_card = [v for v in values if v != high_card]
            score["kickers"] = not_high_card
            score["handIndex"] = 10
            return score


    # format player score dictionary and create the player scores list of dictionaries
    player_scores = []
    for player_hand in hands:
        # TODO: Ideally you would check for empty hands or hands without five cards
        player_score = {
            'cards': player_hand
        }
        # adds other key info to each player's score dictionary
        player_score.update(get_player_score(player_hand))
        abv_player_score = {
            key: value for key, value in player_score.items() if key not in ['straight','flush']
            }
        player_scores.append(abv_player_score)

    for score in player_scores:
        print(score)

    print("")
    
    # SECTION: Score Reporting
    def break_tie(list_of_scores):
        kicker_count = len(list_of_scores[0]["kickers"])

        def kicker_cycle(kicker_int):
            if kicker_int > 0:
                kicker_dict = {}
                for number in range(kicker_int):
                    kicker_dict[number] = []

                # populate the kicker_dict
                kicker_index = 0
                while kicker_index < kicker_int:
                    for score in list_of_scores:
                        kicker_dict[kicker_index].append(score["kickers"][kicker_index])
                    kicker_index += 1
                

                for key in kicker_dict:
                    kicker_collection = kicker_dict[key]
                    ordered_kicker_collection = []
                    for kicker in kicker_collection:
                        ordered_kicker_collection.append(card_order[kicker])

                    kicker_mask = [index for index, value in enumerate(ordered_kicker_collection) if value > min(ordered_kicker_collection)]

                    for idx in kicker_mask:
                        list_of_scores[idx] = {}
                    non_empty_count = sum(1 for dictionary in list_of_scores if dictionary)
                    if non_empty_count == 1:
                        winners = []
                        for score in list_of_scores:
                            if not score == {}:
                                winners.append(score["cards"])
                        return winners

            winners = []
            for score in list_of_scores:
                if not score == {}:
                    winners.append(score["cards"])
            return winners
        
        return kicker_cycle(kicker_count)
    
    # Get score obj or objs of the hands with the best score
    # First, consolidate for hands that have the best hand_index
    best_hand_index = [
        score for score in player_scores if score["handIndex"] == min(score["handIndex"] for score in player_scores)
        ]
    # Check if there is one hand with the best hand_index
    if len(best_hand_index) == 1:
        return [best_hand_index[0]['cards']]

    # Then, if there are multiple hands with the best hand_index, check to see what kind (aka top card)
    best_kind = [
        score for score in best_hand_index if card_order[score["kind"]] == min(card_order[score["kind"]] for score in best_hand_index)
    ]
    
    # After checking kind, return winner if only one remains
    if len(best_kind) == 1:
        return [best_kind[0]['cards']]
    
    # If more than one hands remains after checking kind, its now time to check kickers
    # May result in tie or one winner - returns list regardless
    if len(best_kind) > 1:
        return break_tie(best_kind)


print(best_hands(test_hands))