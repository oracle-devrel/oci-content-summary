# OCI GenAI Automatic Content Extractor & Summarizer

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