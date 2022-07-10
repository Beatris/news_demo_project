import argparse
import pandas as pd

from pathlib import Path
from typing import List

from pydantic import parse_file_as
from text_utils.keywords_extractor import KeywordsExtractor

from news_project.models import News


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Insert news')
    parser.add_argument('news_json', type=Path)
    parser.add_argument('news_csv', type=Path)
    return parser.parse_args()


def insert_news(news_json: Path, news_csv: Path) -> None:
    initial_news_df = pd.read_csv(news_csv, na_values=None)
    initial_news = get_news_from_csv(initial_news_df)
    keywords_extractor = get_keywords_extractor(initial_news)

    news_list = parse_file_as(List[News], news_json)
    for news in news_list:
        news.keywords = keywords_extractor.get_keywords_from_text(news.all_texts)
    
    news_dicts = [news.dict() for news in news_list]
    new_df = pd.concat([pd.DataFrame(news_dicts), initial_news_df])
    new_df.to_csv(news_csv, index=False)


def get_news_from_csv(news_df: pd.DataFrame) -> List[News]:
    return [
        News.parse_obj(row.to_dict())
        for _, row in news_df.iterrows()
    ]


def get_keywords_extractor(initial_news: List[News]) -> KeywordsExtractor:
    train_corpus = [news.all_texts for news in initial_news]
    return KeywordsExtractor.train(train_corpus)


if __name__ == "__main__":
    args = parse_args()
    insert_news(args.news_json, args.news_csv)
