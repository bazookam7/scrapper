from operator import itemgetter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain.schema.output_parser import StrOutputParser
import os
from prompt import CardRatesExtractionTemplate
from structure import CardRates, CardRatesList

prompts = CardRatesExtractionTemplate()
card_rates_parser = JsonOutputParser(pydantic_object=CardRatesList)
card_rates_format_instructions = card_rates_parser.get_format_instructions()
eligible_currencies = {
    "USD",
    "INR",
    "EUR",
    "GBP",
    "CAD",
    "AUD",
    "CHF",
    "HKD",
    "SGD",
    "JPY",
    "CNY",
}
def get_table_data(markdown_text):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    gemini_client = ChatGoogleGenerativeAI(google_api_key=GEMINI_API_KEY, model="gemini-2.0-flash", 
                                       temperature=0.5, max_tokens=None, timeout=None, max_retries=2)

    try:
        first_prompt,second_prompt = prompts.get_prompt()
        first_chain = first_prompt | gemini_client | StrOutputParser()
        second_chain = second_prompt | gemini_client | card_rates_parser

        chain = ({
                            "card_rates_table": first_chain,
                            "format_instructions": itemgetter("format_instructions")
                        }| second_chain)

        def invoke_chain():
            return  chain.invoke({   
                                    "eligible_currencies":eligible_currencies,
                                    "markdown_text":markdown_text,
                                    "format_instructions":card_rates_format_instructions
                                },config={})

        json_response = invoke_chain()
        return json_response["card_rates"]
    except Exception as e:
        print(e)
        return {}










