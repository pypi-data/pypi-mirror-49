from KoreanNewsCrawler.articlecrawler import ArticleCrawler

if __name__ == "__main__":
    Crawler = ArticleCrawler()
    Crawler.set_category("IT과학", "경제")  # 정치, 경제, 생활문화, IT과학, 사회 카테고리 사용 가능
    Crawler.set_date_range(2018, 2018, 1)  # 2017년 1월부터 2018년 4월까지 크롤링 시작
    Crawler.start()
