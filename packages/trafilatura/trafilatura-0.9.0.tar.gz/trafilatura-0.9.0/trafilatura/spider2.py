

from .settings import LANG, MAX_CRAWLED_PAGES, MAX_URLS_BEFORE_SITECHECK, MAX_PAGES_PER_CRAWLED_SITE, MAX_URLS_TO_CHECK, SLEEPTIME, MIN_PAGES_PER_CRAWLED_SITE



    # control
    # ... if len(knownlinks) >= MAX_URLS_TO_CHECK ...
    #if len(knownlinks) < MAX_URLS_TO_CHECK:
    #    # not enough links
    #    logging.warning('not enough: %s, %s pages crawled, %s links in total', domainname, len(done), len(knownlinks))
    #    todo = links.difference(done)
    #    if len(todo) > 0:
    #        logging.warning('crawling more ??? %s %s', domainname, todo)
            # qcrawl.enqueue_call(func=focused_crawler, args=(todo, domainname, homepage, done,), timeout=3600, result_ttl=3600)




def crawl_website(domainname, done, todo):
    # process buffered urls
    bufferdom = 'buffer:' + domainname
    redisresult = redis_db.sunionstore(domainname, [domainname, bufferdom])
    logging.info('union of %s and %s – %s', bufferdom, domainname, redisresult)

    # load
    i = 0
    fwritten = 0
    knownlinks = set()
    downloaded = set()
    # load batch data
    batchpath = write.prepare_batch(13)

    # load crawl info
    for item in redis_db.smembers(domainname):
        # unpickled object check
        if not isinstance(item, str):
            item = item.decode(encoding='UTF-8')
        knownlinks.add(item)

    # iterate todo
    while len(todo) > 0 and len(knownlinks) <= MAX_PAGES_PER_CRAWLED_SITE and i <= MAX_CRAWLED_PAGES:
        i += 1
        link = todo.pop()
        # safety check
        if link in done:
            continue
        # process
        logging.info('looking for internal links: %s', link)
        rget = fetch_url(link, decode=False)
        done.add(link)
        if rget is not None:
            try:
                ip_info = rget.raw._connection.sock.getpeername()
            except AttributeError:
                # TODO: logging.error('ipinfo: %s', link)
                ip_info = '0.0.0.0'
            # inspect
            #if sitecheck.exam_response(rget.headers, rget.data, link) is False:
                # logging.warning('not suitable: %s', link)
            #    continue
            # extract links
            foundlinks = extract_links(decode_response(rget.data), link, False, language=LANG)
            if foundlinks is not None:
                knownlinks = knownlinks.union(foundlinks)
                logging.info('%s found – %s in total', len(foundlinks), len(knownlinks))
            # record
            downloaded.add(link)
            # write
            fwritten += 1
            outfilename = batchpath + '-' + str(fwritten) + '.tmp'
            write.writebatch(link, ip_info, rget.headers, rget.data, outfilename)
            # write batch
            if fwritten >= settings.WRITE_BATCH_SIZE:
                logging.debug('%s pages put in write queue:', fwritten)
                qwrite.enqueue_call(func=write.finalize_batch, args=(batchpath,), timeout=60, result_ttl=600)
                batchpath = write.prepare_batch(13)
                fwritten = 0
            # qwrite.enqueue_call(func=write.writebatch, args=(link, ip_info, rget.headers, rget.data, pathname,), timeout=60, result_ttl=600)

            # fetch.handle_result(rget, link, None)
        # sleep
        sleep(float(SLEEPTIME))

    logging.info('%s pages seen – db: %s', i, redisresult)

    # case A: enough links
    if len(knownlinks) > MIN_PAGES_PER_CRAWLED_SITE: # was 0 # settings.MAX_PAGES_PER_CRAWLED_SITE:
        # add links
        redisresult = redis_db.sadd(domainname, *knownlinks)
        logging.debug('db add: %s', redisresult)
        # put in queue for download
        if len(knownlinks) >= MAX_PAGES_PER_CRAWLED_SITE:
            knownlist = list(knownlinks)
            storelist = knownlist[:MAX_PAGES_PER_CRAWLED_SITE]
        else:
            storelist = list(knownlinks)
        # substract already downloaded pages
        storeset = set(storelist)
        storeset = storeset.difference(downloaded)
        redisresult = redis_db.sadd('meta:todo', *storeset)
        logging.info('add to todo (crawl): %s, local: %s, db: %s', domainname, len(storeset), redisresult)
    # case B: not enough
    else:
        logging.warning('not enough: %s pages crawled, %s links in total', len(done), len(knownlinks))
        logging.warning('out of ideas: %s', domainname)
    # perform cleanup
    processtodo.cleanup(domainname)
    # log changes
    if fwritten > 0:
        logging.debug('%s pages put in write queue:', fwritten)
        qwrite.enqueue_call(func=write.finalize_batch, args=(batchpath,), timeout=60, result_ttl=600)