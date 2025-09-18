import os
import arxiv
import json
import time
from datetime import datetime, timedelta

def search_arxiv(
    query,
    batch_size=50,
    file_name,
    start_date=datetime(2020, 1, 1),
    max_retries=3,
    delay_seconds=3,
    window_days=30
):
    """
    自动按时间窗口抓取 Arxiv 论文，直到最新
    """

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data', 'raw')
    save_path = os.path.join(file_path, file_name)


    client = arxiv.Client(page_size=batch_size, delay_seconds=delay_seconds, num_retries=max_retries)

    # 读取已有结果，支持断点续抓
    try:
        with open(save_path, "r", encoding="utf-8") as f:
            all_results = json.load(f)
            if all_results:
                # 已抓取的最新时间
                latest_date = max(datetime.fromisoformat(p['published']) for p in all_results)
                start_date = latest_date + timedelta(seconds=1)
    except FileNotFoundError:
        all_results = []

    query_keywords = '(('+') OR ('.join([' AND '.join(i.split(' ')) for i in query])+'))'
    # category_filter = ' AND cat:cs'
    
    today = datetime.utcnow()
    current_start = start_date

    while current_start < today:
        current_end = min(current_start + timedelta(days=window_days), today)
        time_filter = f" AND submittedDate:[{current_start.strftime('%Y%m%d0000')} TO {current_end.strftime('%Y%m%d2359')}]"
        # search_query = query + time_filter + category_filter
        search_query = query_keywords + time_filter

        print(f"\n⏳ 抓取时间窗口: {current_start.date()} -> {current_end.date()}")

        search = arxiv.Search(
            query=search_query,
            max_results=batch_size * 100,  # 设置足够大，分批抓取
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        offset = 0
        while True:
            retries = 0
            while retries < max_retries:
                try:
                    results_iter = client.results(search, offset=offset)
                    batch = []
                    for i, result in enumerate(results_iter):
                        batch.append({
                            "id": result.get_short_id(),
                            "title": result.title,
                            "authors": [a.name for a in result.authors],
                            "abstract": result.summary,
                            "categories": result.categories,
                            "published": result.published.isoformat(),
                            "updated": result.updated.isoformat(),
                            "url": result.pdf_url
                        })
                        if len(batch) >= batch_size:
                            break

                    if not batch:
                        # 空页结束当前时间窗口
                        break

                    # 保存增量结果
                    all_results.extend(batch)
                    with open(save_path, "w", encoding="utf-8") as f:
                        json.dump(all_results, f, ensure_ascii=False, indent=2)
                    
                    print(f"✅ 已抓取 {len(batch)} 篇 (offset={offset})")
                    offset += len(batch)
                    time.sleep(delay_seconds)
                    break  # 成功跳出重试

                except Exception as e:
                    retries += 1
                    wait_time = delay_seconds * 2 ** retries
                    print(f"⚠️ 抓取失败: {e}, 重试 {retries}/{max_retries}, 等待 {wait_time} 秒...")
                    time.sleep(wait_time)
            else:
                print(f"❌ 多次重试仍失败，跳过 offset={offset}")
                offset += batch_size

            # 当抓取结果少于 batch_size，说明该窗口抓完
            if len(batch) < batch_size:
                break

        current_start = current_end

    print(f"\n🎉 抓取完成，总共 {len(all_results)} 篇论文，已保存到 {save_path}")
    return all_results


# ===========================
# 示例调用
# ===========================

# papers = fetch_arxiv_auto_window(
#     query="fraud detection behavior sequence",
#     batch_size=20,
#     start_date=datetime(2000, 1, 1),
#     save_path="arxiv_results.json",
#     window_days=30
# )
