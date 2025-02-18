from langchain_core.prompts import  ChatPromptTemplate

class CardRatesExtractionTemplate():
    def __init__(self):
        self.role ="You are a helpful assistant that extracts currency and rates table from the markdown table to a json object with the following structure"

    def get_prompt(self):
        prompt1 = """Extract all the currency and their rates from the markdown table to a json object with the following structure  
            in  the table format of the following structure

            ## Structure:
             -currency: str
             -TT_Buy: float
             -TT_Sell: float

            Rules:
            - Dont miss any currency and their rates
            - Only use tty buy and tty sell rates which are telegraphic transfer rates, if there is any other rate like international prepaid card rate,cash rate, bills etc, then dont use it
            - if TT_Buy and TT_Sell are not present, then dont return the currency or return the currency with TT_Buy and TT_Sell as 0 or return any one if one is present         
            - If you dont find any currency and their rates, return an empty list
            - map the currency to the eligible_currencies list and use the currency from the eligible_currencies list
              for example - dont user 'UNITED STATES DOLLAR' instead use 'USD'
            - even if the currency is not in the eligible_currencies list, return the currency with standard currency codeand their rates




            ## Input:
            eligible_currencies: {eligible_currencies}
            markdown_text:
            {markdown_text}
            """
        image_types_extraction_prompt = ChatPromptTemplate.from_messages(
                    [
                        (
                            "human",
                            prompt1,
                        )
                    ])
        converter_prompt="""## Output Format : convert the given input to given format {format_instructions}

                ## Input:
                card rates table

                ## Generation
                card rates table : {card_rates_table}

                ##Output"
                """
        
        
        converter_prompt_template = ChatPromptTemplate.from_messages(
                    [
                        (
                            "human",
                            converter_prompt ,
                        )
                    ])
        return image_types_extraction_prompt,converter_prompt_template

