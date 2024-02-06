# OCI GenAI Automatic Content Extractor & Summarizer

[![License: UPL](https://img.shields.io/badge/license-UPL-green)](https://img.shields.io/badge/license-UPL-green) [![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=oracle-devrel_oci-content-summary)](https://sonarcloud.io/dashboard?id=oracle-devrel_oci-content-summary)

![](./img/repo_logo.png)

This project gets the 25 trending projects from a day (from [here](https://github.com/trending)), reads their README.md files, and summarizes them in a way which is ready for social media.

Companies can use this in their content generation pipeline strategies, or individuals trying to grow their social media following with organic and up-to-date (fresh everyday) content!

LLM Hyperparams used:

- Prompt:  "Generate a teaser summary for this Markdown file. Share an interesting insight to captivate attention."
- Extractiveness = "AUTO" # HIGH, LOW
- Format = "AUTO" # brackets, paragraph
- Length = "LONG" # high, AUTO
- Temperature = .3 # [0,1]. The lower the temperature, the more consistent and less wild/imaginative generations are

## Requirements

- Python 3.10
- Conda
- [OCI SDK](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm)

### OCI SDK Installation Instructions

Follow these links below to generate a config file and a key pair in your ~/.oci directory:

[SDK Config](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm)
[API Signing Key](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm)
[SDK CLI Installation](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm#configfile)

After completion, you should have following 2 things in your ~/.oci directory:

- A config file(where key file point to private key:key_file=~/.oci/oci_api_key.pem)
- A key pair named oci_api_key.pem and oci_api_key_public.pem

Now make sure you change the reference of key file in config file (where key file point to private key:key_file=/YOUR_DIR_TO_KEY_FILE/oci_api_key.pem)

## Installation

```sh
pip install -r requirements.txt
```

## Automatically Running everything

First, you need to configure a `config.yaml` file that contains this structure, which will allow you to authenticate to OCI and call the OCI GenAI summarization model, to summarize the content from each project's README files:

```yml
compartment_id: "ocid1.compartment.oc1..ocid"
config_profile: "profile_name_in_your_oci_config"
```

You can find your oci configuration in `~/.oci/config`. Make sure you have previously installed [OCI SDK in your computer](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm).

Then, you can run the bash script to generate all outputs in the `output/` dir:

```bash
chmod a+x run.sh # if you don't have exec permissions initially for the .sh file
./run.sh
```

## Running the Spiders / Crawlers

```sh
scrapy runspider trending_spider.py # this will get trending repositories
scrapy runspider info_spider.py # then, for each trending repository, it will extract info.
python main.py # to process their README.md files as well, and runs a summarizer on top of it.
```

## Getting Started with LinkedIn Poster

### Pre-requisites

1. Create or use an existing developer application from the [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps/)
2. Request access to the Sign In With LinkedIn API product. This is a self-serve product that will be provisioned immediately to your application.
3. Generate a 3-legged access token using the Developer Portal [token generator tool](https://www.linkedin.com/developers/tools/oauth/token-generator), selecting the r_liteprofile scope.

## Contributing

This project is open source.  Please submit your contributions by forking this repository and submitting a pull request!  Oracle appreciates any contributions that are made by the open source community.

## License

Copyright (c) 2022 Oracle and/or its affiliates.

Licensed under the Universal Permissive License (UPL), Version 1.0.

See [LICENSE](LICENSE) for more details.

ORACLE AND ITS AFFILIATES DO NOT PROVIDE ANY WARRANTY WHATSOEVER, EXPRESS OR IMPLIED, FOR ANY SOFTWARE, MATERIAL OR CONTENT OF ANY KIND CONTAINED OR PRODUCED WITHIN THIS REPOSITORY, AND IN PARTICULAR SPECIFICALLY DISCLAIM ANY AND ALL IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE.  FURTHERMORE, ORACLE AND ITS AFFILIATES DO NOT REPRESENT THAT ANY CUSTOMARY SECURITY REVIEW HAS BEEN PERFORMED WITH RESPECT TO ANY SOFTWARE, MATERIAL OR CONTENT CONTAINED OR PRODUCED WITHIN THIS REPOSITORY. IN ADDITION, AND WITHOUT LIMITING THE FOREGOING, THIRD PARTIES MAY HAVE POSTED SOFTWARE, MATERIAL OR CONTENT TO THIS REPOSITORY WITHOUT ANY REVIEW. USE AT YOUR OWN RISK. 