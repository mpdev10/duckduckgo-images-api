import duckduckgo_images_api3.api as ddg3

if __name__ == '__main__':
    results = ddg3.search(keywords="flower",
                          print_results=False,
                          max_request_num=1)

    print(results.search_results[0].image)
