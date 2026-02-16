import pandas as pd


def process_reviews(input_meta_filename = False, metadata_fields_to_keep = ['parent_asin','main_category',"title", 'store',"average_rating", "rating_number"],*,  input_review_filename, save_meta = True,
                    review_fields_to_keep):
    '''Reads provided review and metadata json files and returns a filtered csv based on fields that have been selected
    
    Inputs:
    input_review_filename: The review filename + path
    input_meta_filename: The meta filename + path
    save_meta: Boolean for whether you want to save metadata information as well to dataframe (DEFAULT is TRUE)
    metadata_fields: List of metadata fields that you want added to each entry. By default = ['main_category',"title", 'store',"average_rating", "rating_number"]

    Outputs:
    Pandas data frame that has been filtered based on selected columns and whether you want meta data information attached

    Possible fields available to keep from dataset:
    rating	         |float	|Rating of the product (from 1.0 to 5.0).
    title	         |str	|Title of the user review.
    text	         |str	|Text body of the user review.
    images	         |int	|Number of images that are attached to the review 
    parent_asin	     |str	|Parent ID of the product. 
    user_id	         |str	|ID of the reviewer
    timestamp	     |int	|Tuple in the form of (MM/DD/YYYY)]
    verified_purchase|bool	|User purchase verification
    helpful_vote	 |int	|Helpful votes of the review

    '''
    
    df_reviews = pd.read_json(input_review_filename.replace('\\', '/'),lines=True)

    if 'images' in review_fields_to_keep:
        df_reviews['images'] = df_reviews['images'].str.len().astype(bool)

    if 'timestamp' in review_fields_to_keep:
        df_reviews['timestamp'] = df_reviews['timestamp'].apply(lambda x: (x.month, x.day, x.year))  #Save timestamp data in terms of month, day, year
    
    if input_meta_filename and save_meta:
        review_fields_to_keep.append('parent_asin')

    review_filtered_df = df_reviews[review_fields_to_keep]

    del df_reviews  #Remove to free up memory

    if input_meta_filename and save_meta:
        df_meta = pd.read_json(input_meta_filename.replace('\\', '/'),lines=True)
        id_lut = df_meta[metadata_fields_to_keep]
        print("Completed filter + merge of metadata.")
        return review_filtered_df.merge(id_lut, on='parent_asin', how='left').drop(columns= 'parent_asin')
    else:
        print("Completed filter.")
        return review_filtered_df







### EXAMPLE 
### NEED THESE FILES TO RUN
input_file_review = "All_Beauty.jsonl/All_Beauty.jsonl"
input_file_meta = "meta_All_Beauty.jsonl/meta_All_Beauty.jsonl"
###

print(process_reviews(
    input_review_filename = input_file_review,
    input_meta_filename= input_file_meta,                      
    review_fields_to_keep= ['helpful_vote','timestamp','rating','images','text'] 
).head(6))