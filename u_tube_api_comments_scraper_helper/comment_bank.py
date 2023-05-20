import csv
import googleapiclient.discovery
import u_tube_api_comments_scraper_helper.constants as const


def comment_thread_fetching(video_id: str, user_api_key: str):

    fetcher = googleapiclient.discovery.build(const.API_SERVICE_NAME, const.API_VERSION, developerKey=user_api_key)

    frisbee = fetcher.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=65
    )

    PRODUCT = frisbee.execute()
    RESPONSE = PRODUCT

    ALL_COMMENTS = []

    HEADINGS = ["AUTHOR", "COMMENT", "DATE", "TIME", "LIKES"]

    print('\n\t\t\t**** VIEWERS\' COMMENTS ****\n')

    for key, _ in RESPONSE.items():
        if key == 'items':
            COMMENTS_COLLECTION = RESPONSE[key]  # We get the value here. The "value" being the comment response i.e.
            # a dict containing all the comments and associated data of the video in question.

            for comment_bundle in COMMENTS_COLLECTION:  # Iterating to retrieve each comment & associated metrics.
                author = comment_bundle['snippet']['topLevelComment']['snippet']['authorDisplayName']
                comment = comment_bundle['snippet']['topLevelComment']['snippet']['textDisplay']
                comment_date_time = comment_bundle['snippet']['topLevelComment']['snippet']['publishedAt']
                formatted_comment_date = f'{comment_date_time.split("T")[0]}'
                formatted_comment_time = f'{comment_date_time.split("T")[1].replace("Z", "")}'
                comment_likes = comment_bundle['snippet']['topLevelComment']['snippet']['likeCount']

                print(f'{author} comments:\n\t"{comment}"\nDATE: {formatted_comment_date}\nTIME: '
                      f'{formatted_comment_time}\nLIKES: {comment_likes}\n')

                ALL_COMMENTS.append({"AUTHOR": author, "COMMENT": comment, "DATE": formatted_comment_date,
                                     "TIME": formatted_comment_time, "LIKES": comment_likes})

    write_to_file(video_id, HEADINGS, ALL_COMMENTS)


def write_to_file(video_id, column_names, all_comments):
    with open(f'Viewers\' Comments for Video-ID; {video_id}.csv', 'w', encoding='UTF-8', newline="") as comments_file:
        csv_writer = csv.DictWriter(comments_file, fieldnames=column_names)
        csv_writer.writeheader()

        for comment_metrics in all_comments:
            csv_writer.writerow(comment_metrics)

    print('\n\tAll the comments and related data for this video have been saved to a csv file successfully.')
