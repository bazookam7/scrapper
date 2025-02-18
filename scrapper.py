import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import os
import platform
import time
from pdf2image import convert_from_bytes, pdfinfo_from_bytes
import requests
from io import BytesIO
import logging
from google import genai
from google.genai import types
from dao.dao_factory import DaoFactory
from dao.models.sql.card_rates import CardRatesDo
from structure import CardRates
from table_extractor import get_table_data
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.curdir,"set_paths.env"))

def process_image_batch(pdf_file_stream, poppler_path, start_page, end_page):
    batch = convert_from_bytes(
            pdf_file_stream,
            poppler_path=poppler_path,
            first_page=start_page,  # These are actual page numbers (1-based)
            last_page=end_page
        )
    
    images_base64 = []
    for image in batch:
        buffered = BytesIO()
        image.save(buffered, format="PNG", optimize=True, quality=85)
        image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        images_base64.append(image_base64)
        buffered.close()
    return images_base64



def read_images(pdf_file_stream, batch_size=10):
    if platform.system() == "Windows":
        poppler_path = "C:\\Users\\rajat\\Downloads\\Release-24.08.0-0\\poppler-24.08.0\\Library\\bin"
    else:
        poppler_path = None

    start_time = time.time()
    pdf_info = pdfinfo_from_bytes(pdf_file_stream, poppler_path=poppler_path)
    total_pages = int(pdf_info['Pages'])
    print(f"Total pages: {total_pages} in time {time.time() - start_time} seconds")
    images_base64 = []

    # Process in batches using actual page numbers (1-based)
    # for start_page in range(1, total_pages + 1, batch_size):
    #     logging.info(f"Processing batch from page {start_page} to {start_page + batch_size - 1}")
    #     end_page = min(start_page + batch_size - 1, total_pages)
    #     start_time = time.time()
        
    #     logging.info(f"Processing batch from page {start_page} to {end_page} took {time.time() - start_time} seconds")
    #     del batch
    with ThreadPoolExecutor() as executor:
        futures = []
        for start_page in range(1, total_pages + 1, batch_size):
            end_page = min(start_page + batch_size - 1, total_pages)
            futures.append(executor.submit(
                process_image_batch, pdf_file_stream, poppler_path, start_page, end_page
            ))

        for future in futures:
            images_base64.extend(future.result())
        
    return images_base64


def fetch_pdf_from_disk(file_path):
    with open(file_path, "rb") as file:
        return file.read()


def fetch_pdf_to_memory(url):
    """
    Fetches a PDF from a URL and returns it as a BytesIO object.
    
    Args:
        url (str): The URL of the PDF file
        
    Returns:
        BytesIO: The PDF file in memory
        
    Raises:
        requests.RequestException: If there's an error fetching the PDF
    """
    try:
        # Configure logging
        print(f"Fetching PDF from {url}")
        
        # Send GET request with stream=True to handle large files efficiently
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Check if the content type is PDF
        content_type = response.headers.get('content-type', '')
        if 'application/pdf' not in content_type.lower():
            logging.warning(f"Warning: Content-Type is {content_type}, not PDF")
        
        # Read the content into BytesIO
        pdf_in_memory = BytesIO(response.content)
        
        print("PDF successfully loaded into memory")
        return pdf_in_memory
        
    except requests.RequestException as e:
        print(f"Error fetching PDF: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise



def process_images_with_gemini(images_base64, api_key):
    """
    Process images using Gemini model directly through Google AI API
    """
    client = genai.Client(api_key=api_key)
    
    results = []
    for image_b64 in images_base64:
        try:
            # Convert base64 string back to bytes
            image_bytes = base64.b64decode(image_b64)
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    "Extract and convert the image to markdown put table in a table format with a table summary",
                    types.Part.from_bytes(data=image_bytes, mime_type="image/png")
                ]   
            )
            table_data = get_table_data(response.text)
            print(table_data)
            results.append(table_data)
        except Exception as e:
            print(f"Error processing image with Gemini: {str(e)}")
    
    return results

# Example usage:
if __name__ == "__main__":
    pdf_path = os.getenv("PDF_PATH")
    for file in os.listdir(pdf_path):
        try:
            ## IDFC_Forex_Rates
            print(file)
            file_name = file.split(".")[0]
            company_name = file_name.split("_")[0]
            reference_date = date.today()
            ## read pdf file
            pdf_stream = fetch_pdf_from_disk(os.path.join(pdf_path, file))
            images_base64 = read_images(pdf_stream)
            GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        
        # Process images with Gemini
            results = process_images_with_gemini(images_base64, GEMINI_API_KEY)
            currency_set = set()
            ## merge rows like {'currency': 'USD', 'TT_Buy': 84.33, 'TT_Sell': 0} and {'currency': 'USD', 'TT_Buy': 0, 'TT_Sell': 84.33} into one row
            merged_results_per_currency = {}
            for result in results:
                for card_rate in result:
                    currency_set.add(card_rate["currency"])
                    if card_rate["currency"] not in merged_results_per_currency:
                        merged_results_per_currency[card_rate["currency"]] = card_rate
                    else:
                        merged_results_per_currency[card_rate["currency"]]["TT_Buy"] = max(merged_results_per_currency[card_rate["currency"]]["TT_Buy"], card_rate["TT_Buy"])
                        merged_results_per_currency[card_rate["currency"]]["TT_Sell"] = max(merged_results_per_currency[card_rate["currency"]]["TT_Sell"], card_rate["TT_Sell"])
            print(currency_set)
            print(merged_results_per_currency)
            for row in merged_results_per_currency.values():
                if row["currency"] == None:
                    continue
                ## save in db 
                card_rate_do = CardRatesDo(company_name=company_name, reference_date=reference_date, currency=row["currency"],
                                                    tt_buy=row["TT_Buy"], tt_sell=row["TT_Sell"])
                DaoFactory.insert_data(card_rate_do)
            
            
        except Exception as e:
            print(f"Failed to process PDF: {str(e)}")
