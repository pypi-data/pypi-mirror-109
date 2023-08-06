




def yield_dict_to_list(domain_dict):
    inputlist = []
    for website in sorted(domain_dict):
        for urlpath in sorted(domain_dict[website]):
            yield website + urlpath
