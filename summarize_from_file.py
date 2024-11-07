# coding: utf-8
# Copyright (c) 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

##########################################################################
# summarize_text_demo.py
# Supports Python 3
##########################################################################
# Info:
# Get texts from LLM model for given prompts using OCI Generative AI Service.
##########################################################################
# Application Command line(no parameter needed)
# python summarize_text_demo.py
##########################################################################

import oci
import yaml
import json
#import logging
#logging.getLogger('oci').setLevel(logging.DEBUG)

def main(summary_txt: str = "") -> None:

    with open('config.yaml', 'r') as file:
        config_data = yaml.safe_load(file)

    compartment_id = config_data['compartment_id']
    CONFIG_PROFILE = config_data['config_profile']
    config = oci.config.from_file('~/.oci/config', CONFIG_PROFILE)

    # Service endpoint
    endpoint = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"

    generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(config=config, service_endpoint=endpoint, retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10,240))
    chat_detail = oci.generative_ai_inference.models.ChatDetails()
    
    # You can also load the summary text from a file, or as a parameter in main
    #with open('files/summarize_data.txt', 'r') as file:
    #    text_to_summarize = file.read()
    with open('summarize_data.txt', 'r') as file:
        text_to_summarize = file.read()


    content = oci.generative_ai_inference.models.TextContent()
    content.text = "Generate a teaser summary for this Markdown file. Share an interesting insight to captivate attention. Here is the file: {}".format(text_to_summarize)
    message = oci.generative_ai_inference.models.Message()
    message.role = "USER"
    message.content = [content]

    llm_inference_request = oci.generative_ai_inference.models.GenericChatRequest()
    llm_inference_request.api_format = oci.generative_ai_inference.models.BaseChatRequest.API_FORMAT_GENERIC
    llm_inference_request.messages = [message]

    llm_inference_request.max_tokens = 550
    llm_inference_request.temperature = 1.0
    llm_inference_request.frequency_penalty = 0.0
    llm_inference_request.top_p = 0.75

    # cohere.command-r-plus: ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceya7ozidbukxwtun4ocm4ngco2jukoaht5mygpgr6gq2lgq
    # cohere.command for generation: ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceyafhwal37hxwylnpbcncidimbwteff4xha77n5xz4m7p6a
    # new model - llama3: ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceyaycmwwnvu2gaqrffquofgmshlqzcdwpk727n4cykg34oa
    chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id="ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceyaycmwwnvu2gaqrffquofgmshlqzcdwpk727n4cykg34oa")
    chat_detail.chat_request = llm_inference_request
    chat_detail.compartment_id = compartment_id
    chat_response  = generative_ai_inference_client.chat(chat_detail)

    data_dict = vars(chat_response)
    print(data_dict)

    json_result = json.loads(str(data_dict['data']))

    text_result = json_result['chat_response']['choices'][0]['message']['content'][0]['text']
    print(text_result)


    '''
    summarize_text_detail = oci.generative_ai_inference.models.SummarizeTextDetails()
    summarize_text_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id="cohere.command")
    summarize_text_detail.compartment_id = compartment_id
    #summarize_text_detail.input = text_to_summarize

    with open('summarize_data.txt', 'r') as file:
        text_to_summarize = file.read()
    summarize_text_detail.input = text_to_summarize

    summarize_text_detail.additional_command = "Generate a teaser summary for this Markdown file. Share an interesting insight to captivate attention."
    summarize_text_detail.extractiveness = "AUTO" # HIGH, LOW
    summarize_text_detail.format = "AUTO" # brackets, paragraph
    summarize_text_detail.length = "LONG" # high, AUTO
    summarize_text_detail.temperature = .25 # [0,1]

    if "<compartment_ocid>" in compartment_id:
        print("ERROR:Please update your compartment id in target python file")
        quit()

    summarize_text_response = generative_ai_inference_client.summarize_text(summarize_text_detail)

    # Print result
    #print("**************************Summarize Texts Result**************************")
    print(summarize_text_response.data)
    return summarize_text_response.data
    '''
    return text_result

if __name__ == '__main__':
    main()