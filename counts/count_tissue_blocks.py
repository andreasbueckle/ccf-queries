from utils import get_data

def main():
    """A function to count the number of tissue blocks in HuBMAP
    """
    API = "https://apps.humanatlas.io/hra-api/v1/hubmap/rui_locations.jsonld"
    
    # read token
    f = open('access_token.txt', 'r')
    TOKEN = f.readline()
    
    # get data
    rui_locations = get_data(API+'?token='+TOKEN)
    print(len(rui_locations))

    # count HuBMAP tissue blocks
    counter = 0
    
    for donor in rui_locations['@graph']:
        for sample in donor['samples']:
            print(sample)
            counter  = counter + 1
    
    # print result to console
    print(counter)

# driver code
if __name__ == "__main__":
    main()
