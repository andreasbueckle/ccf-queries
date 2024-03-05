import requests
import pandas as pd

# UBERON ID and URL to HRA API 
BRAIN_UBERON_ID = "http://purl.obolibrary.org/obo/UBERON_0000955"
url = "https://apps.humanatlas.io/hra-api/v1/scene"

def main():
    """
    A method to get all tissue blocks for the brain, then provide a summary of which AS has how many collisions
    """
    
    # make http request; no authentication needed since we are only showing public tissue blocks in the HRA Organ Gallery
    scene_endpoint_response = requests.get(url).json()

    # dict to hold metadata for each HuBMAP ID
    result = {}
    
    for node in scene_endpoint_response:
      try:
        if BRAIN_UBERON_ID in node['ccf_annotations']:
          for iri in node['ccf_annotations']:
            if iri in result.keys():
              result[iri] = result[iri] + 1
            else:
              result[iri] = 1
      except:
        continue
  
    # convert for easier export with pandas
    export = {'iri':[], 'counts':[]}
    
    for key in result:
      
      # format UBERON ID for easier comparison with crosswalk
      items = key.split('/')
      formatted = items[len(items)-1].replace("_", ":")
      export['iri'].append(formatted)
      export['counts'].append(result[key])
    
     # export to CSV
    df = pd.DataFrame(data=export)
    df.to_csv("output/brain_collisions.csv", sep=',')    

# driver code
if __name__ == "__main__":
    main()
