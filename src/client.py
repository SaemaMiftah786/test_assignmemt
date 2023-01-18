import logging
from dependencies.scraping import scraper
from dependencies.ingestion import ingestion


logging.basicConfig(level=logging.INFO)

def step_1():
    scraper.Scraper().run()
    logging.info("Finished Scraping data !!!")

def step_2():
    ingestion.Ingest().run()
    logging.info("Finished Ingesting data  !!!")


if __name__ == "__main__":
    step_1()
    step_2()
