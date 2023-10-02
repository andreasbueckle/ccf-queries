from utils import get_data


def main():
    """A function to perform CCF API calls and count numbers and test speed
    """

    SCENE = "https://ccf-api.hubmapconsortium.org/v1/scene"
    ORGAN_SCENE = "https://ccf-api.hubmapconsortium.org/v1/reference-organ-scene"
    
    # get scene endpoint response
    scene = get_data(SCENE)
    
    # catpure TBs
    tissue_blocks_scene = []
    organ_iris = []
    for node in scene:
        if "representation_of" not in node:
            tissue_blocks_scene.append(node)
        else:
            organ_iris.append(node['representation_of'])
    
    print(f'scene returns {len(tissue_blocks_scene)} tissue blocks')
    print(f'scene returns {len(organ_iris)} organs')
    
    # get ref organ IRIs and TBs from ref organ scene endpoint
    dict_organ_tissue_blocks = {}
    tissue_blocks_ref = []
    for iri in organ_iris:
        print("now getting data for " + iri)
        organ = get_data(ORGAN_SCENE+"?organ-iri="+iri)
        counter = 0
        
        for node in organ:
            name = ""
            if "representation_of" not in node:
                counter = counter + 1
                dict_organ_tissue_blocks[organ[0]['reference_organ']].append(node['entityId'])
            else:
                name = organ[0]['reference_organ']
                dict_organ_tissue_blocks[organ[0]['reference_organ']] = []
                
            print(f'Added {counter} tissue blocks to {name}')
    
    print(dict_organ_tissue_blocks)
    for key in dict_organ_tissue_blocks:
        tissue_blocks_ref.append(dict_organ_tissue_blocks[key])
    
    print(
        f'reference-organ-scene returns {len(dict_organ_tissue_blocks)} organs')
    print(f'reference-organ-scene returns {len(tissue_blocks_ref)} tissue blocks')

# driver code
if __name__ == "__main__":
    main()
