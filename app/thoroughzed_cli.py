from app.get_intrinsic_value import get_intrinsic_value


def run_cli():
    id = input("> Please enter the Horse/NFT ID for the horse you'd like to evaluate or type 'q' to quit. ")
    if id.lower() == "q":
        exit()
    while not id.isdigit():
        print("> *** Not a valid ID! ***")
        id = input("> Please enter the Horse/NFT ID for the horse you'd like to evaluate or type 'q' to quit. ")
        if id.lower() == "q":
            exit()
    choice = input("> Would you like to find the (r)elative value or (i)ntrinsic value? Or type 'q' to quit. ")
    if choice.lower() == "q":
        exit()
    while choice != "r" and choice != "i":
        print("> *** Not a valid input! ***")
        choice = input("> Would you like to find the (r)elative value or (i)ntrinsic value? Or type 'q' to quit. ")
        if id.lower() == "q":
            exit()
    if choice == "i":
        cost = input("> Enter the requested price of the horse in USD. Or type 'q' to quit. ")
        if cost.lower() == "q":
            exit()
        while not cost.isdigit():
            print("> *** Not a valid cost! ***")
            cost = input("> Enter the requested price of the horse in USD. Or type 'q' to quit. ")
            if cost.lower() == "q":
                exit()
        results = get_intrinsic_value(int(id), int(cost))
        print(f"> Potential Net Earnings Per Race: ${results[0]}")
        print(f"> Potential 3-Month Yield: {results[1]}%")
        print(f"> Races Needed to Cover Cost of Horse: {results[2]}")


if __name__ == "__main__":
    run_cli()
